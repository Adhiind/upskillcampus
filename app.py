from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse
import secrets, string, os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-development-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ALPHABET = string.ascii_letters + string.digits

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    click_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())

def is_valid_url(value):
    if not value: return False
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc) and "." in parsed.netloc
    except ValueError:
        return False

def create_mapping(original_url):
    for _ in range(10):
        code = "".join(secrets.choice(ALPHABET) for _ in range(6))
        db.session.add(URLMapping(original_url=original_url, short_code=code))
        try:
            db.session.commit()
            return code
        except IntegrityError:
            db.session.rollback()
    raise RuntimeError("Could not create a unique code. Please try again.")

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        original_url = request.form.get("url", "").strip()
        if not is_valid_url(original_url):
            flash("Enter a valid URL beginning with http:// or https://.", "error")
        else:
            try:
                code = create_mapping(original_url)
                short_url = url_for("visit", code=code, _external=True)
                flash("Your short link is ready.", "success")
            except RuntimeError as exc:
                flash(str(exc), "error")
    recent = URLMapping.query.order_by(URLMapping.created_at.desc()).limit(10).all()
    return render_template("index.html", short_url=short_url, recent_urls=recent)

@app.route("/<code>")
def visit(code):
    item = URLMapping.query.filter_by(short_code=code).first_or_404()
    item.click_count += 1
    db.session.commit()
    return redirect(item.original_url, code=302)

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
