import secrets
import random
import requests
from flask import Flask, render_template, url_for, redirect, request, flash, session, make_response, send_from_directory,jsonify, send_file, abort
# from flask_basicauth import BasicAuth
# from alchemy_db import engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from Forms import *
from Tokeniser import Tokenise
from flask_mail import Mail, Message
from Advert_Forms import Job_Ads_Form, Company_Register_Form, Company_Login, Company_UpdateAcc_Form, Freelance_Ads_Form, \
    Freelance_Section, Job_Feedback_Form, Approved_Form
import os
from pywebpush import webpush, WebPushException
from PIL import Image
from sqlalchemy import exc, desc
import rsa
# from flask_security import Security,SQLAlchemyUserDatastore
import pyotp
# ......for local DB
# import MySQLdb
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from models import *
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from wtforms.validators import ValidationError
from datetime import datetime, date, timedelta, timezone
import time
import itsdangerous
import calendar
# from flask_sitemap import Sitemap
from BLOG_CLASS import blog_class
from werkzeug.utils import secure_filename
import platform
import base64
from authlib.integrations.flask_client import OAuth
# from bs4 import BeautifulSoup as b_soup
import requests
import mysql.connector
import sendgrid
# from sendgrid.helpers.mail import Mail
import io
import json
from sqlalchemy.exc import IntegrityError
# from models.user import get_reset_token, very_reset_token
# DB sessions
# db_sessions = sessionmaker(bind=engine)
# db = db_sessions()
import pytz
from Survey_Forms import SurveyForm
from werkzeug.middleware.proxy_fix import ProxyFix


def current_time_wlzone():
    # Get the current UTC time
    timestamp = datetime.now(pytz.utc)

    # Define the user's timezone
    user_timezone = 'Africa/Mbabane'  # Replace this with the user's timezon

    # Create a timezone object
    local_tz = pytz.timezone(user_timezone)

    # Convert UTC time to user's local tim
    local_time = timestamp.astimezone(local_tz)



    return local_time


# Applications
app = Flask(__name__)
# sitemap = Sitemap(app=app)


app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1) # Set x_proto to 1 to trust the first proxy in the chain


app.config['SECRET_KEY'] = 'f9ec9f35fbf2a9d8b95f9bffd18ba9a1'


# Local
if os.environ.get('EMAIL_INFO') == 'info@techxolutions.com':
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tht_db.db"
else:#Online
    app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://techtlnf_tmaz:!Tmazst41#@localhost/techtlnf_tht_db"

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 280}
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['BASIC_AUTH_USERNAME'] = 'tmaz'
app.config['BASIC_AUTH_PASSWORD'] = 'tmaz'

app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'seeker.eswatini@gmail.com' #os.getenv("MAIL") #
app.config['MAIL_PASSWORD'] = 'qcwqtochvppknpbk' #os.getenv("PWD") # 
app.config['MAIL_USE_TLS'] = True

app.config['FOLDER']='attachments'

db.init_app(app)


oauth = OAuth(app)

pub,priv = rsa.newkeys(128)

application = app

# Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Encrypt Password
encrypt_password = Bcrypt(app)

ser = Serializer(app.config['SECRET_KEY'])

# security = Security(app)

# migrate = Migrate(app,db)
# basic_auth = BasicAuth(app)


if os.path.exists("client.json"):
    # Load secrets from JSON file
    with open("client.json") as f:
        creds = json.load(f)

#Google oauth configs
if os.path.exists('client.json'):
    appConfig = {
        "OAUTH2_CLIENT_ID" : creds['clientid'],
        "OAUTH2_CLIENT_SECRET":creds['clientps'],
        "OAUTH2_META_URL":"",
        "FLASK_SECRET": app.config['SECRET_KEY'], #"sdsdjsdsdjfe832j2rj_32jfesdsdjfe832j2rj32j832",
        "FLASK_PORT": 5000  
    }

    oauth.register("tht_oauth",
                client_id = appConfig.get("OAUTH2_CLIENT_ID"),
                client_secret = appConfig.get("OAUTH2_CLIENT_SECRET"),
                    api_base_url='https://www.googleapis.com/',
                    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo', 
                client_kwargs={ "scope" : "openid email profile"},
                server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration',
                jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
                )



# Yet To Be Tested
app.config['SECURITY_TWO_FACTOR_ENABLED_METHODS'] = ['mail', 'sms']
app.config['SECURITY_TWO_FACTOR_SECRET'] = 'jhs&h$$sbUE_&WI*(*7hK5S'


VAPID_PRIVATE_KEY = """MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgGCUsFJL/62KLtxB9
3ESUJ/g1a+dUk62jyA2Mn+WhM0yhRANCAASp/iYNfmIemVxQKO6TNgqon4JE4Fae
EPJ8T1bLHOi/wpQAaY2PInYLBX6mUcU91pnOPeqkbEwgeSQhbAuXi00w"""

VAPID_PUBLIC_KEY = "BKn-Jg1-Yh6ZXFAo7pM2CqifgkTgVp4Q8nxPVssc6L_ClABpjY8idgsFfqZRxT3Wmc496qRsTCB5JCFsC5eLTTA"



class user_class:
    s = None

    def get_reset_token(self, c_user_id):

        s = Serializer(app.config['SECRET_KEY'])

        return s.dumps({'user_id': c_user_id, 'expiration_time': time.time() + 300}).encode('utf-8')

    @staticmethod
    def verify_reset_token(token, expires=1800):

        s = Serializer(app.config['SECRET_KEY'], )

        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except itsdangerous.SignatureExpired:
            flash('Token has expired', 'error')
        except itsdangerous.BadSignature:
            flash('Token is Invalid', 'error')
        except:
            return f'Something Went Wrong'  # f'Token {user_id} not accessed here is the outcome user'

        return user_id


@login_manager.user_loader
def load_user(user_id):
    return user.query.get(user_id)

@app.errorhandler(401)
def custom_401(error):

    return render_template("401_handler.html"), 401

@app.errorhandler(404)
def custom_404(error):
    return render_template("404_handler.html"), 404

@app.errorhandler(500)
def custom_404(error):
    return render_template("500_handler.html"), 500

# Security
# @app.before_request
# def block_non_browsers():
#     # Abort all ip addresses that are stored in forbedden_requests table
#     if request.remote_addr in [ip_obj.ip for ip_obj in forbedden_requests.query.all()]:
#         print("Blocked IP Address: ", request.remote_addr)
#         # abort(403)

#     # Check if the request is from a browser (not a bot or script)
#     if "Mozilla" not in request.headers.get("User-Agent", ""):
#         print("Blocked non-browser request", request.remote_addr)
#         forbidden = forbedden_requests(
#             ip = request.remote_addr,
#             timestamp = current_time_wlzone(),
#             other = request.headers.get("User-Agent", ""),
#             reason = "Blocked non-browser request"
#         )

#         db.session.add(forbidden)
#         db.session.commit()

#         if "facebookexternalhit/1.1" not in request.headers.get("User-Agent", ""): 
#             pass
            # abort(403)


#Security
# @app.before_request
# def enforce_http():
#     if request.is_secure:
#         return redirect(request.url.replace("http://","https://"), code=301)
    

app.config.update(
    SESSION_COOKIE_SECURE=True,     # Only sent over HTTPS
    SESSION_COOKIE_HTTPONLY=True,   # Not accessible via JS
    SESSION_COOKIE_SAMESITE='Strict'  # Blocks CSRF from other domainss
)

def resize_img(img, size_x=30, size_y=30):
    i = Image.open(img)

    if i.size > (200, 200):

        output_size = (size_x, size_y)
        i.thumbnail(output_size)

        i.save(img)
    else:
        pass

    return img


def count_ads():
    from sqlalchemy import text

    users = []
    all = text("SELECT COUNT(*) as total_jobs FROM job_ads")
    jobs = db.session.execute(all).scalar()

    return jobs


# Custom URL generator function with _external=True by default
def my_url_for(endpoint, **values):
    return url_for(endpoint, _external=True, **values)


app.jinja_env.globals['url_for'] = my_url_for

@app.context_processor
def inject_ser():
    with app.app_context():
        db.create_all()
    ser = Serializer(app.config['SECRET_KEY'])  # Define or retrieve the value for 'ser'
    count_jobs = count_ads()


    return dict(ser=ser, count_jobs=count_jobs)


def save_pic(picture, size_x=300, size_y=300):
    _img_name, _ext = os.path.splitext(picture.filename)
    gen_random = secrets.token_hex(8)
    new_img_name = gen_random + _ext

    saved_img_path = os.path.join(app.root_path, 'static/images', new_img_name)

    output_size = (size_x, size_y)
    i = Image.open(picture)
    h, w = i.size

    if h > 400 and w > 400:
        # downsize the image with an ANTIALIAS filter (gives the highest quality)
        img = i.resize(i.size, Image.LANCZOS)
        img.thumbnail(output_size)
    else:
        img = i.resize(i.size, Image.LANCZOS)

    img.save(saved_img_path, optimize=True, quality=95)

    return new_img_name


def delete_img(file_name):
    file_path = os.path.join(app.root_path, 'static/images', file_name)

    if os.path.exists(file_path):
        os.remove(file_path)


def save_pdf(pdf_file):
    _file_name, _ext = os.path.splitext(pdf_file.filename)
    gen_random = secrets.token_hex(8)
    new_file_name_ext = _file_name + "_" + gen_random + _ext

    file_path = os.path.join(app.root_path, 'static/files', new_file_name_ext)

    pdf_file.save(file_path)

    return new_file_name_ext


def delete_pdf(file_name):
    file_path = os.path.join(app.root_path, 'static/files', file_name)

    if os.path.exists(file_path):
        os.remove(file_path)

# Set the session to be permanent and define the lifetime
app.permanent_session_lifetime = timedelta(minutes=1440)  # Example: 30 minutes


def track_visitor():
    # Get visitor's IP address
    visitor_ip = request.remote_addr
    visitor_addr = visitor_ip

    # You can define your own IP address to exclude
    your_ip = 'YOUR_IP_ADDRESS_HERE'  # Replace with your actual IP address

    reg_visitor = visitors.query.filter_by(ip=visitor_ip).first()

    if reg_visitor and not reg_visitor.ip == "102.212.200.73":
        reg_visitor.num_visits +=1
        reg_visitor.latest_visit = current_time_wlzone()
        print("Tracking  Visitor: ", visitor_ip," ",current_time_wlzone())
        print("Tracking First Visited: ",reg_visitor.timestamp)
    elif not reg_visitor:
        # If the visitor is not yours, track them
        visit = visitors(
            ip = visitor_ip,
            timestamp = current_time_wlzone(),  
        )
        visit.num_visits = 0
        visit.num_visits  +=1

        db.session.add(visit)
        print("Tracking New Visitor: ", visitor_ip," ",visit.timestamp)
    db.session.commit()

#upload users with more than 5 days last visitation
# last_visits =[]
# def get_last_visits():
#     today = datetime.now() 
#     users = visitors.query.all()

#     for user in users:
#         days_ago = (today - user.latest_visit).days
#         if days_ago >= 5:
#             last_visits.append(user.ip)
#             missed_posts = jobs_posted.query.filter(jobs_posted.timepstamp > user.latest_visit).all()


def updates_modal(usr_ip=None):
    ifip = None
    if usr_ip:
        ifip = visitors.query.filter_by(ip=usr_ip).first()
    else:
        visitor_addr = request.remote_addr
        ifip = visitors.query.filter_by(ip=visitor_addr).first()

    days_missed = 0
    missed_posts = None
    today = datetime.now()

    if ifip:
        print("Visit Updates: ",ifip.ip )
        print("Check Last visit: ",ifip.latest_visit )
        print("Checked ")
        if ifip.latest_visit and today > ifip.latest_visit:
            days_missed = (today - ifip.latest_visit).days
            print("Your last Visit: ",days_missed)
            missed_posts = jobs_posted.query.filter(jobs_posted.timepstamp > ifip.latest_visit).all()
            print("Missed: ", missed_posts)
        elif not ifip.latest_visit:
            days_missed = (today - ifip.timestamp).days
            print("Your last Visit2: ",days_missed)
            # Fetch posts that were created after the user's first visit (timestamp)
            missed_posts = jobs_posted.query.filter(jobs_posted.timepstamp > ifip.timestamp).all()
            print("Missed2: ", missed_posts)

    # Return or process missed posts for display
    if missed_posts:
        print("You missed the following posts:",len(missed_posts))
    else:
        print("You haven't missed any posts since your last visit.")

    return missed_posts if missed_posts is not None else [], days_missed  # or any other format for the output


