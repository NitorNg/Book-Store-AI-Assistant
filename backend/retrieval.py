# retrieval.py
import re
from models import Book, Policy

NO_MATCH = "No matching store information found."

# ---- EDIT THESE to match models.py exactly ----
BOOK_TITLE = "title"
BOOK_AUTHOR = "author"
BOOK_GENRE = "genre"
BOOK_STOCK = "stock"
BOOK_PRICE = "price"        # set to None if Book has no price column
POLICY_TOPIC = "topic"      # e.g. "returns", "shipping"
POLICY_TEXT = "content"     # the 2-3 sentence policy text
# -----------------------------------------------

# Words customers use -> the policy topic they mean
TOPIC_SYNONYMS = {
    "returns": ["return", "refund", "exchange", "send back"],
    "shipping": ["shipping", "delivery", "deliver", "ship", "postage"],
    "hours": ["hours", "open", "opening", "close", "closing", "when are you"],
    "payment": ["payment", "pay", "card", "cash", "credit", "paypal"],
    "gift cards": ["gift card", "gift cards", "voucher", "gift"],
}


def _clean(text):
    return re.sub(r"[^a-z0-9 ]", " ", (text or "").lower())


def _contains(message, phrase):
    """Whole-word / whole-phrase match, so 'ship' doesn't match 'relationship'."""
    phrase = _clean(phrase).strip()
    return bool(phrase) and re.search(rf"\b{re.escape(phrase)}\b", message) is not None


def _book_line(book):
    title = getattr(book, BOOK_TITLE)
    author = getattr(book, BOOK_AUTHOR)
    genre = getattr(book, BOOK_GENRE)
    stock = getattr(book, BOOK_STOCK)
    line = f"Book: {title} by {author} ({genre})"
    if BOOK_PRICE and getattr(book, BOOK_PRICE, None) is not None:
        line += f", ${float(getattr(book, BOOK_PRICE)):.2f}"
    line += f", in stock ({stock} left)" if stock and stock > 0 else ", out of stock"
    return line


def _policy_matches(policy, message):
    topic = getattr(policy, POLICY_TOPIC)
    if _contains(message, topic):
        return True
    for key, words in TOPIC_SYNONYMS.items():
        if key in _clean(topic) or _clean(topic).strip() in key:
            if any(_contains(message, w) for w in words):
                return True
    return False


def find_info(db, message):
    msg = _clean(message)
    lines = []

    for book in db.query(Book).all():
        title = getattr(book, BOOK_TITLE)
        author = getattr(book, BOOK_AUTHOR)
        genre = getattr(book, BOOK_GENRE)
        author_last = _clean(author).split()[-1] if author else ""
        if (_contains(msg, title)
                or _contains(msg, author)
                or _contains(msg, author_last)
                or _contains(msg, genre)):
            lines.append(_book_line(book))

    for policy in db.query(Policy).all():
        if _policy_matches(policy, msg):
            lines.append(
                f"Policy ({getattr(policy, POLICY_TOPIC)}): {getattr(policy, POLICY_TEXT)}"
            )

    return "\n".join(lines) if lines else NO_MATCH
