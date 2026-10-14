"""Extract historical evidence, check arithmetic, and render the chronology note."""
import hashlib
import html
import json
import re
import subprocess
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STEM = "PREDICTION_CHRONOLOGY_2026"
EVIDENCE = HERE / (STEM + "_evidence")
SNAPSHOTS = [
    ("e1603604aa02e06e5dd397234295e87bb4654b64", "zimmerman_formula.md", "march17_original_manuscript.md"),
    ("3d8c0388f0d13b6f6563143ecc0e0793e1d71519", "real_research/reviews/project_a0z_MUSE_DARK_III_confrontation.py", "june05_confrontation.py"),
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def evidence():
    EVIDENCE.mkdir(exist_ok=True)
    entries = []
    for commit, original, name in SNAPSHOTS:
        raw = git("show", f"{commit}:{original}")
        (EVIDENCE / name).write_bytes(raw)
        author, committer = git("show", "-s", "--format=%aI%n%cI", commit).decode().strip().splitlines()
        entries.append(dict(commit=commit, original_path=original, snapshot=name,
                            author_date=author, committer_date=committer,
                            sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)))
    march = (EVIDENCE / SNAPSHOTS[0][2]).read_text()
    june = (EVIDENCE / SNAPSHOTS[1][2]).read_text()
    assert "2.14 × 10⁻¹⁰" in march and "1.79" in march
    assert "CANONICAL" in june and "CONSTANT" in june and "rho_Lambda" in june
    days = (datetime.fromisoformat("2026-04-24T14:41:00+00:00") - datetime.fromisoformat(entries[0]["committer_date"])).total_seconds() / 86400
    offset = (2.14 - 2.38) / 2.38 * 100
    rise = ((0.315 * 1.09**3 + 0.685)**0.5 - 1) * 100
    assert 37.46 < days < 37.47 and -10.09 < offset < -10.08 and 4.54 < rise < 4.55
    manifest = dict(audit_date="2026-10-14", scope="2026-04-13 through 2026-10-13",
                    snapshots=entries,
                    calculations=dict(days_march_commit_to_muse_submission=days,
                                      march_table_minus_muse_summary_percent=offset,
                                      march_table_minus_muse_mond_rar_percent=(2.14-2.19)/2.19*100,
                                      march_table_minus_muse_mond_median_percent=(2.14-2.27)/2.27*100,
                                      E_at_z_009_minus_one_percent=rise),
                    limitations=["Public Zenodo records establish an earlier related functional forecast, with a slightly different normalization",
                                 "ArXiv submission is not telescope data acquisition",
                                 "No galaxy likelihood fit or Alcock reanalysis reproduced"],
                    sources=[dict(id="2604.22613v1", submitted="2026-04-24T14:41:00Z", checked="2026-10-13", extraction="Primary HTML sections 2-4, Appendices B-E, including Eq. (13)"),
                             dict(id="2608.03576v1", submitted="2026-08-04T12:32:42Z", checked="2026-10-13", extraction="Primary HTML section 4.5 and Table 4"),
                             dict(id="2609.38796v1", submitted_date="2026-09-30", checked="2026-10-13", extraction="Abstract only; full HTML unavailable")])
    (EVIDENCE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    audit = ROOT / "real_research/reviews/muse_frozen_march_audit_2026_10_13"
    audit_files = sorted(p for p in audit.iterdir() if p.is_file() and p.suffix in {".py", ".md", ".json", ".csv", ".pdf", ".png"})
    manifest["followup_audit_files"] = [dict(name=p.name, sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in audit_files]
    (EVIDENCE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with zipfile.ZipFile(HERE / (STEM + "_evidence.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(EVIDENCE.iterdir()):
            z.write(path, arcname=path.name)
        for path in audit_files:
            z.write(path, arcname="followup_audit/" + path.name)
    print(json.dumps(manifest["calculations"], indent=2))


def render():
    font_dir = Path("/opt/homebrew/Caskroom/miniconda/base/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf")
    for name, suffix in [("NoteSerif", ""), ("NoteSerifBold", "-Bold"), ("NoteSerifItalic", "-Italic")]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / f"DejaVuSerif{suffix}.ttf")))
    pdfmetrics.registerFontFamily("NoteSerif", normal="NoteSerif", bold="NoteSerifBold", italic="NoteSerifItalic", boldItalic="NoteSerifBold")
    styles = {
        "body": ParagraphStyle("body", fontName="NoteSerif", fontSize=9.8, leading=14.0, alignment=TA_JUSTIFY, spaceAfter=7, allowWidows=0, allowOrphans=0),
        "title": ParagraphStyle("title", fontName="NoteSerifBold", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=12),
        "heading": ParagraphStyle("heading", fontName="NoteSerifBold", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=6, keepWithNext=True),
        "meta": ParagraphStyle("meta", fontName="NoteSerif", fontSize=9, leading=13, alignment=TA_CENTER, spaceAfter=8),
        "equation": ParagraphStyle("equation", fontName="NoteSerif", fontSize=10, leading=15, alignment=TA_CENTER, spaceAfter=3),
        "cell": ParagraphStyle("cell", fontName="NoteSerif", fontSize=8, leading=11),
        "reference": ParagraphStyle("reference", fontName="NoteSerif", fontSize=8, leading=11, spaceAfter=7, wordWrap="CJK"),
    }
    source = (HERE / (STEM + ".md")).read_text()
    title = source.splitlines()[0][2:]
    pdf_path = HERE / (STEM + ".pdf")
    doc = SimpleDocTemplate(str(pdf_path), pagesize=(612, 792), leftMargin=53, rightMargin=53,
                            topMargin=48, bottomMargin=65, title=title, author="Carl P. Zimmerman")

    def markup(s):
        return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", html.escape(s))

    story = []
    for block in source.strip().split("\n\n"):
        if block.startswith("# "):
            story.append(Paragraph(markup(block[2:]), styles["title"]))
        elif block.startswith("## "):
            story.append(Paragraph(markup(block[3:]), styles["heading"]))
        elif block.startswith("    "):
            for line in block.splitlines():
                story.append(Paragraph(markup(line.strip()), styles["equation"]))
            story.append(Spacer(1, 5))
        elif block.startswith("| "):
            rows = [line for line in block.splitlines() if not line.startswith("|---")]
            cells = [[Paragraph(markup(s.strip()), styles["cell"]) for s in row.strip("|").split("|")] for row in rows]
            widths = [40, 155, 185, 126] if len(cells[0]) == 4 else [132, 69, 305]
            table = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9eef3")),
                                       ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                       ("LINEBELOW", (0, 0), (-1, 0), .6, colors.grey),
                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                                       ("TOPPADDING", (0, 0), (-1, -1), 6)]))
            story.extend([table, Spacer(1, 9)])
        else:
            style = "reference" if re.match(r"\[\d\]", block) else "meta" if block.startswith(("**Carl", "October ")) else "body"
            story.append(Paragraph(markup(block.replace("\n", " ")), styles[style]))

    def footer(canvas, _):
        canvas.setFont("NoteSerif", 8)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(53, 28, "Zimmerman | Prediction chronology | October 14, 2026")
        canvas.drawRightString(559, 28, str(canvas.getPageNumber()))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    abstract = source.split("## Abstract\n\n", 1)[1].split("\n\n##", 1)[0]
    metadata = dict(upload_type="publication", publication_type="preprint", title=title,
                    creators=[dict(name="Zimmerman, Carl P.", affiliation="Briar Creek Tech")],
                    description="<p>" + html.escape(abstract) + "</p>",
                    publication_date="2026-10-14", version="1.2", language="eng",
                    access_right="open", license="cc-by-4.0",
                    keywords=["MOND", "radial acceleration relation", "prediction chronology", "MUSE-DARK", "MIGHTEE", "JUNO", "reproducibility"],
                    related_identifiers=[dict(identifier="10.48550/arXiv.2604.22613", relation="cites", scheme="doi"),
                                         dict(identifier="10.48550/arXiv.2608.03576", relation="cites", scheme="doi")])
    (HERE / (STEM + ".zenodo.json")).write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    print(f"Built {pdf_path.name} ({pdf_path.stat().st_size} bytes)")


if __name__ == "__main__":
    evidence()
    render()
