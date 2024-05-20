from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, insert,select


metadata_obj = MetaData()

movies_table = Table("movie_details",
                     metadata_obj,
                     Column("year_released", Integer, primary_key=True),
                     Column("title", String),
                     Column("rating", Integer),
)

genre_table = Table("genres",
                    metadata_obj,
                    Column("year_released", Integer, primary_key=True),
                    Column("movie_title", ForeignKey("movie_details.title"), nullable=False),
                    Column("genre", String, nullable=False),
)

engine = create_engine("sqlite+pysqlite:///watch.db", echo=True)

metadata_obj.create_all(engine)



print("***********************************************************************************")



movies_to_add_1=[
    (2023,"Megan",8),
    (1996,"Twister",6),
    (1988,"Beetlejuice",8),
    (2016, "Rogue One",2), 
    (1997,"The Fifth Element",9),
    (2014,"Last shift", 8)]
                                

stmt = insert(movies_table).values( 
    [{'year_released':  year_released, 'title': title, 'rating': rating} for year_released, title, rating in movies_to_add_1]) 

with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()


print("*******************************************************************************")

stmt = select(movies_table).where(movies_table.c.title == "Megan")

print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

stmt = select(movies_table).where(movies_table.c.title == "Twister")

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

print("*******************************************************************")



genre_to_add_1=[
    (2023,"Megan", "scifi"),
    (1996,"Twister", "Action"),
    (1988,"Beetlejuice","Comedy-Horror"),
    (2016, "Rogue One","Scifi"), 
    (1997,"The Fifth Element","Scifi"),
    (2014,"Last shift","Horror")]

stmt = insert(genre_table).values([{"year_released": year_released, "movie_title":movie_title,"genre":genre} for year_released, movie_title, genre in genre_to_add_1])

with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()

stmt = select(genre_table).where(genre_table.c.movie_title =="Megan")

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)
