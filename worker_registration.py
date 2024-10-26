import secrets
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Blueprint
from database import connet,commit_all
import re


db = connet()

worker_registration_page = Blueprint('worker_registration_page',__name__)



def validate_password(password):
    # Check for minimum length (adjust as needed)
    if len(password) < 8:
        return "minimum lene is 8"

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return "at least one uppercase letter needed"

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return "at least one lowercase letter needed"

    # Check for at least one digit
    if not re.search(r'\d', password):
        return "at least one digit needed"

    # Check for at least one special character (adjust as needed)
    if not re.search(r'[^\w\s]', password):
        return "at least one special character needed"

    return True


def add_details_employer(name,address,email,mobile,govt,user,password,experience,expertise):
        query = "INSERT INTO worker (name,address,email_id,mobile_no,govt_id,user_id,password,experience,expertise_field) VALUES (%s, %s,%s, %s, %s, %s, %s,%s,%s)"
        val = (name,address,email,mobile,govt,user,password,experience,expertise)
        db.execute(query,val)
        commit_all()
        



@worker_registration_page.route('/register_worker',methods = ['POST'])
def register():
    name = request.form['name']
    address = request.form['address']
    email = request.form['email_id']
    mobile = request.form['mobile_no']
    govt = request.form['govt_id']
    password = request.form['password']
    experience  = request.form['experience']
    expertise = request.form['expertise_field']
    # print(type(Name))
    if '@' not in email:
        flash('incorrect email', 'error')
        return render_template('worker_registration.html')
    if int(mobile)!= True and len(mobile) != 10:
        flash('incorrect mobile no', 'error')
        return render_template('worker_registration.html')
    if len(govt)<4:
        flash('incorrect govt id', 'error')
        return render_template('worker_registration.html')
    if validate_password(password) != True:
        reason = validate_password(password)
        flash(reason,'error')
        return render_template('worker_registration.html')
    user = name[:4]+mobile[7:]+govt[:4]
    print(user)
    add_details_employer(name,address,email,mobile,govt,user,password,experience,expertise)
    flash('registration successful')
    return render_template('worker_login.html')