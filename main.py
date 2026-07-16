import json

class LibraryItem:
    def __init__(self, id, title, author, release_date, available):
        self.id = id
        self.title = title
        self.author = author
        self.release_date = release_date
        self.__available = available

    def take_book(self):
        self.__available = False

    def return_book(self):
        self.__available = True

    def is_available(self):
        return self.__available

    def info(self):
        return ""


class Book(LibraryItem):
    def __init__(self, id, title, author, release_date, available, ISBN, pages):
        super().__init__(id, title, author, release_date, available)
        self.ISBN = ISBN
        self.pages = pages


    def info(self):
        return f"id:{self.id}\ntitle:{self.title}\nrelease date:{self.release_date}\navailable:{self.is_available()}\nISBN:{self.ISBN}\npages:{self.pages}\n"


class Ebook(LibraryItem):
    def __init__(self, id, title, author, release_date, available, format, size):
        super().__init__(id, title, author, release_date, available)
        self.format = format
        self.size = size

    def take_book(self):
        pass

    def info(self):
        return f"id:{self.id}\ntitle:{self.title}\nrelease date:{self.release_date}\navailable:{self.is_available()}\nformat:{self.format}\nsize:{self.size}\n"


class Reader:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.books = []

    def info(self):
        return f"id:{self.id}\nname:{self.name}\nbooks:{[str(book.title) for book in self.books]}\n"

    def get_book(self, book):
        if not book.is_available():
            print("Error: the book is not available")
            return False

        if len(self.books) >= 3:
            print("Error: the reader already has 3 books")
            return False

        self.books.append(book)
        print("The reader has gotten the book")
        return True

    def return_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print("the book was successfully returned")
            return True

        print("Error: the reader does not have this book")
        return False


class Library:
    def __init__(self, books, readers):
        self.books = books
        self.readers = readers

    def add_book(self, id, title, author, release_date, available, ISBN, pages):
        self.books.append(Book(id, title, author, release_date, available, ISBN, pages))
        print ("the book was successfully added")

    def add_ebook(self, id, title, author, release_date, available, format, size):
        self.books.append(Ebook(id, title, author, release_date, available, format, size))
        print("the ebook was successfully added")

    def show_inventory(self):
        print("books:")
        for book in self.books:
            print(book.title)

    def find_by_title(self, title):
       return [book for book in self.books if book.title == title]

    def sort_by_title(self):
        self.books = sorted(self.books, key=lambda x: x.title)
        print("The books were sorted by title")

    def sort_by_release_date(self):
        self.books = sorted(self.books, key=lambda x: x.release_date)
        print("The books were sorted by release date")

    def add_reader(self, id, name):
        self.readers.append(Reader(int(id), name))
        print("the reader was successfully added")

    def reader_info(self):
        for reader in self.readers:
            print(reader.info())

    def book_info(self):
        for book in self.books:
            print(book.info())


    def find_reader_by_ID(self, id):
        return [reader for reader in self.readers if reader.id == id]

    def take_book(self, reader_id, book_title):
        reader = self.find_reader_by_ID(int(reader_id))[0]
        book = self.find_by_title(book_title)[0]
        if reader.get_book(book):
            book.take_book()

    def return_book(self, reader_id, book_title):
        reader = self.find_reader_by_ID(reader_id)[0]
        book = self.find_by_title(book_title)[0]
        if reader.return_book(book):
            book.return_book()

    def show_taken(self):
        for book in self.books:
            if not (book.is_available()):
                print(book.info())

    def save_to_json(self, filename):
        data = {
            "books": [],
            "readers": []
        }

        for book in self.books:

            if isinstance(book, Book):
                data["books"].append({
                    "type": "book",
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "release_date": book.release_date,
                    "available": book.is_available(),
                    "ISBN": book.ISBN,
                    "pages": book.pages
                })

            elif isinstance(book, Ebook):
                data["books"].append({
                    "type": "ebook",
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "release_date": book.release_date,
                    "available": book.is_available(),
                    "format": book.format,
                    "size": book.size
                })

        data["readers"] = [
            {
                "id": reader.id,
                "name": reader.name,
                "books": [book.id for book in reader.books]
            }
            for reader in self.readers
        ]

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Library saved successfully")

    def load_from_json(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        self.books.clear()
        self.readers.clear()

        for book_data in data["books"]:

            if book_data["type"] == "book":
                self.books.append(
                    Book(
                        book_data["id"],
                        book_data["title"],
                        book_data["author"],
                        book_data["release_date"],
                        book_data["available"],
                        book_data["ISBN"],
                        book_data["pages"]
                    )
                )

            elif book_data["type"] == "ebook":
                self.books.append(
                    Ebook(
                        book_data["id"],
                        book_data["title"],
                        book_data["author"],
                        book_data["release_date"],
                        book_data["available"],
                        book_data["format"],
                        book_data["size"]
                    )
                )

        for reader_data in data["readers"]:
            reader = Reader(
                reader_data["id"],
                reader_data["name"]
            )

            for book_id in reader_data["books"]:
                for book in self.books:
                    if book.id == book_id:
                        reader.books.append(book)

            self.readers.append(reader)

        print("Library loaded successfully")


list_of_books = []
list_of_readers = []
library = Library(list_of_books, list_of_readers)
library.load_from_json("library.json")


print("____________________________________\n.                                  .\n.                                  .\n.                                  .\n.   ░█░░░▀█▀░█▀▄░█▀▄░█▀█░█▀▄░█░█   .\n.   ░█░░░░█░░█▀▄░█▀▄░█▀█░█▀▄░░█░   .\n.   ░▀▀▀░▀▀▀░▀▀░░▀░▀░▀░▀░▀░▀░░▀░   .\n.                                  .\n.                                  .\n.                                  .\n____________________________________")


user_input = -1

while user_input !=0:
    print("""
    choose function:
    1.add
    2.show info
    3.sort books
    4.take book
    5.return books
    0.exit program
    """)
    user_input = input("Enter your choice: ")
    if user_input == "1":
        print("""
        1.add book
        2.add ebook
        3.add reader
              """)
        user_input = input("Enter your choice: ")
        if user_input == "1":
            book = input("Enter book's details(id,title,author,release_date,ISBN,pages): ").split(',')
            library.add_book(int(book[0]), book[1], book[2], book[3], True, book[4],int(book[5]))
        elif user_input == "2":
            ebook = input("Enter ebook's details(id,title,author,release_date,format,size): ").split(',')
            library.add_ebook(int(ebook[0]), ebook[1], ebook[2], ebook[3], True, ebook[4], ebook[5])
        elif user_input == "3":
            reader = input("Enter reader's details(id,name): ").split(',')
            library.add_reader(int(reader[0]), reader[1])
        else: print("No such command")

    elif user_input == "2":
        print("""
        1.inventory
        2.reader
        3.books
        """)
        user_input = input("Enter your choice: ")
        if user_input == "1":
            library.show_inventory()
        elif user_input == "2":
            library.reader_info()
        elif user_input == "3":
            library.book_info()

    elif user_input == "3":
        library.sort_by_title()

    elif user_input == "4":
        reader_id = input("Enter reader's ID: ")
        title = input("Enter book's title: ")
        library.take_book(reader_id, title)

    elif user_input == "5":
        reader_id = input("Enter reader's ID: ")
        title = input("Enter book's title: ")
        library.return_book(reader_id, title)
    elif user_input == "0":
        break
    else:
        print("No such command")

library.save_to_json("library.json")



