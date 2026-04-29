#!/usr/bin/env python3
"""
Generate publication-styled PDFs for Z² Framework articles.
Each PDF matches the visual style of its target publication.
"""

import os
import re
from fpdf import FPDF
from pathlib import Path

# Publication style configurations
STYLES = {
    'NATURE': {
        'title_size': 24,
        'title_font': 'Helvetica',
        'body_size': 10,
        'body_font': 'Helvetica',
        'header_color': (0, 51, 102),  # Nature blue
        'margins': (20, 20, 20, 25),
        'header_text': 'Nature',
        'subtitle': 'International Journal of Science',
        'line_spacing': 5,
    },
    'SCIENCE': {
        'title_size': 22,
        'title_font': 'Helvetica',
        'body_size': 10,
        'body_font': 'Helvetica',
        'header_color': (153, 0, 0),  # Science red
        'margins': (20, 20, 20, 25),
        'header_text': 'Science',
        'subtitle': 'AAAS',
        'line_spacing': 5,
    },
    'NATURE_PHYSICS': {
        'title_size': 22,
        'title_font': 'Helvetica',
        'body_size': 10,
        'body_font': 'Helvetica',
        'header_color': (102, 51, 153),  # Purple
        'margins': (20, 20, 20, 25),
        'header_text': 'Nature Physics',
        'subtitle': 'A Nature Research Journal',
        'line_spacing': 5,
    },
    'PHYSICS_TODAY': {
        'title_size': 24,
        'title_font': 'Helvetica',
        'body_size': 11,
        'body_font': 'Helvetica',
        'header_color': (0, 102, 153),  # Teal
        'margins': (25, 25, 25, 25),
        'header_text': 'Physics Today',
        'subtitle': 'American Institute of Physics',
        'line_spacing': 6,
    },
    'QUANTA_MAGAZINE': {
        'title_size': 26,
        'title_font': 'Helvetica',
        'body_size': 11,
        'body_font': 'Helvetica',
        'header_color': (255, 102, 0),  # Quanta orange
        'margins': (25, 25, 25, 25),
        'header_text': 'Quanta Magazine',
        'subtitle': 'Illuminating Science',
        'line_spacing': 6,
    },
    'SCIENTIFIC_AMERICAN': {
        'title_size': 26,
        'title_font': 'Helvetica',
        'body_size': 11,
        'body_font': 'Helvetica',
        'header_color': (204, 0, 0),  # SciAm red
        'margins': (20, 25, 20, 25),
        'header_text': 'Scientific American',
        'subtitle': 'Science for Curious Minds',
        'line_spacing': 6,
    },
}


