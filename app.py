import secrets
import os
from flask import Flask, render_template, request, redirect, url_for, flash,session
from employer_login import login_page
from worker_login import worker_login_page
from employer_home import employer_home_page
from worker_home import worker_home_page
# from worker_registration import worker_registration_page
# from flask_session import  Session

app  = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = '/sessions'  # Optional

# Session(app)





app.register_blueprint(login_page)
app.register_blueprint(worker_login_page)
app.register_blueprint(employer_home_page)
app.register_blueprint(worker_home_page)
# app.register_blueprint(worker_registration_page)


@app.route('/')
def front_page():
    return render_template('first_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 4000)))
