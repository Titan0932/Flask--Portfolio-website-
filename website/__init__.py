from flask import Flask,render_template
from datetime import timedelta



def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']="5C201B" #key for encryption
    app.permanent_session_lifetime=timedelta(minutes=5)               #specified session keys are stored permanently for 5 minutes/can change to days,etc as well even after browser closed
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'       #users is the table to which we reference later
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False                      #basic configurations for setting up a database     

    return app