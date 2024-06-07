
import smtplib
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, select
from sqlalchemy import create_engine
from dotenv import load_dotenv, dotenv_values
import os
from jinja2 import Environment,FileSystemLoader, Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

password = os.getenv("PASSWORD") 
my_email =os.getenv("MY_EMAIL")
to_email= os.getenv("TO_EMAIL")

engine = create_engine("sqlite+pysqlite:///watch.db", echo=True)

conn = engine.connect()

metadata = MetaData() 
m= Table('movie_details', metadata, autoload_with=engine) 

metadata = MetaData() 
g= Table('genres', metadata, autoload_with=engine) 

#from movies table 

#stmt = select(m).where(m.c.title == "Twister")

query = m.select() 

good_movie = conn.execute(query) 
result = good_movie.fetchall() 


for row in result:
    if row.title =="Megan":
        movie_search_title = row.title
        movie_search_rating = row.rating
        
#from genres table 
        
query = g.select() 

good_movie = conn.execute(query) 
result = good_movie.fetchall() 



for row in result:
    if row.movie_title =="Megan":
        movie_search_genre = row.genre


msg = MIMEMultipart('alternative')
msg['Subject'] = "Test movie"
msg['From'] = my_email
msg['To'] = to_email

env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('template.html')
html = template.render(mt=movie_search_title, mg=movie_search_genre, mr=movie_search_rating)
text = "This is a movie to watch {{ movie_search_title}}, the genre is {{ movie_search_genre}} and the rating i give this is {{movie_search_rating}}"

part1= MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)

email_connection = smtplib.SMTP("smtp.gmail.com", port=587)
email_connection.starttls()
email_connection.login(user=my_email, password=password)
email_connection.sendmail(my_email, to_email, msg.as_string())
email_connection.quit()




