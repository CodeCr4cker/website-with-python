"""
╔══════════════════════════════════════════════════════════════╗
║          VIP PDF GENERATOR — Reusable Template               ║
║  Drop in your own title, subtitle, steps, tips, and output  ║
║  path — the styling is handled automatically.                ║
╚══════════════════════════════════════════════════════════════╝

QUICK START
-----------
1. pip install reportlab
2. Edit the "YOUR CONTENT HERE" section at the bottom of this file
3. Run:  python vip_pdf_generator.py

CONTENT TYPES SUPPORTED
------------------------
- Numbered step lists      →  steps = ["Step 1...", "Step 2..."]
- Bullet tip lists         →  tips  = ["Tip 1...", "Tip 2..."]
- Plain paragraphs         →  paragraphs = ["Paragraph text..."]
- Inline code / paths      →  wrap in <code>...</code> tags
- Bold text                →  wrap in <b>...</b> tags

Each section is a dict:
    {
        "heading":     "Section Title",          # shown as gold heading
        "type":        "steps" | "tips" | "text",
        "content":     [ "item1", "item2", ... ] # list of strings (HTML tags ok)
    }
"""

# ── Imports ──────────────────────────────────────────────────────────────────
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    ListFlowable, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch


# ── Colour Palette ────────────────────────────────────────────────────────────
GOLD        = colors.HexColor("#C9A84C")
DARK_GOLD   = colors.HexColor("#8B6914")
CREAM       = colors.HexColor("#FFFDF5")
CHARCOAL    = colors.HexColor("#1C1C1C")
LIGHT_GOLD  = colors.HexColor("#F5E6B8")
CODE_BG     = colors.HexColor("#2B2B2B")


# ── Page Border & Decoration ──────────────────────────────────────────────────
def draw_border(c, doc,
                footer_label="EXCLUSIVE VIP GUIDE  ·  CONFIDENTIAL"):
    """
    Draws the full-page VIP frame on every page.
    Called automatically by doc.build().
    """
    c.saveState()
    w, h = letter

    # Cream background
    c.setFillColor(CREAM)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Outer thick gold border
    c.setStrokeColor(GOLD)
    c.setLineWidth(4)
    c.rect(18, 18, w - 36, h - 36)

    # Inner thin dark-gold border
    c.setStrokeColor(DARK_GOLD)
    c.setLineWidth(1)
    c.rect(26, 26, w - 52, h - 52)

    # Corner diamonds
    for cx, cy in [(18, 18), (w-18, 18), (18, h-18), (w-18, h-18)]:
        c.setFillColor(GOLD)
        p = c.beginPath()
        p.moveTo(cx,   cy + 6)
        p.lineTo(cx+6, cy)
        p.lineTo(cx,   cy - 6)
        p.lineTo(cx-6, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    # Dark header band
    c.setFillColor(CHARCOAL)
    c.rect(26, h - 100, w - 52, 74, fill=1, stroke=0)

    # Gold accent under header
    c.setFillColor(GOLD)
    c.rect(26, h - 106, w - 52, 6, fill=1, stroke=0)

    # Dark footer band
    c.setFillColor(CHARCOAL)
    c.rect(26, 26, w - 52, 40, fill=1, stroke=0)

    # Gold accent above footer
    c.setFillColor(GOLD)
    c.rect(26, 66, w - 52, 4, fill=1, stroke=0)

    # Footer text
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(w / 2, 40, f"✦  {footer_label}  ✦")

    # Page number
    c.setFillColor(LIGHT_GOLD)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w / 2, 30, f"Page {doc.page}")

    c.restoreState()


