"""Assemble the paper PDF."""
import datetime as dt
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Spacer,
                                Paragraph, NextPageTemplate, PageBreak)
from reportlab.lib.units import mm

from paperlib import PAGE, LM, RM, TM, BM, W, ST, GREY, INK
import paper_content as K

OUT = "Flappy_Bird_Neuroevolution_Paper.pdf"
TITLE = "Neuroevolution of a Flappy Bird Controller"
RUN = "Neuroevolution of a Flappy Bird Controller: operators, evaluation noise and generalisation"


def chrome(canvas, doc):
    canvas.saveState()
    n = canvas.getPageNumber()
    canvas.setFont("Serif", 8)
    canvas.setFillColor(GREY)
    if n > 1:
        canvas.drawString(LM, PAGE[1] - TM + 9 * mm, RUN)
        canvas.setStrokeColor(colors.HexColor("#bbbbbb"))
        canvas.setLineWidth(0.4)
        canvas.line(LM, PAGE[1] - TM + 7.5 * mm, PAGE[0] - RM, PAGE[1] - TM + 7.5 * mm)
    canvas.setFont("Serif", 9)
    canvas.drawCentredString(PAGE[0] / 2, BM - 12 * mm, str(n))
    canvas.restoreState()


def main():
    doc = BaseDocTemplate(OUT, pagesize=PAGE, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM, title=TITLE,
                          author="Author Name", subject="Neuroevolution empirical study")
    frame = Frame(LM, BM, W, PAGE[1] - TM - BM, id="body",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="body", frames=[frame], onPage=chrome)])

    story = []
    story += K.front()
    for fn in (K.sec1, K.sec2, K.sec3, K.sec4, K.sec5, K.sec6, K.sec7, K.sec8, K.sec9):
        story += fn()
    refs, uncited = K.back()
    story += refs
    doc.build(story)
    print("pages written ->", OUT)
    if uncited:
        print("WARNING uncited refs:", uncited)


if __name__ == "__main__":
    main()