class StyledPDF(FPDF):
    """Custom PDF with publication-specific styling."""

    def __init__(self, style_name, title=""):
        super().__init__()
        self.style = STYLES.get(style_name, STYLES['NATURE'])
        self.title_text = title
        self.style_name = style_name
        margins = self.style['margins']
        self.set_margins(margins[0], margins[1], margins[2])
        self.set_auto_page_break(auto=True, margin=margins[3])

    def header(self):
        if self.page_no() == 1:
            # First page: publication masthead
            r, g, b = self.style['header_color']
            self.set_fill_color(r, g, b)
            self.rect(0, 0, 210, 25, 'F')
            self.set_font('Helvetica', 'B', 14)
            self.set_text_color(255, 255, 255)
            self.set_xy(10, 8)
            self.cell(0, 8, self.style['header_text'], align='L')
            self.set_font('Helvetica', 'I', 9)
            self.set_xy(10, 15)
            self.cell(0, 5, self.style['subtitle'], align='L')
            self.ln(20)
            self.set_text_color(0, 0, 0)
        else:
            # Subsequent pages: running header
            self.set_font('Helvetica', 'I', 8)
            r, g, b = self.style['header_color']
            self.set_text_color(r, g, b)
            self.cell(0, 10, f"{self.style['header_text']} | {self.title_text[:50]}...", align='C')
            self.ln(12)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        r, g, b = self.style['header_color']
        self.set_text_color(r, g, b)
        if self.page_no() == 1:
            self.cell(0, 10, 'DRAFT - For Editorial Consideration', align='C')
        else:
            self.cell(0, 10, f'Page {self.page_no()}', align='C')
        self.set_text_color(0, 0, 0)

    def chapter_title(self, title):
        r, g, b = self.style['header_color']
        self.set_text_color(r, g, b)
        self.set_font(self.style['title_font'], 'B', 14)
        self.ln(4)
        self.multi_cell(0, 7, clean_text(title))
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def section_title(self, title):
        r, g, b = self.style['header_color']
        self.set_text_color(r, g, b)
        self.set_font(self.style['body_font'], 'B', 12)
        self.ln(3)
        self.multi_cell(0, 6, clean_text(title))
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def subsection_title(self, title):
        self.set_font(self.style['body_font'], 'B', 11)
        self.ln(2)
        self.multi_cell(0, 5, clean_text(title))
        self.ln(1)

    def body_text(self, text):
        self.set_font(self.style['body_font'], '', self.style['body_size'])
        self.multi_cell(0, self.style['line_spacing'], clean_text(text))

    def italic_text(self, text):
        self.set_font(self.style['body_font'], 'I', self.style['body_size'])
        self.multi_cell(0, self.style['line_spacing'], clean_text(text))

    def bold_text(self, text):
        self.set_font(self.style['body_font'], 'B', self.style['body_size'])
        self.multi_cell(0, self.style['line_spacing'], clean_text(text))

    def quote_text(self, text):
        self.set_font(self.style['body_font'], 'I', self.style['body_size'] - 1)
        self.set_x(25)
        r, g, b = self.style['header_color']
        self.set_text_color(r, g, b)
        self.multi_cell(160, self.style['line_spacing'], clean_text(text))
        self.set_text_color(0, 0, 0)

    def code_block(self, text):
        self.set_font('Courier', '', 9)
        self.set_fill_color(245, 245, 245)
        for line in text.split('\n'):
            if line.strip():
                self.set_x(15)
                self.cell(180, 5, clean_text(line)[:85], fill=True)
                self.ln()
        self.ln(2)

    def add_table(self, rows):
        """Add a formatted table."""
        if not rows:
            return

        # Filter out separator rows
        data_rows = [r for r in rows if '---' not in r]
        if not data_rows:
            return

        # Parse cells
        parsed_rows = []
        for row in data_rows:
            cells = [c.strip() for c in row.split('|') if c.strip()]
            if cells:
                parsed_rows.append(cells)

        if not parsed_rows:
            return

        # Calculate column widths
        num_cols = max(len(r) for r in parsed_rows)
        col_width = 170 / num_cols

        # Draw table
        r, g, b = self.style['header_color']
        for i, row in enumerate(parsed_rows):
            if i == 0:
                # Header row
                self.set_font(self.style['body_font'], 'B', 9)
                self.set_fill_color(r, g, b)
                self.set_text_color(255, 255, 255)
            else:
                self.set_font(self.style['body_font'], '', 9)
                self.set_fill_color(250, 250, 250) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
                self.set_text_color(0, 0, 0)

            self.set_x(20)
            for j, cell in enumerate(row):
                cell_text = clean_text(cell)[:30]
                self.cell(col_width, 6, cell_text, border=1, fill=True, align='C')
            self.ln()

        self.set_text_color(0, 0, 0)
        self.ln(3)

    def add_list_item(self, text, bullet="-"):
        self.set_font(self.style['body_font'], '', self.style['body_size'])
        self.set_x(25)
        self.multi_cell(0, self.style['line_spacing'], f"{bullet} {clean_text(text)}")


