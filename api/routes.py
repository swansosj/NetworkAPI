from flask import render_template, url_for, flash, redirect
from api import app, db, bcrypt
from api.forms import RegistrationForm, LoginForm
from api.models import User, Post
from flask_login import login_user, current_user

course = [
    {
    'id':0,
    'course': 'Software Defined Networking',
    'school': 'Florida State College at Jacksonville',
    'instructor': 'Sheldon Swanson'
    }
]

proto = [
    {
    'id':0,
    'name': 'Domain Name System',
    'acron': 'DNS',
    'port': '53',
    'osi': 'application layer',
    'rfc': '1035',
    'purpose': 'Name and IP Address resolution'
    },
    {
    'id':1,
    'name': 'Dynamic Host Control Protocol',
    'acron': 'DHCP',
    'port': '67',
    'osi': 'application layer',
    'rfc': '2131',
    'purpose': 'Dynamic allocation of IP addresses to end hosts'
    },
    {
    'id':2,
    'name': 'File Transfer Protocol',
    'acron': 'FTP',
    'port': '21',
    'osi': 'application layer',
    'rfc': '959',
    'purpose': 'Transfer Files'
    },
    {
    'id':3,
    'name': 'Hypertext Transfer Protocol',
    'acron': 'HTTP',
    'port': '80',
    'osi': 'application layer',
    'rfc': '2616',
    'purpose': 'Delivers Hypertext media to web clients'
    }
]


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/protocols')
def protocols():
    return render_template('protocols.html', title='Protocols', proto=proto)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form )

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login Success!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form )

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(course)

@app.route('/api/protocols', methods=['GET'])
def api_protocols():
    return jsonify(protocols)
