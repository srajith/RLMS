#!/usr/bin/env python

from rlms import db,bcrypt
from rlms.models import User
db.drop_all()
db.create_all()
user = User(username="admin", password=bcrypt.generate_password_hash("password"))
db.session.add(user)
db.session.commit()
