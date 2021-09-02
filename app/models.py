from app import login
from app.database import db
from flask_login import UserMixin

class user0(UserMixin):
 def __init__(self, id):
  self.id = id
  self.role = str
  self.username = str
  self.group = str
 def __repr__(self):
  return "%d/%s/%s/%s/%d" % (self.id)

class dd(UserMixin):
    pass

@login.user_loader
def load_user(id):
    user0 = dd()
    user0.id = id
    db.execute("SELECT username FROM users WHERE id='%s'" %id)
    get = db.fetchone()
    user0.username = get[0]
    return user0





