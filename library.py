"""The main face of the application where all of the classes will interact."""

import file_system
import downloader

class Library:
    """A representation of library that contains downloaded ebooks"""
    def __init__(self) -> None:
        self.downloaded_ebooks = self.load_ebooks()

    def load_ebooks(self) -> dict:        
        return {}

    def start(self) -> None:
        
        while True:

            functionality = int(input("Press 1 to open the download manager, or 2 to read your ebooks: "))

            if functionality == 1:
                self.downloadUI()
            elif functionality == 2:
                self.ereaderUI()
            elif functionality == 0:
                break
    
    def is_downloaded(self, book: "Ebook") -> bool:
        return f"{book.title}, {book.author}" in self.downloaded_ebooks

    def downloadUI(self) -> None:
        title = input("Enter the title of the book: ")
        author = input("Enter the books author: ")

        book = Ebook(title, author)
        if self.is_downloaded(book):
            print(f"{title} book is downloaded, you can read it with option 2.")
            return
        
        f_system = file_system.FileSystem(downloader.Downloader())
        # returns dict of book information         
        m_book = f_system.get_ebook(book.title, book.author)
        print(m_book)
        if m_book:
            Ebook.construct_ebook(m_book, book)
            self.downloaded_ebooks[f"{book.title}, {book.author}"] = book

        #do something if the book wasn't in the catalog


        
    def ereaderUI(self) -> None:
        return
    

class Ebook:

    def __init__(self, title, author) -> None:
        self.book_id = None
        self.title = title
        self.author = author
        self.lang = None
        self.file_path = None
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Ebook):
            return False
        
        return value.author == self.author and value.title == self.title
    
    @classmethod
    def construct_ebook(cls, m_book: dict, book: "Ebook") -> None:
        ...



def main():
    lib = Library()
    lib.downloadUI()



if __name__ == "__main__":
    main()
