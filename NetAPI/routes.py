import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from NetAPI import app, db, bcrypt
from NetAPI.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProtocolForm
from NetAPI.models import User, Post, Protocol
from flask_login import login_user, current_user, logout_user, login_required

course = [
    {
    'id':0,
    'course': 'Software Defined Networking',
    'school': 'Florida State College at Jacksonville',
    'instructor': 'Sheldon Swanson'
    }
]

protolssss = [
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
    protocols = Protocol.query.all()
    return render_template('protocols.html', title='Protocols', protocols=protocols)

@app.route('/protocols/new', methods=['GET','POST'])
@login_required
def new_protocol():
    form = ProtocolForm()
    if form.validate_on_submit():
        protocol = Protocol(name=form.name.data, acronym=form.acronym.data, port=form.port.data, layer=form.layer.data,
                            rfc=form.rfc.data, purpose=form.purpose.data, wiki_link=form.wiki_link.data, rfc_link=form.rfc_link.data, author=current_user)
        db.session.add(protocol)
        db.session.commit()
        flash(f'The protocol has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_protocol.html', title='Add Protocol', form=form, legend='New Protocol')

@app.route('/protocols/<int:protocol_id>', methods=['GET'])
def protocol(protocol_id):
    protocol = Protocol.query.get_or_404(protocol_id)
    return render_template('protocol.html', title=protocol.name, protocol=protocol)

@app.route('/protocols/<int:protocol_id>/update', methods=['GET','POST'])
@login_required
def update_protocol(protocol_id):
    protocol = Protocol.query.get_or_404(protocol_id)
    if protocol.author != current_user:
        abort(403)
    form = ProtocolForm()
    if form.validate_on_submit():
        protocol.name = form.name.data
        protocol.acronym = form.acronym.data
        protocol.port = form.port.data
        protocol.layer = form.layer.data
        protocol.rfc = form.rfc.data
        protocol.purpose = form.purpose.data
        protocol.wiki_link = form.wiki_link.data
        protocol.rfc_link = form.rfc_link.data
        db.session.commit()
        flash(f'Your protocol post has been updated successfully!', 'success')
        redirect(url_for('protocol', protocol_id=protocol.id))
    elif request.method == 'GET':
        form.name.data = protocol.name
        form.acronym.data = protocol.acronym
        form.port.data = protocol.port
        form.layer.data = protocol.layer
        form.rfc.data = protocol.rfc
        form.purpose.data = protocol.purpose
        form.wiki_link.data = protocol.wiki_link
        form.rfc_link.data = protocol.rfc_link
    return render_template('add_protocol.html', title='Update Protocol', form=form, legend='Update Protocol')

@app.route('/protocols/<int:protocol_id>/delete', methods=['POST'])
@login_required
def delete_protocol(protocol_id):
    protocol = Protocol.query.get_or_404(protocol_id)
    if protocol.author != current_user:
        abort(403)
    db.session.delete(protocol)
    db.session.commit()
    flash(f'The protocol has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html', title='Contact')

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
            next_page = request.args.get('next')
            flash(f'Login Success!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form )

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash(f'You have been logged out!', 'success')
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(course)

@app.route('/api/protocols', methods=['GET'])
def api_protocols():
    return jsonify(protocols)