@app.route("/")
def home():
     # Make the session permanent so the expiration time is effective
    session.permanent = True  

    updates,days_missed=updates_modal()


    track_visitor()
    
    # Use the session variable to track modal display
    #..for new visitors mostly
    if "run_modal" not in session:
        print("Modal Not in Session")
        session["run_modal"] = True  # Set to True (modal shown)
        session["modal_displayed_time"] = datetime.now(timezone.utc)  # Track the time modal was shown (The last time it was shown)
    else:
        # Check if modal_displayed_time exists in session
        if "modal_displayed_time" in session:
            # Use aware datetime for comparison
            time_since_display = datetime.now(timezone.utc) - session["modal_displayed_time"]
            # Determine if the modal should be shown based on expiration
            if time_since_display < timedelta(minutes=1440):  # If less than 24 hours(1440) minutes do not show the modal
                session["run_modal"] = False  # Don't show modal again
            else:
                session["run_modal"] = True  # Show modal again after expiration (24 hours elapsed)
                session["modal_displayed_time"] = datetime.now(timezone.utc)  # Update display time (current time)
        else:
            # If modal_displayed_time is not present, set it and show modal
            session["run_modal"] = True
            session["modal_displayed_time"] = datetime.now(timezone.utc)

    with app.app_context():
        db.create_all()

    
    # user_ = user.query.get(1)
    # login_user(user_)
    req_page = session.get('req_page')
    if req_page:
        session['req_page'] = ''
        return redirect(req_page) if req_page else redirect(url_for('home'))

    # posted_jobs = jobs_posted.query.all().order_by(
    #             desc(jobs_posted.timepstamp))
    posted_jobs = jobs_posted.query.order_by(desc(jobs_posted.timepstamp)).all()
    

    return render_template("index.html",posted_jobs=posted_jobs,updates=updates, days_missed=days_missed)


@app.route('/manifest.json')
def serve_manifest():

    return send_file('manifest.json', mimetype='application/manifest+json')


@app.route('/activity_tracker', methods=['POST'])
def track():
    data = request.json
    print(f"[{datetime.now()}] Event received:", data)
    activity = page_activity_analytics(
        page_name = data.get("page"),
        event_type = data.get("eventType"),
        # event_data = data.get("eventData"),
        page_visited_ip = request.remote_addr,
        page_visited_time = current_time_wlzone()
    )
    db.session.add(activity)
    db.session.commit()
    # You can write this to a DB or log it
    return jsonify({"status": "success"}), 200

subscriptions = [] 

# Accept JSON data from frontend subscription and store it
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    subscriptions.append({
        "endpoint": data.get("endpoint"),
        "keys": {
            "p256dh": data["keys"]["p256dh"],
            "auth": data["keys"]["auth"]
        }
    })

    save_details = NotificationsAccess(
        endpoint = data.get("endpoint"),
        p256dh = data["keys"]["p256dh"],
        auth = data["keys"]["auth"],
        ip = request.remote_addr,
        timestamp = current_time_wlzone()
    )
    db.session.add(save_details)
    db.session.commit()

    return jsonify({'status': 'subscribed'})

@app.route('/check_subscriptions', methods=['GET'])
def check_subscriptions():
    ip = request.remote_addr
    sub_status = NotificationsAccess.query.filter_by(ip=ip).first()

    if sub_status:
        print("User Subscribed: ", request.remote_addr, " - ", sub_status.endpoint, " - ", sub_status.timestamp)
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})

@app.route('/update_subscription', methods=['POST'])
def update_subscription():
    data = request.get_json()
    ip = data.get('ip')

    if ip:
        subscription_entry = NotificationsAccess.query.filter_by(ip=ip).first()
        if subscription_entry:
            subscription_entry.endpoint=data.get("endpoint")
            subscription_entry.p256dh=data["keys"]["p256dh"]
            subscription_entry.auth=data["keys"]["auth"]
            subscription_entry.timestamp=current_time_wlzone()

            db.session.commit()
            print("Subscription Updated: ", ip, " - ", subscription_entry.endpoint, " - ", subscription_entry.timestamp)
            return jsonify({'status': 'updated'})
        else:
            return jsonify({'status': 'not_found'})

    return jsonify({'status': 'error'})

@app.route('/freelance_ad')
def freelance_ad():

    return render_template("freelance_ad.html")


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    print("Get Notified: ", request.remote_addr)

    message = request.args.get("message", "Default message") if request.method == "GET" else request.get_json().get("message", "Default message")

    if request.method == 'POST':
        data = request.get_json()
        message = data.get("message", "Hello!")
    else:
        message = request.args.get("message", "Hello from GET!")

    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps({
                    "title": "New Notification",
                    "body": message
                }),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={"sub": "mailto:info@techxolutions.com"}
            )
        except WebPushException as ex:
            print("Push failed:", repr(ex))

    return jsonify({'status': 'notifications sent'})


# @app.route('/load_subscriptions')
def getuser_endpoints():
    
    subscriptions.clear()  # clear existing to avoid duplicates
    endpoints = NotificationsAccess.query.all()
    
    # Get all the endpoints registered or who granted notification permittion
    for endpoint in endpoints:
        subscriptions.append({
            "endpoint": endpoint.endpoint,
            "ip":endpoint.ip,
            "keys": {
                "p256dh": endpoint.p256dh,
                "auth": endpoint.auth
            }
            
        })
    print("Check Subscriptions: ", subscriptions)
    # Now call notify logic manually
    # if days_missed
    message = request.args.get("message", "🚀 You've got a new opportunity!")
    
    for subscriber in subscriptions:
        ip = subscriber.get("ip")  # get IP from dictionary
        sub = {
            "endpoint": subscriber["endpoint"],
            "keys": subscriber["keys"]
        }

        job_missed, days_missed = updates_modal(usr_ip=ip)
        print("++Check The Days: ",days_missed)
        print( "+++Jobs: ", job_missed )
        if days_missed >= 1 and len(job_missed) > 0:
            try:
                webpush(
                    subscription_info=sub,
                    data=json.dumps({
                        "title": "New Jobs Notification",
                        "body": f"🚀 You've got {len(job_missed)} new job alerts waiting!"
                    }),
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims={"sub": "mailto:info@techxolutions.com"}
                )
            except WebPushException as ex:
                print("Push failed:", repr(ex))
    print("Notification Pushed: ",current_time_wlzone())
    # return jsonify({'status': 'notifications sent'})


@app.route("/post_job",methods=["POST","GET"])
def post_job():

    form = JobPostForm()

    if request.method=="POST":
        job = jobs_posted(
            details = form.details.data,
            job_title = form.job_title.data,
            deadline = form.deadline.data,
            link = form.link.data,
            timepstamp = current_time_wlzone()
        )
        print("CHECH IMAGE: ",form.advert_image.data)
        if form.advert_image.data:
            print("IMAGE FOUND: ",form.advert_image.data)
            job.advert_image = save_pic(form.advert_image.data)
            print("IMAGE SAVED: ",job.advert_image)

        db.session.add(job)
        db.session.commit()
        flash("Upload Successful!","success")

        getuser_endpoints()
        print("Called Notification Feature")

    return render_template('post-a-job-form.html',form=form)


# Path to save the responses
responses_file_path = 'responses.json'

# Load existing responses if the file exists
if os.path.exists(responses_file_path):
    with open(responses_file_path, 'r') as file:
        responses = json.load(file)
else:
    responses = []


# Define the home route and survey form
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    if request.method == 'POST':
        # Collect data from the form
        user_response = {
            "ip_address": request.remote_addr,
            "responses": {
                "remote_job_interest": form.remote_job_interest.data,
                "support_initiative": form.support_initiative.data,
                "revolutionize_job_market": form.revolutionize_job_market.data,
                "participate": form.participate.data,
                "encourage_companies": form.encourage_companies.data,
                "reduce_unemployment": form.reduce_unemployment.data,
                "value_experience": form.value_experience.data,
                "industry_experience": form.industry_experience.data,
                "uncover_hidden_talents": form.uncover_hidden_talents.data,
                "work_life_balance": form.work_life_balance.data,
                "confidence_participation": form.confidence_participation.data,
                "platform_knowledge": form.platform_knowledge.data,
                "resources_info": form.resources_info.data,
                "job_interest": form.job_interest.data
            }
        }
        
        # Append the new response to the responses list
        responses.append(user_response)

        # Save the updated responses to JSON file
        with open(responses_file_path, 'w') as file:
            json.dump(responses, file, indent=4)

        return redirect(url_for('thank_you'))

    return render_template('survey.html',form=form)


# <script 'sw.js'><script>
@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')


@app.route("/featured_jobs")
def featured():
     # Make the session permanent so the expiration time is effective
    session.permanent = True  

    updates,days_missed=updates_modal()

    track_visitor()
    
    # Use the session variable to track modal display
    if "run_modal" not in session:
        session["run_modal"] = True  # Set to True (modal shown)
        session["modal_displayed_time"] = datetime.now(timezone.utc)  # Track the time modal was shown
    else:
        # Check if modal_displayed_time exists in session
        if "modal_displayed_time" in session:
            # Use aware datetime for comparison
            time_since_display = datetime.now(timezone.utc) - session["modal_displayed_time"]
            # Determine if the modal should be shown based on expiration
            if time_since_display < timedelta(minutes=1440):  # If less than 30 minutes
                session["run_modal"] = False  # Don't show modal again
            else:
                session["run_modal"] = True  # Show modal again after expiration
                session["modal_displayed_time"] = datetime.now(timezone.utc)  # Update display time
        else:
            # If modal_displayed_time is not present, set it and show modal
            session["run_modal"] = True
            session["modal_displayed_time"] = datetime.now(timezone.utc)
    with app.app_context():
        db.create_all()
    
    posted_jobs = jobs_posted.query.order_by(desc(jobs_posted.timepstamp)).all()
    
    return render_template("featured_jobs.html",posted_jobs=posted_jobs, updates=updates, days_missed=days_missed)


@app.route("/internships")
def internships():
     # Make the session permanent so the expiration time is effective
    session.permanent = True  

    track_visitor()

    return render_template("internships.html")


@app.route("/job_boards")
def job_boards():
     # Make the session permanent so the expiration time is effective
    session.permanent = True  

    updates,days_missed=updates_modal()

    track_visitor()
    
    # Use the session variable to track modal display
    if "run_modal" not in session:
        session["run_modal"] = True  # Set to True (modal shown)
        session["modal_displayed_time"] = datetime.now(timezone.utc)  # Track the time modal was shown
    else:
        # Check if modal_displayed_time exists in session
        if "modal_displayed_time" in session:
            # Use aware datetime for comparison
            time_since_display = datetime.now(timezone.utc) - session["modal_displayed_time"]
            # Determine if the modal should be shown based on expiration
            if time_since_display < timedelta(minutes=1440):  # If less than 30 minutes
                session["run_modal"] = False  # Don't show modal again
            else:
                session["run_modal"] = True  # Show modal again after expiration
                session["modal_displayed_time"] = datetime.now(timezone.utc)  # Update display time
        else:
            # If modal_displayed_time is not present, set it and show modal
            session["run_modal"] = True
            session["modal_displayed_time"] = datetime.now(timezone.utc)
    with app.app_context():
        db.create_all()
    
    return render_template("job_boards.html",updates=updates, days_missed=days_missed)


@app.route('/static/css/style.css')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


# Web
@app.route("/homepage", methods=["POST", "GET"])
def homepage():
    try:
        companies_ls = company_user.query.all()
        comp_len = len(companies_ls)
    except:
        db.create_all()
    if request.method == 'GET':
        pass
        # id_ = request.args.get()

    for cmp in companies_ls:
        pass

    return render_template("index.html", img_1='', img_2='', img_3='', companies_ls=companies_ls, comp_len=comp_len,
                           ser=ser)


@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    register = Register()

    db.create_all()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    image_fl = url_for('static', filename='images/image.jpg')

    if register.validate_on_submit():

        # print(f"Account Successfully Created for {register.name.data}")
        if request.method == 'POST':
            # context
            # If the webpage has made a post e.g. form post
            hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            user1 = job_user(name=register.name.data, email=register.email.data, password=hashd_pwd,
                             confirm_password=hashd_pwd, image="default.jpg",
                             time_stamp=current_time_wlzone())

            try:
                db.session.add(user1)
                db.session.commit()
                flash(f"Account Successfully Created for {register.name.data}", "success")
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"Something went wrong,please check for errors", "error")
                Register().validate_email(register.email.data)

    elif register.errors:
        flash(f"Account Creation Unsuccessful ", "error")

    return render_template("sign_up_form.html", register=register, ser=ser)


@app.route("/about")
def about():
    return render_template("about.html")


# ----------------BLOG---------------------- #
blog_cls = blog_class()

@app.route("/blog_index")
def blog_index():

    blogs_dict = blog_cls.load_blogs()

    blog_titles = blogs_dict.keys()

    return render_template("blog_index.html",blog_titles=blog_titles,blogs_dict=blogs_dict)


@app.route("/blog-page",methods=["POST","GET"])
def blog_page():

    if request.method == "GET":

        title = request.args.get("title")
        print("TITLE: ",title)
        print("TITLE: ", blog_cls.load_blogs()[title]['picture'])
        if title:
            blog = blog_cls.load_blogs()[title]
        else:
            blog=None

    return render_template("blog-page.html",blog=blog,title=title)

