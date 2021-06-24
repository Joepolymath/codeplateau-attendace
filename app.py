from enum import unique
from flask import Flask, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date
from werkzeug.utils import redirect

app = Flask(__name__)

app.secret_key = "b21d878901ac8040094c8e501c7054df2573020c"
# finding the current app path. (Location of this file)
project_dir = os.path.dirname(os.path.abspath(__file__))

# creating a database file (bookdatabase.db) in the above found path.
database_file = "sqlite:///{}".format(os.path.join(project_dir, "codeplateau.db"))

# connecting the database file (bookdatabase.db) to the sqlalchemy dependency.
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# connecting this app.py file to the sqlalchemy
db = SQLAlchemy(app)
today = date.today()
today_str = today.strftime("%Y-%m-%d")
class Attendance(db.Model):
    firstname = db.Column(db.String(40), unique = False, nullable= False)
    lastname = db.Column(db.String(40), unique = False, nullable= False)
    email = db.Column(db.String(40), unique = True, nullable= False, primary_key=True)
    date = db.Column(db.String, nullable = False, default = today_str)

    def __repr__(self):
        return "First Name: {}: Last Name{}".format(self.firstname, self.lastname)

class Registration(db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"This user is {self.username}"

@app.route('/', methods = ["GET", "POST"])
def home():
    if "user" in session:
        if request.form:
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            dateAdded = request.form.get("date")
            print(dateAdded)

            fellow = Attendance(firstname=firstname, lastname=lastname, email=email)
            db.session.add(fellow)
            db.session.commit()
        
        # fellows = Attendance.query.all()

        return render_template("index.html")
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        users = Registration.query.all()
        for user in users:
            if username == user.username and password == user.password:
                session['user'] = user.username
                print("Logged in")
                return redirect(url_for('home'))
                
            else:
                print("unknown user")
    elif "user" in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route('/views', methods=['GET', 'POST'])
def view():
    if "user" in session:
        if request.form:
            choice_date = request.form.get("date")
            fellows_present = Attendance.query.filter_by(date=choice_date).all()
            total_present = len(fellows_present)
            return render_template("views.html", fellows_present=fellows_present, attendance_date=today_str, total_present=total_present, choice_date=choice_date)
        return render_template("views.html")

@app.route('/update/<person>', methods=['GET', 'POST'])
def update(person):
    fellow_to_update = Attendance.query.filter_by(email=person, date=today_str)[0]
    if request.form:
        fellow_to_update.firstname = request.form.get('firstname')
        fellow_to_update.lastname = request.form.get('lastname')
        fellow_to_update.email = request.form.get('email')
        db.session.commit()
        try:
            db.session.commit()
            return redirect(url_for('view'))
        except:
            return render_template("update.html", person=person, fellow_to_update=fellow_to_update)
    else:
        return render_template("update.html", person=person, fellow_to_update=fellow_to_update)

@app.route('/delete/<person>')
def delete(person):
    if "user" in session:
        user_to_delete = Attendance.query.filter_by(email=person, date=today_str)
        # print(user_to_delete)
        db.session.delete(user_to_delete[0])
        db.session.commit()
        return redirect(url_for('view'))
if __name__ == "__main__":
    app.run(debug=True)
