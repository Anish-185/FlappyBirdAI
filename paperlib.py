"""Small typesetting layer on top of reportlab for an arXiv-style paper."""
import os, hashlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image as PILImage

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle, KeepTogether,
                                Image, Preformatted, CondPageBreak)

FD = next(d for d in ("/usr/share/fonts/truetype/liberation/", "/usr/share/fonts/liberation/") if os.path.isdir(d))
for nm, fn in [("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
               ("Serif-I", "LiberationSerif-Italic"), ("Serif-BI", "LiberationSerif-BoldItalic"),
               ("Mono", "LiberationMono-Regular"), ("Mono-B", "LiberationMono-Bold"),
               ("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold")]:
    pdfmetrics.registerFont(TTFont(nm, FD + fn + ".ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-B", italic="Mono", boldItalic="Mono-B")

PAGE = A4
LM, RM, TM, BM = 23 * mm, 23 * mm, 24 * mm, 24 * mm
W = PAGE[0] - LM - RM
INK = colors.HexColor("#111111")
GREY = colors.HexColor("#555555")

FS = 10.0
ST = dict(
    body=ParagraphStyle("body", fontName="Serif", fontSize=FS, leading=12.7, alignment=TA_JUSTIFY,
                        spaceAfter=5.2, textColor=INK, hyphenationLang=None),
    title=ParagraphStyle("title", fontName="Serif-B", fontSize=17.5, leading=21.5, alignment=TA_CENTER, textColor=INK, spaceAfter=8),
    author=ParagraphStyle("author", fontName="Serif", fontSize=11, leading=14, alignment=TA_CENTER, textColor=INK),
    affil=ParagraphStyle("affil", fontName="Serif-I", fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=GREY),
    abs_h=ParagraphStyle("abs_h", fontName="Serif-B", fontSize=10.5, leading=13, alignment=TA_CENTER, spaceAfter=3),
    abs=ParagraphStyle("abs", fontName="Serif", fontSize=9.3, leading=11.7, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=4),
    h1=ParagraphStyle("h1", fontName="Serif-B", fontSize=12.5, leading=15, spaceBefore=13, spaceAfter=5.5, textColor=INK, keepWithNext=1),
    h2=ParagraphStyle("h2", fontName="Serif-B", fontSize=10.6, leading=13, spaceBefore=8.5, spaceAfter=3.5, textColor=INK, keepWithNext=1),
    h3=ParagraphStyle("h3", fontName="Serif-BI", fontSize=10, leading=12.5, spaceBefore=5, spaceAfter=2, textColor=INK, keepWithNext=1),
    cap=ParagraphStyle("cap", fontName="Serif", fontSize=8.8, leading=10.8, alignment=TA_JUSTIFY, textColor=INK, spaceBefore=3, spaceAfter=9),
    tcap=ParagraphStyle("tcap", fontName="Serif", fontSize=8.8, leading=10.8, alignment=TA_JUSTIFY, textColor=INK, spaceBefore=6, spaceAfter=3, keepWithNext=1),
    cell=ParagraphStyle("cell", fontName="Serif", fontSize=8.5, leading=10.2, textColor=INK),
    cellc=ParagraphStyle("cellc", fontName="Serif", fontSize=8.5, leading=10.2, textColor=INK, alignment=TA_CENTER),
    cellh=ParagraphStyle("cellh", fontName="Serif-B", fontSize=8.5, leading=10.2, textColor=INK, alignment=TA_CENTER),
    cellhl=ParagraphStyle("cellhl", fontName="Serif-B", fontSize=8.5, leading=10.2, textColor=INK),
    bul=ParagraphStyle("bul", fontName="Serif", fontSize=FS, leading=12.7, alignment=TA_JUSTIFY, leftIndent=14, bulletIndent=3, spaceAfter=2.6, textColor=INK),
    ref=ParagraphStyle("ref", fontName="Serif", fontSize=8.7, leading=10.8, leftIndent=17, firstLineIndent=-17, alignment=TA_LEFT, spaceAfter=2.6, textColor=INK),
    algo=ParagraphStyle("algo", fontName="Serif", fontSize=8.8, leading=11.3, textColor=INK),
    mono=ParagraphStyle("mono", fontName="Mono", fontSize=7.6, leading=9.6, textColor=INK),
    kw=ParagraphStyle("kw", fontName="Serif", fontSize=9.3, leading=11.7, alignment=TA_LEFT, textColor=INK, spaceBefore=2),
)

# ------------------------------------------------------------------ numbering
_counters = {"fig": 0, "tab": 0, "eq": 0, "alg": 0}
_order = {"fig": [], "tab": [], "eq": [], "alg": []}


def plan(kind, keys):
    _order[kind] = list(keys)


def num(kind, key):
    return _order[kind].index(key) + 1


def F(key):
    return f"Figure&nbsp;{num('fig', key)}"


def T(key):
    return f"Table&nbsp;{num('tab', key)}"


def Q(key):
    return f"Eq.&nbsp;({num('eq', key)})"


def A(key):
    return f"Algorithm&nbsp;{num('alg', key)}"


def S(n):
    return f"Section&nbsp;{n}"


# ------------------------------------------------------------------ citations
REFS = {}          # key -> formatted string
_cited = []


def ref(key, text):
    REFS[key] = text


def C(*keys):
    ids = []
    for k in keys:
        assert k in REFS, k
        if k not in _cited:
            _cited.append(k)
        ids.append(_cited.index(k) + 1)
    ids.sort()
    return "[" + ", ".join(str(i) for i in ids) + "]"


def reference_list():
    out = []
    for i, k in enumerate(_cited, 1):
        out.append(Paragraph(f"[{i}]&nbsp;&nbsp;{REFS[k]}", ST["ref"]))
    uncited = [k for k in REFS if k not in _cited]
    return out, uncited


# ------------------------------------------------------------------ flowables
def P(text, style="body"):
    return Paragraph(text, ST[style])


def H1(n, text):
    return Paragraph(f"{n}&nbsp;&nbsp;{text}", ST["h1"])


def H2(n, text):
    return Paragraph(f"{n}&nbsp;&nbsp;{text}", ST["h2"])


def H3(text):
    return Paragraph(text, ST["h3"])


def bullets(items):
    return [Paragraph(t, ST["bul"], bulletText="\u2022") for t in items]


def numbered(items):
    return [Paragraph(t, ST["bul"], bulletText=f"({i})") for i, t in enumerate(items, 1)]


_EQ_DIR = "/tmp/eqimg"
os.makedirs(_EQ_DIR, exist_ok=True)


def _eq_png(latex, size=11.5):
    h = hashlib.md5((latex + str(size)).encode()).hexdigest()[:10]
    path = f"{_EQ_DIR}/{h}.png"
    if not os.path.exists(path):
        plt.rcParams.update({"mathtext.fontset": "stix", "font.family": "serif"})
        fig = plt.figure(figsize=(6, 0.6))
        fig.text(0.0, 0.5, f"${latex}$", fontsize=size, va="center", ha="left", color="#111111")
        fig.savefig(path, dpi=400, bbox_inches="tight", pad_inches=0.02, transparent=True)
        plt.close(fig)
    return path


def eq(key, latex, size=11.5):
    _counters["eq"] += 1
    n = _counters["eq"]
    assert _order["eq"][n - 1] == key, (key, n)
    path = _eq_png(latex, size)
    w, h = PILImage.open(path).size
    wpt, hpt = w / 400 * 72, h / 400 * 72
    img = Image(path, width=wpt, height=hpt)
    t = Table([[img, Paragraph(f"({n})", ParagraphStyle("en", fontName="Serif", fontSize=FS, alignment=2))]],
              colWidths=[W - 26, 26])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (0, 0), "CENTER"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return [Spacer(1, 2), t, Spacer(1, 3)]


def fig(key, path, caption, width=None):
    _counters["fig"] += 1
    n = _counters["fig"]
    assert _order["fig"][n - 1] == key, (key, n, _order["fig"])
    w, h = PILImage.open(path).size
    width = width or W
    img = Image(path, width=width, height=width * h / w)
    cap = Paragraph(f"<b>Figure {n}.</b> {caption}", ST["cap"])
    return KeepTogether([Spacer(1, 3), img, cap])


def tbl(key, caption, rows, widths, align=None, bold_first_col=False, notes=None, header_rows=1, span=None):
    """Booktabs-style table. rows[0] is the header. widths are fractions of W."""
    _counters["tab"] += 1
    n = _counters["tab"]
    assert _order["tab"][n - 1] == key, (key, n, _order["tab"])
    ncol = len(rows[0])
    align = align or ["l"] + ["c"] * (ncol - 1)
    data = []
    for r, row in enumerate(rows):
        line = []
        for c, cell in enumerate(row):
            if r < header_rows:
                line.append(Paragraph(str(cell), ST["cellhl"] if align[c] == "l" else ST["cellh"]))
            else:
                st = ST["cell"] if align[c] == "l" else ST["cellc"]
                txt = f"<b>{cell}</b>" if (bold_first_col and c == 0) else str(cell)
                line.append(Paragraph(txt, st))
        data.append(line)
    t = Table(data, colWidths=[w * W for w in widths], repeatRows=header_rows)
    cmds = [("LINEABOVE", (0, 0), (-1, 0), 1.0, INK), ("LINEBELOW", (0, header_rows - 1), (-1, header_rows - 1), 0.5, INK),
            ("LINEBELOW", (0, -1), (-1, -1), 1.0, INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    for s in (span or []):
        cmds.append(s)
    t.setStyle(TableStyle(cmds))
    out = [Paragraph(f"<b>Table {n}.</b> {caption}", ST["tcap"]), t]
    if notes:
        out.append(Paragraph(notes, ParagraphStyle("tn", parent=ST["cap"], fontSize=8.2, leading=10, spaceBefore=3, spaceAfter=9)))
    else:
        out.append(Spacer(1, 9))
    return out


def algorithm(key, title, lines):
    _counters["alg"] += 1
    n = _counters["alg"]
    assert _order["alg"][n - 1] == key
    rows = [[Paragraph(f"<b>Algorithm {n}</b>&nbsp;&nbsp;{title}", ST["algo"]), ""]]
    for i, (indent, txt) in enumerate(lines, 1):
        rows.append([Paragraph(f"{i}", ParagraphStyle("ln", parent=ST["algo"], textColor=GREY, fontSize=7.8)),
                     Paragraph(txt, ParagraphStyle("al", parent=ST["algo"], leftIndent=12 * indent))])
    t = Table(rows, colWidths=[19, W - 19])
    t.setStyle(TableStyle([("SPAN", (0, 0), (1, 0)), ("ALIGN", (0, 1), (0, -1), "RIGHT"), ("LINEABOVE", (0, 0), (-1, 0), 1.0, INK), ("LINEBELOW", (0, 0), (-1, 0), 0.5, INK),
                           ("LINEBELOW", (0, -1), (-1, -1), 1.0, INK), ("TOPPADDING", (0, 0), (-1, -1), 1.3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.3), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return KeepTogether([Spacer(1, 4), t, Spacer(1, 8)])


def code(text):
    t = Table([[Preformatted(text.strip("\n"), ST["mono"])]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f5f5")),
                           ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return KeepTogether([t, Spacer(1, 7)])
