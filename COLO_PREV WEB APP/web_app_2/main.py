from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField,DateField,IntegerField,SubmitField
from wtforms.validators import DataRequired
import os
import csv
from csv import DictWriter



class RequestForm(FlaskForm):
    id = IntegerField('Equipment ID', validators=[DataRequired()])
    equipment = StringField('Equipment', validators=[DataRequired()])
    total_requested =IntegerField('Total requested', validators=[DataRequired()])
    date_requested =DateField('Date requested', validators=[DataRequired()])
    submit=SubmitField('Request')

class DeleteData(FlaskForm):
    type_id = IntegerField('Equipment ID', validators=[DataRequired()])
    submit = SubmitField('Delete')

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = RequestForm()
    if form.validate_on_submit():
        all_data = form.data
        all_data.pop('csrf_token')
        all_data.pop('submit')
        print(all_data)

        field_names = ["id","equipment", "date_requested", "total_requested"]
        dict = all_data
        with open('ordered.csv', 'a',  newline='', encoding='utf-8') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(dict)
            f_object.close()
        
            
            

    return render_template("add.html", form=form)

@app.route('/submissions', methods=['GET', 'POST'])
def submissions():
    with open("ordered.csv", 'r') as o_file:
        supply_list=[]
    
        reader_obj = csv.reader(o_file)
        for row in reader_obj: 
            supply_list.append(row)
  
  

    return render_template("submissions.html", s_list =supply_list)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    return render_template("delete.html")

