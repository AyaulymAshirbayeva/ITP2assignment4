# Books API

REST API for managing books using Flask and JSON file storage.

## Project Description

This project is a backend REST API created with Flask.  
The API allows users to create, read, update, delete, and filter book records.  
Data is stored persistently in a JSON file.

---

## Technologies Used

- Python 3
- Flask
- JSON

---

## Installation & Setup

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
python app.py
```

Server URL:

```text
http://127.0.0.1:5000
```

---

## Data Storage

All data is stored in:

```text
books.json
```

Format: JSON array.

Example:

```json
[
    {
        "id": 1,
        "name": "Pride and Prejudice",
        "year": 1813,
        "pages": 434,
        "author": "Jane Austen"
    },
]
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Welcome route |
| GET | /books | Get all books |
| GET | /books/<id> | Get book by ID |
| POST | /books | Create new book |
| PUT | /books/<id> | Update book |
| DELETE | /books/<id> | Delete book |

---

## Example Requests

### POST /books

Request body:

```json
{
    "name": "Atomic Habits",
    "year": 2018,
    "pages": 320,
    "author": "James Clear"
}
```

Success response:

```json
{
    "message": "Book created",
    "book": {
        "id": 1,
        "name": "Atomic Habits",
        "year": 2018,
        "pages": 320,
        "author": "James Clear"
    }
}
```

---

## Filtering

### Filter by author

```text
/books?author=Jane Austen
```

### Filter by year

```text
/books?year=2010
```

### Combined filter

```text
/books?author=Jane Austen&year=1815
```

---

## Author

Name: Ashirbayeva Ayaulym  
Group: SE-2507