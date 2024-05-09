import sqlite3
import smtplib

password = "" #your email app password 
my_email ="" # type your email from
to_email="" #type your email to 

connection = sqlite3.connect("movies.db")

cursor = connection.cursor()

cursor.execute("create table movie_review(year_released integer, title text, rating_out_of_10 integer)")

movie_list =[(2007, "1408", 8),
             (1984, "1984", 7),
             (1988, "Beetlejuice", 8),
             (2016, "Rogue One", 2),
             (1997,"The Fifth Element", 9),
             (2000, "Chicken Run", 7),
             ]


cursor.executemany("insert into movie_review values(?,?,?)", movie_list)

#printing rows in table

for row in cursor.execute("select * from movie_review"):
    print(row)


print("**************************")
#extracting specific rows

cursor.execute("select * from movie_review where title=:t", {"t":"Rogue One"})
movie_search = cursor.fetchall()
print(movie_search)

#creating second table 

cursor.execute("create table genres (title text, genre text)")

movie_genre =[("1408", "Horror"),
             ("1984", "Dystopian"),
             ("Beetlejuice", "Horror-Comedy"),
             ("Rogue One", "Fantasy"),
             ("The Fifth Element", "Sci-Fi"),
             ("Chicken Run", "Comedy"),
             ]

cursor.executemany("insert into genres values(?,?)", movie_genre)

cursor.execute("select * from genres where title=:t", {"t":"1408"})
genre_search = cursor.fetchall()
print(genre_search)

email_connection = smtplib.SMTP("smtp.gmail.com", port=587) #change to your email port 
email_connection.starttls()
email_connection.login(user=my_email, password=password)
email_connection.sendmail(from_addr=my_email, to_addrs=to_email, msg = f"Subject: test \n\n Watch this {genre_search}, not this {movie_search}")
email_connection.close()
                          

connection.close()