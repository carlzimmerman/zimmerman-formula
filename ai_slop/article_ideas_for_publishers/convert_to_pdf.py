#!/usr/bin/env python3
"""
Convert Z² Framework article markdown files to PDF format.
Uses fpdf2 for PDF generation with custom styling for academic publications.
"""

import os
import re
from fpdf import FPDF
from pathlib import Path

class ArticlePDF(FPDF):
    """Custom PDF class for academic-style articles."""

    def __init__(self, title=""):
        super().__init__()
        self.title_text = title
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, self.title_text[:60] + "..." if len(self.title_text) > 60 else self.title_text, align='C')
            self.ln(15)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def parse_markdown(md_content):
    """Parse markdown content into structured elements."""
    elements = []
    lines = md_content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            elements.append(('blank', ''))
            i += 1
            continue

        # Headers
        if line.startswith('# '):
            elements.append(('h1', line[2:].strip()))
        elif line.startswith('## '):
            elements.append(('h2', line[3:].strip()))
        elif line.startswith('### '):
            elements.append(('h3', line[4:].strip()))
        elif line.startswith('#### '):
            elements.append(('h4', line[5:].strip()))

        # Horizontal rule
        elif line.strip() in ['---', '***', '___']:
            elements.append(('hr', ''))

        # Tables
        elif '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            elements.append(('table', table_lines))
            continue

        # Code blocks
        elif line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            elements.append(('code', '\n'.join(code_lines)))

        # Block quotes
        elif line.startswith('>'):
            elements.append(('quote', line[1:].strip()))

        # List items
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            elements.append(('list', line.strip()[2:]))
        elif re.match(r'^\d+\.\s', line.strip()):
            elements.append(('numlist', re.sub(r'^\d+\.\s', '', line.strip())))

        # Bold/italic emphasis (inline)
        elif line.startswith('**') and line.endswith('**'):
            elements.append(('bold', line[2:-2]))
        elif line.startswith('*') and line.endswith('*'):
            elements.append(('italic', line[1:-1]))

        # Regular paragraph
        else:
            elements.append(('para', line.strip()))

        i += 1

    return elements

def clean_text(text):
    """Remove markdown formatting for plain text output."""
    # Handle bullet points and special chars FIRST before any other processing
    text = text.replace('\u2022', '-')  # bullet point
    text = text.replace('\u2023', '-')  # triangular bullet
    text = text.replace('\u2043', '-')  # hyphen bullet
    text = text.replace('\u25E6', 'o')  # white bullet
    text = text.replace('\u2219', '-')  # bullet operator
    text = text.replace('•', '-').replace('·', '-').replace('○', 'o')
    # Remove bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Remove italic
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Remove inline code
    text = re.sub(r'`(.+?)`', r'\1', text)
    # Remove links
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Clean up special chars for PDF
    text = text.replace('²', '2').replace('⁸', '8').replace('⁴', '4').replace('³', '3')
    text = text.replace('π', 'pi').replace('α', 'alpha').replace('Λ', 'Lambda')
    text = text.replace('μ', 'mu').replace('Ω', 'Omega').replace('θ', 'theta')
    text = text.replace('≈', '~').replace('×', 'x').replace('→', '->')
    text = text.replace('ℏ', 'h-bar').replace('ψ', 'psi').replace('φ', 'phi')
    text = text.replace('∝', 'proportional to').replace('∫', 'integral')
    text = text.replace('Σ', 'Sum').replace('δ', 'delta').replace('β', 'beta')
    text = text.replace('γ', 'gamma').replace('ω', 'omega').replace('τ', 'tau')
    text = text.replace('η', 'eta').replace('ε', 'epsilon').replace('ρ', 'rho')
    text = text.replace('σ', 'sigma').replace('λ', 'lambda').replace('ν', 'nu')
    text = text.replace('χ', 'chi').replace('κ', 'kappa').replace('ζ', 'zeta')
    text = text.replace('⊕', '+').replace('⟩', '>').replace('⟨', '<')
    text = text.replace('℃', 'C').replace('−', '-').replace('±', '+/-')
    text = text.replace(''', "'").replace(''', "'").replace('"', '"').replace('"', '"')
    text = text.replace('—', '-').replace('–', '-')
    # More special characters
    text = text.replace('≤', '<=').replace('≥', '>=').replace('≠', '!=')
    text = text.replace('∞', 'infinity').replace('√', 'sqrt').replace('∂', 'd')
    text = text.replace('∇', 'nabla').replace('⁵', '5').replace('⁶', '6')
    text = text.replace('⁷', '7').replace('⁹', '9').replace('⁰', '0').replace('¹', '1')
    text = text.replace('₀', '0').replace('₁', '1').replace('₂', '2').replace('₃', '3')
    text = text.replace('₄', '4').replace('₅', '5').replace('ℝ', 'R').replace('ℤ', 'Z')
    text = text.replace('É', 'E').replace('é', 'e').replace('ü', 'u').replace('ö', 'o')
    # Encode to latin-1 compatible, replacing any remaining problematic chars
    return text.encode('latin-1', errors='replace').decode('latin-1')

