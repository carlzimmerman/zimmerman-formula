import sympy as sp
H,c,b = sp.symbols('H c_chi b', positive=True)
kappa = H/sp.sqrt(1-b**2)
# Edge map exact claim: (c_chi^2 - b^2)^{-1} * kappa(b)^{-2} = c_chi/H^2 ?
expr = 1/((c**2-b**2)) * 1/kappa**2
print("(c^2-b^2)^{-1} kappa^{-2} =", sp.simplify(expr))
# This is (1-b^2)/(H^2 (c^2-b^2)) -- NOT constant in b unless c=1.
# The edge map's "constant c_chi/H^2" must involve kappa(b) with the LUMINAL kappa H/sqrt(1-b^2)
# AND the response uses sqrt(c_chi(c^2-b^2)). Let me check their stated surviving exponent:
surv = sp.sqrt(c*(c**2-b**2))
print("surviving edge exponent sqrt(c(c^2-b^2)) vanishes like sqrt at b->c:",
      sp.series(surv.subs(b,c-sp.Symbol('x',positive=True)), sp.Symbol('x',positive=True),0,2))
print()
print("NOTE: the edge-map 'pole cancels -> constant' identity is for the LUMINAL b->1")
print("response, not the b->c_chi response. My step-5 numeric mislabeled it; the b->c_chi")
print("AMPLITUDE pole is real and does NOT cancel in the amplitude. Corrected in memo.")
print("This does NOT affect the resurgence verdict (singularity-TYPE argument is robust).")
