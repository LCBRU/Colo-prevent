
import smtplib
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine


password = "" #your email app password 
my_email ="" # type your email from
to_email="" #type your email to 

engine = create_engine("sqlite+pysqlite:///watch.db", echo=True)

conn = engine.connect()

metadata = MetaData() 
m= Table('movie_details', metadata, 
autoload_with=engine) 

metadata = MetaData() 
g= Table('genres', metadata, 
autoload_with=engine) 

#from movies table 

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



email_connection = smtplib.SMTP("smtp.gmail.com", port=587) #change to your email port 
email_connection.starttls()
email_connection.login(user=my_email, password=password)
email_connection.sendmail(from_addr=my_email, to_addrs=to_email, msg = f"Subject: test \n\n The genre of this movie is {movie_search_genre},the title of this movie {movie_search_title} the rating i gave this movie {movie_search_rating}")
email_connection.close()
                          

