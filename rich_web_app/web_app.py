from flask import Flask, render_template,redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, HiddenField
from wtforms.validators import DataRequired
import os
SECRET_KEY = os.urandom(32)

data = []

class SupplyForm(FlaskForm):
    equipment = StringField('equipment', validators=[DataRequired()])
    batch_number = IntegerField('batch_number', validators=[DataRequired()])
    disposal_date = DateField('disposal_date', validators=[DataRequired()])


class DeleteForm(FlaskForm):
    pass


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html', equipment=data)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@app.route('/edit/', methods=['GET', 'POST'])
def submit(id=None):
    if id is not None:
        equipment=data[id]
        form = SupplyForm(data=equipment)
    else:
        form=SupplyForm()

    if form.validate_on_submit():
        if id is None:
            equipment = {}
            data.append(equipment)

        equipment['equipment'] = form.equipment.data
        equipment['batch_number'] = form.batch_number.data
        equipment['disposal_date'] = form.disposal_date.data

        return redirect(url_for('index'))

    return render_template('submit.html', form=form, id=id)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    equipment=data[id]
    form = DeleteForm()

    if form.validate_on_submit():
        del data[id]

        return redirect(url_for('index'))

    return render_template('delete.html', form=form, equipment=equipment, id=id)
