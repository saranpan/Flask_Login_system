from flask import Flask, render_template, url_for, flash , redirect  
from forms import RegistrationForm, LoginForm
from SECRET_KEY import SECRET_KEY


app = Flask(__name__)
# prevent CSRF 
app.config['SECRET_KEY'] = SECRET_KEY

# Variable
post = [
    {'author': 'Saran Pannasuriyaporn',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Dec 31, 2021'
        },
    {'author': 'Nuchpol Arpassompob',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Jan 1, 2022'
        }]        
            



#Treat "/" and "/about" as the same routes
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=post)

@app.route("/about")
def about():
    return render_template('about.html',title='about')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)







# debug = True : automatically update without rerun
if __name__ == "__main__":
    app.run(debug=True)

