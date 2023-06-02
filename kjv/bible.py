from flask import Blueprint

bp = Blueprint("bible", __name__)


@bp.route("/")
def index():
    return "Index page"


@bp.route("/<string:book>/")
def book(book):
    return f"Book: {book} page"


@bp.route("/<string:book>/<int:chapter>/")
def chapter(book, chapter):
    return f"Book: {book} chapter: {chapter} page"
