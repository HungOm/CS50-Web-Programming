import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))



def main():
	books =db.execute("SELECT book_id,isbn_id,title,author,year FROM myBooks ORDER BY book_id ASC LIMIT 30").fetchall()
	for book in books:
		print(f"No{book.book_id}.Book name {book.title},  ISBN:{book.isbn_id},  written by {book.author} in {book.year}.")

		#PRINT INPUT
	book_name = input("\nBook_Name/isbn_id: ")
	booksSearch = db.execute("SELECT * FROM myBooks WHERE title =:book_name OR isbn_id=:book_name",{"book_name":book_name}).fetchall()
	for book in booksSearch:
		print(f"Book title:{book.title}, ISBN no.:{book.isbn_id}, Author:{book.author}")

if __name__ == '__main__':
	main()	