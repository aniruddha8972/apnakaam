from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
from flask import Blueprint
from database import connet,commit_all

worker_home_page = Blueprint('worker_home_page',__name__)
db = connet()


def check_session():
    if 'worker_logged_in' in session and session['worker_logged_in']:
        # print(session['worker_user_id'])
        return session['worker_user_id']


def job_status(job_id,worker_id,choice):
    db.execute('SELECT job_status,worker_id from job_status WHERE job_posting_id = %s and worker_id = %s', (job_id,worker_id,))
    output = db.fetchall()
    print(output)
    if len(output) ==0:
        db.execute('SELECT employer_id from job_posting where id = %s', (job_id,))
        employer_id = db.fetchone()
        print(employer_id)
        db.execute( "INSERT INTO job_status (job_posting_id, employer_id, worker_id, job_status) "
            "VALUES (%s, %s, %s, %s)",(job_id,employer_id[0], worker_id,choice))
        status = choice
        commit_all()
        return status
    else:
        return output
    

@worker_home_page.route('/process_response',methods=['POST'])
def process_response_form():
    job_id = request.form['job_id']
    choice = request.form['response']
    worker_id = check_session()
    print(worker_id,job_id,choice)
    status = job_status(job_id, worker_id,choice)
    if status == None:
        return 'status updated successfully now the current status is :' + choice+"ed"
    else:
        return "status already updated priviously : "+status[0][0]+"ed"
    
    
    

@worker_home_page.route('/worker_logout')
def logout():
    
    session.pop('worker_logged_in', False)
    session.pop('worker_user_id', None) # Clear the username from the session
    flash("You have been logged out.", 'success')
    return render_template('worker_login.html')

# commit_all()