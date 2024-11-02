import mysql.connector

# Database configuration

mydb = mysql.connector.connect(
    host = 'sql12.freemysqlhosting.net',
    user = 'sql12742243',
    password = '2X1MRTklsE',
    database = 'sql12742243'
)
def connet():
    return mydb.cursor()

def commit_all():
    mydb.commit()

db = mydb.cursor()
class employer:
    def __init__(self):
        db.execute("CREATE TABLE IF NOT EXISTS employer (name VARCHAR(50) NOT NULL,address VARCHAR(300) NOT NULL,email_id VARCHAR(50) NOT NULL,mobile_no VARCHAR(50) NOT NULL,govt_id VARCHAR(50) NOT NULL,user_id VARCHAR(50) PRIMARY KEY,password VARCHAR(50) NOT NULL);")
        mydb.commit()
    
    def add_employer_details(self,values):
        query = "INSERT INTO employer (name, address, email_id, mobile_no, govt_id, user_id, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        db.execute(query,values)
        mydb.commit()
        print("Success")
    
    def show_all_details(self):
        db.execute('SELECT * FROM employer')
        output = db.fetchall()
        print(output)
        
    def delete_details(self,user_id):
        db.execute('DELETE FROM employer WHERE user_id = %s',(user_id,))
        mydb.commit()
        
        
        
        
        
class job_posting:
    def __init__(self):
        db.execute("CREATE TABLE IF NOT EXISTS job_posting (id INT AUTO_INCREMENT PRIMARY KEY,employer_id VARCHAR(50) NOT NULL,job_title VARCHAR(100) NOT NULL,job_details VARCHAR(500) NOT NULL,location VARCHAR(100) NOT NULL,starting_date DATE NOT NULL,ending_date DATE NOT NULL,experience_requirement VARCHAR(100) NULL,required_skills VARCHAR(100) NULL);")
        mydb.commit()
    
    def add_job_post(self,values):
        query = "INSERT INTO job_posting (employer_id, job_title, job_details, location, starting_date, ending_date, experience_requirement, required_skills) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        db.execute(query,values)
        mydb.commit()
        print("Success")
    
    def show_all_details(self):
        db.execute('SELECT * FROM job_posting')
        output = db.fetchall()
        print(output)
        
    def delete_details(self,job_id):
        db.execute('DELETE FROM job_posting WHERE id = %s',(job_id,))
        mydb.commit()
        
        
        
        
        
        
class worker:
    def __init__(self):
        db.execute("CREATE TABLE IF NOT EXISTS worker (name VARCHAR(50) NOT NULL, address VARCHAR(300) NOT NULL, email_id VARCHAR(50) NOT NULL, mobile_no VARCHAR(50) NOT NULL, govt_id VARCHAR(50) NOT NULL, user_id VARCHAR(50) PRIMARY KEY, password VARCHAR(50) NOT NULL, experience VARCHAR(50) NOT NULL, expertise_field VARCHAR(50) NOT NULL);")
        mydb.commit()
    
    def add_worker_setails(self,values):
        query = "INSERT INTO worker (name, address, email_id, mobile_no, govt_id, user_id, password, experience, expertise_field) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        db.execute(query,values)
        mydb.commit()
        print("Success")
    
    def show_all_details(self):
        db.execute('SELECT * FROM worker')
        output = db.fetchall()
        print(output)
        
    def delete_details(self,user_id):
        db.execute('DELETE FROM worker WHERE user_id = %s',(user_id,))
        mydb.commit()






class job_status:
    def __init__(self):
        db.execute("CREATE TABLE IF NOT EXISTS job_status (job_status_id INT AUTO_INCREMENT PRIMARY KEY, job_posting_id INT NOT NULL, employer_id VARCHAR(50) NOT NULL, worker_id VARCHAR(50) NOT NULL, job_status VARCHAR(20) NOT NULL, daily_rate int NULL);")
        mydb.commit()
    
    def add_worker_setails(self,values):
        query = "INSERT INTO job_status (job_posting_id, employer_id, worker_id, job_status, daily_rate) VALUES (%s, %s, %s, %s, %s)"

        db.execute(query,values)
        mydb.commit()
        print("Success")
    
    def show_all_details(self):
        db.execute('SELECT * FROM job_status')
        output = db.fetchall()
        print(output)
        
    def delete_details(self,status_id):
        db.execute('DELETE FROM job_status WHERE job_status_id = %s',(status_id,))
        mydb.commit()
        


class confirmed_data:
    def __init__(self):
        db.execute("CREATE TABLE IF NOT EXISTS confirmed_data (job_posting_id INT PRIMARY KEY, employer_id VARCHAR(100) NOT NULL, worker_id VARCHAR(100) NOT NULL, job_starting_date VARCHAR(100) NOT NULL, job_ending_date VARCHAR(100) NOT NULL, job_location VARCHAR(100) NOT NULL, rate_per_day VARCHAR(100));")
        mydb.commit()
    
    def add_worker_setails(self,values):
        query = "INSERT INTO confirmed_data (job_posting_id, employer_id, worker_id, job_starting_date, job_ending_date, job_location, rate_per_day) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        db.execute(query,values)
        mydb.commit()
        print("Success")
    
    def show_all_details(self):
        db.execute('SELECT * FROM confirmed_data')
        output = db.fetchall()
        print(output)
        
    def delete_details(self,job_id):
        db.execute('DELETE FROM confirmed_data WHERE job_posting_id = %s',(job_id,))
        mydb.commit()





connet()
Employer = employer()
Worker = worker()
Job_post = job_posting()
Job_status = job_status()
Final_data = confirmed_data()
commit_all()
# val = ("John Doe", "123 Main St", "johndoe@example.com", "1234567890", "ABC12345", "johndoe123", "password123")
# Employer.add_employer_details(val)

