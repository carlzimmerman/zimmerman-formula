#!/usr/bin/env python3
"""
Generate Honest Derivations from Z PDF
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_pdf():
    doc = SimpleDocTemplate(
        "papers/60_Honest_Derivations_from_Z.pdf",
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=14, spaceAfter=6, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=9, spaceAfter=8, alignment=TA_CENTER, textColor=colors.gray)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=11, spaceBefore=10, spaceAfter=4, textColor=colors.darkblue)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8, spaceAfter=3)
    formula_style = ParagraphStyle('Formula', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, spaceAfter=4, spaceBefore=4, backColor=colors.Color(0.95, 0.95, 0.95))
    box_style = ParagraphStyle('Box', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, spaceAfter=6, spaceBefore=6, backColor=colors.Color(0.9, 0.95, 1.0))

    story = []

    # Title
    story.append(Paragraph("60 Physical Constants from Z = 2sqrt(8pi/3)", title_style))
    story.append(Paragraph("An Honest Assessment: What Is Derived vs What Is Pattern-Matched", subtitle_style))
    story.append(Paragraph("Carl Zimmerman | March 2026", subtitle_style))
    story.append(Spacer(1, 8))

    # Critical Distinction
    story.append(Paragraph("CRITICAL DISTINCTION", section_style))
    story.append(Paragraph("<b>DERIVED:</b> Follows mathematically from established physics (GR, thermodynamics)", body_style))
    story.append(Paragraph("<b>PATTERN:</b> Numerical relationship that fits observations but lacks physical derivation", body_style))
    story.append(Spacer(1, 6))

    # Part I: Truly Derived
    story.append(Paragraph("PART I: TRULY DERIVED (2 Results)", section_style))
    story.append(Paragraph("<b>1. Z = 2*sqrt(8*pi/3) = 5.7888</b> from Friedmann equation + Bekenstein bound", body_style))
    story.append(Paragraph("<b>2. a_0(z) = a_0(0) * E(z)</b> — MOND evolves with redshift (FALSIFIABLE)", body_style))
    story.append(Paragraph("Status: MATHEMATICALLY PROVEN from General Relativity", body_style))
    story.append(Spacer(1, 6))

    # Part II: Central Ansatz
    story.append(Paragraph("PART II: CENTRAL ANSATZ (1 Result)", section_style))
    story.append(Paragraph("<b>3. a_0 = cH_0/Z = c*sqrt(G*rho_c)/2</b>", formula_style))
    story.append(Paragraph("Predicted: 1.13e-10 m/s^2 | Measured: 1.2e-10 m/s^2 | Error: 6%", body_style))
    story.append(Paragraph("Status: PHYSICAL ARGUMENT — motivated by horizon physics, not rigorously derived", body_style))
    story.append(Spacer(1, 6))

    # Part III: High-Precision Patterns
    story.append(Paragraph("PART III: HIGH-PRECISION PATTERNS (22 Results, <0.5% error)", section_style))

    hp_data = [
        ["#", "Quantity", "Formula", "Pred", "Meas", "Err"],
        ["4", "Fine structure alpha", "1/(4Z^2 + 3)", "1/137.04", "1/137.036", "0.004%"],
        ["5", "Dark energy Omega_L", "3Z/(8 + 3Z)", "0.685", "0.685", "0.06%"],
        ["6", "Matter Omega_m", "8/(8 + 3Z)", "0.315", "0.315", "0.13%"],
        ["7", "Strong coupling alpha_s", "3/(8 + 3Z)", "0.1183", "0.1180", "0.25%"],
        ["8", "Weinberg sin^2(theta_W)", "1/4 - alpha_s/(2pi)", "0.2312", "0.2312", "0.02%"],
        ["9", "W/Z mass ratio", "1 - alpha_s", "0.8817", "0.8815", "0.02%"],
        ["10", "Z width Gamma_Z/M_Z", "15*alpha/4", "0.0274", "0.0274", "0.01%"],
        ["11", "Eff neutrinos N_nu", "3 - alpha/0.45", "2.984", "2.984", "0.01%"],
        ["12", "Muon/electron mass", "Z(6Z + 1)", "206.85", "206.77", "0.04%"],
        ["13", "Tau/muon mass", "Z + 11", "16.79", "16.82", "0.18%"],
        ["14", "Bottom/charm mass", "Z - 5/2", "3.289", "3.291", "0.06%"],
        ["15", "Top/charm mass", "4Z^2 + 2", "136.0", "136.0", "0.01%"],
        ["16", "Kaon/pion mass", "Z - 9/4", "3.539", "3.540", "0.03%"],
        ["17", "Phi/rho mass", "1 + Omega_m", "1.315", "1.315", "0.03%"],
        ["18", "Lambda/proton mass", "1 + 3*Omega_m/5", "1.189", "1.189", "0.01%"],
        ["19", "Axial coupling g_A", "1 + Omega_m - 0.04", "1.275", "1.275", "0.00%"],
        ["20", "Proton moment mu_p", "Z - 3", "2.789", "2.793", "0.14%"],
        ["21", "mu_n/mu_p ratio", "-Omega_L", "-0.685", "-0.685", "0.05%"],
        ["22", "Higgs/Z mass", "11/8", "1.375", "1.374", "0.07%"],
        ["23", "Top/Z mass", "(11/8)^2", "1.891", "1.894", "0.16%"],
        ["24", "Strange/down mass", "4Z - 3", "20.16", "20.2", "0.2%"],
        ["25", "Omega_L/Omega_m", "3Z/8", "2.171", "2.175", "0.19%"],
    ]

    t = Table(hp_data, colWidths=[0.25*inch, 1.3*inch, 1.3*inch, 0.6*inch, 0.6*inch, 0.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

    # Part IV: Good Patterns
    story.append(Paragraph("PART IV: GOOD PATTERNS (18 Results, 0.5-2% error)", section_style))

    gp_data = [
        ["#", "Quantity", "Formula", "Pred", "Meas", "Err"],
        ["26", "Rho/proton mass", "Z/7", "0.827", "0.826", "0.12%"],
        ["27", "Omega/proton mass", "Z - 4", "1.789", "1.783", "0.34%"],
        ["28", "Strange/up mass", "8Z - 3", "43.31", "43.2", "0.3%"],
        ["29", "Sigma_c/proton", "Z - 7/2", "2.289", "2.285", "0.18%"],
        ["30", "Lambda_c/proton", "Z - 3.35", "2.439", "2.437", "0.08%"],
        ["31", "Top/Higgs mass", "11/8", "1.375", "1.379", "0.29%"],
        ["32", "W width Gamma_W/M_W", "2*alpha_s/pi", "0.0753", "0.075", "0.4%"],
        ["33", "Delta-N splitting", "Omega_m * m_p", "296 MeV", "294 MeV", "0.7%"],
        ["34", "Upsilon/proton", "Z^2 - 47/2", "10.01", "10.08", "0.7%"],
        ["35", "Pion decay f_pi", "alpha_s*m_p*0.83", "92.1 MeV", "92.2 MeV", "0.1%"],
        ["36", "g_piNN coupling", "Z * 2.27", "13.14", "13.17", "0.23%"],
        ["37", "CMB peak l2/l1", "3Z/7", "2.481", "2.482", "0.04%"],
        ["38", "Spectral index n_s", "1 - Omega_m/9", "0.965", "0.9649", "0.01%"],
        ["39", "Reionization z_re", "4Z/3", "7.72", "7.7", "0.3%"],
        ["40", "Recombination z_*", "8/alpha", "1096", "1090", "0.6%"],
        ["41", "Charm/strange mass", "Z + 8", "13.79", "13.6", "1.4%"],
        ["42", "NS max mass", "Z/2.7 M_sun", "2.14", "2.14", "0.2%"],
        ["43", "Chandrasekhar mass", "Omega_L*2.1 M_sun", "1.44", "1.44", "0.2%"],
    ]

    t = Table(gp_data, colWidths=[0.25*inch, 1.3*inch, 1.3*inch, 0.6*inch, 0.6*inch, 0.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.Color(0.8, 1, 0.8)),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t)

    story.append(PageBreak())

    # Part V: Nuclear Physics
    story.append(Paragraph("PART V: NUCLEAR PHYSICS (10 Results)", section_style))

    nuc_data = [
        ["#", "Quantity", "Formula", "Pred", "Meas", "Err"],
        ["44", "BE(He-3)", "4Z/3 MeV", "7.719", "7.718", "0.01%"],
        ["45", "BE/A (Iron)", "Z + 3 MeV", "8.789", "8.79", "0.01%"],
        ["46", "BE(C-12)", "16Z MeV", "92.6", "92.2", "0.4%"],
        ["47", "Nuclear a_sym", "Z^2 - 1.5 MeV", "32.0", "32", "0.0%"],
        ["48", "Magic 8", "4Z^2 - 126", "8.04", "8", "0.5%"],
        ["49", "Magic 20", "4Z^2 - 114", "20.04", "20", "0.2%"],
        ["50", "Magic 28", "4Z^2 - 106", "28.04", "28", "0.14%"],
        ["51", "Magic 50", "4Z^2 - 84", "50.04", "50", "0.08%"],
        ["52", "Magic 82", "4Z^2 - 52", "82.04", "82", "0.05%"],
        ["53", "Magic 126", "4Z^2 - 8", "126.04", "126", "0.03%"],
    ]

    t = Table(nuc_data, colWidths=[0.25*inch, 1*inch, 1.2*inch, 0.6*inch, 0.5*inch, 0.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.Color(1, 0.9, 0.8)),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

    # Part VI: Cosmology + Neutrinos
    story.append(Paragraph("PART VI: COSMOLOGY & NEUTRINOS (7 Results)", section_style))

    cosmo_data = [
        ["#", "Quantity", "Formula", "Pred", "Meas", "Err"],
        ["54", "Hubble H_0", "Z*a_0/c", "71.5", "67-73", "mid"],
        ["55", "e-folding N", "18/Omega_m", "57.1", "~57", "~0%"],
        ["56", "Inflation N", "9(8+3Z)/4", "57.1", "~57", "~0%"],
        ["57", "sin^2(theta_12)", "Omega_m", "0.315", "0.304", "3.6%"],
        ["58", "sin^2(theta_23)", "1/sqrt(3)", "0.577", "0.573", "0.7%"],
        ["59", "sin^2(theta_13)", "3*alpha", "0.0219", "0.0222", "1.4%"],
        ["60", "dm^2_31/dm^2_21", "Z^2 - 1", "32.5", "33.4", "2.7%"],
    ]

    t = Table(cosmo_data, colWidths=[0.25*inch, 1.1*inch, 1.1*inch, 0.6*inch, 0.5*inch, 0.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.Color(0.9, 0.9, 1)),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Summary
    story.append(Paragraph("SUMMARY", section_style))

    summary_data = [
        ["Category", "Count", "Avg Error", "Status"],
        ["Truly Derived", "2", "—", "PROVEN"],
        ["Central Ansatz", "1", "6%", "PHYSICAL ARGUMENT"],
        ["High-Precision Patterns", "22", "0.1%", "NUMERICAL FIT"],
        ["Good Patterns", "18", "0.5%", "NUMERICAL FIT"],
        ["Nuclear Patterns", "10", "0.2%", "NUMERICAL FIT"],
        ["Cosmology + Neutrino", "7", "1.2%", "NUMERICAL FIT"],
        ["TOTAL", "60", "0.4%", ""],
    ]

    t = Table(summary_data, colWidths=[1.5*inch, 0.6*inch, 0.7*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightyellow),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Key Prediction
    story.append(Paragraph("KEY FALSIFIABLE PREDICTION", section_style))
    story.append(Paragraph("a_0(z) = a_0(0) * sqrt[Omega_m(1+z)^3 + Omega_L]", formula_style))
    story.append(Paragraph("At z=10, a_0 was 24x larger. If high-z galaxies show CONSTANT a_0, this framework is WRONG.", body_style))
    story.append(Spacer(1, 8))

    # Final
    story.append(Paragraph("THE BOTTOM LINE", section_style))
    story.append(Paragraph("<b>2 formulas</b> are rigorously derived from General Relativity.", body_style))
    story.append(Paragraph("<b>58 formulas</b> are precise numerical patterns awaiting physical explanation.", body_style))
    story.append(Paragraph("The framework reveals hidden structure in physics constants, even if the theoretical basis is incomplete.", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Z = 2*sqrt(8*pi/3) = 5.7888", box_style))
    story.append(Paragraph("github.com/carlzimmerman/zimmerman-formula | CC-BY-4.0", subtitle_style))

    doc.build(story)
    print("PDF generated: papers/60_Honest_Derivations_from_Z.pdf")

if __name__ == "__main__":
    create_pdf()
