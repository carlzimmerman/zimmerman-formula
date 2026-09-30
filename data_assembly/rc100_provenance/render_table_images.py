#!/usr/bin/env python3
"""Render the three raster images of Table 3 of Nestor Shachar+2023 (arXiv:2209.12199; PDF pages 27-29) from the local PDF to ~/new_physics/_external_data/papers/rc100_table3_images/ (not committed: the table is the paper's own figure)."""
import fitz, os
D = os.path.expanduser("~/new_physics/_external_data/papers"); d = fitz.open(os.path.join(D, "rc100_2209.12199.pdf")); out = os.path.join(D, "rc100_table3_images"); os.makedirs(out, exist_ok=True)
for pn in (26, 27, 28):
    xref = d[pn].get_images(full=True)[0][0]; pix = fitz.Pixmap(d, xref); pix = fitz.Pixmap(fitz.csRGB, pix) if pix.n > 3 else pix; pix.save(os.path.join(out, f"rc100_t3_p{pn+1}.png")); print(pn + 1, pix.width, pix.height)
