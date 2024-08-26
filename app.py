from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from db import engine, load_jobs_from_db, load_job_from_db, add_application_to_db, add_user_to_db, get_user_by_email

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['jwt_secret_key']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

def create_token(email):
    token = jwt.encode({
        'user': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_token(token):
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded['user']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def load_user(email):
    user = get_user_by_email(email)
    if user:
        return User(email)
    return None

@app.route("/")
def home_page():
    jobs = load_jobs_from_db()
    return render_template("homedemo.html", jobs=jobs)

@app.route("/jobs/<id>")
def show_job(id):
    job = load_job_from_db(id)
    return render_template("jobpage.html", job=job)

@app.route("/jobs/<id>/apply", methods=['POST'])
def apply_to_job(id):
    if not current_user.is_authenticated:
        session['application_data'] = request.form.to_dict()
        session['job_id'] = id
        return redirect(url_for('login_page'))

    data = request.form
    add_application_to_db(id, data)
    return render_template("application_submitted.html", application=data)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        add_user_to_db(email, hashed_password)
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            user_obj = User(email)
            login_user(user_obj)
            token = create_token(email)
            resp = redirect(url_for('home_page'))
            resp.set_cookie('token', token)
            # Check if there is application data in the session
            application_data = session.pop('application_data', None)
            job_id = session.pop('job_id', None)
            if application_data and job_id:
                add_application_to_db(job_id, application_data)
                return render_template("application_submitted.html", application=application_data)
            return resp
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route("/logout")
def logout_page():
    logout_user()
    resp = redirect(url_for('home_page'))
    resp.delete_cookie('token')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
