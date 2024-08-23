import os
from sqlalchemy import create_engine, text

my_secret = os.environ['db_connection_string']
engine = create_engine(my_secret)

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
    query= text("INSERT INTO applications(job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES(:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

    conn.execute(query, {"job_id":job_id, "full_name":application['full_name'], "email":application['email'], "linkedin_url":application['linkedin_url'], "education":application['education'], "work_experience":application['work_experience'],"resume_url":application['resume_url']})

    conn.commit()