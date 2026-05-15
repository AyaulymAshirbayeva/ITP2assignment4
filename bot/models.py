class Book:
    def __init__(self, name, author, year, pages):
        self.name = name
        self.__author = author
        self.year = year
        self.pages = pages

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    def info(self):
        return f"{self.name} by {self.author}"

    def __str__(self):
        return f"Book: {self.name} ({self.year})"


class ClassicBook(Book):
    def __init__(self, name, author, year, pages, genre):
        super().__init__(name, author, year, pages)
        self.genre = genre

    def classic_info(self):
        return f"Classic book: {self.name}, genre: {self.genre}"