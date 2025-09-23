#!/usr/bin/env python3
# app.py -- Flask wrapper for ASCII Designer (with export)
import io
import json
from flask import Flask, request, Response, render_template_string, send_file
import pyfiglet

app = Flask(__name__)

# ANSI color codes (for embedding into exported / raw files)
ANSI_COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m"
}

# CSS colors used for HTML preview (browsers don't render ANSI)
CSS_COLORS = {
    "red": "#ff6b6b",
    "green": "#7ee787",
    "yellow": "#ffd86b",
    "blue": "#7fb4ff",
    "magenta": "#d48bff",
    "cyan": "#7fffd4",
    "white": "#e6eef8"
}

# HTML template (inline for easy deploy)
HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>ASCII Designer (Web)</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; background:#071026; color:#dbeafe; padding:20px; }
  .panel { max-width:1000px; margin:auto; }
  form { display:flex; gap:8px; flex-wrap:wrap; align-items:end; margin-bottom:12px; }
  label { font-size:0.85rem; color:#9fb0d9; display:block; }
  input, select { padding:8px; border-radius:6px; background:#001428; color:#dbeafe; border:1px solid #153047; }
  button { padding:8px 12px; border-radius:6px; border:none; cursor:pointer; background:#2b9a77; color:white; }
  pre.banner { background:#001528; padding:18px; border-radius:8px; overflow:auto; white-space:pre; font-family: Menlo, Monaco, "Courier New", monospace; font-size:13px; }
  .meta { color:#8fa6c8; font-size:0.9rem; margin-top:10px; }
  .row { display:flex; gap:8px; align-items:center; }
</style>
</head>
<body>
  <div class="panel">
    <h1>ASCII Designer — Web Demo</h1>
    <form method="get" action="/">
      <div>
        <label for="text">Text</label>
        <input id="text" name="text" value="{{ text|e }}" required>
      </div>

      <div>
        <label for="font">Font</label>
        <select id="font" name="font">
          <option value="">(use default)</option>
          {% for f in fonts %}
            <option value="{{f}}" {% if f==font %}selected{% endif %}>{{f}}</option>
          {% endfor %}
        </select>
      </div>

      <div>
        <label for="align">Align</label>
        <select id="align" name="align">
          <option value="left" {% if align=='left' %}selected{% endif %}>left</option>
          <option value="center" {% if align=='center' %}selected{% endif %}>center</option>
          <option value="right" {% if align=='right' %}selected{% endif %}>right</option>
        </select>
      </div>

      <div>
        <label for="color">Color (preview)</label>
        <select id="color" name="color">
          <option value="">(none)</option>
          {% for c in colors %}
            <option value="{{c}}" {% if c==color %}selected{% endif %}>{{c}}</option>
          {% endfor %}
        </select>
      </div>

      <div style="display:flex; gap:6px;">
        <button type="submit">Preview</button>
        <button formaction="/export" formmethod="get" type="submit">Export</button>
      </div>
    </form>

    {% if banner %}
      <label>Preview</label>
      <pre class="banner" style="color: {{ css_color }};">{{ banner }}</pre>
      <div class="meta">
        <strong>Usage:</strong> Preview via query params or use <code>/export?format=python|raw|json</code> to download.
      </div>
    {% else %}
      <div class="meta">Enter text and press Preview or Export.</div>
    {% endif %}

    <div style="margin-top:12px; color:#9fb0d9;">
      <strong>Available fonts:</strong> {{ fonts|join(', ') }}
    </div>
  </div>
</body>
</html>
"""

# Helper utilities
def render_banner(text: str, font: str) -> str:
    """Return ASCII art using pyfiglet (raises FontNotFound)."""
    fig = pyfiglet.Figlet(font=font) if font else pyfiglet.Figlet()
    return fig.renderText(text)

def align_text(ascii_text: str, align: str, width: int = 80) -> str:
    lines = ascii_text.splitlines()
    if not lines:
        return ascii_text
    if align == "left":
        return "\n".join(lines)
    if align == "center":
        return "\n".join(line.center(width) for line in lines)
    if align == "right":
        return "\n".join(line.rjust(width) for line in lines)
    return "\n".join(lines)

def embed_ansi(ascii_text: str, color_name: str) -> str:
    if color_name and color_name in ANSI_COLORS:
        return ANSI_COLORS[color_name] + ascii_text + ANSI_COLORS["reset"]
    return ascii_text

def make_python_export(banner_text: str, var_name: str = "BANNER", embed_color: bool = False, color_name: str = None) -> str:
    """Return Python source that defines a variable containing the banner and prints it."""
    text_for_export = banner_text
    if embed_color and color_name:
        code = ANSI_COLORS.get(color_name, "")
        reset = ANSI_COLORS.get("reset", "")
        text_for_export = code + banner_text + reset
    # Use json.dumps to produce a safe Python string literal with escapes
    py_literal = json.dumps(text_for_export)
    py_source = f"# Generated ASCII banner (variable: {var_name})\n{var_name} = {py_literal}\n\nif __name__ == '__main__':\n    print({var_name})\n"
    return py_source

@app.route("/", methods=["GET"])
def index():
    text = request.args.get("text", "")
    font = request.args.get("font", "")
    align = request.args.get("align", "left")
    color = request.args.get("color", "")

    banner = ""
    css_color = CSS_COLORS.get(color, "#dbeafe")

    if text:
        try:
            banner_raw = render_banner(text, font) if font else render_banner(text, None)
            banner = align_text(banner_raw, align)
        except pyfiglet.FontNotFound:
            banner = f"[Error] Font '{font}' not found."

    return render_template_string(
        HTML,
        banner=banner,
        text=text,
        font=font,
        align=align,
        color=color,
        css_color=css_color,
        fonts=pyfiglet.getFonts(),
        colors=list(ANSI_COLORS.keys())[:-1]  # exclude 'reset'
    )

@app.route("/ascii", methods=["GET"])
def ascii_plain():
    """Return plain-text banner (useful for CLI-like embedding)."""
    text = request.args.get("text", "Hello")
    font = request.args.get("font", "")
    align = request.args.get("align", "left")
    color = request.args.get("color", None)

    try:
        banner_raw = render_banner(text, font) if font else render_banner(text, None)
    except pyfiglet.FontNotFound:
        return Response(f"Error: Font '{font}' not found.", mimetype="text/plain", status=400)

    banner = align_text(banner_raw, align)

    # Optionally embed ANSI color codes for plain text
    if color:
        banner = embed_ansi(banner, color)

    return Response(banner, mimetype="text/plain; charset=utf-8")

@app.route("/export", methods=["GET"])
def export():
    """
    Export endpoint parameters:
      - text (string)
      - font (optional)
      - align (left|center|right)
      - format (python|raw|json)  -> default python
      - var  (python variable name, default: BANNER)
      - embed_color (1 or 0) -> include ANSI codes inside exported content
      - color (color name) -> for embedding
    """
    text = request.args.get("text", "Hello")
    font = request.args.get("font", "")
    align = request.args.get("align", "left")
    fmt = request.args.get("format", "python")
    varname = request.args.get("var", "BANNER")
    embed_color = request.args.get("embed_color", "0") in ("1", "true", "yes")
    color = request.args.get("color", None)

    try:
        banner_raw = render_banner(text, font) if font else render_banner(text, None)
    except pyfiglet.FontNotFound:
        return Response(f"Error: Font '{font}' not found.", mimetype="text/plain", status=400)

    banner = align_text(banner_raw, align)

    if fmt == "raw":
        output_text = banner
        if embed_color and color:
            output_text = embed_ansi(output_text, color)
        b = output_text.encode("utf-8")
        return send_file(io.BytesIO(b), as_attachment=True, download_name="banner.txt", mimetype="text/plain; charset=utf-8")

    if fmt == "json":
        payload = {"text_lines": banner.splitlines()}
        if embed_color and color:
            payload["color"] = color
        b = json.dumps(payload, indent=2).encode("utf-8")
        return send_file(io.BytesIO(b), as_attachment=True, download_name="banner.json", mimetype="application/json; charset=utf-8")

    # default: python export
    py_source = make_python_export(banner, var_name=varname, embed_color=embed_color, color_name=color)
    b = py_source.encode("utf-8")
    return send_file(io.BytesIO(b), as_attachment=True, download_name="banner.py", mimetype="text/x-python; charset=utf-8")

if __name__ == "__main__":
    # Use python app.py (not `flask run`) so Fly will run it without FLASK_APP env
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", "8080")))
