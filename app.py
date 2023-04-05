from flask import Flask, render_template, request, redirect, session, url_for
import firebase_admin
from firebase_admin import db,auth
from firebase_admin import credentials
import pyrebase
import json
import uuid

app = Flask(__name__)
app.secret_key = "kjdsd32423r3r@#@#@(!jbdsfwef)"
firebaseConfig = json.load(open('/Users/ripunjaysingh/learn/GOOGLE_SOLUTIONS/cred.json'))
firebass = pyrebase.initialize_app(firebaseConfig)
sb = firebass.database()
username=None
cred = credentials.Certificate("/Users/ripunjaysingh/learn/GOOGLE_SOLUTIONS/cred.json")
firebase=firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://urbanworkers-21f47-default-rtdb.firebaseio.com/'
})
pb = pyrebase.initialize_app(json.load(open('/Users/ripunjaysingh/learn/GOOGLE_SOLUTIONS/cred.json')))

user_id = None

@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():  

    return render_template('registrationform.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            global username
            username=email.split('@')[0]
            print(email,password)
            try:
                user = firebass.auth().sign_in_with_email_and_password(email, password)
                session['user'] = user
                print("success")
                jwt = user['idToken']
                global user_id
                user_id = user['localId']
                print(user_id)
                user_type = sb.child("users").child(username).get().val()['user_type']
                print(user_type)
                if user_type.lower() == 'get-hired':
                    return redirect(url_for('worker_interface'))
                elif user_type.lower() == 'hire':
                    return redirect(url_for('index'))
            except Exception as e:
                return f"{e}"
        return render_template("index.html")


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
        username=email.split('@')[0]
        id=str(uuid.uuid4())
        user=auth.create_user(
               email=email,
               password=password    
        )

        sb.child('users').child(username).set({
        'name': name,
        'email': email,
        'phone_no': phone_no,
        'address': address,
        'password': password,
        'dob': dob,
        'adhar': adhar,
        'user_type': select_option

            })

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


@app.route('/hirer_interface', methods=['GET', 'POST'])
def hirer_interface():
    if request.method == 'POST':
        work_type = request.form['work_type']
        amount = request.form['amount']
        start_date = request.form['start_date']
        working_hours = request.form['working_hours']
        email = request.form['email']
        phone = request.form['phone']
        sb.child('users').child(username).child('jobs_posted').child(work_type).set({
        'work_type': work_type,
        'amount': amount,
        'start_date': start_date,
        'working_hours': working_hours,
        'email': email,
        'phone': phone
        })
    
    return render_template('jobs_form.html')

@app.route('/hire', methods=['GET', 'POST'])
def index():

    return render_template('hirer.html')

if __name__ == '__main__':
    app.run(debug=True)