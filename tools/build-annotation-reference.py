"""Build a two-page PDF with identical visible notes and different print flags."""

from pathlib import Path

import pymupdf


output = Path(__file__).resolve().parents[1] / "assets" / "pdf-annotation-print-check.pdf"

with pymupdf.open() as document:
    document.set_metadata({
        "title": "PDF annotation print comparison",
        "author": "Printer Resolve",
        "subject": "A controlled example of a screen-only note and a printable note",
    })
    for flags in [0, pymupdf.PDF_ANNOT_IS_PRINT]:
        page = document.new_page(width=612, height=792)
        note = page.add_freetext_annot(
            pymupdf.Rect(80, 80, 490, 129), "Receipt 4187", fontsize=18,
            text_color=(0, 0, 0),
        )
        note.set_flags(flags)
        note.update()
    document.save(output, no_new_id=True, deflate=True)
