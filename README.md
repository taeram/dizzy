Dizzy
=====

Dizzy is a wrapper for the DNS Made Easy API in Python.

Requirements
============
You'll need the following:

* [Python 2.7.3](http://www.python.org/)
* [pip](https://github.com/pypa/pip)

Installation
============

```bash
    # Clone the repo
    git clone https://github.com/taeram/dizzy.git ~/.dizzy
    cd ~/.dizzy/

    # Install the dependencies
    sudo pip install -r requirements.txt

    # Add your DNS Made Easy API credentials to your dizzy environment
    sudo tee ~/.dizzy/.env << EOF
    DNSMADEEASY_API_KEY=api-key-goes-here
    DNSMADEEASY_SECRET_KEY=secret-key-goes-here
    EOF

    # Voila!
    ~/.dizzy/dizzy.py
```

Usage
=====

Update an A record. 

In this example, we're updating www.example.com to point to 127.0.0.1

Request
```bash
~/.dizzy/dizzy.py example.com update www 127.0.0.1
```

Response
```
www.example.com. 3600 IN A 127.0.0.1
```
