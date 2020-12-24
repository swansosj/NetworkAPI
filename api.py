#!/usr/bin/python3

import flask
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)


course = [
    {'id':0,
    'course': 'Software Defined Networking',
    'school': 'Florida State College at Jacksonville',
    'instructor': 'Sheldon Swanson'}
]

protocols = [
    {'id': 0,
    'name': 'Domain Name System',
    'acronym': 'DNS',
    'port': '53',
    'osi': 'application layer',
    'rfc': '1035',
    'purpose': 'Name and IP Address resolution'},
    {'id': 1,
    'name': 'Dynamic Host Control Protocol',
    'acronym': 'DHCP',
    'port': '67',
    'osi': 'application layer',
    'rfc': '2131',
    'purpose': 'Dynamic IP Address Allocation'},
    {'id': 2,
    'name': 'File Transfer Protocol',
    'acronym': 'FTP',
    'port': '21',
    'osi': 'application layer',
    'rfc': '959',
    'purpose': 'Transfer Files'},
    {'id': 3,
    'name': 'Hypertext Transfer Protocol',
    'acronym': 'HTTP',
    'port': '80',
    'osi': 'application layer',
    'rfc': '2616',
    'purpose': 'Service web pages to web clients'},
    {'id': 4,
    'name': 'Hypertext Transfer Protocol Secure',
    'acronym': 'HTTPS',
    'port': '443',
    'osi': 'application layer',
    'rfc': '2818',
    'purpose': 'Securly services web pages to web clients'},
    {'id': 5,
    'name': 'Internet Message Access Protocol',
    'acronym': 'IMAP',
    'port': '993',
    'osi': 'application layer',
    'rfc': '3501',
    'purpose': 'Retrieve email messages by email clients from mail servers'},
    {'id': 6,
    'name': 'Lightweight Directory Access Protocol',
    'acronym': 'LDAP',
    'port': '389,636',
    'osi': 'application layer',
    'rfc': '4511',
    'purpose': 'Vendor neurtral directory services protocol commonly used for authentiction against directory servers'},
    {'id': 7,
    'name': 'Network Time Protocol',
    'acronym': 'NTP',
    'port': '123',
    'osi': 'application layer',
    'rfc': '5905',
    'purpose': 'Time/clock syncronyzation between computer systems'},
    {'id': 8,
    'name': 'Post Office Protocol Version 3',
    'acronym': 'POP3',
    'port': '110',
    'osi': 'application layer',
    'rfc': '1939',
    'purpose': 'Retrieve email messages by email clients from mail servers'},
    {'id': 9,
    'name': 'Real-time Transport Protocol',
    'acronym': 'RTP',
    'port': 'Random 16384-32767',
    'osi': 'application layer',
    'rfc': '3550',
    'purpose': 'Carry medium streams such as audio and video via UDP'},
    {'id': 10,
    'name': 'Session Initiation Protocol',
    'acronym': 'SIP',
    'port': '5060,5061',
    'osi': 'application layer',
    'rfc': '3261',
    'purpose': 'Session manager for endpoint media sessions such as voice and video'},
    {'id': 11,
    'name': 'Simple Mail Transfer Protocol',
    'acronym': 'SMTP',
    'port': '25',
    'osi': 'application layer',
    'rfc': '5321',
    'purpose': 'Send and retrieve email messages'},
    {'id': 12,
    'name': 'Simple Network Management Protocol',
    'acronym': 'SNMP',
    'port': '161,162',
    'osi': 'application layer',
    'rfc': '1157',
    'purpose': 'Monitor network devices by querying the MIB tables'},
    {'id': 13,
    'name': 'Secure Shell',
    'acronym': 'SSH',
    'port': '22',
    'osi': 'application layer',
    'rfc': '4253',
    'purpose': 'Secure connection for managment of network devices and services'},
    {'id': 14,
    'name': 'Telnet',
    'acronym': 'Telnet',
    'port': '23',
    'osi': 'application layer',
    'rfc': '854',
    'purpose': 'Unsecure connection for managment of network devices and services. Should NOT be used!'},
    {'id': 15,
    'name': 'Address Resolution Protocol',
    'acronym': 'ARP',
    'port': 'N/A',
    'osi': 'data link layer',
    'rfc': '826',
    'purpose': 'Resolves layer two MAC addresses to Layer 3 IP addresses'}
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome SDN World!!!</h1><p>This is an example API service with Flask</p>"

@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(course)

@app.route('/api/protocols', methods=['GET'])
def api_protocols():
    return jsonify(protocols)

if __name__ == '__main__':
    app.run(port=80, debug=True, host='0.0.0.0',)
