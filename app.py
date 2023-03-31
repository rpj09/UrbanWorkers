from flask import Flask, render_template, request
import pyrebase
import uuid
#https://urbanworkers-21f47-default-rtdb.firebaseio.com/
app = Flask(__name__)

config = {
  "apiKey": "AIzaSyDLob3jrEFEfaxZyq9keF2gU9j-NQRgZic",
  "authDomain": "urbanworkers-21f47.firebaseapp.com",
  "databaseURL": "",
  "projectId": "urbanworkers-21f47",
  "storageBucket": "urbanworkers-21f47.appspot.com",
  "messagingSenderId": "645367486525",
  "appId": "1:645367486525:web:88905f7fc97042eeea7254",
  "measurementId": "G-XMQ9WP3XPY"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_data = db.child("users").child(username).get().val()
        
        if user_data and user_data["password"] == password:
            return "You're logged in!"
        else:
            return "Invalid credentials."
    
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():  # sourcery skip: avoid-builtin-shadow
    """    
        if request.method == 'POST':
            name=request.form.get("name")
            email=request.form.get("email")
            phone_no=request.form.get("phone_no")
            address=request.form.get("address")
            # get input values from registration form
            
            # generate unique random id as Firebase key
            id=str(uuid.uuid4())
            
            # create a new child with the generated key under users node
            db.child("users").child(id).set({
                "name": name,
                "email": email,
                "phone_no": phone_no,
                "address": address,
                })
            
    """       
        
    return render_template('registrationform.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name=request.form.get("name")
        email=request.form.get("email")
        phone_no=request.form.get("phone_no")
        address=request.form.get("address")
         # get input values from registration form
        
         # generate unique random id as Firebase key
        id=str(uuid.uuid4())
         
         # create a new child with the generated key under users node
        db.child("users").child(id).set({
             "name": name,
             "email": email,
             "phone_no": phone_no,
             "address": address,
              })
         
         
    
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)