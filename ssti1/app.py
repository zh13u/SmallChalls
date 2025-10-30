from flask import Flask, render_template_string, abort , request
import os

app = Flask(__name__)
FLAG = os.path.join(os.path.dirname(__file__), 'flag.txt')

@app.route('/')
def index():
    return '''
    <p>Enter a Jinja2 template below and see the rendered result.</p>
    <form method="POST" action="/render">
      <textarea name="tmpl" rows="8" cols="80">{{Hello}}</textarea><br>
      <input type="submit" value="Render">
    </form>
    <p>Goal: read the contents of <code>flag.txt</code> in the app directory.</p>
    <p>Hint: Jinja2 object traversal (e.g. scanning <code>__subclasses__()</code>) can help.</p>
    '''

@app.route("/render", methods=["POST"])
def render_tmpl():
    tmpl = request.form.get("tmpl", "")
    try:
        rendered = render_template_string(tmpl)
        # small naive filter to block obvious direct calls - still intentionally vulnerable
        if any(s in tmpl for s in ["os.system", "subprocess", "exec(", "eval("]):
            return "Payload contains disallowed substrings.", 400
        return rendered
    except Exception as e:
        return "<pre>Rendering error:\\n{}</pre>".format(e), 400
    
@app.route("/admin")
def admin():
    key = request.args.get("k", "")
    if key != "letmein_admin":
        abort(403)
    return "<h2>Admin panel</h2><p>Nothing here.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)