# ── Style Definitions ─────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'VIPTitle',
        parent=base['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=GOLD,
        alignment=1,
        spaceAfter=4,
        spaceBefore=0,
        leading=26,
    )
    subtitle_style = ParagraphStyle(
        'VIPSubtitle',
        parent=base['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        textColor=LIGHT_GOLD,
        alignment=1,
        spaceAfter=0,
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=base['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=DARK_GOLD,
        spaceBefore=16,
        spaceAfter=6,
        leading=16,
    )
    body_style = ParagraphStyle(
        'VIPBody',
        parent=base['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=CHARCOAL,
        spaceAfter=6,
        leading=15,
    )
    tip_style = ParagraphStyle(
        'VIPTip',
        parent=base['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        textColor=DARK_GOLD,
        spaceAfter=4,
        leading=13,
        leftIndent=10,
    )
    code_style = ParagraphStyle(
        'VIPCode',
        parent=base['Normal'],
        fontName='Courier',
        fontSize=9,
        textColor=LIGHT_GOLD,
        backColor=CODE_BG,
        spaceAfter=6,
        leading=13,
        leftIndent=10,
        rightIndent=10,
        borderPadding=(6, 8, 6, 8),
    )

    return {
        "title":   title_style,
        "subtitle": subtitle_style,
        "heading": section_heading,
        "body":    body_style,
        "tip":     tip_style,
        "code":    code_style,
    }


# ── Core Builder ──────────────────────────────────────────────────────────────
def generate_vip_pdf(
    output_path: str,
    title: str,
    subtitle: str,
    sections: list,
    footer_label: str = "EXCLUSIVE VIP GUIDE  ·  CONFIDENTIAL",
):
    """
    Build a VIP-styled PDF.

    Parameters
    ----------
    output_path   : str   – Where to save the PDF (e.g. "MyGuide.pdf")
    title         : str   – Large gold heading shown in the header band
    subtitle      : str   – Smaller italic line below the title
    sections      : list  – List of section dicts (see module docstring)
    footer_label  : str   – Text shown in the footer band (optional)

    Section dict format
    -------------------
    {
        "heading": "Section Title",          # optional gold heading
        "type":    "steps" | "tips" | "text" | "code",
        "content": ["line 1", "line 2", ...]
    }
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=1.55 * inch,
        bottomMargin=1.1 * inch,
    )

    S = build_styles()
    elements = []

    # ── Header ──────────────────────────────────────────────────────────────
    elements.append(Paragraph(title, S["title"]))
    elements.append(Paragraph(subtitle, S["subtitle"]))
    elements.append(Spacer(1, 14))
    elements.append(HRFlowable(width="100%", thickness=1.5,
                                color=GOLD, spaceAfter=10))

    # ── Sections ─────────────────────────────────────────────────────────────
    for section in sections:
        heading  = section.get("heading", "")
        sec_type = section.get("type", "text")   # "steps" | "tips" | "text" | "code"
        content  = section.get("content", [])

        if heading:
            elements.append(Paragraph(heading, S["heading"]))

        if sec_type == "steps":
            items = [Paragraph(item, S["body"]) for item in content]
            elements.append(
                ListFlowable(items,
                             bulletType='1',
                             leftIndent=20,
                             bulletFontSize=10,
                             bulletColor=GOLD)
            )

        elif sec_type == "tips":
            for item in content:
                elements.append(Paragraph(f"✦  {item}", S["tip"]))

        elif sec_type == "code":
            for line in content:
                elements.append(Paragraph(line, S["code"]))

        else:  # "text" / default
            for item in content:
                elements.append(Paragraph(item, S["body"]))

        elements.append(Spacer(1, 6))

    # ── Footer divider ───────────────────────────────────────────────────────
    elements.append(HRFlowable(width="100%", thickness=1.5,
                                color=GOLD, spaceAfter=0))

    # ── Build ────────────────────────────────────────────────────────────────
    doc.build(
        elements,
        onFirstPage=lambda c, d: draw_border(c, d, footer_label),
        onLaterPages=lambda c, d: draw_border(c, d, footer_label),
    )
    print(f"✅  PDF saved → {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
#  ✏️  YOUR CONTENT HERE — Edit everything below to create your own VIP PDF
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    generate_vip_pdf(

        # ── Output file path ─────────────────────────────────────────────────
        output_path="My_VIP_Guide.pdf",

        # ── Header ───────────────────────────────────────────────────────────
        title    = "VIP GUIDE: Block Any Website on Your PC",
        subtitle = "Windows Edition  ·  Step-by-Step Instructions",

        # ── Footer label (optional) ───────────────────────────────────────────
        footer_label = "EXCLUSIVE VIP GUIDE  ·  CONFIDENTIAL",

        # ── Sections ─────────────────────────────────────────────────────────
        # Each section is a dict with "heading", "type", and "content" keys.
        #
        # type options:
        #   "steps"  →  numbered list  (use for instructions)
        #   "tips"   →  gold ✦ bullets (use for pro tips / notes)
        #   "text"   →  plain body paragraphs
        #   "code"   →  dark background monospaced block
        #
        # HTML tags supported inside strings:
        #   <b>bold</b>   <i>italic</i>   <br/>  &nbsp;
        #   <font name='Courier' size='9'>inline code</font>
        # ─────────────────────────────────────────────────────────────────────
        sections = [

            {
                "heading": "Step-by-Step Instructions",
                "type":    "text",
                "content": [
                    "Follow the steps below carefully. This method uses the Windows "
                    "<b>hosts</b> file to redirect unwanted domains to your local "
                    "machine — no third-party software required."
                ],
            },

            {
                "heading": "",          # no heading — continues from above
                "type":    "steps",
                "content": [
                    "Open <b>Notepad</b> as Administrator (right-click → Run as administrator).",
                    "Press <b>Ctrl + O</b> to open a file.",
                    "Navigate to: <b>C:/Windows/System32/drivers/etc</b>",
                    "Change file type filter to <b>All Files (*.*)</b>.",
                    "Open the file named <b>hosts</b>.",
                    "Scroll to the very bottom of the file.",
                    "Add one line per website you want to block:",
                ],
            },

            {
                "heading": "",
                "type":    "code",
                "content": [
                    "127.0.0.1    www.example.com",
                    "127.0.0.1    example.com",
                ],
            },

            {
                "heading": "",
                "type":    "steps",
                "content": [
                    "Save the file (<b>Ctrl + S</b>).",
                    "Restart your browser for changes to take effect.",
                ],
            },

            {
                "heading": "Pro Tips",
                "type":    "tips",
                "content": [
                    "Block both <b>www.site.com</b> and <b>site.com</b> for full coverage.",
                    "To unblock, simply delete the corresponding lines.",
                    "Flush DNS after saving: open Command Prompt and run "
                    "<font name='Courier' size='9'>ipconfig /flushdns</font>",
                    "Changes are system-wide — all browsers are affected simultaneously.",
                ],
            },

        ],  # end sections
    )


# ══════════════════════════════════════════════════════════════════════════════
#  EXAMPLE — Another guide with different content (uncomment to use)
# ══════════════════════════════════════════════════════════════════════════════
#
# generate_vip_pdf(
#     output_path   = "Python_Cheatsheet.pdf",
#     title         = "VIP PYTHON CHEATSHEET",
#     subtitle      = "Essential Commands & Patterns  ·  Quick Reference",
#     footer_label  = "PYTHON QUICK REFERENCE  ·  FOR INTERNAL USE",
#     sections = [
#         {
#             "heading": "List Comprehensions",
#             "type":    "text",
#             "content": ["A concise way to create lists based on existing lists."],
#         },
#         {
#             "heading": "",
#             "type":    "code",
#             "content": [
#                 "squares = [x**2 for x in range(10)]",
#                 "evens   = [x for x in range(20) if x % 2 == 0]",
#             ],
#         },
#         {
#             "heading": "Dictionary Tricks",
#             "type":    "tips",
#             "content": [
#                 "Use .get(key, default) to avoid KeyError.",
#                 "dict.items() returns key-value pairs for looping.",
#                 "Merge two dicts with {**dict1, **dict2} (Python 3.5+).",
#             ],
#         },
#     ],
# )