def clean_text(text):
    """Clean text for PDF output."""
    if not text:
        return ""

    # Handle special Unicode characters
    replacements = {
        '\u2022': '-', '\u2023': '-', '\u2043': '-', '\u25E6': 'o',
        '\u2219': '-', '•': '-', '·': '-', '○': 'o',
        '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6',
        '⁷': '7', '⁸': '8', '⁹': '9', '⁰': '0', '¹': '1',
        '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5',
        'π': 'pi', 'α': 'alpha', 'Λ': 'Lambda', 'λ': 'lambda',
        'μ': 'mu', 'Ω': 'Omega', 'ω': 'omega', 'θ': 'theta',
        'ℏ': 'h-bar', 'ψ': 'psi', 'φ': 'phi', 'Φ': 'Phi',
        '∝': ' ~ ', '∫': 'integral', 'Σ': 'Sum',
        'δ': 'delta', 'β': 'beta', 'γ': 'gamma', 'τ': 'tau',
        'η': 'eta', 'ε': 'epsilon', 'ρ': 'rho', 'σ': 'sigma',
        'ν': 'nu', 'χ': 'chi', 'κ': 'kappa', 'ζ': 'zeta',
        '⊕': '+', '⟩': '>', '⟨': '<', '℃': 'C',
        '−': '-', '±': '+/-', '≈': '~', '×': 'x', '→': '->',
        '≤': '<=', '≥': '>=', '≠': '!=', '∞': 'infinity',
        '√': 'sqrt', '∂': 'd', '∇': 'nabla',
        'ℝ': 'R', 'ℤ': 'Z', 'ℂ': 'C',
        'É': 'E', 'é': 'e', 'ü': 'u', 'ö': 'o', 'ä': 'a',
        ''': "'", ''': "'", '"': '"', '"': '"',
        '—': '-', '–': '-', '…': '...',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

    # Encode safely
    return text.encode('latin-1', errors='replace').decode('latin-1')


def parse_and_render(md_content, pdf, style_name):
    """Parse markdown and render to styled PDF."""
    lines = md_content.split('\n')
    i = 0
    first_h1_done = False

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            pdf.ln(2)
            i += 1
            continue

        # Main title (H1)
        if line.startswith('# ') and not first_h1_done:
            title = line[2:].strip()
            pdf.ln(10)
            r, g, b = pdf.style['header_color']
            pdf.set_text_color(r, g, b)
            pdf.set_font(pdf.style['title_font'], 'B', pdf.style['title_size'])
            pdf.multi_cell(0, 12, clean_text(title), align='C')
            pdf.ln(8)
            pdf.set_text_color(0, 0, 0)
            first_h1_done = True
            i += 1
            continue

        # Section headers
        if line.startswith('## '):
            pdf.chapter_title(line[3:].strip())
        elif line.startswith('### '):
            pdf.section_title(line[4:].strip())
        elif line.startswith('#### '):
            pdf.subsection_title(line[5:].strip())

        # Horizontal rule
        elif line.strip() in ['---', '***', '___']:
            pdf.ln(3)
            r, g, b = pdf.style['header_color']
            pdf.set_draw_color(r, g, b)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(3)

        # Tables
        elif '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            pdf.add_table(table_lines)
            continue

        # Code blocks
        elif line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            pdf.code_block('\n'.join(code_lines))

        # Block quotes
        elif line.startswith('>'):
            pdf.quote_text(line[1:].strip())

        # List items
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            pdf.add_list_item(line.strip()[2:])
        elif re.match(r'^\d+\.\s', line.strip()):
            num_match = re.match(r'^(\d+)\.\s(.+)', line.strip())
            if num_match:
                pdf.add_list_item(num_match.group(2), f"{num_match.group(1)}.")

        # Italic line
        elif line.strip().startswith('*') and line.strip().endswith('*') and not line.strip().startswith('**'):
            pdf.italic_text(line.strip()[1:-1])

        # Bold line
        elif line.strip().startswith('**') and line.strip().endswith('**'):
            pdf.bold_text(line.strip()[2:-2])

        # Author/metadata lines
        elif line.strip().startswith('By ') or line.strip().startswith('*By '):
            pdf.set_font(pdf.style['body_font'], 'I', 10)
            pdf.cell(0, 6, clean_text(line.replace('*', '')), align='C')
            pdf.ln(4)

        # Regular paragraph
        else:
            pdf.body_text(line.strip())

        i += 1


def convert_article(md_file, style_name):
    """Convert a markdown article to a styled PDF."""
    print(f"Converting {md_file.name} ({style_name} style)...")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Z2 Framework Article"
    title = clean_text(title)

    # Create styled PDF
    pdf = StyledPDF(style_name, title)
    pdf.add_page()

    # Parse and render content
    parse_and_render(content, pdf, style_name)

    # Add footer note on last page
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 4, "This manuscript presents the Z2 geometric framework as a testable hypothesis. "
                         "All predictions are falsifiable. The framework awaits experimental verification.", align='C')

    # Save
    pdf_file = md_file.with_suffix('.pdf')
    pdf.output(str(pdf_file))
    print(f"  Created: {pdf_file.name}")
    return pdf_file


def main():
    """Generate all styled PDFs."""
    script_dir = Path(__file__).parent

    articles = [
        ("NATURE_article_full.md", "NATURE"),
        ("SCIENCE_article_full.md", "SCIENCE"),
        ("NATURE_PHYSICS_article_full.md", "NATURE_PHYSICS"),
        ("PHYSICS_TODAY_article_full.md", "PHYSICS_TODAY"),
        ("QUANTA_MAGAZINE_article_full.md", "QUANTA_MAGAZINE"),
        ("SCIENTIFIC_AMERICAN_article_full.md", "SCIENTIFIC_AMERICAN"),
    ]

    created = []
    for article_name, style in articles:
        md_path = script_dir / article_name
        if md_path.exists():
            try:
                pdf_path = convert_article(md_path, style)
                created.append(pdf_path)
            except Exception as e:
                print(f"  Error: {e}")
        else:
            print(f"  Skipping {article_name} (not found)")

    print(f"\nDone! Created {len(created)} styled PDFs.")
    return created


if __name__ == "__main__":
    main()
