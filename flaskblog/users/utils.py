import os, secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def split_file_name(file_name):
    return file_name.split('.')[0]

def check_duplicate_file(check_file,all_file):
    name_list = list(map(split_file_name,all_file))
    if check_file in name_list:
        random_hex = secrets.token_hex(8)
        return check_duplicate_file(random_hex, all_file)
    else: 
        return check_file

def save_picture(form_picture):

    all_picture = os.listdir('flaskblog\static\profile_pics')
    
    # Prevent duplicated profile picture file name
    random_hex = check_duplicate_file(secrets.token_hex(8),all_picture)

    #f_ext as file name (eg. JPG, PNG)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static\profile_pics', picture_fn)
    
    

    #To save the memory of our database
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_mail(user):
    token = user.request_token()

    msg = Message('Password Reset Request',
                  sender='wallik.noreply@gmail.com',
                  recipients=[user.email])

    msg.body = f'''Hi {user.username}
    To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

Ignore this message if you didn't request'''

    mail.send(msg)
