"""Rebuild the one-page print and copy reference linked from the streaks guide."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "print-quality-reference.pdf"


def make_reference():
    # Embed the Vera fonts shipped with ReportLab so the samples render consistently.
    for name, filename in [("Vera", "Vera.ttf"), ("VeraBold", "VeraBd.ttf")]:
        pdfmetrics.registerFont(TTFont(name, filename))
    page = Canvas(str(OUTPUT), pagesize=letter, invariant=True, pageCompression=1)
    page.setTitle("Print and copy comparison sheet | Printer Resolve")
    page.setAuthor("Printer Resolve")
    page.setSubject("Visual comparisons for missing bands, pale text and copy-only lines")

    def text(x, y, value, size=11, bold=False):
        page.setFillGray(0.12)
        page.setFont("VeraBold" if bold else "Vera", size)
        page.drawString(x, y, value)

    def section(y, heading):
        page.setStrokeGray(0.7)
        page.setLineWidth(0.6)
        page.line(54, y + 18, 558, y + 18)
        text(54, y, heading, 13, bold=True)

    text(54, 742, "PRINTER RESOLVE", 10, bold=True)
    text(54, 704, "Print and copy comparison sheet", 24, bold=True)
    text(54, 680, "Print one copy on plain paper. Use Fit for A4 or US Letter. Mark the top edge")
    text(54, 665, "and keep its orientation the same for the flatbed and feeder copies.")

    section(620, "1   Compare the same marks across the page")
    for x, label in [(54, "LEFT"), (231, "CENTRE"), (408, "RIGHT")]:
        text(x, 594, label, 9, bold=True)
        text(x, 566, "Aa 28 / Mm 64", 16)
        for i in range(6):
            page.setFillGray(0)
            page.rect(x, 547 - i * 7, 150, 2, stroke=0, fill=1)

    section(475, "2   Look for a missing band or an uneven block")
    # DeviceGray lightness, with identical page geometry for all four patches.
    for x, level, label in [(54, 0.0, "Black"), (183, 0.25, "Dark grey"),
                            (312, 0.50, "Mid-grey"), (441, 0.75, "Light grey")]:
        page.setFillGray(level)
        page.rect(x, 408, 117, 40, stroke=0, fill=1)
        text(x, 390, label, 10)
    text(54, 365, "Each block is uniform in the file. The paper, print mode and driver affect its shade.", 10)

    section(320, "3   Check the white area for an added line")
    text(54, 298, "The space between these two small marks is intentionally empty.", 10)
    for x in [54, 551]:
        page.setLineWidth(1.1)
        page.setStrokeGray(0.25)
        page.line(x, 253, x + 7, 253)

    section(183, "Record which output first shows the mark")
    for i, (name, hint) in enumerate([("Direct print", "Compare with this PDF on screen."),
                                      ("Flatbed copy", "Use a clean direct print or a known-clean original."),
                                      ("Feeder copy", "Use that same original, once, in the same orientation.")]):
        y = 155 - i * 22
        text(54, y, name, 11, bold=True)
        text(153, y, hint, 10)
    text(54, 70, "Interpret the results at printerresolve.com/printer-faded-streaked-pages", 10)
    page.showPage()
    page.save()


if __name__ == "__main__":
    make_reference()
