from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

if __name__ == '__main__':
    app.run()


# NOTE: This is not the ideal method to handle auth. Passwords should be salted and hashed, and obviously not stored
# in plaintext in an app. However, this works to demonstrate the requirement of authentication
@auth.get_password
def get_password(username):
    if username == 'Randall':
        return 'potatosack'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# Dummy data
contacts = [
    {
        'id': 1,
        'name': 'Ronald Snorlax',
        'phones': [
            {'type': 'work', 'number': '+1(212)867-5309'},
            {'type': 'home', 'number': '1-900-MIX-A-LOT'}
            ],
        'addresses': [
            {'type': 'home', 'address': 'A1A Beachfront Ave, Miami, FL, 32080'},
            {'type': 'work', 'address': '1 Infinite Loop Road, Cupertino, CA, 90210'}
            ],
        'emails': [
            {'type': 'home', 'email': 'rsnore@compuserve.net'},
            {'type': 'work', 'email': 'bgates@aol.com'}
        ]
    },
    {
        'id': 2,
        'name': 'Emily Grace',
        'phones': [
            {'type': 'work', 'number': '+91 0010-212'},
            {'type': 'home', 'number': '911'}
        ],
        'addresses': [
            {'type': 'home', 'address': 'Tietgensgade 37, DK-1566 COPENHAGEN V, DENMARK'},
            {'type': 'work', 'address': 'Sølvgade 83, opg. S, DK-1307 København K., DENMARK'}
        ],
        'emails': [
            {'type': 'home', 'email': 'egrace@geocities.com'},
            {'type': 'work', 'email': 'darkener@prodigy.net'}
        ]
    }
]


@app.route('/')
def index():
    return 'Not the droids you\'re looking for'


# GET: Returns all contacts
@app.route('/manager/api/v1.0/contacts', methods=['GET'])
def get_contacts():
    return jsonify({'contacts': [make_public_contact(contact) for contact in contacts]})


# GET: Returns specific contact
@app.route('/manager/api/v1.0/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    return jsonify({'contact': contact[0]})


# POST: Creating a new contact only requires name
@app.route('/manager/api/v1.0/contacts', methods=['POST'])
@auth.login_required
def create_contact():
    if not request.json or 'name' not in request.json:
        abort(400)
    contact = {
        'id': contacts[-1]['id'] + 1,
        'name': request.json['name'],
        'phones': request.json.get('phones', ""),
        'addresses': request.json.get('addresses', ""),
        'emails': request.json.get('emails', "")
    }
    contacts.append(contact)
    return jsonify({'contact': contact}), 201


# DELETE: Just go ham on deletion
@app.route('/manager/api/v1.0/contacts/<int:contact_id>', methods=['DELETE'])
@auth.login_required
def delete_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    contacts.remove(contact[0])
    return jsonify({'result': True})


# PUT: Don't go ham on updates
# TODO: "Store a ref to the authenticated user in the modified record"
@app.route('/manager/api/v1.0/contacts/<int:contact_id>', methods=['PUT'])
@auth.login_required
def update_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    if not request.json:
        abort(400)
    contact[0]['name'] = request.json.get('name', contact[0]['name'])
    contact[0]['phones'] = request.json.get('phones', contact[0]['phones'])
    contact[0]['addresses'] = request.json.get('addresses', contact[0]['addresses'])
    contact[0]['emails'] = request.json.get('emails', contact[0]['emails'])
    contact[0]['modified_by'] = auth.username()
    return jsonify({'contact': contact[0]})


# Returns contacts with a URI instead of a contactID
def make_public_contact(contact):
    new_contact = {}
    for field in contact:
        if field == 'id':
            new_contact['uri'] = url_for('get_contact', contact_id=contact['id'], _external=True)
        else:
            new_contact[field] = contact[field]
    return new_contact


# These are provided so that error responses return JSON as expected
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)



