from flask import Flask, request, send_file, Response
from vip_pdf_generator import generate_vip_pdf
import tempfile, os

app = Flask(__name__)

def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS, GET"
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

@app.route("/generate", methods=["GET", "POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return Response("OK", status=200)

    if request.method == "GET":
        return Response("Backend is running!", status=200)

    data         = request.json or {}
    title        = data.get("title", "VIP Guide")
    subtitle     = data.get("subtitle", "")
    footer_label = data.get("footer_label", "EXCLUSIVE VIP GUIDE")
    sections     = data.get("sections", [])

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    generate_vip_pdf(
        output_path  = tmp_path,
        title        = title,
        subtitle     = subtitle,
        footer_label = footer_label,
        sections     = sections,
    )

    return send_file(
        tmp_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="VIP_Guide.pdf"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

# ### Key changes:
# - Uses `@app.after_request` — applies CORS to **every** response automatically
# - `Access-Control-Allow-Origin: *` — allows **all** origins (safest fix)
# - Added a `GET` route so you can test in browser directly
# - No dependency on `flask-cors` library

# ---

# ## Step 4 — Also update `requirements.txt`

# Remove `flask-cors` since we no longer need it:
# ```
# flask
# reportlab
# ```

# ---

# ## Step 5 — Verify it worked

# After Render redeploys, open this in your browser:
# ```
# https://vip-pdf-generator.onrender.com/generate
