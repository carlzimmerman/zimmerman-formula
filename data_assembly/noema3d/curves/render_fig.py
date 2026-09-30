#!/usr/bin/env python3
"""Extract the raster image of Fig. 5 (paper 1 PDF page 15) from the source PDF to ~/new_physics/_external_data/noema3d/fig5_raw.png (not committed). The PDF sha256 is in ../manifest.json."""
import fitz, os, hashlib
D = os.path.expanduser("~/new_physics/_external_data/noema3d"); d = fitz.open(os.path.join(D, "arxiv_2604.18503v2.pdf")); p = d[14]; xref = p.get_images(full=True)[0][0]
pix = fitz.Pixmap(d, xref); pix = fitz.Pixmap(fitz.csRGB, pix) if pix.n > 3 else pix; out = os.path.join(D, "fig5_raw.png"); pix.save(out)
print(out, pix.width, pix.height, hashlib.sha256(open(out, "rb").read()).hexdigest())
