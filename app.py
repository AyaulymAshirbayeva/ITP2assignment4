import time

from flask import Flask, request, jsonify, Config
import json
import os
import telebot
import config

from bot.handlers import (
    start_command,
    help_command,
    echo_command,
    save_command,
    list_command,
    fact_command,
    validate_command,
    about_command,
    search_command,
    translate_command,
    stats_command
)

app = Flask(__name__)

bot = telebot.TeleBot(config.BOT_TOKEN)

FILE_NAME = "books.json"

def load_books():

    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:

        try:
            return json.load(file)

        except:
            return []


def save_books(books):

    with open(FILE_NAME, "w") as file:
        json.dump(books, file, indent=4)


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Telegram Books Bot API",
        "status": "running"
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    print("HIT")

    json_data = request.get_json()
    print(json_data)
    update = telebot.types.Update.de_json(json_data)

    if update.message:

        message = update.message
        text = message.text

        if text.startswith("/start"):
            start_command(message, bot)

        elif text.startswith("/help"):
            help_command(message, bot)

        elif text.startswith("/echo"):
            echo_command(message, bot)

        elif text.startswith("/save"):
            save_command(message, bot)

        elif text.startswith("/list"):
            list_command(message, bot)

        elif text.startswith("/fact"):
            fact_command(message, bot)

        elif text.startswith("/validate"):
            validate_command(message, bot)

        elif text.startswith("/about"):
            about_command(message, bot)

        elif text.startswith("/search"):
            search_command(message, bot)

        elif text.startswith("/translate"):
            translate_command(message, bot)

        elif text.startswith("/stats"):
            stats_command(message, bot)

    return "OK", 200

@app.route("/books", methods=["GET"])
def get_books():

    books = load_books()

    author = request.args.get("author")
    min_pages = request.args.get("min_pages")
    year = request.args.get("year")
    sort = request.args.get("sort")

    if year:

        if not year.isdigit():
            return jsonify({
                "error": "Year must be a number"
            }), 400

        books = [
            b for b in books
            if b["year"] == int(year)
        ]

    if author:

        books = [
            b for b in books
            if b["author"].lower() == author.lower()
        ]

    if min_pages:

        if not min_pages.isdigit():
            return jsonify({
                "error": "min_pages must be a number"
            }), 400

        books = [
            b for b in books
            if b["pages"] >= int(min_pages)
        ]

    if sort == "year":
        books.sort(key=lambda x: x["year"])

    return jsonify({
        "books": books
    }), 200

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    books = load_books()

    for book in books:

        if book["id"] == book_id:
            return jsonify(book), 200

    return jsonify({
        "error": f"Book with id {book_id} not found"
    }), 404


@app.route("/books", methods=["POST"])
def create_book():

    data = request.get_json()

    required_fields = [
        "name",
        "year",
        "pages",
        "author"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    if not isinstance(data["year"], int):
        return jsonify({
            "error": "Year must be an integer"
        }), 400

    if data["year"] < 1 or data["year"] > 2026:
        return jsonify({
            "error": "Year must be between 1 and 2026"
        }), 400

    if not isinstance(data["pages"], int):
        return jsonify({
            "error": "Pages must be an integer"
        }), 400

    if data["pages"] <= 0:
        return jsonify({
            "error": "Pages must be greater than 0"
        }), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({
            "error": "Name must be a non-empty string"
        }), 400

    if not isinstance(data["author"], str) or not data["author"].strip():
        return jsonify({
            "error": "Author must be a non-empty string"
        }), 400

    books = load_books()

    new_id = 1

    if books:
        new_id = max(book["id"] for book in books) + 1

    new_book = {
        "id": new_id,
        "name": data["name"],
        "year": data["year"],
        "pages": data["pages"],
        "author": data["author"]
    }

    books.append(new_book)

    save_books(books)

    return jsonify({
        "message": "Book created",
        "book": new_book
    }), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):

    books = load_books()

    for book in books:

        if book["id"] == book_id:

            data = request.get_json()

            if "name" in data:

                if not isinstance(data["name"], str) or not data["name"].strip():
                    return jsonify({
                        "error": "Name must be a non-empty string"
                    }), 400

                book["name"] = data["name"]

            if "year" in data:

                if not isinstance(data["year"], int):
                    return jsonify({
                        "error": "Year must be an integer"
                    }), 400

                if data["year"] < 1 or data["year"] > 2026:
                    return jsonify({
                        "error": "Year must be between 1 and 2026"
                    }), 400

                book["year"] = data["year"]

            if "pages" in data:

                if not isinstance(data["pages"], int):
                    return jsonify({
                        "error": "Pages must be an integer"
                    }), 400

                if data["pages"] <= 0:
                    return jsonify({
                        "error": "Pages must be greater than 0"
                    }), 400

                book["pages"] = data["pages"]

            if "author" in data:

                if not isinstance(data["author"], str) or not data["author"].strip():
                    return jsonify({
                        "error": "Author must be a non-empty string"
                    }), 400

                book["author"] = data["author"]

            save_books(books)

            return jsonify({
                "message": "Book updated",
                "book": book
            }), 200

    return jsonify({
        "error": f"Book with id {book_id} not found"
    }), 404


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    books = load_books()

    for book in books:

        if book["id"] == book_id:

            books.remove(book)

            save_books(books)

            return jsonify({
                "message": f"Book with id {book_id} deleted successfully"
            }), 200

    return jsonify({
        "error": f"Book with id {book_id} not found"
    }), 404

if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(2)
    bot.set_webhook(url=config.WEBHOOK_URL)

    app.run(debug=True, port=5003)
