from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import db,auth
from firebase_admin import credentials
import pyrebase
import json
import uuid

app = Flask(__name__)

firebaseConfig = {
  "apiKey": "AIzaSyDLob3jrEFEfaxZyq9keF2gU9j-NQRgZic",
  "authDomain": "urbanworkers-21f47.firebaseapp.com",
  "databaseURL": "https://urbanworkers-21f47-default-rtdb.firebaseio.com",
  "projectId": "urbanworkers-21f47",
  "storageBucket": "urbanworkers-21f47.appspot.com",
  "messagingSenderId": "645367486525",
  "appId": "1:645367486525:web:88905f7fc97042eeea7254",
  "measurementId": "G-XMQ9WP3XPY"
}

firebass = pyrebase.initialize_app(firebaseConfig)
sb = firebass.database()
#auth = firebase.auth()
cred = credentials.Certificate("/Users/ripunjaysingh/learn/GOOGLE_SOLUTIONS/cred.json")
firebase=firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://urbanworkers-21f47-default-rtdb.firebaseio.com/'
})
pb = pyrebase.initialize_app(json.load(open('/Users/ripunjaysingh/learn/GOOGLE_SOLUTIONS/cred.json')))

user_id = None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = sb.auth().sign_in_with_email_and_password(email, password)
            jwt = user['idToken']
            global user_id
            user_id = user['localId']
            
            return render_template("home.html")
        except:
            return render_template("index.html")
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():  

    return render_template('registrationform.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
        """        user_type = sb.child("users").child(user_id).child("user_type").get().val()
                print(user_type)
                if user_type == 'Get Hired':
                    return render_template('workers.html')
                elif user_type == 'Hire':
                    return render_template('hirer.html')
        """
        return render_template("home.html")



@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name=request.form.get("name")
        email=request.form.get("email")
        phone_no=request.form.get("phone")
        address=request.form.get("address")
        password=request.form.get("password")
        dob=request.form.get("dob")
        adhar=request.form.get("adhar")
        select_option = request.form['selectOption']

        #print(name,email,phone_no,address,password,dob,adhar,select_option)
        
         # generate unique random id as Firebase key
        id=str(uuid.uuid4())
        user=auth.create_user(
               email=email,
               password=password    
        )

        sb.child('users').push({
        'name': name,
        'email': email,
        'phone_no': phone_no,
        'address': address,
        'password': password,
        'dob': dob,
        'adhar': adhar,
        'user_type': select_option

            })
        
    """
            db.reference().child('users').push({
            'name': name,
            'email': email,
            'phone_no': phone_no,
            'address': address,
            'password': password,
            'dob': dob,
            'adhar': adhar

                })"""

    return render_template('submit.html')

@app.route('/worker_interface', methods=['GET', 'POST'])
def worker_interface():
        rows = [
        {
            "work_type": "Web Development",
            "amount": "$1000",
            "start_date": "April 15, 2023",
            "working_hours": "9am-5pm",
            "email": "john@example.com",
            "phone": "123-456-780"
        },
        {
            "work_type": "Graphic Design",
            "amount": "$500",
            "start_date": "May 1, 2023",
            "working_hours": "10am-2pm",
            "email": "jane@example.com",
            "phone": "555-555-5555"
        }
    ]
        return render_template("workers.html", rows=rows)

@app.route('/hire', methods=['GET', 'POST'])
def index():
    workers = [
        {
            "name": "Worker 1",
            "location": {
                "lat": 37.7749,
                "lng": -122.4194
            }
        },
        {
            "name": "Worker 2",
            "location": {
                "lat": 37.7799,
                "lng": -122.4294
            }
        },
        {
            "name": "Worker 3",
            "location": {
                "lat": 37.7699,
                "lng": -122.4194
            }
        },
        {
            "name": "Worker 4",
            "location": {
                "lat": 37.7749,
                "lng": -122.4094
            }
        },
        {
            "name": "Worker 5",
            "location": {
                "lat": 37.7699,
                "lng": -122.4294
            }
        }
    ]
    return render_template('hirer.html', workers=workers)

if __name__ == '__main__':
    app.run(debug=True)