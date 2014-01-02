madcoin-python is a set of Python libraries that allows easy access to the bitcoin peer-to-peer cryptocurrency client API throw a Restful API.

Documentation
=============

Documentation can be found here, or in the source archive. It is built
using Epydoc:

[http://epydoc.sourceforge.net/]: http://epydoc.sourceforge.net/

Installation instructions
=========================

In this repo you will find everything you would need to make it works

madcoin-python uses `setuptools` for the install script. There are no dependencies apart from Python itself.

```
  $ sudo aptitude install python-setuptools
  $ sudo aptitude install python-pip
  $ sudo aptitude install git
```

Install the virtual enviroment to start working/run on our project

```
  $ sudo pip install virtualenv
  $ virtualenv venv
  $ source venv/bin/activate
```

If we wanna exit from our virtual enviroment we can run 

```
  $ deactivate
```
With this command line we can test if our virtual enviroment is working properly 

```
$ which python
/home/israel/Desktop/madcoin-restful-api/madcoin/venv/bin/python
```

After install our virtual enviroment we have to install our dependencies

```
  $ pip install flask #small framework to our python app
  $ pip install simplejson #lower json controller to handle Decimal Types
  $ pip install -e git://github.com/laanwj/bitcoin-python.git#egg=bitcoin-python #Bitcoin library to comunicate our project with our bitcoind
```

If we want to generate the documentation we can run the next line:

```
  $ pip install epydoc
```

You can clone the repo using the following command:

```
  $ git clone git@bitbucket.org:madcapsulemedia/madcoin-restful-api.git
```

Run instructions
================

After clone the project go to `madcoin-restful-api/madcoin` folder and set execute rights to the `run.py` script and the execute it

```
  $ chmod a+x run.py
  $ python run.py
```

Do not forget to configure and run your coins server daemon first

```
  $ nano ~/.bitcoin/bitcoin.conf
  $ ./bitcoind
```

How to use it
=============

To connect our `app` to our `bitcoind` we have to run first the connect command following this URL:

[connect to local]: http://127.0.0.1:5000/connectlocal

Then if we wanna check the info of our coin server:

[get info]: http://127.0.0.1:5000/getinfo

We only have to connect ones to be able to access to the server, in the `debug mode` we can find anoying that the server is gonna reload each time we made a change that's means that we have to connect each time to the server, we can change this behavior with the following line inside the `run.py` file:

```
app.run(debug=True, host='0.0.0.0', use_reloader=False)

```

Instead of

```
app.run(debug=True, host='0.0.0.0')
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