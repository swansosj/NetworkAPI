#!/usr/bin/python3

import flask
from flask import Flask, render_template, url_for, flash, redirect
from flask import request, jsonify
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '78192317937fc773856866c82a6f4297'


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form )

@app.route('/login')
def login():
    form = LoginForm()
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

if __name__ == '__main__':
    app.run(port=80, debug=True, host='0.0.0.0',)
