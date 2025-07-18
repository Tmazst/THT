
# from alchemy_db import db.Model
from sqlalchemy import  MetaData, ForeignKey
from flask_login import login_user, UserMixin
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import app

db = SQLAlchemy()


#from app import login_manager

metadata = MetaData()


#Users class, The class table name 'h1t_users_cvs'
class user(db.Model,UserMixin):

    __tablename__ = 'user'
    # __table_args__ = {'extend_existing': True}

    #Create db.Columns
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    image = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120), unique=True)
    token = db.Column(db.String(255), unique=True,nullable=True)
    store_2fa_code=db.Column(db.String(255))
    time_stamp=db.Column(db.DateTime())
    confirm_password = db.Column(db.String(120), unique=True)
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(120))
    freelancers_tbl = relationship("Esw_Freelancers", backref='freelancers', lazy=True)

    __mapper_args__ = {
        "polymorphic_identity":'user',
        'polymorphic_on':role
    }

# class store_otps(db.Model,UserMixin):
#     user_id = db.Column(db.Integer,pri)
class job_user(user):

    __tablename__ = 'job_user'

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    school = db.Column(db.String(120))
    tertiary = db.Column(db.String(255))
    contacts = db.Column(db.String(20))
    date_of_birth = db.Column(db.DateTime())
    experience = db.Column(db.String(500))
    skills = db.Column(db.String(500))
    hobbies = db.Column(db.String(120))
    address = db.Column(db.String(120))
    reference_1 = db.Column(db.String(120))
    reference_2 = db.Column(db.String(120))
    other = db.Column(db.String(120)) #Resume
    jobs_applied_for = relationship("Applications", backref='Applications.job_title', lazy=True)
    hired_user = relationship("hired", backref='Hired Applicant', lazy=True)

    __mapper_args__={
            "polymorphic_identity":'job_user'
        }

class company_user(user):

    __tablename__ = 'company_user'
    # __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    company_address = db.Column(db.String(120))
    company_contacts = db.Column(db.String(120))
    web_link = db.Column(db.String(120))
    fb_link = db.Column(db.String(120))
    twitter_link = db.Column(db.String(120))
    youtube = db.Column(db.String(120))
    other = db.Column(db.String(120))
    payment_options = db.Column(db.String(100))
    job_ads = relationship("Jobs_Ads", backref='Jobs_Ads.job_title',lazy=True)
    applicantions_posted = relationship("Applications", backref='employer', lazy=True)
    freelance_job_ads = relationship("Freelance_Jobs_Ads", backref='Freelance_Jobs_Ads.service_title', lazy=True)

    __mapper_args__ = {
        "polymorphic_identity": 'company_user'
    }

class user_experince_entries(db.Model, UserMixin): #table form filling prior tht experience

    id = db.Column(db.Integer, ForeignKey('job_user.id'), primary_key=True)
    portfolio_pdf = db.Column(db.String(120))
    fl_experience = db.Column(db.String(120))
    other_fl = db.Column(db.String(120))
    what_do_you_do = db.Column(db.String(1000))


class jobs_posted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advert_image = db.Column(db.String(120))
    job_title = db.Column(db.String(60))
    details = db.Column(db.String(60))
    deadline = db.Column(db.Date)
    timepstamp = db.Column(db.DateTime)
    link = db.Column(db.String(150))


class easyapply(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, ForeignKey('user.id'))
    letter = db.Column(db.String(120))
    company_email =  db.Column(db.String(120))
    cv = db.Column(db.String(120))
    job_title = db.Column(db.String(120))
    portfolio_link = db.Column(db.String(120))
    resume = db.Column(db.String(120))
    other_doc = db.Column(db.String(120))#ID
    other_doc1 = db.Column(db.String(120))#License
    other_doc2 = db.Column(db.String(120))#Other
    other_doc3 = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime)
    tracking_ids = relationship("Tracking", backref='easyapply', lazy=True)
    certificate_ids = relationship("Certificate", backref='easyapply', lazy=True)


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ea_id = db.Column(db.Integer, ForeignKey('easyapply.id'))
    cert_file = db.Column(db.String(120))


class Tracking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, ForeignKey('user.id'))
    appl_id = db.Column(db.Integer, ForeignKey('easyapply.id'))
    unique_id = db.Column(db.String(120))
    recipient = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime)
    status = db.Column(db.String(120))
    last_seen = db.Column(db.DateTime)
    other = db.Column(db.String(120))
    other1 = db.Column(db.String(120))


