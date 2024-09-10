import matplotlib
import numpy as np
import #Make sure that flask_login and bcrypt are installed
from flask_login import login_user,logout_user,current_user,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

from django import shortcuts

#Position all of this after the db and app have been initialised

login_manager.init_app(app)
@login_manager.user_loader
def user_loader(user_id):
    #TODO change here
    return User.query.get(user_id)

import seaborn as sb
print("My changes are done")
print("123456789")