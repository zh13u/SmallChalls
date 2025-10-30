from flask import Flask, request, render_template, jsonify, session
import subprocess, os, time
from markupsafe import escape

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET"])
def index():
    # store last attempts in session for UI history
    attempts = session.get("attempts", [])
    return render_template("index.html", attempts=attempts)

@app.route("/ping", methods=["POST"])
def ping():
    target = request.form.get("target", "").strip()
    if not target:
        return jsonify({"ok": False, "output": "Target is required."}), 400

    # vulnerable part: builds a shell string with user input (intentional for CTF)
    try:
        cmd = f"ping -c 3 {target}"
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=6)
        output = out.decode(errors="replace")
    except subprocess.CalledProcessError as e:
        output = e.output.decode(errors="replace")
    except Exception as e:
        output = f"Error: {e}"

    # record attempt in session (for UI only)
    attempts = session.get("attempts", [])
    attempts.insert(0, {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "target": escape(target), "snippet": escape(output[:300])})
    session["attempts"] = attempts[:10]  # keep last 10
    return jsonify({"ok": True, "output": output})

if __name__ == "__main__":
    # Note: flag file should be created in the Dockerfile or container image, not here.
    app.run(host="0.0.0.0", port=2001, debug=False)
