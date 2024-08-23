from flask import Flask, render_template, request, jsonify
from db import engine, load_jobs_from_db, load_job_from_db, add_application_to_db


app=Flask(__name__)

@app.route("/")
def home_page():
  jobs=load_jobs_from_db()
  return render_template("homedemo.html", jobs=jobs)

@app.route("/jobs/<id>")
def show_job(id):
  job=load_job_from_db(id)
  return render_template("jobpage.html",job=job)

@app.route("/jobs/<id>/apply", methods=['post'])
def apply_to_job(id):
  data=request.form
  job= load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template("application_submitted.html",application=data)


  
if __name__=="__main__":
  app.run(host='0.0.0.0', debug=True)
  