def convert_md_to_pdf(md_file, pdf_file):
    """Convert a markdown file to PDF."""
    print(f"Converting {md_file} to PDF...")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title from first H1
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Z2 Framework Article"
    title = clean_text(title)

    elements = parse_markdown(content)

    pdf = ArticlePDF(title)
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.multi_cell(0, 10, title, align='C')
    pdf.ln(5)

    # Process elements
    for elem_type, elem_content in elements:
        if elem_type == 'blank':
            pdf.ln(3)

        elif elem_type == 'h1':
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 16)
            pdf.multi_cell(0, 8, clean_text(elem_content))
            pdf.ln(3)

        elif elem_type == 'h2':
            pdf.ln(4)
            pdf.set_font('Helvetica', 'B', 14)
            pdf.multi_cell(0, 7, clean_text(elem_content))
            pdf.ln(2)

        elif elem_type == 'h3':
            pdf.ln(3)
            pdf.set_font('Helvetica', 'B', 12)
            pdf.multi_cell(0, 6, clean_text(elem_content))
            pdf.ln(2)

        elif elem_type == 'h4':
            pdf.ln(2)
            pdf.set_font('Helvetica', 'BI', 11)
            pdf.multi_cell(0, 6, clean_text(elem_content))
            pdf.ln(1)

        elif elem_type == 'hr':
            pdf.ln(3)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(3)

        elif elem_type == 'para':
            pdf.set_font('Helvetica', '', 10)
            pdf.multi_cell(0, 5, clean_text(elem_content))

        elif elem_type == 'quote':
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_x(25)
            pdf.multi_cell(0, 5, clean_text(elem_content))
            pdf.set_x(10)

        elif elem_type == 'list':
            pdf.set_font('Helvetica', '', 10)
            pdf.set_x(20)
            pdf.multi_cell(0, 5, "- " + clean_text(elem_content))

        elif elem_type == 'numlist':
            pdf.set_font('Helvetica', '', 10)
            pdf.set_x(20)
            pdf.multi_cell(0, 5, clean_text(elem_content))

        elif elem_type == 'code':
            pdf.set_font('Courier', '', 9)
            pdf.set_fill_color(245, 245, 245)
            for code_line in elem_content.split('\n'):
                pdf.set_x(15)
                pdf.cell(180, 5, clean_text(code_line)[:90], fill=True)
                pdf.ln()
            pdf.ln(2)

        elif elem_type == 'table':
            pdf.set_font('Helvetica', '', 9)
            for i, row in enumerate(elem_content):
                if '---' in row:
                    continue
                cells = [c.strip() for c in row.split('|') if c.strip()]
                if cells:
                    col_width = 180 / len(cells)
                    for cell in cells:
                        if i == 0:
                            pdf.set_font('Helvetica', 'B', 9)
                        else:
                            pdf.set_font('Helvetica', '', 9)
                        pdf.cell(col_width, 6, clean_text(cell)[:25], border=1)
                    pdf.ln()
            pdf.ln(3)

        elif elem_type == 'bold':
            pdf.set_font('Helvetica', 'B', 10)
            pdf.multi_cell(0, 5, clean_text(elem_content))

        elif elem_type == 'italic':
            pdf.set_font('Helvetica', 'I', 10)
            pdf.multi_cell(0, 5, clean_text(elem_content))

    # Save PDF
    pdf.output(pdf_file)
    print(f"  Created: {pdf_file}")

def main():
    """Convert all article markdown files to PDF."""
    script_dir = Path(__file__).parent

    articles = [
        "NATURE_article_full.md",
        "NATURE_PHYSICS_article_full.md",
        "SCIENCE_article_full.md",
        "QUANTA_MAGAZINE_article_full.md",
        "SCIENTIFIC_AMERICAN_article_full.md",
        "PHYSICS_TODAY_article_full.md"
    ]

    for article in articles:
        md_path = script_dir / article
        if md_path.exists():
            pdf_path = script_dir / article.replace('.md', '.pdf')
            try:
                convert_md_to_pdf(str(md_path), str(pdf_path))
            except Exception as e:
                print(f"  Error converting {article}: {e}")
        else:
            print(f"  Skipping {article} (not found)")

    print("\nDone! PDFs created in article_ideas_for_publishers/")

if __name__ == "__main__":
    main()
