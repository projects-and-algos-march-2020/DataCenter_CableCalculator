from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = 'password'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datacenter_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, server_default=func.now())  
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class daily_work_fibers(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    brick_position = db.Column(db.String(45))
    rack_position = db.Column(db.String(45))
    fiber_length = db.Column(db.String(45))
    number_cable = db.Column(db.String(45))
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("users", foreign_keys=[users_id], backref="daily_work_fibers", cascade="all")
    created_at = db.Column(db.DateTime, server_default=func.now())  
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

@app.route("/")
def index():
    return(render_template('index.html'))

@app.route("/add", methods=["POST"])
def add_user():
    is_valid = True
    if len(request.form['UN']) < 2:
        is_valid = False
        flash("Please enter a username that is atleast 3 characters long")
    if len(request.form['PW']) < 4:
        is_valid = False
        flash("Password should be at least 5 characters")
    if not request.form['PW'] == request.form['Confirm_PW']:
        is_valid = False
        flash("Password does not match")

    if is_valid:
        
        pw_hash = bcrypt.generate_password_hash(request.form['PW'])

        new_instance_of_a_user = users(username=request.form['UN'], password=pw_hash)
        db.session.add(new_instance_of_a_user)
        db.session.commit() 
    
    return redirect('/')

@app.route("/login", methods=["POST"])
def login():
    user = users.query.filter_by(username=request.form['UN']).first_or_404()

    if not bcrypt.check_password_hash(user.password, request.form['PW']):
         flash("Incorrect password")
         return redirect("/") 
    else: 
        session['user_id'] = user.id 
        return redirect("/menu") 
    return redirect('/')

@app.route("/menu")
def menu():
    if 'user_id' not in session:
        return redirect('/')
    user = users.query.filter_by(id=session['user_id']).first_or_404()
    cable = daily_work_fibers.query.all()

    print(session)
    return render_template("menu.html", user=user, cable=cable)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/edit')
def edit():
    user = users.query.filter_by(id=session['user_id']).first_or_404()
    return render_template("edit.html", user=user)

@app.route('/calculator')
def calculator():
    user = users.query.filter_by(id=session['user_id']).first_or_404()
    cable = daily_work_fibers.query.all()
    return render_template("calculator.html", user=user,  cable=cable)

@app.route('/delete_cable/<cable_id>')
def delete_cable(cable_id):
    print(cable_id)
    daily_work_fibers.query.filter_by(id=cable_id).delete()
    db.session.commit()
    return redirect('/calculator')

# @app.route('/delete_user/<user.id>')
# def delete_cable(user.id):
#     print(user.id)
#     return redirect

@app.route('/print_friendly')
def printerfriendly():
    user = users.query.filter_by(id=session['user_id']).first_or_404()
    cable = daily_work_fibers.query.all()
    return render_template("printerfriendly.html", user=user, cable=cable)

@app.route('/datacenter_editor')
def datacenter_editor():
    user = users.query.filter_by(id=session['user_id']).first_or_404()
    cable = daily_work_fibers.query.all()
    return render_template("datacenter_editor.html", user=user, cable=cable)

@app.route('/math', methods=["POST"])
def math():
    in_row = abs((int(str(request.form['RP'])[:-2]) - int(str(request.form['BP'])[:-2]))) * 2
    print("in row", in_row)
    
    number_rows = abs((int(str(request.form['RP'])[:2]) - int(str(request.form['BP'])[:2]))) * 5
    print("number rows", number_rows)
    
    rack_drop = int(10)
    brick_drop = int(15)
    
    answer = (int(in_row) + int(number_rows) + int(rack_drop) + int(brick_drop)) / int(3)
    print("answer", answer)
    
    total = round(answer) 
    print("total", total)
    
    new_instance_of_a_cable = daily_work_fibers(brick_position=request.form['BP'], rack_position=request.form['RP'], fiber_length=total, number_cable=request.form['CA'], users_id=session['user_id'])

    db.session.add(new_instance_of_a_cable)
    db.session.commit() 
    return redirect('/calculator')

if __name__ == '__main__':
    app.run(debug=True)