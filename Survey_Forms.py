from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, TextAreaField,BooleanField,DateField,URLField,MultipleFileField,RadioField
from wtforms.validators import DataRequired,Length,Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from flask_wtf.file import FileField , FileAllowed


# Define your survey form
class SurveyForm(FlaskForm):
    remote_job_interest = RadioField(
        'I am an employer and want to learn more about remote job opportunities.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    support_initiative = RadioField(
        'I support this initiative but am unsure if I should participate.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    revolutionize_job_market = RadioField(
        'This initiative could revolutionize the job market in our region.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    participate = RadioField(
        'I would like to participate in this initiative.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    encourage_companies = RadioField(
        'I encourage more companies to create remote job openings.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    reduce_unemployment = RadioField(
        'Remote jobs can reduce unemployment and promote equal opportunities.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    value_experience = RadioField(
        'Remote jobs provide valuable experience for inexperienced workers.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    industry_experience = RadioField(
        'Remote jobs help individuals with disabilities gain industry experience.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    uncover_hidden_talents = RadioField(
        'These initiatives can uncover and highlight hidden talents in our region.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    work_life_balance = RadioField(
        'I believe remote work can improve work-life balance.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    confidence_participation = RadioField(
        'I feel confident in my ability to participate in remote work.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    platform_knowledge = RadioField(
        'I am aware of platforms that connect freelancers with employers.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    resources_info = RadioField(
        'I would like to receive more information about available resources for remote work.',
        choices=[('Strongly Disagree', 'Strongly Disagree'),
                 ('Disagree', 'Disagree'),
                 ('Agree', 'Agree'),
                 ('Strongly Agree', 'Strongly Agree')],
        validators=[Optional()]
    )
    job_interest = TextAreaField(
        'What types of remote or freelance jobs interest you the most?',
        validators=[Optional()]
    )
    submit = SubmitField('Submit')