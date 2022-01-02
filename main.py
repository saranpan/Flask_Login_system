"""
Purpose of this file is to show how we work with SQL 
"""




from flaskblog import db
from flaskblog import User, Post

# Launch database (uncomment if there is no site.db yet)
"""
db.create_all()

# User
user_1 = User(username='Wallik',email='runpan4edu@gmail.com',password='123456')
db.session.add(user_1)

user_2 = User(username='Macrostalight',email='earthza@gmail.com',password='1212312121')
db.session.add(user_2)

db.session.commit()
"""

print(f'All User: {User.query.all()}')
print(f'First User: {User.query.first()}')
print(User.query.filter_by(username='Wallik').all() )
print(User.query.filter_by(username='Macrostalight').first() )
print(User.query.filter_by(password='123456').first() )


def filter_query(username):
    return User.query.filter_by(username=username).first()


user = filter_query('Wallik')
print(user.id)

# Post
"""
post_1 = Post(title='Blog 1', content='First Post Content',user_id=user.id)
post_2 = Post(title='Blog 2', content='Second Post Content',user_id=user.id)

db.session.add(post_1)
db.session.add(post_2)

db.session.commit()
"""

print(f'All post: {Post.query.all()}')
print(f'First post by wallik: {Post.query.filter_by(user_id = 1).first()}')

print(Post.query)
