from downloader import Downloader

from datetime import date
import datetime
import csv
import sys

# have to split the csv on use regex \d+,"text"


class FileSystem:

    """The file system where all of the ebooks will be accessed"""

    def __init__(self, downloader) -> None:
        self.downloader = downloader
        # books that can be downloaded
        self.catalog = self.import_catalog()
        # downloaded books sorted by genre

    def import_catalog(self) -> list:
        # check to see if the catalog is outdate
        if FileSystem.validate_cat():
            # if the catalog is outdated pull the updated version from project gutenberg
            self.downloader.download_cat()
        # parse csv into books
        m_books = {}
        try:
            with open("catalog/catalog.csv") as file:
                books_reader = csv.DictReader(file)
                for book in books_reader:
                    m_book = ebook_meta(book)
                    m_books[f"{get_title(m_book)}, {get_author(m_book)}"] = m_book
        except FileNotFoundError:
            sys.exit(1)

        return m_books
           
    # validates the amount of time that has passed 
    # since the current catalog.csv file has been downloaded, updates every week.
    @classmethod
    def validate_cat(cls) -> bool:
        curr_date = date.today()
        file = "catalog/last_catalog_update.txt"
        
        try:
            with open(file) as f:
                old_date = f.read()
        except FileNotFoundError:
            curr_date_str = date.today().strftime("%Y-%m-%d")
            with open(file, "w") as f:
                f.write(curr_date_str)
            return True
    
        # converts the old_date to a date object and validate that the csv is up to date
        old_date = datetime.datetime.strptime(old_date, "%Y-%m-%d").date()
        if (curr_date - datetime.timedelta(days = 7) >= old_date):
            # updates the time since the catalog needs to be redownloaded
            curr_date_str = date.today().strftime("%Y-%m-%d")
            with open(file, "w") as f:
                f.write(curr_date_str)
            return True       
        # catalog is up-to-date
        return False
    
    def get_ebook(self, title: str, author: str):
        book_key = f"{title}, {author}"
        m_book = self.catalog.get(book_key)
        return m_book


def ebook_meta(book: dict) -> dict:   
    m_book = {}
    m_book["ID"] = book["Text#"]
    m_book["Title"] = book["Title"]
    m_book["Authors"] = book["Authors"]
    m_book["Lang"] = book["Language"]
    m_book["Genre"] = book["Bookshelves"]
 
    for meta in m_book:
        if "\n" in m_book[meta]:
            m_book[meta] = m_book[meta].replace("\n", " ")
    
    return m_book 
    
def get_title(book: dict) -> str:
    return book["Title"]

def get_author(book: dict) -> str:
    # edit so you can remove the () in the first name () disambiguates the middle name
    authors = book["Authors"]
    if "," in authors:
        author = book["Authors"].split(", ")
        return f"{author[1]} {author[0]}"
    return authors

def get_book_id(book: dict) -> str:
    return book["ID"]

    

def main():
    downloader = Downloader()
    filesystem = FileSystem(downloader)
    i = 20 

    for book in filesystem.catalog:
        if i == 0:
            break
        print(f"{book}: {filesystem.catalog.get(book)}")
        i -= 1


    


if __name__ == "__main__":
    main()
            

