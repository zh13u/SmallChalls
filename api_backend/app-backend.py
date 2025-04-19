from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64
import hashlib
import jwt

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag TEXT NOT NULL
        )
    """)

    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'fake_password'))
    c.execute("INSERT OR IGNORE INTO flags (flag) VALUES (?)", ('CTB{fake_flag}',))

    conn.commit()
    conn.close()

init_db()

PRIVATE_KEY = None
PUBLIC_KEY = None
JWKS = None

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    numbers = public_key.public_numbers()
    key_id = hashlib.sha256(public_pem.encode()).hexdigest()[:16]
    jwk = {
        "kty": "RSA",
        "kid": key_id,
        "use": "sig",
        "n": base64.urlsafe_b64encode(numbers.n.to_bytes(256, 'big')).rstrip(b'=').decode(),
        "e": base64.urlsafe_b64encode(numbers.e.to_bytes(3, 'big')).rstrip(b'=').decode()
    }

    return private_pem, public_pem, {"keys": [jwk]}

PRIVATE_KEY, PUBLIC_KEY, JWKS = generate_keys()

@app.route('/')
def index():

    return "Hi! this's src web here......https://drive.google.com/drive/folders/1RaJM8V7XaFdhHYREagI_uOXJkCdGr_-X?usp=sharing"

@app.route('/.well-known/jwks.json', methods=['GET', 'POST'])
def jwks():
    return jsonify(JWKS)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    payload = {
        "username": "guest",
        "role": "guest",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "kid": JWKS["keys"][0]["kid"]
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return jsonify({"token": token})

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    token = request.args.get('token', '') or request.form.get('token', '')
    if not token:
        return render_template('dashboard.html', error="Token is required")

    try:
        
        search = request.args.get('search', '') or request.form.get('search', '')
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        query = f"SELECT 1 FROM flags WHERE id = '{search}'"
        c.execute(query)
        result = c.fetchone()
        conn.close()

        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        if decoded.get("role") == "guest" and result:
            username = decoded['username']
            return jsonify({"message":"Research True"} or {"username": username})
        return jsonify({"message":"Research False"} or {"username": username})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    token = request.args.get('token') or request.form.get('token')
    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["HS256", "RS256"])
        if decoded.get("role") == "admin":
            return jsonify({"message": "Welcome Admin!", "username": decoded['username'], "flag": "CTB{fake_flag}"})
        return jsonify({"message": "Access Denied", "role": decoded['role']})
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
