import json


class Book:
    def __init__(self, title, author, status="Available"):
        self.title = title
        self.author = author
        self.status = status

    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nStatus: {self.status}"


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)
        book.status = "Borrowed"
        print(f"{self.name} borrowed '{book.title}' successfully.")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.status = "Available"
            print(f"{self.name} returned '{book.title}' successfully.")
        else:
            print(f"{self.name} does not have '{book.title}'.")

    def display_borrowed_books(self):
        if self.borrowed_books:
            print(f"{self.name}'s borrowed books:")
            for book in self.borrowed_books:
                print(book)
                print("-" * 20)
        else:
            print(f"{self.name} has not borrowed any books.")


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)
        print("Book added successfully.")

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print("Book removed successfully.")
        else:
            print("Book not found in the library.")

    def display_books(self):
        if self.books:
            for book in self.books:
                print(book)
                print("-" * 20)
        else:
            print("No books in the library.")

    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                print(book)
                return
        print("Book not found in the library.")

    def add_user(self, user):
        self.users.append(user)
        print(f"User '{user.name}' added successfully.")

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
            print(f"User '{user.name}' removed successfully.")
        else:
            print("User not found.")

    def display_users(self):
        if self.users:
            for user in self.users:
                print(f"User: {user.name}")
                user.display_borrowed_books()
                print("-" * 20)
        else:
            print("No users in the library.")

    def borrow_book(self, user, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                if book.status == "Available":
                    user.borrow_book(book)
                    return
                else:
                    print("Book is already borrowed.")
                    return
        print("Book not found in the library.")

    def return_book(self, user, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                user.return_book(book)
                return
        print("Book not found in the library.")

    def save_library_data(self, filename):
        data = {
            "books": [
                {
                    "title": book.title,
                    "author": book.author,
                    "status": book.status
                }
                for book in self.books
            ],
            "users": [
                {
                    "name": user.name,
                    "borrowed_books": [book.title for book in user.borrowed_books]
                }
                for user in self.users
            ]
        }
        with open(filename, "w") as file:
            json.dump(data, file)
        print("Library data saved successfully.")

    def load_library_data(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.books = [
                    Book(book["title"], book["author"], book["status"])
                    for book in data["books"]
                ]
                self.users = [
                    User(user["name"])
                    for user in data["users"]
                ]
                for user, user_data in zip(self.users, data["users"]):
                    user.borrowed_books = [
                        book
                        for book in self.books
                        if book.title in user_data["borrowed_books"]
                    ]
            print("Library data loaded successfully.")
        except FileNotFoundError:
            print("Library data file not found.")

# Example usage
library = Library()

book1 = Book("Python Crash Course", "Eric Matthes")
book2 = Book("The Pragmatic Programmer", "Andrew Hunt and David Thomas")
book3 = Book("Clean Code", "Robert C. Martin")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

user1 = User("Aryan")
user2 = User("Abhishek")
user3 = User("Shubham")

library.add_user(user1)
library.add_user(user2)
library.add_user(user3)

library.borrow_book(user1, "Python Crash Course")
library.borrow_book(user2, "The Pragmatic Programmer")
library.borrow_book(user3, "Clean Code")

library.display_users()

library.return_book(user1, "Python Crash Course")

library.save_library_data("library_data.json")

library2 = Library()
library2.load_library_data("library_data.json")

library2.display_users()
