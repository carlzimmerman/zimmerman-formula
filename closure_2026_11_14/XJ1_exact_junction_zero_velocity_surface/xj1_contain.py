#!/usr/bin/env python3
"""XJ1 (AMENDMENT_A5, reported): are today's rotation curves inside the caustic radii? For each of SPARC's 175 galaxies:
its last measured radius against R_fold, R_2 and R_3 at z = 0 and its own M_b (PD1's M_b: the largest enclosed baryon mass
at mass-to-light 0.5; brackets 0.3 and 0.8), from this lane's shell runs with FZS1's interpolation in mass (log R linear
in log M_b; M_b^(1/3) beyond the ends). Inside the settled radius the exact junction is the law, so a galaxy wholly inside
keeps PD1's rotation-curve numbers.
  python3 -I -B xj1_contain.py -> xj1_contain.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, warnings
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
G_KPC = 4.3009172706e-6
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field")); a_ = sys.argv; sys.argv = [a_[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import qx8 as Q8
sys.argv = a_
GALS = Q8.load_sparc()
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def at0(S, c):
    o = np.argsort(S[:, 1]); return float(np.interp(0.0, S[o, 1], S[o, c]))
RES = dict(lane="XJ1", part="containment of SPARC's last radii (AMENDMENT_A5; reported)", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})
for ft in ("canonical", "alt"):
    T = {M: np.array(json.load(open(os.path.join(HERE, "shells", f"xj1_shells_{ft}_M{M:g}.json")))["series"]) for M in MASSES}
    tab = {c: np.array([at0(T[M], c) for M in MASSES]) for c in (2, 6, 7)}
    def R0(lM, c):
        R = tab[c]
        if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
        if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
        return float(10 ** np.interp(lM, MASSES, np.log10(R)))
    R = {}
    for ups in (0.5, 0.3, 0.8):
        rows = []
        for q in GALS:
            r = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + ups * q["Vdisk"] ** 2 + 1.4 * ups * q["Vbul"] ** 2
            lM = math.log10(max(float(np.max(np.clip(VB2 * r / G_KPC, 0, None))), 1e3)); rl = float(r[-1])
            rows.append((q["name"], lM, rl, rl / R0(lM, 2), rl / R0(lM, 6), rl / R0(lM, 7)))
        o = {}
        for j, nm in ((3, "R_fold"), (4, "R_2"), (5, "R_3")):
            v = np.array([x[j] for x in rows]); k = int(np.argmax(v)); bey = [(rows[i][0], round(float(v[i]), 3)) for i in np.nonzero(v > 1)[0]]
            o[nm] = dict(n_beyond=len(bey), beyond=bey, worst=rows[k][0], worst_ratio=float(v[k]), median_ratio=float(np.median(v)))
        R[f"ups{ups}"] = o
        P(f"[{ft}] mass-to-light {ups}: last radius over R_fold / R_2 / R_3 at z 0: worst " + " / ".join(f"{o[n]['worst_ratio']:.3f} ({o[n]['worst']})" for n in ("R_fold", "R_2", "R_3"))
          + "; galaxies beyond: " + " / ".join(str(o[n]["n_beyond"]) for n in ("R_fold", "R_2", "R_3")) + "; median ratio " + " / ".join(f"{o[n]['median_ratio']:.3f}" for n in ("R_fold", "R_2", "R_3"))
          + (f"; beyond R_3: {o['R_3']['beyond']}" if o["R_3"]["n_beyond"] else ""))
    R["caustic_over_fold_at_z0"] = {str(M): [float(tab[6][i] / tab[2][i]), float(tab[7][i] / tab[2][i])] for i, M in enumerate(MASSES)}
    P(f"[{ft}] R_2 / R_fold and R_3 / R_fold at z 0 by log M_b: " + "; ".join(f"{M:g}: {tab[6][i] / tab[2][i]:.3f} / {tab[7][i] / tab[2][i]:.3f}" for i, M in enumerate(MASSES)))
    RES["footings"][ft] = R
json.dump(RES, open(os.path.join(HERE, "xj1_contain.json"), "w"), indent=1)
open(os.path.join(HERE, "xj1_contain.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
