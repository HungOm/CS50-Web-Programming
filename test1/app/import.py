import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Create new table if table does exists 
def createTable(db):
	db.execute("CREATE TABLE IF NOT EXISTS myBooks(Book_id SERIAL PRIMARY KEY NOT NULL,isbn_id VARCHAR NOT NULL,Title VARCHAR NOT NULL, Author VARCHAR NOT NULL, Year INTEGER NOT NULL,UNIQUE(isbn_id))")
	db.execute("CREATE TABLE IF NOT EXISTS users(User_id SERIAL PRIMARY KEY NOT NULL,username VARCHAR NOT NULL, email VARCHAR NOT NULL, password VARCHAR NOT NULL,UNIQUE(username,email))")
	db.execute("CREATE TABLE IF NOT EXISTS flights(flisht_id SERIAL PRIMARY KEY NOT NULL, origin VARCHAR NOT NULL,destination VARCHAR NOT NULL, duration INTEGER NOT NULL)")
	db.execute("CREATE TABLE IF NOT EXISTS users2(id SERIAL PRIMARY KEY NOT NULL,username VARCHAR UNIQUE NOT NULL, email VARCHAR UNIQUE NOT NULL,password VARCHAR UNIQUE NOT NULL)")

# open csv and add into database
def main():
	createTable(db)

	# import csv data from source files
	# f = open("books.csv")
	# reader = csv.reader(f)
	# headers = next(reader) #this loop ignore files line of CSV which is header.
	# for isbnID,title,author,year in reader:
		
		
	# 	# add into data base
	# 	db.execute("INSERT INTO myBooks(isbn_id,Title, Author, Year) VALUES(:isbn_id, :Title, :Author, :Year)",
 # #                    {"isbn_id":isbnID,"Title":title, "Author":author, "Year":year})
	# # 	print(f"Added a book named {title} with ISBN:{isbnID} written by {author} in {year}.")
	# f = open("flights.csv")
	# reader = csv.reader(f)
	# for origin, destination, duration in reader:
	# 	db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
 #                    {"origin": origin, "destination": destination, "duration": duration})
	# 	print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
	db.commit()
	# BookList = db.execute("SELECT * FROM Books WHERE Book_id>4)")
	# print(BookList)

if __name__ == "__main__":
    main()
