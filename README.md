## Application Launch

To launch this application: from the directory in which app.py is located, run

```
python.exe -m flask run
```

The app shall be available on http://localhost:5000/

## Endpoints

**GET Contacts** /manager/api/v1.0/contacts

Get a list of contacts


**GET Contacts (Search)**
/manager/api/v1.0/contacts?name=<search_term>

Get a list of contacts, seaching by the name field


**GET Contacts**
/manager/api/v1.0/contacts/<contact_id>

Get a contact where the id is contact_id


**POST New Contact**
/manager/api/v1.0/contacts

Create a new contact


**DELETE Contact**
/manager/api/v1.0/contacts/<contact_id>

Delete a contact


**PUT Contact**
/manager/api/v1.0/contacts/<contact_id>

Replace a contact's data


**Blank Index**
/manager/api/v1.0/

Currently blank


## Notes
All data is stored in memory. The username:pw is store in app.py to fulfill a requirement
that data not be read from the filesystem. 