from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Not the droids you\'re looking for'


if __name__ == '__main__':
    app.run()

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


# GET: Returns all contacts
@app.route('/manager/api/v1.0/contacts', methods=['GET'])
def get_contacts():
    return jsonify({'contacts': contacts})


# GET: Returns specific contact
@app.route('/manager/api/v1.0/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    return jsonify({'contact': contact[0]})


# POST: Creating a new contact only requires name
@app.route('/manager/api/v1.0/contacts', methods=['POST'])
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
def delete_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    contacts.remove(contact[0])
    return jsonify({'result': True})


# PUT: Don't go ham on updates
@app.route('/manager/api/v1.0/contacts/<int:contact_id>', methods=['PUT'])
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
    return jsonify({'contact': contact[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)



