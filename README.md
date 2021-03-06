madcoin-python is a set of Python libraries that allows easy access to the bitcoin peer-to-peer cryptocurrency client API throw a Restful API.

Documentation
=============

Documentation can be found here, or in the source archive. It is built
using Epydoc:

[http://epydoc.sourceforge.net/](http://epydoc.sourceforge.net/)

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

You can clone the repo using the following command:

```
  $ git clone git@bitbucket.org:madcapsulemedia/madcoin-restful-api.git
```

After install our virtual enviroment we have to install our dependencies and there are two options to do that:

## First option

```
  $ pip install flask #small framework to our python app
  $ pip install uwsgi #this is the server to host our app in production mode
  $ pip install flask-cors #plugin to support CORS on our flasky app
  $ pip install simplejson #lower json controller to handle Decimal Types
  $ pip install -e git://github.com/laanwj/bitcoin-python.git#egg=bitcoin-python #Bitcoin library to comunicate our project with our bitcoind
```

If you are having troubles installing bitcoin-python from `git` you can try with this command instead the above:

```
  $ pip install -e git+https://github.com/laanwj/bitcoin-python.git#egg=bitcoin-python
```

If we want to generate the documentation we can run the next line:

```
  $ pip install epydoc
```

## Second option

```
  $ pip install -r requirements.txt
```

Run instructions
================

#### In production

To run our app we are going to use `uWSGI` using the following command:

```
uwsgi --socket 0.0.0.0:5000 --wsgi-file run_pro.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 --protocol=http
```

That's allow us to access our app on `SERVER_URL:5000` and to access locally to a log JSON file on `127.0.0.1:9191`

> Is important to notice that for the production enviroment we are using a different `run.py` file that for development porpouse

#### In developemnt mode

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

If you wanna run the server with your own config file you should have to create a config file first and try to load it, like that:

```
  $ export MADCOIN_CONFIG="/path/to/settings.py"
  $ python run.py
```


How to use it
=============

#### In production

We are gonna use uWSGI to deploy our app and that's should be enought to know, you only need to access to the server address on the config port as:

```
    SERVER_URL:5000/getinfo
```

#### In development

As we are still developing this proyect you have to add to your "/etc/hosts" file the following entries

```
SERVER_IP_ADDRESS bitcoin.mad.local
SERVER_IP_ADDRESS litecoin.mad.local
```

Then if we wanna check the info of our coin server:

```
http://bitcoin.mad.local:5000/getinfo
```

#####If we are not using `werkzeug.wsgi` wWSGI development server (only for development porpuse):

We only have to connect ones to be able to access to the server, in the `debug mode` we can find anoying that the server is gonna reload each time we made a change that's means that we have to connect each time to the server, we can change this behavior with the following line inside the `run.py` file:

```
app.run(debug=True, host='0.0.0.0', use_reloader=False)

```

Instead of

```
app.run(debug=True, host='0.0.0.0')
```

Testing it
==========

If you wanna test our code you have to have the server running and runs as well the file test.py

```
  $ python test.py
```

Contributing
============

If you are interested in improve the code or fix some bug, your welcome just keep in mind one rule the code below was written following the `PEP8` style guide for Python code.

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
* 1003 - Address provided was not found

Resources
=========

* http://flask.pocoo.org/
* http://www.virtualenv.org/
* https://github.com/laanwj/bitcoin-python