@app.route("/write_blog", methods=["POST", "GET"])
def blog_writer():
    # blog_form = Blog_Form()

    if request.method == "POST":

        title = request.form['title']
        body = request.form['body']
        author = request.form['author']
        image_path = request.files['blog-image']

        print("BODY: ",body)

        file_name = secure_filename(image_path.filename)

        # image_path.save("static/images/"+file_name)

        # image_path = save_pic(file_name)

        #Create hash for image name
        img_name, _ext = os.path.splitext(file_name)
        gen_random = secrets.token_hex(8)
        new_img_name = gen_random + _ext

        #Save image in designated path
        image_path.save(os.path.join(app.root_path,"static/images/blog_images", new_img_name))

        # print("Image Name: ", new_img_name)

        blog_cls.blogs_filer(title, body, author, new_img_name)

        return redirect(url_for("blog_writer"))


    return render_template("blog_writer.html")



@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    from sqlalchemy import update

    cv = Update_account_form()
    # print("Current User: ",current_user.name)

    image_fl = url_for('static', filename='images/' + current_user.image)

    the_freelancer = Esw_Freelancers.query.filter_by(uid=current_user.id).first()

    if request.method == 'POST':

        if cv.validate_on_submit():
            id = current_user.id
            usr = job_user.query.get(id)

            # Image
            if usr.image and cv.image_pfl.data:
                delete_img(usr.image)
                usr.image = save_pic(picture=cv.image_pfl.data)

            elif cv.image_pfl.data and not usr.image:
                pfl_pic = save_pic(picture=cv.image_pfl.data)
                usr.image = pfl_pic

            # PDF
            if usr.other and cv.cv_file.data:
                delete_pdf(usr.other)
                usr.other = save_pdf(cv.cv_file.data)

            elif cv.cv_file.data and not usr.other:
                file = save_pdf(cv.cv_file.data)
                usr.other = file

            usr.name = cv.name.data
            usr.email = cv.email.data
            usr.date_of_birth = cv.date_of_birth.data
            usr.contacts = cv.contacts.data
            usr.school = cv.school.data
            usr.tertiary = cv.tertiary.data
            usr.address = cv.address.data
            usr.hobbies = cv.hobbies.data
            usr.reference_1 = cv.reference_1.data
            usr.reference_2 = cv.reference_2.data
            usr.skills = cv.skills.data
            usr.experience = cv.experience.data

            db.session.commit()

            flash("Account Updated Successfully!!", "success")

        elif cv.errors:
            pass

    elif cv.errors:
        flash("Update Unsuccessful!!, check if all fields are filled", "error")

    return render_template("account.html", cv=cv, title="Account", image_fl=image_fl, ser=ser,
                           the_freelancer=the_freelancer)


