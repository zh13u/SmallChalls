from flask import Flask, render_template, request, redirect, url_for, send_file, abort, flash, session
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_ROOT = os.path.join(BASE_DIR, "uploads")
USERS_FILE = os.path.join(BASE_DIR, "users.json")

ALLOWED_EXT = {"txt", "png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_ROOT, exist_ok=True)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def create_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": generate_password_hash(password)
    }
    save_users(users)
    user_dir = os.path.join(UPLOAD_ROOT, username)
    os.makedirs(user_dir, exist_ok=True)
    return True

def verify_user(username, password):
    users = load_users()
    if username not in users:
        return False
    return check_password_hash(users[username]["password"], password)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def allowed_ext(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in ALLOWED_EXT

@app.route("/")
@login_required
def index():
    username = session["username"]
    user_dir = os.path.join(UPLOAD_ROOT, username)
    files = sorted(os.listdir(user_dir))
    return render_template("index.html", files=files, username=username)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password required", "error")
            return redirect(url_for("register"))
        if "/" in username or "\\" in username:
            flash("Invalid username", "error")
            return redirect(url_for("register"))
        ok = create_user(username, password)
        if not ok:
            flash("Username already exists", "error")
            return redirect(url_for("register"))
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if verify_user(username, password):
            session["username"] = username
            flash("Logged in as " + username, "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out", "success")
    return redirect(url_for("login"))

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        f = request.files.get("file")
        if not f or f.filename == "":
            flash("No file selected", "error")
            return redirect(url_for("upload"))
        filename = secure_filename(f.filename)
        if not allowed_ext(filename):
            flash("Extension not allowed", "error")
            return redirect(url_for("upload"))
        user_dir = os.path.join(UPLOAD_ROOT, session["username"])
        os.makedirs(user_dir, exist_ok=True)
        path = os.path.join(user_dir, filename)
        f.save(path)
        flash("Uploaded: " + filename, "success")
        return redirect(url_for("index"))
    return render_template("upload.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        content = request.form.get("content", "")
        if not name:
            flash("Name required", "error")
            return redirect(url_for("create"))
        filename = secure_filename(name)
        if "." not in filename:
            filename = filename + ".txt"
        if not allowed_ext(filename):
            flash("Extension not allowed", "error")
            return redirect(url_for("create"))
        user_dir = os.path.join(UPLOAD_ROOT, session["username"])
        os.makedirs(user_dir, exist_ok=True)
        path = os.path.join(user_dir, filename)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        flash("Created: " + filename, "success")
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/files")
@login_required
def view_file():
    username = session["username"]
    filename = request.args.get("filename", "")
    if filename == "":
        abort(400)
    user_dir = os.path.join(UPLOAD_ROOT, username)
    filepath = os.path.join(user_dir, filename)

    if not os.path.exists(filepath):
        return abort(404)

    try:
        # If download query provided, force send as attachment
        if request.args.get("download"):
            return send_file(filepath, as_attachment=True, download_name=filename)
        return send_file(filepath, conditional=True)
    except Exception:
        abort(500)

@app.route("/view")
@login_required
def view_page():
    username = session["username"]
    filename = request.args.get("filename", "")
    if filename == "":
        abort(400)
    user_dir = os.path.join(UPLOAD_ROOT, username)
    filepath = os.path.join(user_dir, filename)
    if not os.path.exists(filepath):
        return abort(404)

    # Determine preview type based on extension
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    kind = "unknown"
    content = None
    if ext in {"txt", "md"}:
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
                data = fh.read()
            # Limit to avoid rendering extremely large files
            content = data if len(data) <= 200_000 else data[:200_000] + "\n\n… truncated …"
            kind = "text"
        except Exception:
            kind = "unknown"
    elif ext in {"png", "jpg", "jpeg", "gif"}:
        kind = "image"

    return render_template("view.html", filename=filename, kind=kind, content=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2007)
