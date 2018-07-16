from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

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


@app.route('/manager/api/v1.0/contacts', methods=['GET'])
def get_contacts():
    return jsonify({'contacts': contacts})


@app.route('/manager/api/v1.0/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = [contact for contact in contacts if contact['id'] == contact_id]
    if len(contact) == 0:
        abort(404)
    return jsonify({'contact' : contact[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
