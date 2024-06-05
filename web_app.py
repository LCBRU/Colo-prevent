from flask import Flask, render_template,redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import os
SECRET_KEY = os.urandom(32)


class SupplyForm(FlaskForm):
    equipment = StringField('equipment', validators=[DataRequired()])
    batch_number = StringField('batch_number', validators=[DataRequired()])
    disposal_date = StringField('disposal_date', validators=[DataRequired()])


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SupplyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)

@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')