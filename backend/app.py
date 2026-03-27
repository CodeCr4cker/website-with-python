from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from vip_pdf_generator import generate_vip_pdf
import tempfile, os

app = Flask(__name__)
CORS(app)  # allows your GitHub Pages frontend to call this API

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    # Pull content from the request
    title        = data.get("title", "VIP Guide")
    subtitle     = data.get("subtitle", "")
    footer_label = data.get("footer_label", "EXCLUSIVE VIP GUIDE")
    sections     = data.get("sections", [])

    # Generate PDF into a temp file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    generate_vip_pdf(
        output_path  = tmp_path,
        title        = title,
        subtitle     = subtitle,
        footer_label = footer_label,
        sections     = sections,
    )

    # Send PDF back as a download
    response = send_file(
        tmp_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"{title[:30].replace(' ', '_')}.pdf"
    )

    # Clean up temp file after sending
    @response.call_on_close
    def cleanup():
        os.unlink(tmp_path)

    return response

if __name__ == "__main__":
    app.run(debug=True)
