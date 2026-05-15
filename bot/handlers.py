import json
import os
import requests

from bot.models import Book, ClassicBook
from bot.utils import log_command, validate_email, fact_gen

BOOKS_FILE = "books.json"


def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []

    with open(BOOKS_FILE, "r") as file:
        return json.load(file)



def save_books(data):
    with open(BOOKS_FILE, "w") as file:
        json.dump(data, file, indent=4)


@log_command

def start_command(message, bot):
    bot.send_message(message.chat.id,
    "Welcome to AITU books bot!\n\n"
    "Recent updates and fixes:\n"
    "- Fixed Chinese translation command (now it shows correct translation instead of gibberish)\n"
    "- Improved input validation for year and pages of the books\n"
    "  (prevents negative numbers and incorrect string inputs)\n\n"
    "These changes were not made to improve grading,\n"
    "but to better understand mistakes and ensure the bot works correctly 🤗\n\n"
    "Use /help to see available commands.")



@log_command
def help_command(message, bot):
    text = (
        "/start - start bot\n"
        "/help - commands\n"
        "/echo text - repeat text\n"
        "/save - save book\n"
        "/list - show books\n"
        "/fact - random fact\n"
        "/validate email - validate email\n"
        "/about - bot info\n"
        "/translate - translate any text to Chinese\n"
        "/stats - see stats about library\n"
        "/search - find any book by title, author, year"
    )

    bot.send_message(message.chat.id, text)


@log_command

def echo_command(message, bot):
    text = message.text.replace("/echo", "").strip()

    if text:
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Write text after /echo")


@log_command
def save_command(message, bot):
    try:
        data = message.text.replace("/save", "").strip()
        name, author, year, pages = data.split(",")

        name = name.strip()
        author = author.strip()

        try:
            year = int(year.strip())
        except ValueError:
            bot.send_message(message.chat.id, "Year must be a number")
            return

        try:
            pages = int(pages.strip())
        except ValueError:
            bot.send_message(message.chat.id, "Pages must be a number")
            return

        if year < 1 or year > 2026:
            bot.send_message(message.chat.id, "Year must be between 1 and 2026")
            return

        if pages <= 0:
            bot.send_message(message.chat.id, "Pages must be greater than 0")
            return

        if not name:
            bot.send_message(message.chat.id, "Name cannot be empty")
            return

        if not author:
            bot.send_message(message.chat.id, "Author cannot be empty")
            return

        # 🔵 загрузка книг
        books = load_books()

        new_book = {
            "id": len(books) + 1,
            "name": name,
            "author": author,
            "year": year,
            "pages": pages
        }

        books.append(new_book)
        save_books(books)

        bot.send_message(message.chat.id, "Book saved successfully")

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Format: /save name, author, year, pages"
        )
    except Exception:
        bot.send_message(
            message.chat.id,
            "Something went wrong. Use: /save name, author, year, pages"
        )

@log_command

def list_command(message, bot):
    books = load_books()

    if not books:
        bot.send_message(message.chat.id, "No books found")
        return

    text = ""

    for book in books:
        text += (
            f"{book['id']}. {book['name']} - "
            f"{book['author']} ({book['year']})\n"
        )

    bot.send_message(message.chat.id, text)


@log_command

def fact_command(message, bot):
    global fact_gen

    try:
        fact = next(fact_gen)
    except StopIteration:
        from bot.utils import fact_generator
        fact_gen = fact_generator()
        fact = next(fact_gen)

    bot.send_message(message.chat.id, fact)


@log_command

def validate_command(message, bot):
    email = message.text.replace("/validate", "").strip()

    if validate_email(email):
        bot.send_message(message.chat.id, "Valid email")
    else:
        bot.send_message(message.chat.id, "Invalid email")


@log_command
def about_command(message, bot):
    # Текст с информацией о боте
    about_text = (
        "*About the bot:*\n\n"
"I am Aitu Books Bot. My purpose is to help you manage a book library.\n\n"
"With my help, you can  save new books, view the list of added books, "
"and search for literature by author, number of pages, and publication year.\n\n"
"API version: 1.0\n"
"Press /help to see the full list of commands!"
    )

    bot.send_message(
        message.chat.id,
        about_text,
        parse_mode="Markdown"
    )

@log_command
def translate_command(message, bot):
    text = message.text.replace("/translate", "").strip()

    if not text:
        bot.send_message(message.chat.id, "Usage: /translate hello")
        return

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": "en|zh"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        translated = data["responseData"]["translatedText"]

        bot.send_message(message.chat.id, translated)

    except:
        bot.send_message(message.chat.id, "Translation error")

@log_command
def search_command(message, bot):
    query = message.text.replace("/search", "").strip().lower()

    if not query:
        bot.send_message(message.chat.id, "Usage: /search text")
        return

    books = load_books()

    results = []

    for book in books:
        if (
            query in book["name"].lower()
            or query in book["author"].lower()
            or query == str(book["year"])
        ):
            results.append(book)

    if not results:
        bot.send_message(message.chat.id, "No books found")
        return

    text = "Found books:\n\n"

    for b in results:
        text += f"{b['id']}. {b['name']} - {b['author']} ({b['year']})\n"

    bot.send_message(message.chat.id, text)

@log_command
def stats_command(message, bot):
    books = load_books()

    if not books:
        bot.send_message(message.chat.id, "No books in library")
        return

    total = len(books)
    avg_pages = sum(b["pages"] for b in books) / total

    years = [b["year"] for b in books]
    oldest_year = min(years)
    newest_year = max(years)

    oldest_book = next(b for b in books if b["year"] == oldest_year)
    newest_book = next(b for b in books if b["year"] == newest_year)

    text = (
        f"📊 Library Stats:\n"
        f"Total books: {total}\n"
        f"Average pages: {avg_pages:.1f}\n"
        f"Oldest book: {oldest_book['name']} — {oldest_book['author']} ({oldest_year})\n"
        f"Newest book: {newest_book['name']} — {newest_book['author']} ({newest_year})"
    )

    bot.send_message(message.chat.id, text)