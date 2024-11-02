from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask import Blueprint
from database import connet
from worker_registration import worker_registration_page



mycursor = connet()

worker_login_page = Blueprint('worker_login_page',__name__)

worker_login_page.register_blueprint(worker_registration_page)




def get_details():
    mycursor.execute('SELECT employer.name, job_posting.job_title, job_posting.job_details, job_posting.location, job_posting.starting_date, job_posting.ending_date, job_posting.required_skills, job_posting.id FROM employer INNER JOIN job_posting ON employer.user_id = job_posting.employer_id ')
    output = mycursor.fetchall()
    worker_user_id = session['worker_user_id']
    mycursor.execute('select job_posting_id,job_status from job_status where worker_id =%s',(worker_user_id,))
    job_statuses = mycursor.fetchall()
    print(job_statuses)
    return output,job_statuses

def transform(output,job_statuses):
    main = []
    job_ids = []
    for i in range(len(job_statuses)):
        job_ids.append(job_statuses[i][0])
    print(job_ids)
    
    
    for i in range(len(output)):
        l = output[i]
        # print(l)
        l_set ={}
        if l[7] in job_ids:
            continue
        else:
            l_set['employer_name'] = l[0]
            l_set['job_title'] = l[1]
            l_set['detalis'] = l[2]
            l_set['location'] = l[3]
            l_set['starting_date'] = l[4]
            l_set['ending_date'] = l[5]
            l_set['nessesry_skills'] = l[6]
            l_set['job_id'] = l[7]
        
        main.append(l_set)
    # print(job_statuses)
        
        # job_id.append(l[7])
    # print(job_id)
    return main

# @worker_login_page.route('/job_openings',methods=['POST'])
# def posted_jobs():
#     output= transform(get_details())
#     print(output)
    
#     return output






@worker_login_page.route('/worker_login_view')
def login_view():
    return render_template('worker_login.html')


@worker_login_page.route('/worker_registration')
def register():
    
    return render_template('worker_registration.html')

@worker_login_page.route('/worker_home')
def worker_home():
    if "worker_logged_in" in session and session["worker_logged_in"] == True:
        print(session['worker_user_id'])
        output,job_ids= get_details()
        details = transform(output,job_ids)
        return render_template('worker_home.html',users = details)
    else:
        flash("You are not logged in")
        return render_template('worker_login.html')



@worker_login_page.route('/worker_login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    #conneting with database
    # print(password)
    # print(username)
    mycursor.execute('select password from worker where  user_id = %s',(username,))
    pas= mycursor.fetchone()
    # print(pas)
    if pas == None:
        flash('incorrect user_id or password', 'warning')
        return redirect(url_for('worker_login_page.login_view'))
    else:
        passkey = "".join(pas)
        print(passkey)
        if passkey == password:
            session["worker_logged_in"] = True
            session['worker_user_id'] = username
            flash('hello '+username)
            return redirect(url_for('worker_login_page.worker_home'))
        else:
            flash("Invalid username or password", 'error')
            return redirect(url_for('worker_login_page.worker_login_view'))