class online_courses(db.Model):

    __tablename__ = "online_courses"

    id = db.Column(db.Integer, primary_key=True)
    course_name =  db.Column(db.String(120))
    university =  db.Column(db.String(120))
    describe =  db.Column(db.String(120))
    site =  db.Column(db.String(120))
    course_starts=db.Column(db.Date)
    intro_link =  db.Column(db.String(120))
    course_link =  db.Column(db.String(120))
    other=db.Column(db.String(120))
    other1=db.Column(db.String(120))
    other2=db.Column(db.String(120))
    course_image=db.Column(db.String(120))


class Esw_Freelancers(db.Model, UserMixin): #A table form filling prior tht experience

    __table_name__ = 'esw_freelancers'

    fl_id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, ForeignKey('user.id'))
    portfolio_pdf = db.Column(db.String(120))
    fl_experience = db.Column(db.String(300))
    other_fl = db.Column(db.String(120)) #Selling Tag
    other_fl1 = db.Column(db.String(120)) #Skills
    other_fl2 = db.Column(db.String(120))
    other_fl3 = db.Column(db.String(120))
    other_fl4 = db.Column(db.String(120))
    fb_link = db.Column(db.String(120))
    pinterest_link = db.Column(db.String(120))
    linkedin_link = db.Column(db.String(120))
    twitter_link = db.Column(db.String(120))
    youtube = db.Column(db.String(120))
    instagram_link = db.Column(db.String(120))
    what_do_you_do = db.Column(db.String(1000))


class Freelancers(job_user): #A table form filling prior tht experience
    pass
#     id = db.Column(db.Integer, ForeignKey('job_user.id'), primary_key=True)
#     portfolio_pdf = db.Column(db.String(120))
#     fl_experience = db.Column(db.String(120))
#     other_fl = db.Column(db.String(120))
#     what_do_you_do = db.Column(db.String(1000))


#After the user finishes the current(latest) job contract they supposed to fill a form to be used to store their work experience
class users_tht_portfolio(db.Model, UserMixin): #A table for tht experince
    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, ForeignKey('job_user.id'))
    job_details = db.Column(db.Integer, ForeignKey('job_ads.job_id')) #these entery I will the company(job_posted_by) which posted the job & other details about the job
    portfolio_feedback = db.Column(db.String(1000))
    date_employed = db.Column(db.DateTime())
    approved = db.Column(db.Boolean)
    portfolio_other = db.Column(db.String(120))
    other2 = db.Column(db.String(120))


class hired(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, ForeignKey('company_user.id'))
    hired_user_id = db.Column(db.Integer, ForeignKey('user.id'))
    job_details = db.Column(db.String(120)) #Job Id will be sent to the route and be stored in database
    usr_cur_job = db.Column(db.Boolean) #To check which job is open(current job) for the user
    hired_date = db.Column(db.DateTime())
    #I need to add a pending entry checker; a current job of the job_user to identify entry here   ----pending


class page_activity_analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(120))
    page_url = db.Column(db.String(120))
    event_type = db.Column(db.String(120))
    event_data = db.Column(db.String(120))
    page_visited_by = db.Column(db.String(120))
    page_visited_time = db.Column(db.DateTime())
    page_visited_ip = db.Column(db.String(120))
    page_visited_device = db.Column(db.String(120))
    page_visited_browser = db.Column(db.String(120))



class Hire_Freelancer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, ForeignKey('user.id'))
    freelancer_id = db.Column(db.Integer, ForeignKey('user.id'))
    purpose_for_hire = db.Column(db.String(120))
    job_done_approved = db.Column(db.Boolean, default=False)
    hired_date = db.Column(db.DateTime()) #Expression Date
    other_hr = db.Column(db.String(120)) #Sealing Deal
    other_hr1 = db.Column(db.String(120))
    other_hr2 = db.Column(db.String(120))
    #I need to add a pending entry checker; a current job of the job_user to identify entry here   ----pending

class Email_Verifications(db.Model, UserMixin):

    __table_name__='email_verifications'

    email_id = db.Column(db.Integer,ForeignKey('user.id'), primary_key=True)
    generated_hash = db.Column(db.String(120))
    time_stamp = db.DateTime()

