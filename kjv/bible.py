from flask import Blueprint

bp = Blueprint("bible", __name__)

from kjv.db import get_db


@bp.route("/")
def index():
    return "Index page"


@bp.route("/<string:book>/")
def book(book):
    return f"Book: {book} page"


@bp.route("/<string:book>/<int:chapter>/")
def chapter(book, chapter):
    # Get verse from database
    db = get_db()
    verse = db.execute(
        "SELECT t from kjv WHERE b = ? AND c = ? AND v = ?", (1, 1, 1)
    ).fetchone()
    return f"Book: {book} chapter: {chapter} verse: {verse[0]}"
