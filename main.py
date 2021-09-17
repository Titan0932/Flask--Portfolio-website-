from website import create_app
from flask import Flask, render_template,request,url_for,redirect,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy





app=create_app()


db=SQLAlchemy(app)        #db is the object for our database for app 



class users(db.Model):                                                              #the database class: name should be as above?
    _id=db.Column("id",db.Integer, primary_key=True)
    uname=db.Column(db.String(100))
    uemail=db.Column(db.String(100))

    def __init__(self,username,email):
        self.uname=username
        self.uemail=email



@app.route('/view5C201B')
def view():
    if not users.query.all():
        flash("Database Empty!!")
    return render_template('view.html', values=users.query.all())

@app.route('/view5C201B/del=<email>')
def del_users(email):
    found_user=users.query.filter_by(uemail=email).first()
    if found_user:
        found_user=users.query.filter_by(uemail=email).delete()
        db.session.commit()
        flash(f'{email} deleted')
    else:
        flash('User not found')
    return render_template('view.html')




@app.route('/',methods=["POST","GET"])
def login():

    if request.method=="POST":
        session.permanent=True          #makes this session permanent
        user=request.form["Username"]
        passw=request.form["Password"]
        email=request.form["Email"]
        if user=="" or passw=="" or email=="":
            flash("Please Enter all login credentials")
            return redirect(url_for('login'))               # If form submitted without input redirect back to login
        if passw!="Alohomora":                                     #only users with password enter
            flash("Incorrect password!!")
            return redirect(url_for('login'))
        else:
            found_user=users.query.filter_by(uemail=email).first() and users.query.filter_by(uname=user).first()         #check if a user exists in the database
            if not found_user:                       
                usr=users(user,email)                          #if new user, add username and email to the database
                db.session.add(usr)
                db.session.commit()                                         #new data isnt immediately added. 'commit' saves all the changes made to the database

        session["user"]=user                                    # stores username in dictionary session under key: "user"
        return redirect(url_for('home'))
    else:
        if "user" in session:
            flash('Already Logged in')
            return redirect(url_for('home'))
        return render_template('login.html')
            
        



@app.route('/home', methods=["POST","GET"])
def home():
    if "user" in session:
        user=session["user"]
        if request.method=="POST":
            email=request.form["Email"]                             #if logged in initially, store the email in the session
            session["Email"]=email
        
        flash(f'{user} logged in!!')                            #if user has logged in, go to home
        return render_template('Home.html')     
    else:
        flash("Please Login First")
        return redirect(url_for("login"))               #if not then go to login page        



@app.route('/logout')
def logout():
    if "user" in session:

        flash('Logged out Successfully!!')
        session.pop("user", None)  # remove data of key:"user" from session
    else:
        flash('Please Login First')
    return redirect(url_for('login'))           #go back to login page
    

    
    
@app.route('/contact/')
def contact():
    if "user" in session:
        return render_template('contacts.html')
    else:
        flash("Please Login First")
        return redirect(url_for("login")) 

@app.route('/projects/')
def projects():
    if "user" in session:
        return render_template('projects.html')
    else:
        flash("Please Login First")
        return redirect(url_for("login")) 

@app.route('/resume/')
def resume():
    if "user" in session:
        return render_template('resume.html')
    else:
        flash("Please Login First")
        return redirect(url_for("login")) 

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)