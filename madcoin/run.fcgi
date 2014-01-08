#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from app import app

import os, pwd
os.environ["HOME"] = pwd.getpwuid(os.getuid()).pw_dir

if __name__ == '__main__':
    WSGIServer(app).run()
