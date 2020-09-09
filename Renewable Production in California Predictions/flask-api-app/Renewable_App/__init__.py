# this init folder allows the runServer code in the root of repo to treat this directory as a package 

from flask import Flask
app = Flask(__name__, template_folder='templates')

import Renewable_App.views
import Renewable_App.api