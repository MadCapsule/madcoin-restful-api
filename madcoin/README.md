madcoin-python is a set of Python libraries that allows easy access to the bitcoin peer-to-peer cryptocurrency client API throw a Restful API.

Documentation
===========================

Documentation can be found here, or in the source archive. It is built
using Sphinx:

http://laanwj.github.com/bitcoin-python/doc/

Installation instructions
===========================

bitcoin-python uses setuptools for the install script. There are no dependencies apart from Python itself.

::

  $ python setup.py build
  $ python setup.py install

Pypi / Cheeseshop
==================

It is possible to install the package through Pypi (cheeseshop), see http://pypi.python.org/pypi?:action=display&name=bitcoin-python

::

  $ pip install bitcoin-python

TODO
======
These things still have to be added:

- SSL support (including certificate verification) for managing remote bitcoin daemons.

======

sudo pip install virtualenv
sudo pip install https://github.com/pypa/virtualenv/tarball/develop
source ENV/bin/activate
which python
pip install flask
pip install epydoc
pip install -e git://github.com/laanwj/bitcoin-python.git#egg=bitcoin-python
python main.py #to run the app

Resources
======

* http://flask.pocoo.org/
* http://www.virtualenv.org/
* https://github.com/laanwj/bitcoin-python
