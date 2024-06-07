from flask import Flask, render_template,redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField,SubmitField,FieldList,FormField
from wtforms.validators import DataRequired, Optional
import os
SECRET_KEY = os.urandom(32)


class SupplyForm(FlaskForm):
    equipment = StringField('equipment', validators=[Optional()])
    batch_number = IntegerField('batch_number', validators=[Optional()])
    disposal_date = DateField('disposal_date', validators=[Optional()])
  

    
class AdditonalForm(FlaskForm):
    more_fields = FieldList(FormField(SupplyForm), min_entries=4)
    submit = SubmitField('submit')
    edit = SubmitField('edit')
    delete = SubmitField('delete')


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = AdditonalForm()
    if form.validate_on_submit():
        return redirect('/success')

    return render_template('submit.html', form=form)

@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')

