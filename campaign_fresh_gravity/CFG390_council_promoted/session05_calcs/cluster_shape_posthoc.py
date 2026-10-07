"""POST-HOC, reported only (not frozen): the log-slope of the missing mass M_c itself over 100-1000 kpc, against the baryons,
the law's phantom, and X-COP's own NFW mass fit (M_NFW column; inherited modelling). Which known shape is it closest to?"""
import os, sys, io, contextlib, numpy as np
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity")); sys.path.insert(0, os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C, cluster_audit as CA
cl = [CA.load_cluster(p.name) for p in sorted(CA.DATA.iterdir()) if p.is_dir()]
R = CA.RADII; gas, stars, mh = CA.profiles(cl, R); _, _, mnfw = CA.profiles(cl, R, model="M_NFW"); mb = gas + stars
sel = (R >= 100) & (R <= 1000)
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    gb = 6.674e-11 * mb * 1.989e30 / (R * 3.0857e19) ** 2; ml = C.nu_mono(gb / a0) * mb
    def sl(M):
        s = []
        for i in range(len(cl)):
            y = M[i, sel]; ok = np.isfinite(y) & (y > 0)
            s.append(np.polyfit(np.log10(R[sel][ok]), np.log10(y[ok]), 1)[0])
        return np.median(s), np.percentile(s, 16), np.percentile(s, 84)
    for lab, M in (("missing mass M_c", mh - ml), ("baryons M_b", mb), ("phantom M_ph", ml - mb), ("hydrostatic M_HSE", mh),
                   ("X-COP NFW total", mnfw), ("NFW total minus baryons", mnfw - mb)):
        m, lo, hi = sl(M); print(f"{foot:9s} d lnM / d ln r, 100-1000 kpc: {lab:24s} median {m:+.2f} (16-84% {lo:+.2f}..{hi:+.2f})")
