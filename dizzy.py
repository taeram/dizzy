#!/usr/bin/env python
"""A wrapper for the DNS Made Easy API v2.0"""

from datetime import datetime
from hashlib import sha1
from hmac import new as hmac
import requests
from os import getenv, \
               path
import json
import sys

class Dizzy(object):
    """
    A wrapper for the DNS Made Easy API v2.0
    """

    def __init__(self, api_key, secret_key):
        self.base_url = "https://api.dnsmadeeasy.com/V2.0/dns/managed"
        self.api_key = api_key
        self.secret_key = secret_key
        self.data_format = "json"

    def get_domains(self):
        """ Get the list of all domains in your account """

        domains = []
        result = {
            "totalPages": 1,
            "page": 1
        }
        while result is None or result['page'] <= result['totalPages']:
            result = self.request("?page=%s" % result['page'])
            for domain in result['data']:
                domains.append(domain)
            result['page'] += 1

        return domains

    def get_domain(self, domain_name):
        """ Get the configuration of this domain """

        domains = self.get_domains()
        for domain in domains:
            if domain['name'] == domain_name:
                return domain

        return None

    def get_domain_records(self, domain_name):
        """ Get all records for this domain """

        domain = self.get_domain(domain_name)

        records = []
        result = {
            "totalPages": 1,
            "page": 1
        }
        while result is None or result['page'] <= result['totalPages']:
            result = self.request("%s/records?page=%s" % (domain['id'], result['page']))
            for record in result['data']:
                records.append(record)
            result['page'] += 1

        return records

    def get_domain_record(self, domain_name, record_name):
        """ Get a specific record for this domain """

        records = self.get_domain_records(domain_name)
        for record in records:
            if record['name'] == record_name:
                return record

        return None

    def update_a_record(self, domain_name, record_name, value):
        """ Update an a record in this domain """

        record = self.get_domain_record(domain_name, record_name)
        record['value'] = value

        self.request(
            "%s/records/%s/" % (record['sourceId'], record['id']),
            "PUT",
            record
        )

        return record

    def request(self, url_postfix, request_type="GET", data=None):
        """ Make a request to the API """

        request_url = self.base_url + '/' + url_postfix
        request_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        request_hmac = hmac(self.secret_key, request_date, sha1).hexdigest()

        headers = {
            "x-dnsme-apiKey": self.api_key,
            "x-dnsme-requestDate": request_date,
            "x-dnsme-hmac": request_hmac,
            "Accept": "application/" + self.data_format,
            "Content-Type": "application/" + self.data_format
        }

        if request_type is "GET":
            req = requests.get(
                request_url,
                headers=headers
            )
        elif request_type is "PUT":
            req = requests.put(
                request_url,
                data=json.dumps(data),
                headers=headers
            )

        if req.status_code > 200:
            if req.status_code is 404:
                raise Exception("%s API endpoint not found" % url_postfix)
            else:
                raise Exception(req.text)

        if len(req.text) > 0:
            return json.loads(req.text)
        else:
            return True

def usage():
    sys.stderr.write("""Usage: %s [domain name] [command]

Command can be one of:
    update [record_name] [ip_address]       Update an A record
""" % path.basename(sys.argv[0]))
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()

    domain_name = sys.argv[1]
    command = sys.argv[2]

    api_key = getenv('DNSMADEEASY_API_KEY')
    secret_key = getenv('DNSMADEEASY_SECRET_KEY')

    if not api_key or not secret_key:
        print "API Key or Secret Key not set. Please see README.md for instructions"
        sys.exit(1)

    dizzy = Dizzy(api_key, secret_key)
    if command == "update":
        if len(sys.argv) < 5:
            usage()

        record_name = sys.argv[3]
        record_value = sys.argv[4]

        record = dizzy.update_a_record(domain_name, record_name, record_value)
        print "%s.%s. %s IN A %s" % (record['name'], domain_name, record['ttl'], record['value'])
    else:
        usage()
