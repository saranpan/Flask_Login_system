
from flaskblog import db

#db.create_all()

from flaskblog.models import User, Post

#user = User(username='walnut', email='walnut@gmail.com', password='saaas')
#db.session.add(user)
#db.session.commit()

for user in User.query.all():
    print(user)
    #db.session.delete(user)
    #db.session.commit()
#db.session.commit()
    

#deleted_user = User.query.filter_by(username='junior').first()
#print(deleted_user)
#db.session.delete(deleted_user)
#db.session.commit()

