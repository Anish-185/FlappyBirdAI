"""Builds docs/How_to_Run.pdf, the step-by-step run guide."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table,
                                TableStyle, Image, KeepTogether)

OUT = "docs/How_to_Run.pdf"
REPO = "https://github.com/Anish-185/FlappyBirdAI"

ss = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=22, spaceAfter=4)
SUB = ParagraphStyle("sub", parent=ss["Normal"], fontSize=11, textColor=colors.HexColor("#555555"),
                     alignment=1, spaceAfter=14)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=14, spaceBefore=12, spaceAfter=4,
                    textColor=colors.HexColor("#1f5f2a"))
P = ParagraphStyle("p", parent=ss["Normal"], fontSize=10.5, leading=14.5, spaceAfter=5)
NOTE = ParagraphStyle("note", parent=P, fontSize=9.5, leading=13, textColor=colors.HexColor("#444444"),
                      backColor=colors.HexColor("#fff7dd"), borderPadding=6, spaceBefore=4, spaceAfter=9)
CODE = ParagraphStyle("code", fontName="Courier", fontSize=9, leading=11.5)
CELL = ParagraphStyle("cell", parent=P, fontSize=9, leading=11.5, spaceAfter=0)


def code(s):
    t = Table([[Preformatted(s.strip("\n"), CODE)]], colWidths=[16.5 * cm], spaceBefore=3, spaceAfter=10)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f2f2f2")),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def table(rows, widths):
    t = Table([[Paragraph(c, CELL) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfeedd")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def step(n, title, *body):
    return [KeepTogether([Paragraph(f"Step {n} - {title}", H2), *body[:2]]), *body[2:]]


story = [
    Paragraph("Flappy Bird AI - How to Run", H1),
    Paragraph(f"Step-by-step guide for {REPO}", SUB),
    Paragraph(
        "This project uses a <b>genetic algorithm</b> to evolve a small neural network that plays Flappy "
        "Bird. The repository already contains every training log (606 runs), so you can watch the trained "
        "bird and rebuild all results within a minute. Retraining from scratch is optional and takes "
        "about 45 minutes.", P),
    Paragraph("You only need to type the commands in the grey boxes. Lines starting with <font "
              "face='Courier'>#</font> are comments.", P),
]

story += step(1, "Install the prerequisites",
    Paragraph("You need <b>Python 3.10 or newer</b> and <b>git</b>. Check them in a terminal:", P),
    code("python --version      # or: python3 --version\ngit --version"),
    Paragraph("If either is missing, install it:", P),
    table([["System", "Command"],
           ["Ubuntu / Debian", "<font face='Courier'>sudo apt install python3 python3-venv git fonts-liberation</font>"],
           ["Arch / Omarchy", "<font face='Courier'>sudo pacman -S python git ttf-liberation</font>"],
           ["Fedora", "<font face='Courier'>sudo dnf install python3 git liberation-serif-fonts "
                      "liberation-sans-fonts liberation-mono-fonts</font>"],
           ["macOS", "<font face='Courier'>brew install python git</font>"],
           ["Windows", "Install Python from python.org (tick <i>Add python.exe to PATH</i>) and Git from git-scm.com"]],
          [3.2 * cm, 13.3 * cm]),
    Paragraph("The Liberation fonts are only needed for Step 8 (building the paper PDF).", NOTE))

story += step(2, "Download the project",
    code(f"git clone {REPO}.git\ncd FlappyBirdAI"),
    Paragraph("Every command after this one is run inside the <font face='Courier'>FlappyBirdAI</font> folder.", P))

story += step(3, "Create a virtual environment",
    Paragraph("A virtual environment keeps this project's libraries separate from the rest of your "
              "system. Many Linux systems block <font face='Courier'>pip install</font> outside one.", P),
    code("python -m venv .venv"),
    Paragraph("Then <b>activate</b> it. Do this again every time you open a new terminal:", P),
    code("source .venv/bin/activate        # Linux / macOS\n.venv\\Scripts\\activate           # Windows"),
    Paragraph("Your prompt now starts with <font face='Courier'>(.venv)</font>.", P))

story += step(4, "Install the libraries",
    code("pip install -r requirements.txt"),
    Paragraph("This installs numpy, scipy, pandas, matplotlib, numba (makes the game simulator fast), "
              "reportlab (writes PDFs), pillow and pygame-ce (the game window). It takes a minute or two.", P),
    Paragraph("Check that everything installed:", P),
    code("python -c \"import numpy, scipy, pandas, matplotlib, numba, reportlab, pygame; print('ok')\""))

story += step(5, "Watch the trained bird play",
    code("python play.py"),
    Paragraph("A window opens and the best evolved bird flies through a level it never saw during "
              "training. The top line shows the level number and the pipes cleared so far.", P),
    Image("docs/viewer.png", width=5.2 * cm, height=6.5 * cm),
    Spacer(1, 6),
    table([["Key", "Action"],
           ["SPACE or mouse click", "Next level (there are 30 unseen test levels)"],
           ["UP / DOWN", "Double / halve the speed"],
           ["ESC", "Quit"]], [4.5 * cm, 12 * cm]),
    Spacer(1, 6),
    Paragraph("You can watch the champion of any experiment, and set the starting speed:", P),
    code("python play.py rule_ga          # the 2-gene hand-designed rule\n"
         "python play.py rs               # random search - much worse\n"
         "python play.py pool_1           # trained on only 1 level\n"
         "python play.py base --fps=240   # start 4x faster"))

story += step(6, "Reproduce the statistics",
    code("python analysis.py"),
    Paragraph("This takes about 5 seconds. It prints one table per study and saves "
              "<font face='Courier'>results.pkl</font>. The most important columns:", P),
    table([["Column", "Meaning"],
           ["median, q1, q3", "Pipes cleared on the 30 unseen test levels (median and quartiles over 12 runs)"],
           ["surv", "Fraction of test levels survived for the full 10,000 frames"],
           ["delta", "Cliff's delta effect size vs. the reference condition (-1 to +1)"],
           ["p, p_holm", "Mann-Whitney U p-value, raw and after Holm correction (below 0.05 = significant)"],
           ["auc, e50", "Area under the learning curve; evaluations needed to reach 50 pipes"]],
          [3.2 * cm, 13.3 * cm]))

story += step(7, "Regenerate the figures",
    code("python figures.py"),
    Paragraph("This takes about 7 seconds and rewrites the 11 images in "
              "<font face='Courier'>figures/</font>. Open them with any image viewer.", P))

story += step(8, "Rebuild the paper",
    code("python build_paper.py"),
    Paragraph("This takes about 3 seconds and writes "
              "<font face='Courier'>Flappy_Bird_Neuroevolution_Paper.pdf</font>. The warning "
              "<i>uncited refs: ['deb', 'boxcar']</i> is harmless.", P),
    Paragraph("This step needs the Liberation fonts from Step 1. On macOS or Windows, edit the "
              "<font face='Courier'>FD</font> line in <font face='Courier'>paperlib.py</font> to point at a "
              "folder containing LiberationSerif-Regular.ttf.", NOTE))

story += step(9, "(Optional) Retrain everything from scratch",
    Paragraph("<font face='Courier'>experiments.py</font> skips any experiment that already has a log, so "
              "move the shipped logs out of the way first:", P),
    code("mv logs logs_shipped            # Windows: ren logs logs_shipped\n"
         "python experiments.py           # about 45 minutes on one core"),
    Paragraph("Progress is written to <font face='Courier'>logs/progress.txt</font>. If you stop it, "
              "run the same command again and it continues where it left off. Other options:", P),
    code("python experiments.py base rs    # train only these experiments (~1 min each)\n"
         "python experiments.py --secs=600 # stop after about 10 minutes"),
    Paragraph("Then repeat Steps 6-8 to see results from your own runs. The paper's text has its "
              "numbers typed in, so after retraining the figures change but the text does not.", P),
    Paragraph("Expect 56 of the 60 experiments to match the shipped logs exactly. The 4 fitness-sharing "
              "experiments (div_share1-4) depend on your CPU's math library and may come out "
              "different. See the <i>Reproducibility note</i> in README.md.", NOTE))

story += [Paragraph("Troubleshooting", H2),
    table([["Problem", "Fix"],
           ["<font face='Courier'>error: externally-managed-environment</font>",
            "You skipped Step 3. Create and activate the virtual environment, then retry."],
           ["<font face='Courier'>ModuleNotFoundError: No module named 'numpy'</font> (or similar)",
            "The virtual environment is not active. Run the activate command from Step 3."],
           ["<font face='Courier'>ModuleNotFoundError: No module named 'game'</font>",
            "Run commands from inside the FlappyBirdAI folder (Step 2)."],
           ["<font face='Courier'>TTFError: Can't open file ... LiberationSerif-Regular.ttf</font>",
            "Install the Liberation fonts (Step 1) or edit FD in paperlib.py (Step 8)."],
           ["experiments.py finishes instantly", "All logs already exist. See Step 9."],
           ["play.py: no window appears", "It needs a desktop. On a remote server use Steps 6-8 instead."],
           ["First run of a script is slow", "numba is compiling the simulator. Later runs use the cache."]],
          [7 * cm, 9.5 * cm]),
    Paragraph("Command summary", H2),
    code("git clone https://github.com/Anish-185/FlappyBirdAI.git && cd FlappyBirdAI\n"
         "python -m venv .venv && source .venv/bin/activate\n"
         "pip install -r requirements.txt\n"
         "python play.py           # watch the bird\n"
         "python analysis.py       # statistics\n"
         "python figures.py        # figures/\n"
         "python build_paper.py    # paper PDF\n"
         "python experiments.py    # retrain (only after moving logs/ aside)")]


def footer(canvas, doc):
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"page {doc.page}")


if __name__ == "__main__":
    SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=1.8 * cm,
                      bottomMargin=1.8 * cm, title="Flappy Bird AI - How to Run").build(
        story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", OUT)
