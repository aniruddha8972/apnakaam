# import secrets
from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask import Blueprint
from database2 import db
from employer_registration import employer_registration_page
# from app import get_user
# from employer_home import home_page

# mycursor = connet()
# user_details = None

login_page = Blueprint('login_page',__name__)
login_page.register_blueprint(employer_registration_page)



def get_requests():
    employer_id = session['employer_user_id']
    db.execute('select job_posting.job_title,worker.name,worker.experience,worker.expertise_field,job_status.job_status_id from worker inner join job_status on worker.user_id = job_status.worker_id inner join job_posting on job_posting.id = job_status.job_posting_id where job_posting.employer_id = %s and job_status.job_status = %s',(employer_id,'accept',))
    job_requests = db.fetchall()
    print(job_requests)
    return job_requests

def request_transform(job_requests):
    requests = []
    for i in range(len(job_requests)):
        l = job_requests[i]
        l_set = {}
        l_set['job_title'] = l[0]
        l_set['worker_name'] = l[1]
        l_set['experience'] = l[2]
        l_set['expertise'] = l[3]
        l_set['job_status_id'] = l[4]
        
        
        requests.append(l_set)
    return requests


# @login_page.route('/job_requests',methods = ['POST'])



def get_details(emp_id):
    db.execute('select id , job_title, location from job_posting where employer_id = %s',(emp_id,))
    output = db.fetchall()    
    return output

def transform(output):
    main = []
    for i in range(len(output)):
        l = output[i]
        print(l)
        l_set ={}
        
        l_set['id'] = l[0]
        l_set['job_title'] = l[1]
        l_set['location'] = l[2]
        main.append(l_set)
    return main

def posted_jobs():
    # emp_id = request.form['id']
    emp_id = session['employer_user_id']
    print(emp_id)
    output = get_details(emp_id)
    main = transform(output)
    return main

    
    
    
    





@login_page.route('/login_view')
def login_view():
    return render_template('employer_login.html')




@login_page.route('/registration')
def register():
    return render_template('employer_registration.html')





@login_page.route('/employer_home')
def employer_home():
    if 'employer_user_id' in session:
        print(session['employer_user_id'])
        get_details = request_transform(get_requests())
        get_job_posts = posted_jobs()
        return render_template('employer_home.html', users = get_details, job_posts = get_job_posts)
    else:
        flash('no login session detected','error')
        return redirect(url_for('login_page.login_view'))
    
    



@login_page.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    #conneting with database
    db.execute('select password from employer where  user_id = %s',(username,))
    # print(password)
    # print(username)
    pas= db.fetchone()
    # print(pas)
    if pas == None:
        flash('incorrect user_id or password', 'warning')
        return redirect(url_for('login_page.login_view'))
    else:
        passkey = "".join(pas)
        print(passkey)
        if passkey == password:
            flash('hello '+username)
            session["employer_logged_in"] = True
            session['employer_user_id'] = username
            return redirect(url_for('login_page.employer_home'))
        else:
            flash("Invalid username or password", 'error')
            return redirect(url_for('login_page.login_view'))


# print(session['user_id'])

    

# if __name__ == '__main__':
#     login_page.run(debug=True)