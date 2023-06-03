from flask import Blueprint, render_template

from werkzeug.exceptions import abort

bp = Blueprint("bible", __name__)

from kjv.db import get_db

from .meta import old_testament, new_testament


def get_book_meta_data(book):
    target = old_testament.get(book)
    if target is not None:
        return target

    target = new_testament.get(book)
    if target is not None:
        return target

    # At this point, target is None and view will have to handle error
    return target


@bp.route("/")
def index():
    return render_template(
        "bible/index.html", old_testament=old_testament, new_testament=new_testament
    )


@bp.route("/<string:book>/")
def book(book):
    target = get_book_meta_data(book)
    if target is not None:
        return render_template("bible/book.html", book=target)

    if target is None:
        abort(404, f"Book: {book} does not exist.")


@bp.route("/<string:book>/<int:chapter>/")
def chapter(book, chapter):
    target = get_book_meta_data(book)

    if target is None:
        abort(404, f"Book: {book} does not exist.")

    # Check if chapter parameter is valid
    if chapter < 1 or chapter > target.get("chapters"):
        abort(404, f"Chapter: {chapter} not in book: {book}")

    # Get verses from database
    db = get_db()
    verses = db.execute(
        "SELECT * from kjv WHERE b = ? AND c = ?", (target.get("book_no"), chapter)
    ).fetchall()

    if target is not None:
        return render_template(
            "bible/chapter.html", book=target, chapter=chapter, verses=verses
        )
