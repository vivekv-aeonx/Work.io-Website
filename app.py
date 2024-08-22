from flask import Flask, render_template
from db import engine, load_jobs_from_db, load_job_from_db


app=Flask(__name__)

@app.route("/")
def home_page():
  jobs=load_jobs_from_db()
  return render_template("homedemo.html", jobs=jobs)

@app.route("/jobs/<id>")
def show_job(id):
  job=load_job_from_db(id)
  return render_template("jobpage.html",job=job)

if __name__=="__main__":
  app.run(host='0.0.0.0', debug=True)
  