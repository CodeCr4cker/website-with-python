from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from vip_pdf_generator import generate_vip_pdf
import tempfile, os

app = Flask(__name__)

# ✅ THIS IS THE FIX — explicitly allow your GitHub Pages domain
CORS(app, origins=["https://codecr4cker.github.io"])

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers["Access-Control-Allow-Origin"] = "https://codecr4cker.github.io"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    data = request.json

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

    response = send_file(
        tmp_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"{title[:30].replace(' ', '_')}.pdf"
    )
    response.headers["Access-Control-Allow-Origin"] = "https://codecr4cker.github.io"

    @response.call_on_close
    def cleanup():
        os.unlink(tmp_path)

    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
