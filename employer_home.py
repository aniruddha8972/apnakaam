from flask import Flask, render_template, request, redirect, url_for, flash,jsonify,session
from flask import Blueprint
from database import connet,commit_all
# from employer_login import get_user_id
from datetime import datetime
employer_home_page = Blueprint('employer_home_page',__name__)





db = connet()



def post_job(employer_id,job_title,job_details,location,starting_date,ending_date,experience,required_skills):
        query = "INSERT INTO job_posting (employer_id,job_title,job_details,location,starting_date,ending_date,experience_requirement,required_skills) VALUES (%s, %s,%s, %s, %s, %s, %s,%s)"
        val = (employer_id,job_title,job_details,location,starting_date,ending_date,experience,required_skills)
        db.execute(query,val)
        commit_all()
        
def home_page():
    return render_template('employer_home.html')        
        
@employer_home_page.route("/emplyer_job_posting",methods=["POST"])
def add_details():
    employer_id = session['employer_user_id']
    job_title = request.form['job_title']
    job_details = request.form['job_description']
    location = request.form['location']
    starting_date = datetime.strptime(request.form['starting_date'],'%Y-%m-%d')
    ending_date =  datetime.strptime(request.form['ending_date'],'%Y-%m-%d')
    experience_requirement = request.form['experience']
    required_skills = request.form['skills']
    try:
        post_job(employer_id,job_title,job_details,location,starting_date,ending_date,experience_requirement,required_skills)
        flash('Job posting submitted successfully')
        commit_all()
        return render_template('employer_home.html')
    except:
        flash('error in job posting')
        return render_template('employer_home.html')
    
    
    
    
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

@employer_home_page.route('/your_jobs')
def your_jobs(output):
    
    # output = transform(posted_jobs())
    # print(output)
    return render_template('posted_jobs.html',users= output)

def check_session():
    if 'employer_logged_in' in session and session['employer_logged_in']:
        return session['employer_user_id']
        



@employer_home_page.route('/posted_jobs',methods=['POST'])
def posted_jobs():
    # emp_id = request.form['id']
    emp_id2 = check_session()
    print(emp_id2)
    output = get_details(emp_id2)
    main = transform(output)

        
    return your_jobs(main)

# @employer_home_page.route('/session')
# def show_username():
#     if 'username' in session:
#         username = session['username']
#         return render_template('employer_home.html', logged_in=True, user_id=username)
        
# show_username()

        


# print(session['user_id'])


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
    
        
        
        
        
        
    
    













