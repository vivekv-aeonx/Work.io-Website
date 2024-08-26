import os
from sqlalchemy import create_engine, text

my_secret = os.environ['db_connection_string']
engine = create_engine(my_secret)

def add_user_to_db(email, hashed_password):
    with engine.connect() as conn:
        query = text("INSERT INTO users (email, password) VALUES (:email, :password)")
        conn.execute(query, {"email": email, "password": hashed_password})
        conn.commit()

def get_user_by_email(email):
    with engine.connect() as conn:
        query = text("SELECT * FROM users WHERE email=:email")
        result = conn.execute(query, {"email": email})
        user = result.fetchone()
        if user:
            return user._asdict()
        return None


def load_jobs_from_db():
  with engine.connect() as conn:
    result= conn.execute(text("select * from jobs"))

    jobs=[]
    for row in result.all():
      jobs.append(row._asdict())
    return jobs

def load_job_from_db(id):
  with engine.connect() as conn:
    result= conn.execute(text("select * from jobs where id=:val"), {"val":id})
    rows=result.all()
    if len(rows)==0:
      return None
    else:
      return rows[0]._asdict()

def add_application_to_db(job_id, application):
    with engine.connect() as conn:
        query = text("""
            INSERT INTO applications(job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
            VALUES(:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
        """)
        conn.execute(query, {
            "job_id": job_id,
            "full_name": application.get('full_name'),
            "email": application.get('email'),
            "linkedin_url": application.get('linkedin_url'),
            "education": application.get('education'),
            "work_experience": application.get('work_experience'),
            "resume_url": application.get('resume_url')
        })
        conn.commit()
