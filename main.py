from flask import Flask, request, render_template_string, send_file, redirect, url_for
import pyfiglet
import io
import json

app = Flask(__name__)

COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m"
}

AVAILABLE_FONTS = [
    "slant","big","block","banner3-D","cyberlarge",
    "standard","doom","isometric1","larry3d","starwars"
]

SIZE_MAP = {"small": "block", "medium": "standard", "large": "big"}

# Simple HTML template (inline for easy deploy)
TEMPLATE = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>ASCII Banner Demo</title>
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; padding: 20px; background:#0f172a; color:#e6eef8; }
.container { max-width: 900px; margin: auto; }
form { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:12px; }
label { display:block; font-size:0.85rem; margin-bottom:4px; color:#9fb0d9; }
select,input[type=text] { padding:8px; background:#071029; color:#e6eef8; border:1px solid #244; border-radius:6px; }
button { padding:8px 12px; border-radius:6px; border:none; cursor:pointer; background:#2b7; color:#012; }
pre.banner { background:#001528; padding:18px; border-radius:8px; overflow:auto; white-space:pre; font-family: Menlo, Monaco, "Courier New", monospace; color:#cfefff; }
small.hint { color:#7ea1c9; display:block; margin-top:6px; }
.footer { margin-top:20px; font-size:0.9rem; color:#8fa6c8; }
</style>
</head>
<body>
<div class="container">
<h2>ASCII Banner — Live Demo</h2>

<form method="GET" action="/">
  <div>
    <label for="text">Text</label>
    <input id="text" name="text" value="{{text|e}}" />
  </div>

  <div>
    <label for="font">Font</label>
    <select id="font" name="font">
      <option value="">(use size preset)</option>
      {% for f in fonts %}
      <option value="{{f}}" {% if f==font %}selected{% endif %}>{{f}}</option>
      {% endfor %}
    </select>
  </div>

  <div>
    <label for="size">Size</label>
    <select id="size" name="size">
      <option value="">(default)</option>
      <option value="small" {% if size=='small' %}selected{% endif %}>small</option>
      <option value="medium" {% if size=='medium' %}selected{% endif %}>medium</option>
      <option value="large" {% if size=='large' %}selected{% endif %}>large</option>
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
    <label for="color">Color (preview only)</label>
    <select id="color" name="color">
      <option value="">(none)</option>
      {% for c in colors %}
      <option value="{{c}}" {% if c==color %}selected{% endif %}>{{c}}</option>
      {% endfor %}
    </select>
  </div>

  <div style="align-self:end;">
    <button type="submit">Preview</button>
  </div>

  <div style="align-self:end;">
    <button formaction="/export" formmethod="get" type="submit">Export</button>
  </div>
</form>

{% if banner %}
  <div>
    <label>Preview</label>
    <pre class="banner">{{banner}}</pre>
    <small class="hint">Tip: use Export to download as Python/raw/JSON.</small>
  </div>
{% endif %}

<div class="footer">
  <strong>Available fonts:</strong> {{fonts|join(', ')}} <br>
  <small>Deploy this app to Replit/Render and share the URL for one-click demos.</small>
</div>
</div>
</body>
</html>
"""

def render_banner(text, font_choice):
    fig = pyfiglet.Figlet(font=font_choice)
    return fig.renderText(text)

def align_text(ascii_text, align):
    lines = ascii_text.splitlines()
    if not lines:
        return ascii_text
    if align == "left":
        return "\n".join(lines)
    maxw = max(len(l) for l in lines)
    if align == "center":
        return "\n".join(line.center(maxw) for line in lines)
    return "\n".join(line.rjust(maxw) for line in lines)

@app.route("/", methods=["GET"])
def index():
    text = request.args.get("text", "PHISHDETECT")
    font = request.args.get("font") or ""
    size = request.args.get("size") or ""
    align = request.args.get("align") or "left"
    color = request.args.get("color") or ""

    # decide font (font override > size > default)
    if font:
        font_choice = font
    elif size and size in SIZE_MAP:
        font_choice = SIZE_MAP[size]
    else:
        font_choice = "slant"

    try:
        raw = render_banner(text, font_choice)
    except Exception as e:
        raw = f"[Error rendering with font {font_choice}: {e}]"

    aligned = align_text(raw, align)

    # For web preview, we won't apply ANSI color codes (browsers don't render them).
    # Instead, we could style with CSS, but keep text color neutral for readability.
    banner_for_display = aligned

    return render_template_string(TEMPLATE,
                                  banner=banner_for_display,
                                  text=text,
                                  font=font,
                                  size=size,
                                  align=align,
                                  color=color,
                                  fonts=AVAILABLE_FONTS,
                                  colors=list(COLORS.keys())[:-1]
                                  )

@app.route("/export", methods=["GET"])
def export():
    # Export endpoint supports format query: python/raw/json
    text = request.args.get("text", "PHISHDETECT")
    font = request.args.get("font") or ""
    size = request.args.get("size") or ""
    align = request.args.get("align") or "left"
    fmt = request.args.get("format") or "python"
    export_var = request.args.get("var") or "BANNER"

    if font:
        font_choice = font
    elif size and size in SIZE_MAP:
        font_choice = SIZE_MAP[size]
    else:
        font_choice = "slant"

    try:
        raw = render_banner(text, font_choice)
    except Exception as e:
        return f"Error: {e}", 400

    aligned = align_text(raw, align)
    lines = aligned.splitlines()

    if fmt == "raw":
        data = "\n".join(lines)
        return send_file(io.BytesIO(data.encode("utf-8")), download_name="banner.txt", as_attachment=True)

    if fmt == "json":
        payload = {"text_lines": lines}
        data = json.dumps(payload, indent=2)
        return send_file(io.BytesIO(data.encode("utf-8")), download_name="banner.json", as_attachment=True)

    # default python
    banner_text = "\n".join(lines)
    pycode = f"# Generated ASCII banner (variable: {export_var})\n{export_var} = '''\\\n{banner_text}\n'''\n\nif __name__ == '__main__':\n    print({export_var})\n"
    return send_file(io.BytesIO(pycode.encode("utf-8")), download_name="banner.py", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
