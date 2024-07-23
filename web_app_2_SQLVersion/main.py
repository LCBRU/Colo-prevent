from flask import Flask,render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,DateField,IntegerField,SubmitField
from wtforms.validators import DataRequired
import os
import csv
from csv import DictWriter
import pandas as pd 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

#create sql tables 

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


#creating forms 

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

#creating config for sql tables

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///colo_prevent.db"
db.init_app(app)

class Ordered(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    equipment: Mapped[str] 
    date_ordered: Mapped[date]
    total_requested: Mapped[str]

with app.app_context():
    db.create_all()

#secret ket for wtforms 

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = RequestForm()
    if form.validate_on_submit():
            new_order =Ordered (
                equipment= form.equipment.data,
                date_ordered = form.date_requested.data,
                total_requested = form.total_requested.data                
                )
            db.session.add(new_order)
            db.session.commit()
    
            return redirect("/submissions")
        
            
            

    return render_template("add.html", form=form)

@app.route('/submissions', methods=['GET', 'POST'])
def submissions():
    ordered = db.session.execute(db.select(Ordered).order_by(Ordered.id)).scalars()
    ordered_list=[]
    for queried in ordered:
        ordered_list.append(queried)

    return render_template("submissions.html", ordered_list=ordered_list)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    delete_id = id
    if id== delete_id:
        query_del = db.session.execute(db.select(Ordered).where(Ordered.id == delete_id)).scalar()
        db.session.delete(query_del)
        db.session.commit()
        return redirect("/submissions")
    return render_template('delete.html', id=id)
    
        

    

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    edit_id = id
    if id== edit_id:
        query_edit = db.session.execute(db.select(Ordered).where(Ordered.id == edit_id)).scalar()
        prev_equip = query_edit.equipment
        prev_total_req = query_edit.total_requested
        prev_date_ordered= query_edit.date_ordered
        ed_form=EditData(equipment=prev_equip,total_requested=prev_total_req, date_requested=prev_date_ordered) 

    
    if ed_form.validate_on_submit():
        
            query_edit.equipment= ed_form.equipment.data
            query_edit.date_ordered = ed_form.date_requested.data
            query_edit.total_requested = ed_form.total_requested.data
            db.session.add(query_edit)
            db.session.commit()
            return redirect("/submissions")
        

    return render_template('edit.html', ed_form = ed_form, id=id)

