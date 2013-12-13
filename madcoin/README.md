madcoin-python is a set of Python libraries that allows easy access to the bitcoin peer-to-peer cryptocurrency client API throw a Restful API.

Documentation
=============

Documentation can be found here, or in the source archive. It is built
using Epydoc:

[http://epydoc.sourceforge.net/]: http://epydoc.sourceforge.net/

Installation instructions
=========================

In this repo you will find everything you would need to make it works

madcoin-python uses setuptools for the install script. There are no dependencies apart from Python itself.

```
  $ sudo pip install virtualenv
  $ sudo pip install https://github.com/pypa/virtualenv/tarball/develop
  $ virtualenv venv
  $ source venv/bin/activate
  $ which python
  $ pip install flask
  $ pip install epydoc
  $ pip install -e git://github.com/laanwj/bitcoin-python.git#egg=bitcoin-python
```

Run instructions
================

Set execute rights to the `run.py` script and the execute it

```
  $ chmod a+x run.py
  $ python run.py
```

Do not forget to configure and run your coins server daemon first

```
  $ ~/.bitcoin/bitcoin.conf
  $ ./bitcoind
```

Generating documentation
========================

There are a config file `epydoc.conf` for generate the documentation using `epydoc`

With the following code we generate our documentation in the `apidocs` folder

To generate the documentation you should have all our project dependencies installed in the main system because a bug between virtualenv and epydoc

```
  $ epydoc --config epydoc.conf
```

Errors Codes
============

* 1000 - OK (no error)
* 1001 - The address that you provided is invalid
* 1002 - Account does not have enough funds available

Resources
=========

* http://flask.pocoo.org/
* http://www.virtualenv.org/
* https://github.com/laanwj/bitcoin-python

TODO
====
These things still have to be added:

* SSL support (including certificate verification) for managing remote coin daemons.