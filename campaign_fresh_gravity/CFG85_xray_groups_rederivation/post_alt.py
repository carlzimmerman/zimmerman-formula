import re,sys
src=open('cfg85_rederive.py').read()
src=src.split("# ------------------------------------------------------------------ summary")[0]
# strip run-time output heavy parts: just exec whole up to summary, then extra
exec(compile(src,'x','exec'))
print("POSTHOC unscaled-rho_c,g readings for V3u/V4u")
for nm,kw in (("V3u",dict(norm_fac=1.2,m2500_fac=1.2,rho_mode="g0")),("V4u",dict(norm_fac=0.8,m2500_fac=0.8,rho_mode="g0"))):
    r=L_stat(**kw); print(nm, f"{r['med']:+.3f} z {r['z']:+.2f}")
