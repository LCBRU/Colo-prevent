from flask import Flask,render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField,DateField,IntegerField,SubmitField
from wtforms.validators import DataRequired
import os
import csv
from csv import DictWriter
import pandas as pd 



class RequestForm(FlaskForm):
    equipment = StringField('Equipment', validators=[DataRequired()])
    total_requested =IntegerField('Total requested', validators=[DataRequired()])
    date_requested =DateField('Date requested', validators=[DataRequired()])
    submit=SubmitField('Request')

class DeleteData(FlaskForm):
    submit = SubmitField('Delete')

class EditData(FlaskForm):
    equipment = StringField('Equipment', validators=[DataRequired()])
    total_requested =IntegerField('Total requested', validators=[DataRequired()])
    date_requested =DateField('Date requested', validators=[DataRequired()])
    submit = SubmitField('Edit')


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

        field_names = ["equipment", "date_requested", "total_requested"]
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

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    del_form = DeleteData()

    if del_form.validate_on_submit():
        row_id= id
        data = pd.read_csv("ordered.csv")
        data.drop(data.index[row_id], inplace=True)
        data.reset_index(drop=True, inplace=True)
        data.to_csv('ordered.csv', index=False)


        print (data)
    

    
    return render_template("delete.html", del_form=del_form, id=id)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    ed_form=EditData()
    edit_eqipment = ed_form.equipment.data
    edit_date_req  = ed_form.date_requested .data
    edit_total_req = ed_form.total_requested.data
    
    if ed_form.validate_on_submit():
        edit_data = pd.read_csv("ordered.csv")
        edit_data.at[id,'Equipment']=edit_eqipment
        edit_data.at[id,'Date ordered']=edit_date_req
        edit_data.at[id,'Total requested']=edit_total_req
        edit_data.reset_index(drop=True, inplace=True)
        edit_data.to_csv('ordered.csv', index=False)
        print(edit_data)
        

    return render_template('edit.html', ed_form = ed_form, id=id)

