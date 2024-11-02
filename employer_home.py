from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
from flask import Blueprint
from database2 import connet,commit_all
from employer_login import employer_home
from datetime import datetime
employer_home_page = Blueprint('employer_home_page',__name__)





db = connet()



def post_job(employer_id,job_title,job_details,location,starting_date,ending_date,experience,required_skills):
    if session['add_jobs']:
        query = "INSERT INTO job_posting (employer_id,job_title,job_details,location,starting_date,ending_date,experience_requirement,required_skills) VALUES (%s, %s,%s, %s, %s, %s, %s,%s)"
        val = (employer_id,job_title,job_details,location,starting_date,ending_date,experience,required_skills)
        db.execute(query,val)
        # commit_all()
        session['add_jobs'] =False
        flash("job details successfully added")
    else:
        flash('this job deltails is already submitted')
        
def home_page():
    return render_template('employer_home.html')        
        
@employer_home_page.route("/emplyer_job_posting",methods=["POST"])
def add_details():
    if request.method == 'POST':
        employer_id = session['employer_user_id']
        job_title = request.form['job_title']
        job_details = request.form['job_description']
        location = request.form['location']
        session['add_jobs'] = True
        starting_date = datetime.strptime(request.form['starting_date'],'%Y-%m-%d')
        ending_date =  datetime.strptime(request.form['ending_date'],'%Y-%m-%d')
        experience_requirement = request.form['experience']
        required_skills = request.form['skills']
        print(employer_id,job_title,job_details,location,starting_date,ending_date,experience_requirement,required_skills)
        try:
            post_job(employer_id,job_title,job_details,location,starting_date,ending_date,experience_requirement,required_skills)
            commit_all()
            return employer_home()
        except:
            flash('error in job posting')
            return employer_home()
    else:
        return 
    
    
    


@employer_home_page.route('/logout')
def logout():
    commit_all()
    session.pop('employer_user_id', None)  # Clear the username from the session
    flash("You have been logged out.", 'success')
    return render_template('employer_login.html')


# @employer_home_page.route('/')




@employer_home_page.route('/request_response',methods=['POST'])
def employer_response_form():
    job_status_id = request.form['job_status_id']
    employer_choice = request.form['response']
    employer_id  = session['employer_user_id']
    if employer_choice == 'reject':
        db.execute('delete from job_status where job_status_id = %s',(job_status_id,))
        commit_all()
        return "worker_rejected"
    elif employer_choice == 'accept':
        db.execute('select job_status.job_posting_id,job_status.employer_id,job_status.worker_id,job_posting.starting_date,job_posting.ending_date,job_posting.location from job_status inner join job_posting on job_status.job_posting_id = job_posting.id where job_status.job_status_id = %s',(job_status_id,))
        mem = db.fetchall()
        val = mem[0]
        job_posting_id = val[0]
        print(val,job_posting_id)
        sql = "INSERT INTO confirmed_data (job_posting_id, employer_id, worker_id, job_starting_date, job_ending_date, job_location) VALUES (%s, %s, %s, %s, %s, %s)"
        db.execute(sql, val)
        commit_all()
        db.execute("delete from job_status where job_posting_id = %s",(job_posting_id,))
        db.execute("delete from job_posting where id = %s",(job_posting_id,))
        commit_all()
        return "worker_selected"
    
        
        
        
        
        
    
    













