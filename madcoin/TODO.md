These things still have to be added:

* SSL support (including certificate verification) for managing remote coin daemons. (bitcoin-python library)

* I recommend implementing to_json methods on your objects that return a Python object (dictionary etc.) that can be safely converted to JSON by jsonify.

* There are more info from the coin service that the showed here.

* Finish to setup the file requirements.txt (to autoinstall all the dependecies)

* Create a Vagrant enviroment to be able to spread our develop enviroment