class Jobs_Ads(db.Model, UserMixin):

    __tablename__ = "job_ads"

    job_id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    pay_type = db.Column(db.String(50))
    job_type = db.Column(db.String(50))
    about_company = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.String(200))
    work_duration = db.Column(db.DateTime)
    work_duration2 = db.Column(db.DateTime)
    work_days = db.Column(db.String(60))
    work_hours = db.Column(db.String(60))
    responsibilities = db.Column(db.String(200))
    qualifications = db.Column(db.String(200))
    age_range = db.Column(db.String(60))
    benefits = db.Column(db.String(200))
    application_deadline = db.Column(db.DateTime, nullable=False)
    contact_person = db.Column(db.String(60))
    other = db.Column(db.String(120))
    date_posted = db.Column(db.DateTime, default=datetime.now(), nullable=False) #Records itself
    job_posted_by = db.Column(db.Integer, ForeignKey('company_user.id'),nullable=False) #Records itself
    applicantions = relationship("Applications", backref='All Applications', lazy=True)
    tht_portfolio_hired = relationship("users_tht_portfolio", backref='users_tht_portfolio.id', lazy=True)

class Applications(db.Model, UserMixin):

    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, ForeignKey('job_user.id'), nullable=False)
    employer_id = db.Column(db.Integer, ForeignKey('company_user.id'), nullable=False)
    job_details_id = db.Column(db.Integer, ForeignKey('job_ads.job_id'), nullable=False)
    other = db.Column(db.String(120))
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    closed = db.Column(db.String(200))

class FreeL_Applications(db.Model, UserMixin):

    __tablename__ = 'freelance_applications'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, ForeignKey('job_user.id'), nullable=False)
    employer_id = db.Column(db.Integer, ForeignKey('company_user.id'), nullable=False)
    other = db.Column(db.String(120))
    freel_job_details_id = db.Column(db.Integer, ForeignKey('freelance_job_ads.job_id'), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    closed = db.Column(db.String(200))


class Freelance_Jobs_Ads(db.Model, UserMixin):

    __tablename__ = "freelance_job_ads"

    job_id = db.Column(db.Integer, primary_key=True)
    service_title = db.Column(db.String(100))  #e.g Logo Design
    service_category = db.Column(db.String(100))   #e.g Design & Technology
    specialty = db.Column(db.String(100))      #e.g Graphic Designer
    description = db.Column(db.String(200))
    project_duration = db.Column(db.DateTime)  #Project duration
    project_duration2 = db.Column(db.DateTime)
    project_prerequits = db.Column(db.String(500))
    working_days = db.Column(db.String(60))
    other = db.Column(db.String(200))
    application_deadline = db.Column(db.DateTime, nullable=False)
    contact_person = db.Column(db.String(60))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    job_posted_by = db.Column(db.Integer, ForeignKey('company_user.id'),nullable=False) #Records itself
    applications = relationship("FreeL_Applications", backref='FreeL_Applications.id', lazy=True)

class testimonials(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    title = db.Column(db.String(10)) #db.Column(db.Boolean, default=False)
    occupation = db.Column(db.String(80))
    company = db.Column(db.String(80))
    testimony = db.Column(db.String(200))
    image = db.Column(db.String(120))


class visitors(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(122))
    other = db.Column(db.String(122))
    other1 = db.Column(db.String(122))
    latest_visit = db.Column(db.DateTime)
    num_visits = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    page_stats_id = relationship("page_visits_stats",backref="visitors",lazy=True)
    sources_stats_id = relationship("page_visits_sources",backref="visitors",lazy=True)


class page_visits_stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, ForeignKey("visitors.id"))
    home = db.Column(db.Integer)
    featured = db.Column(db.Integer)
    freelance = db.Column(db.Integer)
    courses = db.Column(db.Integer)
    jo_boards = db.Column(db.Integer)
    other = db.Column(db.Integer)
    last_visit = db.Column(db.DateTime)

class page_visits_sources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, ForeignKey("visitors.id"))
    source = db.Column(db.String(122))
    timestamp = db.Column(db.DateTime)


class Survey_Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class NotificationsAccess(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255))
    p256dh = db.Column(db.String(255))
    auth = db.Column(db.String(255))
    ip = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)

class forbedden_requests(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    other = db.Column(db.String(255))