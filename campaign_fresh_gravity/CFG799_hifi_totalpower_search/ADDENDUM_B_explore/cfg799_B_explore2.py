"""CFG799 ADDENDUM B, EXPLORATORY decomposition part 2: where the 541.700 GHz excess lives, and baseline robustness.
Sets no class; changes no frozen rule.  Imports the unchanged ../ADDENDUM_B_full90/cfg799.py (sha256 7486117b...a81488).

Run:  python3 -I cfg799_B_explore2.py <data_dir> <out_dir>

DECLARED LIST (fixed before the first run; every row is reported, none is selected):
  K1  reproduce B1 (nu_t a = -6.577 mK, nu_2 a = +15.343 mK).
  E7  localise the excess.  At nu_2 and at nu_t, for H and V separately, stack the spectra grouped by
        (a) WBS sub-band index used (0..3); (b) target-IF tercile (equal spectrum counts); (c) observation-id tercile
        (a proxy for epoch).  Report a, sigma, z per group.  A fixed-RF line would be flat across these groups; an
        instrumental feature tied to a sub-band or an IF range would concentrate in some of them.
  E8  baseline robustness.  The frozen fit is a degree-3 Legendre baseline over +-50 MHz plus the fixed Gaussian.  Repeat
        the stack with degree 1, 2, 3, 4, 5 and half-window 25, 50, 100 MHz (15 variants; the masks M1-M4 stay at the
        frozen definition, only the fit changes).  For every variant report nu_t and nu_2 total-power a, sigma (formal,
        chi2-inflated), z, the H-only nu_2 z, and the standard deviation of the total-power z over a 1 MHz scan of +-40 MHz
        excluding +-5 MHz about nu_t and about nu_2 (the empirical-null scale).  The frozen variant is degree 3 / +-50.
      This is a sensitivity table.  It is not used to choose a baseline: the frozen result stays the number of record.
"""
import importlib.util, json, os, sys
import numpy as np

DATA = os.path.abspath(sys.argv[1]); OUTD = os.path.abspath(sys.argv[2])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["cfg799.py", DATA]
spec = importlib.util.spec_from_file_location("cfg799", os.path.join(HERE, "..", "ADDENDUM_B_full90", "cfg799.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
OUT, R = [], {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


man, obs = m.load()
spectra = []
for oid, o in obs.items():
    a = m.anchor(o)
    if a["ok"]:
        spectra += m.build_spectra(oid, o, a["tS"])
sp, drops = m.prep(spectra)
NU = (("nu_t", m.NU_T), ("nu_2", m.NU_2))
P("CFG799 ADDENDUM B exploratory decomposition, part 2 (sets no class)")
for name, nu in NU:
    st = m.stack(m.amps(sp, nu))
    want = {"nu_t": -6.577e-3, "nu_2": 15.343e-3}[name]
    P(f"  K1 {name}: a = {st['a'] * 1e3:+.3f} mK z {st['z']:+.2f}  {'REPRODUCES B1' if abs(st['a'] - want) < 1e-5 else 'DOES NOT REPRODUCE'}")
    assert abs(st["a"] - want) < 1e-5

# ---- E7
P("\nE7 localisation (a +- sigma in mK, z, n spectra)")
R["E7"] = {}
ifc_all = np.array([s["ifc"] for s in sp]); obs_all = np.array([int(s["obs"]) for s in sp])
if_edges = np.quantile(ifc_all, [1 / 3, 2 / 3]); ob_edges = np.quantile(obs_all, [1 / 3, 2 / 3])
P(f"  target-IF tercile edges {if_edges[0]:.0f}, {if_edges[1]:.0f} MHz (range {ifc_all.min():.0f}-{ifc_all.max():.0f}); "
  f"obsid tercile edges {ob_edges[0]:.0f}, {ob_edges[1]:.0f}")


def terc(v, e):
    return 0 if v <= e[0] else (1 if v <= e[1] else 2)


GROUPS = (("sub-band", lambda s: s["sb"], 4), ("IF tercile", lambda s: terc(s["ifc"], if_edges), 3),
          ("obsid tercile", lambda s: terc(int(s["obs"]), ob_edges), 3))
for name, nu in NU:
    a = m.amps(sp, nu); R["E7"][name] = {}
    for pol in ("h", "v"):
        ap = [x for x in a if x[2]["pol"] == pol]
        for glab, gf, ng in GROUPS:
            cells = []
            for g in range(ng):
                st = m.stack([x for x in ap if gf(x[2]) == g])
                cells.append(st); R["E7"][name].setdefault(pol, {}).setdefault(glab, []).append(st)
            P(f"  [{name}] {pol.upper()} {glab:13s} " + " | ".join(
                f"{g}: {c['a'] * 1e3:+6.1f}+-{c['sig'] * 1e3:4.1f} z {c['z']:+5.2f} (n {c['n']:3d})" if c["n"] else f"{g}: none" for g, c in enumerate(cells)))

# ---- E8
P("\nE8 baseline robustness (frozen = degree 3, +-50 MHz).  columns: nu_t a+-sig (z) | nu_2 a+-sig (z) | nu_2 H-only z | far-step z std")
orig_fit, orig_leg, orig_half = m.fit_one, m.legendre_design, m.HALF
deltas = np.arange(-40, 40.01, 1.0); far = (np.abs(deltas) > 5) & (np.abs(deltas - 36) > 5)


def variant(deg, half):
    def fit(IFax, y, flag, centre, inject=0.0, with_line=True):
        m.legendre_design = lambda x, ncoef=deg + 1: orig_leg(x, ncoef)
        m.HALF = half
        try:
            return orig_fit(IFax, y, flag, centre, inject=inject, with_line=with_line)
        finally:
            m.legendre_design, m.HALF = orig_leg, orig_half
    return fit


R["E8"] = {}
for half in (25.0, 50.0, 100.0):
    for deg in (1, 2, 3, 4, 5):
        m.fit_one = variant(deg, half)
        row = {}
        for name, nu in NU:
            row[name] = m.stack(m.amps(sp, nu))
        ah = [x for x in m.amps(sp, m.NU_2) if x[2]["pol"] == "h"]
        zh = m.stack(ah)["z"]
        zs = np.array([m.stack(m.amps(sp, m.NU_T + d / 1000))["z"] for d in deltas])
        sd = float(np.nanstd(zs[far])); mu = float(np.nanmean(zs[far]))
        R["E8"][f"deg{deg}_half{half:g}"] = dict(row, H_nu2_z=zh, far_std=sd, far_mean=mu)
        tag = "  <- frozen" if (deg == 3 and half == 50.0) else ""
        P(f"  deg {deg}, +-{half:3g} MHz: nu_t {row['nu_t']['a'] * 1e3:+6.1f}+-{row['nu_t']['sig'] * 1e3:4.1f} ({row['nu_t']['z']:+5.2f}) | "
          f"nu_2 {row['nu_2']['a'] * 1e3:+6.1f}+-{row['nu_2']['sig'] * 1e3:4.1f} ({row['nu_2']['z']:+5.2f}) | H z {zh:+5.2f} | "
          f"std {sd:4.2f} mean {mu:+5.2f} (n {row['nu_t']['n']}){tag}")
m.fit_one = orig_fit

open(os.path.join(OUTD, "explore2.out"), "w").write("\n".join(OUT) + "\n")
json.dump(R, open(os.path.join(OUTD, "explore2_results.json"), "w"), indent=1, default=str)