@app.route("/login", methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    login = Login()
    # if request.method == 'POST':

    #     if login.validate_on_submit():
    #         user_login = user.query.filter_by(email=login.email.data).first()
    #         if user_login and encry_pw.check_password_hash(user_login.password, login.password.data):
                
    #             login_user(user_login)

    #             req_page = request.args.get('next')
    #             flash("Login Successful!")
    #             return redirect(req_page) if req_page else redirect(url_for('home'))
    #         else:
    #             flash("Login Access Denied! Check your password and email","error")
    #             return redirect('login')

    return render_template('login_form.html', title='Login', login=login)


@app.route("/log_in", methods=["POST", "GET"])
def login_():
    login = Login()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':

        if login.validate_on_submit():
            user_login = user.query.filter_by(email=login.email.data).first()
            
            

            if user_login:
                arg_token = user_class().get_reset_token(user_login.id)

            if user_login:
                session['user_id'] = user_login.id
            if request.form.get('stay_signed_in'):
                token = secrets.token_urlsafe(16)  # Generate a 16-character token
                user_login.token = token
                db.session.commit()
                # Set a persistent cookie with the token
                resp = make_response("Login successful")
                resp.set_cookie('stay_signed_in', token, httponly=True, max_age=60 * 60 * 24 * 30)  # 30 days
                return resp

            else:
                if user_login and encry_pw.check_password_hash(user_login.password, login.password.data):
                    if not request.form.get("use_2fa_auth") == 'y' and user_login.verified:
                        login_user(user_login)
                        # After login required prompt, take me to the page I requested earlier
                        req_page = request.args.get('next')
                        flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                        return redirect(req_page) if req_page else redirect(url_for('home'))

                    elif request.form.get("use_2fa_auth") == 'y' and user_login.verified:
                        # send_opt(user_login.id)
                        # two_fa_form = Two_FactorAuth_Form()
                        Quick_Gets.uid_token = arg_token
                        return redirect(
                            url_for('two_factor_auth', arg_token=arg_token))  # user_id=arg_token,

                    elif request.form.get("use_2fa_auth") == 'y' and not user_login.verified:
                        Quick_Gets.uid_token = arg_token
                        return redirect(url_for('verification', arg=arg_token))

                    elif not request.form.get("use_2fa_auth") == 'y' and not user_login.verified:
                        user_id_ = user_login.id
                        return redirect(url_for('verification', arg=arg_token))


                else:
                    flash(f"Login Unsuccessful, please use correct email or password", "error")

    return render_template('login_form.html', title='Login', login=login)


def generate_6_digit_code():
    return str(random.randint(100000, 999999))


class Quick_Gets:
    otp_attr = None
    uid_token = None


# @app.route('/send_2fa/<arg_token>', methods=['POST', 'GET'])  # /<arg_token>
def send_otp(otp_code,arg_token):
    # Generate an OTP (One-Time Password) for the current time

    user_id = user_class().verify_reset_token(arg_token)
    user_obj = user.query.get(user_id)
    two_fa_form = Two_FactorAuth_Form()

    app.config["MAIL_SERVER"] = "smtp.googlemail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    # em = app.config["MAIL_USERNAME"] = os.environ.get("EMAIL")
    # app.config["MAIL_PASSWORD"] = os.environ.get("PWD")

    mail = Mail(app)

    msg = Message("The Hustlers Time 2-FA", sender=em, recipients=[user_obj.email])
    msg.body = f""" Copy the Login Code Below & Paste to login using the 2-Factor Authentication Method. Please note
that the Code is Valid for 60 seconds.

    Your 2-Factor Code:  {otp_code}


    """

    try:
        mail.send(msg)
        # user_obj.store_2fa_code = otp_key
        # db.session.commit()
        flash(f"Your 2 Factor Auth Code is sent to your Email!!", "success")
        # print("2 FA : ",otp.now())
        # return redirect(url_for('two_factor_auth', arg_token=arg_token, _external=True))  #

    except Exception as e:
        flash(f'Ooops Something went wrong!! Please Retry', 'error')
        return "The mail was not sent"



# 2FA Auth
class OTP_Code:
    otpcode_ = None
    otp_ = None

import time

class Stopwatch:
    count_started = None

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def usage(self):
        print("\n----------- STOPWATCH -----------")
        print("|-> s      : start the stopwatch |")
        print("|-> Ctrl+C : stop the stopwatch  |")
        print("----------- STOPWATCH -----------")

    def start(self):
        self.start_time = time.time()

    def start_countdown(self, seconds_countdown=3):
        user_input = input("\n-> Press 's' when you're ready to start: ")
        while seconds_countdown > 0:
            print(f"\rStarting in {seconds_countdown}...", end="")
            time.sleep(1)
            seconds_countdown -= 1
            self.count_started = True
        print("\rGO !", end="")
        self.count_started = None
        return False

    def stop(self):
        self.end_time = time.time()
        print(f"\n\nTotal elapsed time: {(self.end_time - self.start_time):.3f} seconds\n")
        exit(0)

    # def run(self):
    #     self.usage()
    #     self.start_countdown()
    #     self.start()
    #     try:
    #         while True:
    #             print(f"\rElapsed time: {(time.time() - self.start_time):.0f} seconds", end="")
    #             time.sleep(1)
    #     except KeyboardInterrupt:
    #         self.stop()


@app.route('/2fa/<arg_token>', methods=['POST', 'GET'])  # /<arg_token>
def two_factor_auth(arg_token):
    two_fa_form = Two_FactorAuth_Form()
    user_id = user_class().verify_reset_token(arg_token)
    user_obj = user.query.get(user_id)
    otp_key = pyotp.random_base32()

    otp = pyotp.TOTP('ATILOJ6TCBODFZIBDLU377NLM3AZXPBG', interval=300)
    otp_code = otp.now()

    print("OTP Code: ", otp_code)

    # otp_code = generate_otp()
    # Send Email with code and token
    if not OTP_Code.otpcode_ or otp_code != OTP_Code.otpcode_:
        send_otp(otp_code, arg_token)
        OTP_Code.otpcode_=otp_code

    if request.method == 'POST':
        otp_code_input = two_fa_form.use_2fa_auth_input.data
        # Verify an OTP for the provided secret key
        # user_obj.store_2fa_code key saved in the database
        # otp_obj = pyotp.TOTP(otp_key) #)
        # otp = OTP_Code.otp_
        is_valid_otp = otp.verify(otp_code_input)
        code_time = 300

        print('DEBUG 2-FA: ', is_valid_otp, otp_code_input)

        if otp_code == otp_code_input:
            login_user(user_obj)
            req_page = request.args.get('next')
            flash(f"Hey! {user_obj.name.title()} You're Logged In!", "success")
            return redirect(req_page) if req_page else redirect(url_for('home'))
        else:
            flash(f"Code Not Valid", "error")
            # return redirect(url_for('two_factor_auth',arg_token=arg_token))

    return render_template('2_facto_form.html', two_fa_form=two_fa_form, _external=True)



@app.before_request
def load_user_from_cookie():
    if 'user_id' not in session and 'stay_signed_in' in request.cookies:
        token = request.cookies.get('stay_signed_in')
        usr = user.query.filter_by(token=token).first()
        if usr:
            session['user_id'] = usr.id
            login_user(usr)


@app.route('/logout')
def log_out():
    logout_user()
    # session.pop('user_id', None)
    # make_response('Logged out').delete_cookie('stay_signed_in')

    return redirect(url_for('home'))


@app.route("/contact", methods=["POST", "GET"])
def contact_us():
    contact_form = Contact_Form()
    if request.method == "POST":
        if contact_form.validate_on_submit():
            def send_link():
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                app.config['MAIL_PASSWORD'] = 'qcwqtochvppknpbk'
                em = app.config["MAIL_USERNAME"] = "seeker.eswatini@gmail.com"
                # app.config["MAIL_PASSWORD"] = os.environ.get("PWD")

                mail = Mail(app)

                msg = Message(contact_form.subject.data, sender=contact_form.email.data, recipients=["seeker.eswatini@gmail.com"])
                msg.body = f"""{contact_form.message.data}
{contact_form.email.data}
                    """
                try:
                    mail.send(msg)
                    flash("Message Successfully Sent!!", "success")
                    return "Email Sent"
                except Exception as e:
                    # print(e)
                    flash(f'Ooops Something went wrong!! Please Retry', 'error')
                    return "The mail was not sent"

                # Send the pwd reset request to the above email

            send_link()

        else:
            flash("Please be sure to fill both email & message fields, correctly", "error")

    return render_template("contact_page.html", contact_form=contact_form)


@app.route("/companies")
def companies():
    companies_list = company_user.query.all()

    return render_template("companies.html", companies_list=companies_list)


@app.route("/reset/<token>", methods=['POST', "GET"])
def reset(token):
    reset_form = Reset()

    if request.method == 'POST':
        # if reset_form.validate_on_submit():
        # if current_user.is_authenticated:
        #     #Current User Changing Password
        #     #....script compares
        #     if encry_pw.check_password_hash(current_user.password, reset_form.old_password.data):
        #         # token = Tokenise().get_reset_token(current_user.id)
        #         #print("Reset Token: ", token)
        #         # v_user_id = Tokenise().verify_reset_token(token)
        #         #print("User_id: ", v_user_id)
        #
        #         pass_reset_hash_lc = encry_pw.generate_password_hash(reset_form.new_password.data)
        #
        #         usr = user.query.get(current_user.id)
        #         usr.password = pass_reset_hash_lc
        #         db.session.commit()
        #
        #         # logout_user()
        #
        #         flash(f"Password Changed Successfully!", "success")
        #         return redirect(url_for("login"))
        #     else:
        #         flash(f"Ooops! Passwords don't match, You might have forgotten your Old Password", "error")
        # else:

        try:
            flash(f"Trying to Reset Please wait", "success")
            usr_obj = user_class().verify_reset_token(token)
            flash(f"User Id {usr_obj}", "success")
            pass_reset_hash = encry_pw.generate_password_hash(reset_form.new_password.data)
            usr_obj = user.query.get(usr_obj)
            usr_obj.password = pass_reset_hash
            db.session.commit()

            flash(f"Password Changed Successfully!", "success")

            return redirect(url_for("login"))
        except:
            print("Password Reset Failed!!")
            flash(f"Password Reset Failed, Please try again later", "error")
            return None

    return render_template("pass_reset.html", reset_form=reset_form)


@app.route("/reset_request", methods=['POST', "GET"])
def reset_request():
    reset_request_form = Reset_Request()

    if current_user.is_authenticated:
        logout_user()

    if request.method == 'POST':
        if reset_request_form.validate_on_submit():
            # Get user details through their email
            usr_email = user.query.filter_by(email=reset_request_form.email.data).first()

            if usr_email is None:
                # print("The email you are request for is not register with T.H.T, please register first, Please Retry")
                flash(
                    "The email you are requesting a password reset for, is not registered with T.H.T, please register as account first",
                    'error')

                return redirect(url_for("reset_request"))

            def send_link(usr_email):
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                # em = app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
                # app.config["MAIL_PASSWORD"] = os.getenv("PWD")

                mail = Mail(app)

                token = user_class().get_reset_token(usr_email.id)
                msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[usr_email.email])
                msg.body = f"""Good day, {usr_email.name}
                
You have requested a password reset for your The Hustlers Time Account.
To reset your password, visit the following link:{url_for('reset', token=token, _external=True)}

If you did not requested the above message please ignore it, and your password will remain unchanged.
"""

                try:
                    mail.send(msg)
                    flash('An email has been sent with instructions to reset your password', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"

            # Send the pwd reset request to the above email
            send_link(usr_email)

            return redirect(url_for('login'))

    return render_template("reset_request.html", reset_request_form=reset_request_form)


@app.route("/how_does_it_work")
def tht_how():
    return render_template("how_does_it_work.html", ser=ser)


@app.route("/job_ads_form", methods=["POST", "GET"])
@login_required
def job_ads_form(udi=None):
    job_ad_form = Job_Ads_Form()
    job_ads_model = Jobs_Ads

    usr_id = request.args.get("udi")

    db.create_all()
    job_ad = None

    if request.method == 'POST':
        print("Check Start Date: ", job_ad_form.start_date.data, job_ad_form.work_hours_bl.data)
        if job_ad_form.validate_on_submit():
            job_post1 = job_ads_model(
                job_title=job_ad_form.job_title.data,
                description=job_ad_form.description.data,
                category=request.form.get('field_category_sel'),
                responsibilities=job_ad_form.responsibilities.data,
                qualifications=job_ad_form.qualifications.data,
                contact_person=job_ad_form.posted_by.data,
                job_type=request.form.get('job_type_sel'),
                application_deadline=job_ad_form.application_deadline.data,
                job_posted_by=current_user.id,
                about_company=job_ad_form.about_company.data
            )

            # if bools are True
            if job_ad_form.pay_type_bl.data:
                # print('Job Type: ', job_ad_form.pay_type_bl.data)
                job_post1.pay_type = job_ad_form.other_pay_type.data

            if job_ad_form.other_job_type.data:
                job_post1.job_type = job_ad_form.other_job_type.data

            if job_ad_form.work_duration_bl.data:
                job_post1.work_duration = job_ad_form.start_date.data
                job_post1.work_duration2 = job_ad_form.end_date.data

            if job_ad_form.work_days_bl.data:
                job_post1.work_days = job_ad_form.work_days.data

            if job_ad_form.work_hours_bl.data:
                job_post1.work_hours = job_ad_form.work_hours.data

            if job_ad_form.age_range_bl.data:
                job_post1.age_range = job_ad_form.age_range.data

            if job_ad_form.benefits_bl.data:
                job_post1.benefits = job_ad_form.benefits.data

            if not request.form.get('field_category_sel'):
                job_post1.category = job_ad_form.category.data

            db.session.add(job_post1)
            db.session.commit()

            if request.args.get("udi"):
                uid = request.args.get("udi")
                id_ = ser.loads(uid)['data2']

                #Check if the user is not currently hired somewhere
                usr_is_cur_hired = hired.query.filter_by(usr_cur_job=1, hired_user_id=id_).first()
                if usr_is_cur_hired:
                    company = company_user.query.get(usr_is_cur_hired.comp_id)
                    flash(f"This Job Seeker is currently hired and working for: {company.name}")
                    db.session.delete(Jobs_Ads.query.get(job_post1.job_id))
                    return redirect(url_for("users"))

                # Logic to hire the user and update the application status
                hire_user = hired(
                    comp_id=current_user.id,
                    hired_user_id=id_,
                    job_details=job_post1.job_id,
                    usr_cur_job=1,  # Currently hired
                    hired_date=datetime.utcnow()
                )

                db.session.add(hire_user)

                #-------APPLICATION-------#
                apply = Applications(
                    applicant_id=id_,
                    job_details_id=job_post1.job_id,  # db.query(Jobs_Ads).get(jb_id),
                    employer_id=current_user.id
                )

                # Check if application not sent before
                job_appl = Applications.query.filter_by(job_details_id=job_post1.job_id, applicant_id=id_).first()
                company_obj = company_user.query.get(apply.employer_id)

                # print('----------------------job_appl: ',job_appl)
                if not job_appl:
                    db.session.add(apply)
                    db.session.commit()
                    # job_title = Jobs_Ads.query.get(jb_id).job_title
                    # job_id = Jobs_Ads.query.get(jb_id).job_id
                    # return render_template("send_application.html", send_application=send_application, job_id=job_id,
                    #                        job_title=job_title,
                    #                        company_obj=company_obj, ser=ser)
                #--------END APPLICATION CODE--------_#

                close_appl = Applications.query.filter_by(job_details_id=job_post1.job_id).first()
                if close_appl:
                    close_appl.closed = "Yes"  # This means that this user is hired

                db.session.commit()

                # flash message for successful hiring
                flash(f'You have successfully hired {user.query.get(id_).name} for {Jobs_Ads.query.get(job_post1.job_id).job_title}',
                    'success')

                return redirect(url_for("users"))


            flash('Job Posted Successfully!!', 'success')

    # elif request.method == "GET":
    #     job_ad = Jobs_Ads.query.filter_by(job_id=ser.loads(request.args.get("jo_id"))['data_11']).first()

    return render_template("job_ads_form.html", job_ad_form=job_ad_form, ser=ser, job_ad=job_ad,usr_id=usr_id)


@app.route("/online_form", methods=["POST", "GET"])
def online_courses_form(udi=None):
    print("Test Points")
    form = OnlineCoursesForm()
    print("Test Points 1")

    if request.method == 'POST':
        print("Test Points 2")
        if form.validate_on_submit():
            print("Test Points 3")
            post = online_courses(
                    site =  form.site .data,
                    university =  form.university.data,
                    describe = form.describe.data,
                    course_name = form.course_name.data,
                    course_starts = form.course_starts.data,
                    intro_link = form.intro_link.data,
                    course_link=form.course_link.data
            )
            print("Test Points 4")
            # if bools are True
            if form.course_image.data:
                post.course_image = save_pic(form.course_image.data)
            print("Test Points 5")
            db.session.add(post)
            db.session.commit()

            flash('Course Posted Successfully!!', 'success')
        else:
            for error in form.errors:
                print("Errors in Online Courses: ",error)

    # elif request.method == "GET":
    #     job_ad = Jobs_Ads.query.filter_by(job_id=ser.loads(request.args.get("jo_id"))['data_11']).first()

    return render_template("post_course.html", form=form)


@app.route("/online_courses", methods=["POST", "GET"])
def courses(udi=None):

    course_list = [
    "Introduction to Python Programming",
    "Data Science and Analytics",
    "Digital Marketing Fundamentals",
    "Graphic Design Basics",
    "Web Development Bootcamp",
    "Project Management Essentials",
    "Social Media Marketing Strategies",
    "Financial Accounting",
    "Creative Writing Techniques",
    "Machine Learning for Beginners",
    "Cybersecurity Essentials",
    "Photography for Beginners",
    "Video Editing Basics",
    "User Experience (UX) Design",
    "Public Speaking and Communication Skills",
    "Artificial Intelligence Concepts",
    "SEO Fundamentals",
    "Mobile App Development",
    "Business Communication Skills",
    "Health and Wellness Coaching",
    "Introduction to Cloud Computing",
    "Blockchain Technology",
    "Introduction to Graphic Design",
    "Language Learning (e.g., Spanish, French)",
    "Interior Design Basics",
    "Remote Team Management",
    "Ethical Hacking Fundamentals",
    "Virtual Assistance Training",
    "Introduction to Game Development"
]

    courses = online_courses.query.all()

    return render_template("online_courses.html", courses=courses,course_list=course_list)


class jo_id_cls:
    id_ = None



@app.route("/edit_job_ads_form", methods=["POST", "GET"])
@login_required
def eidt_job_ads_form():
    job_ad_form = Job_Ads_Form()
    job_ads_model = Jobs_Ads

    db.create_all()
    job_ad = None
    jo_id = None

    if request.method == 'POST':
        # print("Check Start Date: ", job_ad_form.start_date.data,job_ad_form.work_hours_bl.data)
        if job_ad_form.validate_on_submit():
            job_post1 = Jobs_Ads.query.filter_by(job_id=ser.loads(request.args.get("jo_id"))['data_11']).first()

            job_post1.job_title = job_ad_form.job_title.data,
            job_post1.description = request.form.get('description'),
            job_post1.category = request.form.get('field_category_sel'),
            job_post1.responsibilities = job_ad_form.responsibilities.data,
            job_post1.qualifications = request.form.get('qualifications'),
            job_post1.contact_person = job_ad_form.posted_by.data,
            job_post1.job_type = request.form.get('job_type_sel'),
            job_post1.application_deadline = job_ad_form.application_deadline.data,
            job_post1.about_company = job_ad_form.about_company.data

            # if bools are True
            if job_ad_form.pay_type_bl.data:
                # print('Job Type: ', job_ad_form.pay_type_bl.data)
                job_post1.pay_type = job_ad_form.other_pay_type.data

            if job_ad_form.other_job_type.data:
                job_post1.job_type = job_ad_form.other_job_type.data

            if job_ad_form.work_duration_bl.data:
                job_post1.work_duration = job_ad_form.end_date.data
                job_post1.work_duration2 = job_ad_form.end_date.data

            if job_ad_form.work_days_bl.data:
                job_post1.work_days = job_ad_form.work_days.data

            if job_ad_form.work_hours_bl.data:
                job_post1.work_hours = job_ad_form.work_hours.data

            if job_ad_form.age_range_bl.data:
                job_post1.age_range = job_ad_form.age_range.data

            if job_ad_form.benefits_bl.data:
                job_post1.benefits = request.form.get('benefits')

            if not request.form.get('field_category_sel'):
                job_post1.category = job_ad_form.category.data

            # print("Check Category: ",request.form.get('field_category_sel'))
            # db.session.add(job_post1)
            db.session.commit()

            flash('Post Successfully Updated!!', 'success')
        else:
            flash('Could not update, please check if all fields are filled properly', 'error')
            if job_ad_form.errors:
                for field, errors in job_ad_form.errors.items():
                    for error in errors:
                        print("ERRORS:", error)
            return redirect(url_for("job_adverts"))

    elif request.method == "GET":
        jo_id = request.args.get("jo_id")
        # jo_id_func(jo_id)
        if jo_id:
            jo_id_cls.id_ = jo_id
            job_ad = Jobs_Ads.query.filter_by(job_id=ser.loads(jo_id)['data_11']).first()

        else:
            job_ad = Jobs_Ads.query.filter_by(job_id=ser.loads(jo_id_cls.id_)['data_11']).first()

    return render_template("edit_job_ads_form.html", job_ad_form=job_ad_form, ser=ser, job_ad=job_ad)


@app.route("/fl_job_ads_form", methods=["POST", "GET"])
# @login_required
def fl_job_ads_form():
    fl_job_ad_form = Freelance_Ads_Form()
    fl_job_ads_model = Freelance_Jobs_Ads

    form = request.form

    db.create_all()

    if request.method == 'POST':
        if current_user and not current_user.is_authenticated:
            flash("You are not registered in the system", "warning")
            return redirect(url_for("fl_job_ads_form"))
        if fl_job_ad_form.validate_on_submit():
            job_post1 = fl_job_ads_model(
                service_title = fl_job_ad_form.service_title.data,
                description=fl_job_ad_form.description.data,
                project_duration=fl_job_ad_form.start_date.data,
                working_days=fl_job_ad_form.days_of_work.data,
                job_posted_by=fl_job_ad_form.posted_by.data,
                # date_posted = datetime.utcnow(),
                application_deadline=fl_job_ad_form.application_deadline.data,
                contact_person=current_user.id
            )

            # if bools are True
            if not form.get("job_title"):
                job_post1.service_title = fl_job_ad_form.other_job.data
               

            db.session.add(job_post1)
            db.session.commit()

            flash('Job Post was successful', 'success')

    return render_template("fl_job_ads_form.html", fl_job_ad_form=fl_job_ad_form, ser=ser)

class Indeed_Search:
    def indeed_url_nearme(self,location=None):

        template = "https: // za.indeed.com / q - swaziland, -eswatini - manzini - jobs.html?vjk = d9da936268eed4c9"
        url = template.format(location)

        return url

# -----------------INDEED JOBS-------------------#
@app.route('/indeed_jobs')
def get_jobs():
    api_key = 'YOUR_INDEED_API_KEY'
    base_url = 'https://api.indeed.com/ads/apisearch'
    params = {
        'publisher': api_key,
        'q': 'python developer',  # Customize your job search query here
        'format': 'json',
        'limit': 10  # Number of job listings to fetch
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    return jsonify(data)


@app.route("/show_hired_users")
# @basic_auth.required
def show_hired_users():
    hired_users = hired.query.all()
    job_ads = Jobs_Ads

    return render_template("show_hired_users.html", users=hired_users, user=user, job_ads=job_ads, ser=ser)


@app.route("/send_endof_term_form")
# @basic_auth.required
def send_endof_term_form():
    if request.method == 'GET':
        if current_user.is_authenticated:
            # Get user details through their email
            job_user_obj = user.query.filter_by(id=ser.loads(request.args.get('id'))['data7']).first()

            usr_close_curr_job = hired.query.filter_by(usr_cur_job=1, hired_user_id=job_user_obj.id).first()
            if usr_close_curr_job:
                usr_close_curr_job.usr_cur_job = 0
                db.session.commit()

            # usr_email = user.query.filter_by(email=reset_request_form.email.data).first()

            if usr_close_curr_job:
                def send_link(job_user_obj):
                    app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                    app.config["MAIL_PORT"] = 587
                    app.config["MAIL_USE_TLS"] = True
                    # em = app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
                    # app.config["MAIL_PASSWORD"] = os.getenv("PWD")

                    mail = Mail(app)

                    token = user_class().get_reset_token(job_user_obj.id)
                    msg = Message("End of Term Form", sender="noreply@demo.com", recipients=[job_user_obj.email])
                    msg.body = f"""Good day, {job_user_obj.name}

Thank you for your valuable skills you have displayed while working with us.

Before we finalize our agreement, please click the link below and complete the "End of Term Form." This form helps The Hustlers Time to create a portfolio for you. 
If you fill out 2 or more placement forms, they will be combined to make a single work experience profile for you.

Please visit the following link:{url_for('job_feedback', token=token, _external=True)}

We {current_user.name} wish you all the best as you are climbing the ladder of success.
        """
                    try:
                        mail.send(msg)
                        # flash(f'You have sent an email of the "/End of Term Form/" to {job_user_obj.name}',
                        #       'success')
                        return "Email Sent"
                    except Exception as e:
                        flash('Ooops, Something went wrong Please Retry!!', 'error')
                        return "The mail was not sent"

                # Send the pwd reset request to the above email
                send_link(job_user_obj)

                return f' [End of Term Form] successfully sent to {job_user_obj.name}'


@app.route("/job_feedback_form/<token>", methods=['POST', 'GET'])
@login_required
def job_feedback(token):
    feedback_form = Job_Feedback_Form()

    if request.method == 'POST':
        # try:
        the_freelancer = users_tht_portfolio.query.get(current_user.id)
        flash(f"Trying to Verify, Please wait", "success")
        job_user_id = user_class().verify_reset_token(token)
        # Check current job where the current user is engaged on
        user_hired = hired.query.filter_by(hired_user_id=current_user.id,
                                           usr_cur_job=1).first()  # usr_cur_job=1 checks which job placement is the user currently place on (their current job will maked by 1/True
        if user_hired:
            company = user.query.get(Jobs_Ads.query.get(user_hired.job_details).job_posted_by)
        # session.query(entity).filter_by(**criteria)
        # createria = {current_user.id}
        # curr_job = hired.query.filter_by=)
        if current_user.is_authenticated and user_hired:
            portfolio_details = users_tht_portfolio(
                usr_id=current_user.id,
                portfolio_feedback=feedback_form.job_feedback.data,
                date_employed=user_hired.hired_date,
                approved=False,
                job_details=user_hired.job_details  # Use job_posted_by to get company details
            )

            if not users_tht_portfolio.query.filter_by(usr_id=current_user.id, approved=False).first():
                db.session.add(portfolio_details)
                db.session.commit()
            else:
                flash(f"""Job Seekers Details could not be processed, This entry already exist in the system
or The current might have a pending report that is not yet approved""", "success")

            flash(f"Updated Successfully!", "success")

            def send_link():
                # app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                # app.config["MAIL_PORT"] = 587
                # app.config["MAIL_USE_TLS"] = True
                # em = app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
                # app.config["MAIL_PASSWORD"] = os.getenv("PWD")

                mail = Mail(app)

                token = user_class().get_reset_token(current_user.id)
                msg = Message("RE:End of Term Form", sender="noreply@demo.com",
                              recipients=[company.email])
                msg.body = f"""Good day, 

Please received my 'End of Term' report. Upon approving the information contained in it, please click 'approve' button to confirm.
Visit the following link to approve:{url_for('approve_report', token=token, _external=True)}

Thank you for being part of my future endeavors, I hope to meet you again.

                            """

                try:
                    mail.send(msg)
                    flash(
                        f'You have sent an email of the "/End of Term Form/" to {company.email} for approval',
                        'success')
                    return "Email Sent"
                except Exception as e:
                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"
                    # Send the pwd reset request to the above email

            send_link()
        else:
            flash(f"Something went wrong please try again later, ", "error")
        # except Exception as e:
        #     flash(f"Something went wrong please try again later, : {e}", "error")
        #     return "The mail was not sent"

    return render_template("job_feedback.html", feedback_form=feedback_form)


@app.route("/approve_report/<token>", methods=['POST', 'GET'])
@login_required
def approve_report(token):
    # Get user's identity
    approve_form = Approved_Form()
    approve_user_rp = user_class().verify_reset_token(token)

    user_ = user.query.get(approve_user_rp)

    # if approve_user_rp:
    usr_portfolio_entry = users_tht_portfolio.query.filter_by(usr_id=approve_user_rp, approved=False).first()

    # flash(f"DEBUG USER PORTFoLIO; UID: {usr_portfolio_entry.usr_id} Approved: {usr_portfolio_entry.approved}")
    if current_user.is_authenticated and current_user.role == 'company_user':

        if request.method == 'POST' and usr_portfolio_entry:
            usr_portfolio_entry.approved = True  # The company has approved the end of term form, it will not be changed again
            db.session.commit()
            # Delete this entry from the hired table
            qry_closed_in_hrd_tbl = hired.query.filter_by(usr_cur_job=0, hired_user_id=approve_user_rp).first()
            if qry_closed_in_hrd_tbl:
                db.session.delete(qry_closed_in_hrd_tbl)
                db.session.commit()

            flash('Approved Successfully!!', 'success')

    return render_template('approve_report.html', approve_user_rp=approve_user_rp,
                           usr_portfolio_entry=usr_portfolio_entry, approve_form=approve_form, user_=user_)


@app.route("/meet_freelancers")
def meet_freelancers():
    esw_freelancers = Esw_Freelancers.query.all()

    return render_template("meet_freelancers.html", esw_freelancers=esw_freelancers, user=user)


@app.route("/pdf_viewer")
def pdf_viewer():
    if request.method == "GET":
        pdf_file = request.args.get("opn_fl")

    return render_template("pdf_viewer.html", pdf_file=pdf_file)


@app.route("/freelancer_viewed")
@login_required
def freelancer_viewed():
    if request.method == "GET":
        id_ = request.args['frid']
        fr_id = ser.loads(id_)['data13']
        esw_freelancer = Esw_Freelancers.query.filter_by(uid=fr_id).first()
        user_ = user.query.get(esw_freelancer.uid)

        years = (current_time_wlzone().date() - user_.date_of_birth).days

        usr_years = int(years / 365)

        print("User Years: ", esw_freelancer.portfolio_pdf)

    return render_template("freelancer_viewed.html", esw_freelancer=esw_freelancer, user_=user_, usr_years=usr_years)


@app.route("/freelancers_form", methods=["POST", "GET"])
@login_required
def freelancers():
    freelancer = Freelance_Section()

    the_freelancer = Esw_Freelancers.query.filter_by(uid=current_user.id).first()

    if current_user.role == 'job_user':
        if request.method == "POST":
            if freelancer.validate_on_submit():
                freelancer_details = Esw_Freelancers(
                    uid=current_user.id,
                    other_fl=freelancer.other_fl.data,
                    other_fl1=freelancer.skills.data,
                    fl_experience=freelancer.experience.data,
                    what_do_you_do=freelancer.what_do_you_do.data,
                    fb_link=freelancer.fb_link.data,
                    pinterest_link=freelancer.pinterest_link.data,
                    linkedin_link=freelancer.linkedin_link.data,
                    twitter_link=freelancer.twitter_link.data,
                    youtube=freelancer.youtube_link.data,
                    instagram_link=freelancer.instagram_link.data,
                )

                if freelancer.portfolio_file.data:
                    freelancer_details.portfolio_pdf = save_pdf(freelancer.portfolio_file.data)

                db.session.add(freelancer_details)
                db.session.commit()
                flash('You have successfully joined the Eswatini Freelance Pool!!', 'success')
            else:
                for error in freelancer.errors:
                    print("Error: ", error)
                    flash("There is an error somewhere", "error")
    else:
        flash("Page is available only for Job Seekers", "warning")
        return redirect(url_for('home'))
    return render_template("freelance_form.html", freelancer=freelancer, the_freelancer=the_freelancer)


@app.route("/freelancers_form_update", methods=["POST", "GET"])
@login_required
def freelancers_form_update():
    freelancer = Freelance_Section()

    the_freelancer = Esw_Freelancers.query.filter_by(uid=current_user.id).first()

    if current_user.role == 'job_user':
        if request.method == "POST":
            if freelancer.validate_on_submit():

                the_freelancer.other_fl = freelancer.other_fl.data
                the_freelancer.other_fl1 = freelancer.skills.data
                the_freelancer.fl_experience = request.form.get("experience")
                the_freelancer.what_do_you_do = request.form.get("what_do_you_do")
                the_freelancer.fb_link = freelancer.fb_link.data
                the_freelancer.pinterest_link = freelancer.pinterest_link.data
                the_freelancer.linkedin_link = freelancer.linkedin_link.data
                the_freelancer.twitter_link = freelancer.twitter_link.data
                the_freelancer.youtube = freelancer.youtube_link.data
                the_freelancer.instagram_link = freelancer.instagram_link.data

                # the_freelancer.portfolio_pdf=freelancer.portfolio_file.data

                if freelancer.portfolio_file.data and the_freelancer.portfolio_pdf:
                    delete_pdf(the_freelancer.portfolio_pdf)
                    the_freelancer.portfolio_pdf = save_pdf(freelancer.portfolio_file.data)

                elif freelancer.portfolio_file.data and not the_freelancer.portfolio_pdf:
                    file = save_pdf(freelancer.portfolio_file.data)
                    the_freelancer.portfolio_pdf = file

                db.session.commit()
                flash(f'Update was Successful !!', 'success')

            else:
                for error in freelancer.errors:
                    print("Error: ", error)
                    flash("There is an error somewhere", "error")
    else:
        flash("Page is available only for Job Seekers", "warning")
        return redirect(url_for('home'))
    return render_template("freelance_form.html", freelancer=freelancer, the_freelancer=the_freelancer)


@app.route("/company_retieve")
def cmp_user_profile():
    from sqlalchemy import text

    users = []
    all = text('''SELECT * FROM job_applications;''')
    # db has binded the engine's database file
    for ea_user in db.execute(all):
        users.append(list(ea_user))

    return f"{users}"


def date_filter(input):
    if input.startswith('today'):
        today_jobs = Jobs_Ads.query.filter(Jobs_Ads.date_posted >= date.today()).all()
        return today_jobs
    elif input.startswith('yesterday'):
        yesterday = date.today() - timedelta(days=1)
        yesterday_jobs = Jobs_Ads.query.filter(Jobs_Ads.date_posted >= yesterday).all()
        return yesterday_jobs
    elif input.startswith('this_week'):
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        this_week_jobs = Jobs_Ads.query.filter(Jobs_Ads.date_posted.between(start_of_week, end_of_week)).all()
        return this_week_jobs
    elif input.startswith('this_month'):
        today = date.today()
        start_of_month = date(day=1, month=today.month, year=today.year)
        _, last_day = calendar.monthrange(today.year, today.month)
        end_of_month = date(day=last_day, month=today.month, year=today.year)
        this_month_jobs = Jobs_Ads.query.filter(Jobs_Ads.date_posted.between(start_of_month, end_of_month)).all()
        return this_month_jobs
    else:
        flash('No Entries', 'error')


@app.route("/job_ads", methods=["GET", "POST"])
# @basic_auth.required
def job_adverts():
    date_today = current_time_wlzone()
    token = user_class()
    encry = encry_pw
    if current_user.is_authenticated:
        if not current_user.image and not current_user.school:
            flash("Attention!! Your Account needs to be updated Soon, Please go to Account and update the empty fields",
                  "error")

    no_image_fl = 'static/images/default.jpg'

    db.create_all()
    usr = user()


    job_ads_form = Job_Ads_Form()
    if request.method == 'GET':
        # id = request.args.get()
        id_ = request.args.get('id')
        if id_:
            enc_id = ser.loads(id_)["data_1"]
            value = request.args.get('value')
            # print("Check Get Id: ",id)
            if enc_id:
                # Filter Ads with a specific company's id
                # job_ads = Jobs_Ads.query.filter_by(job_posted_by=enc_id).order_by(desc(Jobs_Ads.date_posted))
                job_ads_latest = [job for job in
                                  Jobs_Ads.query.filter_by(job_posted_by=enc_id).order_by(desc(Jobs_Ads.date_posted)) if
                                  (job.application_deadline - date_today).days >= 0]
                job_ads_older = [job for job in
                                 Jobs_Ads.query.filter_by(job_posted_by=enc_id).order_by(desc(Jobs_Ads.date_posted)) if
                                 (job.application_deadline - date_today).days < 0]


                category_list_unfltd = [item.category for item in job_ads_latest]
                category_set = set(category_list_unfltd)


        # For all companies
        elif not id_:  # not value and
            job_ads_latest = [job for job in Jobs_Ads.query.order_by(desc(Jobs_Ads.date_posted)).all() if
                              (job.application_deadline - date_today).days >= 0]
            job_ads_older = [job for job in Jobs_Ads.query.order_by(desc(Jobs_Ads.date_posted)).all() if
                             (job.application_deadline - date_today).days < 0]


            category_list_unfltd = [item.category for item in job_ads_latest]

            category_set = set(category_list_unfltd)

    # Fix jobs adds does not have hidden tag
    if days_to_lauch.days <= 0:
        return render_template("job_ads_gui.html", job_ads_latest=job_ads_latest, job_ads_older=job_ads_older,
                               job_ads_form=job_ads_form, db=db,
                               company_user=company_user, user=usr, no_image_fl=no_image_fl, ser=ser, date_today=date_today,
                               category_set=category_set,days_to_lauch=days_to_lauch)
    else:
        return redirect(url_for("intro_eswatini_jobs"))



@app.route("/job_ad_opened", methods=["GET", "POST"])
@login_required
def view_job():
    if request.method == 'GET':
        id_ = request.args.get('id')
        dcry_jbid = ser.loads(id_)["data"]
        job_ad = Jobs_Ads.query.get(dcry_jbid)

        deadln = job_ad.application_deadline - current_time_wlzone()
        days_left = deadln.days
        chekif_usr_applied = Applications.query.filter_by(job_details_id=dcry_jbid,
                                                          applicant_id=current_user.id).first()
        print("User Applied Before? : ", chekif_usr_applied)

    return render_template('job_ad_opened.html', item=job_ad, db=db, company_user=company_user, ser=ser,
                           days_left=days_left
                           , chekif_usr_applied=chekif_usr_applied)


@app.route("/job_ads_filtered", methods=["GET", "POST"])
# @basic_auth.required
def job_adverts_filtered():
    if current_user.is_authenticated:
        # print("Current User")
        if not current_user.image and not current_user.school:
            flash("Attention!! Your Account needs to be updated Soon, Please go to Account and update the empty fields",
                  "error")

    no_image_fl = 'static/images/default.jpg'

    usr = user()
    # job_ads = []
    # job_ads = db.query(company_user.job_ads).all()
    job_ads_form = Job_Ads_Form()
    if request.method == 'GET':
        value = request.args.get('value')

        jobs_categories = Jobs_Ads.query.all()
        category_set = None
        if jobs_categories:
            category_list_unfltd = [item.category for item in jobs_categories]
            category_set = set(category_list_unfltd)

        if value not in ['today', 'yesterday', 'this_week', 'this_month']:
            job_ads = Jobs_Ads.query.filter(Jobs_Ads.category.like(f"{value}%")).all()

        elif value in ['today', 'yesterday', 'this_week', 'this_month']:
            job_ads = date_filter(value)

    # Fix jobs adds does not have hidden tag
    return render_template("job_ads_filtered.html", job_ads=job_ads, job_ads_form=job_ads_form, db=db,
                           company_user=company_user, user=usr, no_image_fl=no_image_fl, ser=ser,
                           category_set=category_set)


@app.route("/freelance_job_ads", methods=["GET", "POST"])
def freelance_job_adverts():
    if current_user.is_authenticated:
        # print("Current User")
        if not current_user.image and not current_user.school:
            flash("Attention!! Your Account needs to be updated Soon, Please go to Account and update the empty fields",
                  "error")
        else:
            pass
    else:
        pass

    no_image_fl = 'static/images/default.jpg'

    db.create_all()
    usr = user()
    # job_ads = []
    # job_ads = db.query(company_user.job_ads).all()

    if request.method == 'GET':
        id = request.args.get('id')
        # print("Check Get Id: ",id)
        if id:
            # Filter Ads with a specific company's id
            fl_job_ads = Freelance_Jobs_Ads.query.filter_by(job_posted_by=id).order_by(
                desc(Freelance_Jobs_Ads.date_posted))
        else:
            fl_job_ads = Freelance_Jobs_Ads.query.order_by(desc(Freelance_Jobs_Ads.date_posted))

    fl_job_ads_form = Freelance_Ads_Form()

    return render_template("freelance_jobs_ui.html", fl_job_ads=fl_job_ads, fl_job_ads_form=fl_job_ads_form, db=db,
                           company_user=company_user, user=usr, no_image_fl=no_image_fl, ser=ser)

    # Fix jobs adds does not have hidden tag
    if days_to_lauch.days <= 0:
        return render_template("freelance_jobs_ui.html", fl_job_ads=fl_job_ads, fl_job_ads_form=fl_job_ads_form, db=db,
                           company_user=company_user, user=usr, no_image_fl=no_image_fl, ser=ser)
    else:
        return redirect(url_for("intro_eswatini_fl"))


@app.route("/fl_applications", methods=["GET", "POST"])
def fl_applications():
    # Get all applications from Applications database
    all_applications = FreeL_Applications.query.all()

    # print("Debug Application List: ", db.query(job_user).get(all_applications[0].applicant_id).name )

    esw_freelancers = Esw_Freelancers

    applications = FreeL_Applications()

    freelance_ads = Freelance_Jobs_Ads

    return render_template("fl_applications.html", all_applications=all_applications, user=user,
                           freelance_ads=freelance_ads,
                           applications=applications, db=db, ser=ser, esw_freelancers=esw_freelancers)


@app.route("/send_application_fl", methods=["GET", "POST"])
@login_required
def send_application_fl():
    send_application = FreeL_Applications()

    db.create_all()

    if not current_user.image and not current_user.school:
        redirect(url_for('account'))
        flash("Warning!! Your Account needs to be updated Soon, You won't be able to send Application if not so",
              "error")

    else:
        if current_user.is_authenticated:

            if request.method == "GET":
                tender_id = request.args['tender_id']

                apply = FreeL_Applications(
                    applicant_id=current_user.id,
                    freel_job_details_id=tender_id,  # db.query(Jobs_Ads).get(jb_id),
                    employer_id=Freelance_Jobs_Ads.query.get(tender_id).job_posted_by,

                )

                # Check if application not sent before
                job_obj = FreeL_Applications.query.filter_by(freel_job_details_id=tender_id,
                                                             applicant_id=current_user.id).first()
                company_obj = company_user.query.get(apply.employer_id)

                # print('----------------------job_obj: ',job_obj)
                if not job_obj:
                    db.session.add(apply)
                    db.session.commit()
                    return flash(f'''Application sent Successfully!!.''', 'success')
                else:
                    # fl = flash(f"Application with this details Already Submitted!!", "error")
                    return f'''This Application Already Submitted.'''

    return f'Something went Wrong, Please return to the previuos page'


@app.route("/tender_ad_opened", methods=["GET", "POST"])
def view_tender():
    if request.method == 'GET':
        id = request.args['id']

        tender_ad = Freelance_Jobs_Ads.query.get(id)

        # print("Job Ad Title: ",job_ad.job_title)

    return render_template('tender_ad_opened.html', item=tender_ad, db=db, company_user=company_user, ser=ser)


# ------------------------------COMPANIES DATA------------------------------- #
@app.route("/company_sign_up", methods=["POST", "GET"])
def company_sign_up_form():
    company_register = Company_Register_Form()

    db.create_all()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':

        if company_register.validate_on_submit() or company_register.errors['payment_options']:
            # context

            # If the webpage has made a post e.g. form post

            # print('Create All..........................................')
            company_hashd_pwd = encry_pw.generate_password_hash(company_register.company_password.data).decode('utf-8')
            # Base.metadata.create_all()
            # ....user has inherited the Base class
            # db.create_all()
            user1 = company_user(
                name=company_register.company_name.data, email=company_register.company_email.data,
                password=company_hashd_pwd,
                confirm_password=company_hashd_pwd,
                company_contacts=company_register.company_contacts.data, image="default.jpg",
                company_address=company_register.company_address.data,
                web_link=company_register.website_link.data,
                fb_link=company_register.facebook_link.data,
                twitter_link=company_register.twitter_link.data,
                youtube=company_register.youtube_link.data,
                payment_options=request.form.get('payment_options'),
                time_stamp=datetime.utcnow(),
                                 )

            if company_register.company_logo.data:
                user1.image = save_pic(picture=company_register.company_logo.data)

            try:
                try:
                    db.session.add(user1)
                    db.session.commit()
                    flash(f"Account Successfully Created for {company_register.company_name.data}", "success")
                except exc.IntegrityError:
                    flash(
                        f"This email is already registered on this platform, Please use a regeister a different email",
                        "error")
                    return render_template("company_signup_form.html", company_register=company_register)
                except Exception as e:
                    db.session.rollback()
                    flash(f"Something went wrong {e}, Please re-enter your details", "error")
                    return redirect(url_for('company_sign_up_form'))
                return redirect(url_for('login'))
            except:
                flash(f"Something went wrong, check for errors", "error")
                Register().validate_email(company_register.company_email.data)

            return redirect(url_for('login'))

            # #print(company_register.name.data,company_register.email.data)
        elif company_register.errors:
            for error in company_register.errors:
                print("Company Acc Errors:", error)
                print("Company Acc Errors:", request.form.get("payment_options"))
            flash(f"Account Creation Unsuccessful ", "error")
        # print(company_register.errors)

    # from myproject.models import user
    return render_template("company_signup_form.html", company_register=company_register, ser=ser)


@app.route("/company_login", methods=["POST", "GET"])
def company_login():
    company_login = Company_Login()

    # image_fl = url_for('static', filename='images/' + current_user.image)

    user_class.cls_name = company_user
    # if current_company_user.is_authenticated:
    #     return redirect(url_for('home'))
    if request.method == 'POST':

        if company_login.validate_on_submit():
            # #print(f"Account Successfully Created for {company_login.name.data}")
            company_user_login = company_user.query.filter_by(email=company_login.company_email.data).first()
            # flash(f"Hey! {user_login.password} Welcome", "success")
            if company_user_login and encry_pw.check_password_hash(company_user_login.password,
                                                                   company_login.company_password.data):
                login_user(company_user_login)
                # After company_login required prompt, take me to the page I requested earlier
                req_page = request.args.get('next')
                flash(f"{company_user_login.name.title()} You're Logged In!", "success")
                return redirect(req_page) if req_page else redirect(url_for('home'))
            else:
                flash(f"Login Unsuccessful, please use correct email or password", "error")
                # print(company_login.errors)

    return render_template('company_login_form.html', title='Company Login', company_login=company_login, ser=ser)

@app.route("/google_signup", methods=["POST","GET"])
def google_signup():

    return render_template('google_signup.html')

#google login
@app.route("/google_login", methods=["POST","GET"])
def google_login():

    if current_user.is_authenticated:
        req_page = request.args.get('next')
        return redirect(req_page) if req_page else redirect(url_for('home'))

    return oauth.tht_oauth.authorize_redirect(redirect_uri=url_for("google_signin",_external=True))


#login redirect
@app.route("/google_signin", methods=["POST","GET"])
def google_signin():

    # Step 1: Handle the OAuth2 callback and exchange the authorization code for an access token
    token = oauth.tht_oauth.authorize_access_token()

    # Step 2: Parse the ID token from the response to get user information
    # user_info = oauth.tht_oauth.parse_id_token(token)
    
    # Step 3: Store user info in the Flask session for persistence
    session['user'] = token

    pretty=session.get("user")

    usr_info = pretty.get('userinfo')
    verified = usr_info.get("email_verified")
    usr_email = usr_info.get("email")
    usr_name=usr_info.get("name")
    usr_athash=usr_info.get("at_hash")

    if not verified:
        flash("Access Denied!, Your Email is not verified with Google")
        flash("Please, Set up your account manually")
        return redirect(url_for('sign_up'))
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #Sign Up
    if not user.query.filter_by(email=usr_email).first():

        print("Email Not Found!, We will register")

        # context
        hashd_pwd = encrypt_password.generate_password_hash(usr_athash).decode('utf-8')
        user1 = user(name=usr_name, email=usr_email, password=hashd_pwd,
                        confirm_password=hashd_pwd, image="default.jpg",time_stamp=current_time_wlzone(),verified=True)

        try:
            db.session.add(user1)
            db.session.commit()

            #Login user
            usr_obj = user.query.filter_by(email=usr_email).first()
            #Check if user have a church id
            login_user(usr_obj)
            flash(f"Welcome! {usr_obj.name.title()}", "success")

            req_page = request.args.get('next')
            return redirect(req_page) if req_page else redirect(url_for('home'))

        
        except IntegrityError:
            db.session.rollback()  # Rollback the session on error
            return jsonify({"message": "Email already exists"}), 409
        
        except Exception as e:
                db.session.rollback()  # Rollback on any other error
                return jsonify({"message": "An error occurred", "error": str(e)}), 500
        
    else:
        user_login = user.query.filter_by(email=usr_email).first()

        if not user_login.verified:
            login_user(user_login)
            return redirect(url_for('verification'))

        login_user(user_login)
        flash(f"welcome! {user_login.name.title()}", "success")

        session['req_page'] = request.args.get('next')

        return '''
                    <script type="text/javascript">
                        window.opener.postMessage('auth_complete', '*');
                        window.close();  // Optionally close the popup
                    </script>
                '''
          
        # if request.accept_mimetypes['text/html']:  # Checking if the request expects HTML
        #     print("1. Request accepts text/html")
        #     print("Check if Popup: ",request.args)
        #     if 'popup' in request.args:  # Conditional redirect for popup logic
        #         print("Message to close pop window sent!")
        #         return '''
        #             <script type="text/javascript">
        #                 window.opener.postMessage('auth_complete', '*');
        #                 window.close();  // Optionally close the popup
        #             </script>
        #         '''
        #     else:
        #         print("3. Redirect for Wider Screens")
        #         # Regular redirect for full page load
        #         return redirect(req_page) if req_page else redirect(url_for('home')) # Redirect to main dashboard page
        # else:
        #     return jsonify({'status': 'success'}), 200  # For APIs, return JSON response
    


# ---------------COMPANY ACCOUNT---------------------#
@app.route("/company_account", methods=["GET", "POST"])
@login_required
def company_account():
    company_update = Company_UpdateAcc_Form()

    image_fl = url_for('static', filename='images/' + current_user.image)

    if request.method == "POST":

        # if company_update.validate_on

        id = current_user.id
        cmp_usr = company_user.query.get(id)

        # print('DEBUG UPDATE 1: ', cmp_usr.web_link)

        if cmp_usr.image and company_update.company_logo.data:
            delete_img(cmp_usr.image)
            cmp_usr.image = save_pic(picture=company_update.company_logo.data)

        elif company_update.company_logo.data and not cmp_usr.image:
            pfl_pic = save_pic(picture=company_update.company_logo.data)
            cmp_usr.image = pfl_pic

        cmp_usr.name = company_update.company_name.data
        cmp_usr.email = company_update.company_email.data
        cmp_usr.contacts = company_update.company_contacts.data
        cmp_usr.web_link = company_update.website_link.data
        cmp_usr.fb_link = company_update.facebook_link.data
        cmp_usr.company_address = company_update.company_address.data
        cmp_usr.twitter_link = company_update.twitter_link.data
        cmp_usr.youtube = company_update.youtube_link.data
        cmp_usr.payment_options = request.form.get('payment_options')

        db.session.commit()

        flash(f"Updated Successful!!", "success")

        # print('DEBUG UPDATE: ',cmp_usr.web_link)

    return render_template("company_account.html", company_update=company_update, image_fl=image_fl, ser=ser)


# -------------------PARTNERING COMPANIES----------------------#
@app.route("/partnering_companies", methods=["GET", "POST"])
def partnering_companies():
    job_ads = Jobs_Ads.query.all()

    # Fix jobs adds does not have hidden tag
    return render_template("partnering_companies.html", job_ads=job_ads, job_ads_form=job_ads_form, db=db,
                           company_user=company_user, user=usr, no_image_fl=no_image_fl, ser=ser)


@app.route("/send_application", methods=["GET", "POST"])
@login_required
def send_application():
    send_application = Applications()

    db.create_all()

    if not current_user.image and not current_user.school:
        redirect(url_for('account'))
        flash("Warning!! Your Account needs to be updated Soon, You won't be able to send Application if not so",
              "error")

    else:
        if current_user.is_authenticated:

            if request.method == "GET":
                id_ = request.args['job_id']
                jb_id = ser.loads(id_)['data1']
                apply = Applications(
                    applicant_id=current_user.id,
                    job_details_id=jb_id,  # db.query(Jobs_Ads).get(jb_id),
                    employer_id=Jobs_Ads.query.get(jb_id).job_posted_by
                )

                # Check if application not sent before
                job_appl = Applications.query.filter_by(job_details_id=jb_id, applicant_id=current_user.id).first()
                company_obj = company_user.query.get(apply.employer_id)

                # print('----------------------job_appl: ',job_appl)
                if not job_appl:
                    db.session.add(apply)
                    db.session.commit()
                    job_title = Jobs_Ads.query.get(jb_id).job_title
                    job_id = Jobs_Ads.query.get(jb_id).job_id
                    return render_template("send_application.html", send_application=send_application, job_id=job_id,
                                           job_title=job_title,
                                           company_obj=company_obj, ser=ser)
                else:
                    # fl = flash(f"Application with this details Already Submitted!!", "error")
                    return f'''This Application Already Submitted before.
                     Please Wait for a Reply!!'''

    return f'Something went Wrong, Please return to the previuos page'


@app.route("/company_jb_ads", methods=["GET", "POST"])
@login_required
def local_jb_ads():
    if request.method == 'GET':
        id = ser.loads(request.args['id'])
        job_ad = Jobs_Ads.query.get(id)
        # print("Job Ad Title: ",job_ad.job_title)


@app.route("/delete_entry", methods=["GET", "POST"])
def delete_entry():
    if request.method == 'GET':
        j_id = ser.loads(request.args.get("jo_id"))['data_2']
        appl_tions = Applications.query.filter_by(job_details_id=j_id, applicant_id=current_user.id).first()

        db.session.delete(appl_tions)
        db.session.commit()

        flash("Successfully Deleted!!", "success")

        return redirect(url_for("job_adverts"))

    return f''


@app.route("/delete_post", methods=["GET", "POST"])
@login_required
def delete_post():
    if request.method == 'GET':
        pid = ser.loads(request.args.get("pstid"))['data']
        post = jobs_posted.query.get(pid)

        db.session.delete(post)
        db.session.commit()

        flash("Successfully Deleted!!", "success")

        return redirect(url_for("home"))

    return f''


def log_email_delivery(recipient_email,user_id,appl_id,token=None, status=None):
    # Create a new log entry
    print("email: ", recipient_email)
    print("User Id: ", user_id)
    print("token: ", token)
    print("status: ", status)

    if status == "Failed":
        return jsonify({"Error":"Message Not Sent please confirm if recipient email is correct"})

    new_log = Tracking(
        uid = user_id,
        recipient=recipient_email,
        appl_id=appl_id,
        status=status,
        last_seen=None,  # Set to None by default
        timestamp=current_time_wlzone(),
        unique_id = token 
    )

    db.session.add(new_log)
    db.session.commit()
    print(f"Tracking Entry Recorded with Token: {new_log.unique_id}", "success")


def update_last_seen(log_entry):
    # log_entry = Tracking.query.filter_by(company_email=recipient_email).order_by(Tracking.id.desc()).first()
    if log_entry:
        log_entry.last_seen = current_time_wlzone()  # Update to the current UTC time
        print("Last Seen: ", log_entry.last_seen)
        db.session.commit()

# Get request from client email box 
@app.route('/track_email_open/<token>', methods=['GET'])
def track_email_opened(token):
    log_entry = Tracking.query.filter_by(unique_id=token).first()
    if log_entry:
        # Update last seen timestamp on email open
        update_last_seen(log_entry)
        
        # Send back a transparent 1x1 GIF
        # This is a simple transparent pixel
        pixel_data = io.BytesIO()
        pixel_data.write(b'\x47\x38\x39\x61\x01\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00')
        pixel_data.seek(0)
        return send_file(pixel_data, mimetype='image/gif')
    else:
        return '', 404


@app.route("/job_reports", methods=["GET", "POST"])
@login_required
def job_reports():

    # reports = easyapply.query.filter_by(uid=current_user.id).order_by(easyapply.timestamp).all()
    # print("REPORTS: ",reports)
    reports = Tracking.query.filter_by(uid=current_user.id).order_by(Tracking.timestamp).all()

    return render_template("applications_report.html",reports=reports,apply_obj= easyapply )


@app.route("/easy_apply", methods=["GET", "POST"])
def easy_apply():

    form = EasyApplyForm()
    certificates_ = []

    if request.method =="POST":
        application = easyapply(
            uid = current_user.id,
            company_email  = form.company_email.data,
            portfolio_link  = form.portfolio_link.data,
            job_title = form.subject.data,
            timestamp = current_time_wlzone()
        )
        #Letter
        if form.letter.data:
            application.letter = save_pdf(form.letter.data)

        #CV
        if form.cv.data:
            application.cv = save_pdf(form.cv.data)

        #ID
        if form.id.data:
            application.other_doc = save_pdf(form.id.data)

        #Drivers
        if form.drivers.data:
            application.other_doc1= save_pdf(form.drivers.data)

        db.session.add(application)
        db.session.commit()

        ea_obj = easyapply.query.filter_by(uid=current_user.id).order_by(easyapply.timestamp.desc()).first()
        print("Company Email:", ea_obj.id )
        print("Easy Apply Latest Application: ", ea_obj.timestamp)
        print("Application Id:", ea_obj.id )

        # We are recording certificates in a different model/table
        if form.certificates.data:
            files = form.certificates.data
            for file in files:
                cert = Certificate (
                    #Job Application Id
                    ea_id = ea_obj.id
                )
                cert.cert_file = save_pdf(file)
                certificates_.append(cert.cert_file)
                db.session.add(cert)
            db.session.commit()
            print("Certificates: ",certificates_)
        print("Application Saved in database")

        # Send Email And Track Delivery
        recipient_email = form.company_email.data
        subject = form.subject.data
        bodyy = form.body.data
        token = secrets.token_urlsafe(32) 
        appl_id = ea_obj.id
        print("Email Token Created: ",token)

        
        letter = form.letter.data
        cv_file = form.cv.data
        id_file = form.id.data
        drivers_file = form.drivers.data

        print("----Docs from Form Object----")
        print("CV: ",cv_file.filename)
        print("Letter: ",letter.filename)
        print("ID: ",id_file.filename)
        print("Drivers: ",drivers_file.filename)
        print("--------------------------------")
            
        # app.config['MAIL_USE_SSL'] = False
        mail = Mail(app)
        user_email = current_user.email

        # Create the tracking pixel URL
        pixel_url = url_for('track_email_opened', token=token, _external=True)

        bodyy += f"""<br><img src="{pixel_url}" width="1" height="1" alt="" style="display:none;" />"""

        def send_email():
            print("Subject: ", subject)
            print("Body: ",bodyy)
            print("Email: ",recipient_email)

            # Create and send the email
            msg = Message(subject, sender="noreply@gmail.com", recipients=[recipient_email, user_email])
            msg.html = bodyy
            print("Msg: ",msg.html)

            # ----Docs from Model Object----
            print("----Docs from Model Object----")
            print("CV: ",application.cv)
            print("Letter: ",application.letter)
            print("ID: ",application.other_doc)
            print("Drivers: ",application.other_doc1)
            print("--------------------------------")
            
            # Check if the attachment file exists
            cv_file_path = None
            lttr_file_path = None
            id_file_path = None
            drivers_file_path = None
            if application.cv:
                cv_file_path = os.path.join("static/files",application.cv)
            if application.letter:
                lttr_file_path = os.path.join("static/files",application.letter)
            if application.other_doc:
                id_file_path = os.path.join("static/files",application.other_doc)
            if application.other_doc1:
                drivers_file_path = os.path.join("static/files",application.other_doc1)

            if application.cv and os.path.exists(cv_file_path):
                with app.open_resource(cv_file_path) as fp:
                    msg.attach(application.cv, cv_file.mimetype, fp.read())
                    print("Attached CV")

            # Check if the attachment file exists
            if application.letter and os.path.exists(lttr_file_path):
                with app.open_resource(lttr_file_path) as fp:
                    msg.attach(application.letter, letter.mimetype, fp.read())
                    print("Attached Letter")

            # Drivers
            if application.other_doc and os.path.exists(drivers_file_path):
                with app.open_resource(drivers_file_path) as fp:
                    msg.attach(application.other_doc1, drivers_file.mimetype, fp.read())
                    print("Attached Drivers")

            # ID
            if application.other_doc1 and os.path.exists(id_file_path):
                with app.open_resource(id_file_path) as fp:
                    msg.attach(application.other_doc, id_file.mimetype, fp.read())
                    print("Attached ID")

            # Attached Certicates
            if form.certificates.data:
                for cert in certificates_:
                    cert_file_path = os.path.join("static/files",cert)
                    if os.path.exists(cert_file_path):
                        with app.open_resource(cert_file_path) as fp:
                            msg.attach(cert, letter.mimetype, fp.read())
                            print("Attached Certificate")

            # try:
            with app.app_context():
                mail.send(msg)

            log_email_delivery(recipient_email,current_user.id,appl_id,token=token,status='Sent')  # Log email delivery status
            flash("Email Sent Successfully! Check your inbox we have copied the email you sent to the receiver", "success")
            # except Exception as e:
            #    log_email_delivery(recipient_email,current_user.id,token=token,status='Failed')  # Log failure status
            #    print(f'Error sending email: {e}')

        send_email()
        

    return render_template("easy_apply.html", form=form)


@app.route("/download_")
def downloadapp():

    return render_template("download_app.html")

@app.route("/download_app")
def downloadapk():

    file_path = "/home/techtlnf/public_html/public_html/thehustlerstime.apk" # Full file path to the APK

    return send_file(file_path, as_attachment=True, download_name='thehustlerstime.apk')


@app.route("/users")
def users():
    from sqlalchemy import text

    user_v = []
    users_ = user.query.all()

    return render_template("user.html", users=users_, ser=ser)


@app.route("/user_viewed", methods=["GET", "POST"])
def view_user():
    # if current_user.role == 'company_user':
    uid = ser.loads(request.args['id'])['data6']
    company_usr = company_user
    job_ad = Jobs_Ads
    portfolio_model = users_tht_portfolio.query.filter_by(usr_id=uid).all()
    portfolio_approved_jobs = users_tht_portfolio.query.filter_by(approved=True).all()
    # The placement that is not marked as approved, assuming is still open / the user is still working
    portfolio_current_job = hired.query.filter_by(usr_cur_job=1, hired_user_id=uid).first()
    job_usr = user.query.get(uid)

        # if request.method == 'POST':
        #     pass
    # else:
    #     flash(f'Only Registered Employers can Hire Job Seekers','warning')
        # print("Job Ad Title: ",job_ad.job_title)

    return render_template('user_viewed.html', job_usr=job_usr, db=db, user=user, company_user=company_user,
                           portfolio_approved_jobs=portfolio_approved_jobs
                           , ser=ser, current_job=portfolio_current_job, company_usr=company_usr, job_ad=job_ad)


@app.route("/verified/<token>", methods=["POST", "GET"])
# Email verification link verified with a token
def verified(token):
    # Check to verify the token received from the user email
    # process the user_id for the following script
    user_id = user_class.verify_reset_token(token)

    # if current_user.is_authenticated:
    #     # usr_obj = user_class().verify_reset_token(token)
    #     check_hash = encry_pw.check_password_hash(token,current_user.is_authenticated+str(current_user.id))
    #     flash(f'User ID is {token} is found','error')
    #

    try:
        usr = user.query.get(user_id)
        usr.verified = True
        db.session.commit()
        if usr.verified:
            qry_usr = user.query.get(user_id)
            if not current_user.is_authenticated:
                login_user(usr)
            flash(f"Welcome, {qry_usr.name}; Please Finish Updating your Profile!!", "success")
            return redirect(url_for('account'))
    except Exception as e:
        flash(f"Something went wrong, Please try again ", "error")

    return render_template('verified.html')


@app.route("/verification/<arg>", methods=["POST", "GET"])
# User email verification @login
# @login the user will register & when the log in the code checks if the user is verified first...
def verification(arg):
    # Manage DB tables
    db.create_all()
    if arg:
        try:
            usr_ = user.query.get(user_class.verify_reset_token(arg))
        except:
            return 'Something Wrong'

    def send_veri_mail():
        if arg:

            app.config["MAIL_SERVER"] = "smtp.googlemail.com"
            app.config["MAIL_PORT"] = 587
            app.config["MAIL_USE_TLS"] = True
            # Creditentials saved in environmental variables
            # em = app.config["MAIL_USERNAME"] = "pro.dignitron@gmail.com"  # os.getenv("MAIL")
            # app.config["MAIL_PASSWORD"] = os.getenv("PWD")
            app.config["MAIL_DEFAULT_SENDER"] = '"The Hustlers Time" <no-reply@gmail.com>'
            app.config["MAIL_DEFAULT_SENDER"] = '"noreply@gmail.com"'

            mail = Mail(app)

            token = arg  # user_class().get_reset_token(arg)
            usr_email = usr_.email

            msg = Message(subject="Email Verification", sender="no-reply@gmail.com", recipients=[usr_email])

            msg.body = f"""Hi, {usr_.name}
            
Please follow the link below to verify your email with The Hustlers Time:
            
Verification link;
{url_for('verified', token=token, _external=True)}
            """
            try:
                mail.send(msg)
                flash(f'An email has been sent with a verification link to your email account', 'success')
                return "Email Sent"
            except Exception as e:
                flash(f'Email not sent here', 'error')
                return "The mail was not sent"

    try:
        if not usr_.verified:
            send_veri_mail()
        else:
            return redirect(url_for("home"))
    except:
        flash(f'Debug {usr_.email}', 'error')
        return redirect(url_for("login"))

    return render_template('verification.html', ser=ser)


# (1) Company Views All Applications under her name
@app.route("/job_applications", methods=["GET", "POST"])
def applications():
    # Get all applications from Applications database
    all_applications = Applications.query.all()

    # print("Debug Application List: ", db.query(job_user).get(all_applications[0].applicant_id).name )

    applications = Applications()

    job_usr = job_user
    job_ads = Jobs_Ads

    return render_template("applications.html", all_applications=all_applications, job_user=job_usr, job_ads=job_ads,
                           applications=applications, db=db, ser=ser)


# (2) They view each applicant of their choice
@app.route("/view_applicant", methods=["GET", "POST"])
def view_applicant():
    if request.method == 'GET':
        id_ = ser.loads(request.args['uid'])['data4']
        app_id = ser.loads(request.args['app_id'])['data5']
        job_usr = job_user.query.get(id_)

    return render_template("view_applicant.html", job_usr=job_usr, app_id=app_id, ser=ser)


# (3) After viewing the applicant, they hire the applicant
@app.route("/hire_applicant", methods=["GET", "POST"])
@login_required
def hire_applicant():
    if current_user.is_authenticated and current_user.role == 'company_user':
        if request.method == 'GET':
            # Based on the context, consider handling the 'POST' method as well

            try:
                encr_id = request.args['id']
                id_ = ser.loads(encr_id)['data2']
                encr_app_id = request.args.get('app_id')
                job_usr = job_user.query.get(id_)

                if not encr_app_id:
                    flash(f"Please Fill the form below to Complete the Hiring Process of {job_usr.name};")
                    return redirect(url_for("job_ads_form",udi=encr_id))
                else:
                    app_id = ser.loads(encr_app_id)['data3']

                # Logic to hire the user and update the application status
                hire_user = hired(
                    comp_id=current_user.id,
                    hired_user_id=id_,
                    job_details=app_id,
                    usr_cur_job=1,  # Currently hired
                    hired_date=datetime.utcnow()
                )
                db.session.add(hire_user)

                close_appl = Applications.query.filter_by(job_details_id=app_id).first()
                close_appl.closed = "Yes"  # This means that this user is hired

                db.session.commit()

                # flash message for successful hiring
                flash(
                    f'You have successfully hired {user.query.get(id_).name} for {Jobs_Ads.query.get(app_id).job_title}',
                    'success')
            except Exception as e:
                # flash message for error
                flash(f'Something went wrong: {e}', 'error')

            # return a response for the GET request
            return render_template("hire_applicant.html", job_usr=job_usr, db=db)

        elif request.method == 'POST':
            # Logic for POST method (if needed)
            # return a response for the POST request
            return redirect(url_for('desired_endpoint'))

    else:
        flash("Only Companies are allowed recruit Job Seekers")
        return redirect(url_for("users"))

    # return a response for scenarios other than GET or POST request
    return render_template("hire_applicant.html", job_usr=None, db=db)


class Store_UID:
    id_ = None

# (3) After viewing the freelancer, they hire the applicant

@app.route("/hire_freelancer", methods=["GET", "POST"])
@login_required
def hire_freelancer():
    counter = 0

    id_ = None
    esw_freelancers = Esw_Freelancers
    freelancer_user = None

    if request.method == 'GET' and request.args.get('id'):
        # Based on the context, consider handling the 'POST' method as well

        try:
            encr_id = request.args['id']
            id_ = ser.loads(encr_id)['data17']
            freelancer_user = user.query.get(id_)
            Store_UID.id_ = id_

        except Exception as e:
            # flash message for error
            flash(f'Something went wrong: {e}', 'error')

    elif request.method == 'POST':
        id_ = Store_UID.id_
        # flash(f" Log {id_}","success")
        if id_:
            # flash(f'Post Request {Store_UID.id_}', 'success')
            # Logic to hire the user and update the application status
            hire_freelanca = Hire_Freelancer(
                freelancer_id=id_,
                employer_id=current_user.id,
                purpose_for_hire=request.form.get('purpose_for_hire'),
                hired_date=datetime.utcnow()
            )

            db.session.add(hire_freelanca)
            db.session.commit()

            def send_mail():

                job_id_token = ser.dumps(
                    {'data11': hire_freelanca.id})  # user_class().get_reset_token(hire_freelanca.id)
                user_obj = user.query.get(id_)

                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                # em = app.config["MAIL_USERNAME"] = os.environ.get("EMAIL")
                # app.config["MAIL_PASSWORD"] = os.environ.get("PWD")

                mail = Mail(app)

                msg = Message("Expression of Interest for your Services", sender=em, recipients=[user_obj.email])
                msg.body = f""" Hi {user_obj.name}

{current_user.name} has expressed an interest to hire the quality of your services. Please attend to this message as soon as you read this
by following the link below to see all the details.
                    
 View Details & Sign-up the Deal!: {url_for('fl_approve_deal', token=job_id_token, _external=True)}


                    """

                try:
                    mail.send(msg)
                    flash(
                        f'You have successfully sent an expression of interest to hire {user.query.get(id_).name} services',
                        'success')

                except Exception as e:
                    flash(f'Ooops Something went wrong!! Please Retry', 'error')
                    return "The mail was not sent"

            while counter == 0:
                send_mail()
                counter = +1
            # flash message for successful hiring

    # return a response for scenarios other than GET or POST request
    return render_template("hire_freelancer.html", freelancer_user=freelancer_user, user=user,
                           esw_freelancers=esw_freelancers)


@app.route("/fl_approve_deal/<token>", methods=['POST', 'GET'])
@login_required
def fl_approve_deal(token):
    # Get user's identity
    # approve_form = Approved_Form()

    # Job ID
    deal_id = ser.loads(token)['data11']  # user_class().verify_reset_token(token)

    deal_obj = Hire_Freelancer.query.get(deal_id)

    # Check if the user(current_user.id) is the one being assign this job(deal_obj.freel_id)
    if current_user.id == deal_obj.freelancer_id:

        if request.method == 'POST':

            deal_obj.other_hr = "Taken_" + str(deal_obj.freelancer_id)

            def send_mail():

                # job_id_token = user_class().get_reset_token(hire_freelanca.id)
                user_obj = user.query.get(deal_obj.freelancer_id)

                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                # em = app.config["MAIL_USERNAME"] = os.environ.get("EMAIL")
                # app.config["MAIL_PASSWORD"] = os.environ.get("PWD")

                mail = Mail(app)

                msg = Message("Re:Expression of Interest for your Services", sender=em, recipients=[user_obj.email])
                msg.body = f""" Hi {user.query.get(deal_obj.employer_id).name}

{current_user.name} has approved and agrees to offer the services you requested below; 

Job Brief:

{deal_obj.purpose_for_hire}

                                """

                try:
                    mail.send(msg)
                    flash(
                        f'Congratulations Deal Sealed!!',
                        'success')

                except Exception as e:
                    flash(f'Ooops Something went wrong!! Please Retry', 'error')
                    return "The mail was not sent"

            send_mail()

    return render_template('approve_deal.html', deal_obj=deal_obj, user=user)


@app.route("/tht_intro_eswatini")
def intro_eswatini():


    return render_template("tht_intro_eswatini.html")


@app.route("/tht_intro_freelancers")
def intro_eswatini_fl():


    return render_template("freelance_ad_intro.html")


@app.route("/tht_intro_jobs")
def intro_eswatini_jobs():


    return render_template("jobs_ads_intro.html")

@app.route('/sitemap.xml')
def sitemap():

    return send_from_directory(app.static_folder, 'sitemap.xml')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
