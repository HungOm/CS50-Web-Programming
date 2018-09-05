import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	db.execute("CREATE TABLE IF NOT EXISTS Books(ISBN, Title, Author, Year)")
	db.commit()
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title, author, publish_year in reader:
        db.execute("INSERT INTO Books(ISBN,Title, Author, Year) VALUES (:ISBN,:Title, :Author :Year)",
                    {"ISBN":isbn,"Title":title, "Author":author, "Year":publish_year})
        print(f"Added a book name {Title} with '\'ISBN:\'{ISBN} written by {Author} in {duration}.")
    db.commit()

if __name__ == "__main__":
    main()
