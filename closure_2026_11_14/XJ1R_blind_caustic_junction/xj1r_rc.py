#!/usr/bin/env python3
"""XJ1R part (b) (FROZEN_CRITERIA.md sections 3 and 5): do today's rotation curves lie inside R_k(z = 0; M_b), k = 2 and 3?
SPARC's 175 galaxies via QX8's load_sparc (closure_2026_11_06/QX8_sparc_exact_field/qx8.py, imported read-only as PD1 does);
M_b = PD1's baryon mass: max_r [V_B^2 r / G] (floor 1e3 Msun), V_B^2 = sgn(V_gas) V_gas^2 + Y V_disk^2 + 1.4 Y V_bul^2;
Y = 0.5 graded, 0.3 and 0.8 reported. R_last = the largest measured radius. R_k from xj1r_rk.rk_kpc (FZS1's rules).
KS4: FLD1's SPARC line from this lane's R_1 with FLD1's mass (0.5 L[3.6] + 1.33 M_HI) and FLD1's clamp at the mass ends.
    nice -n 19 python3 -I -B xj1r_rc.py -> xj1r_rc.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import xj1r_rk as RK
sys.path.insert(1, os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field"))
_a = sys.argv; sys.argv = [_a[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import qx8 as Q8
sys.argv = _a
G_KPC = 4.3009172706e-6                                   # PD1's constant (kpc (km/s)^2 / Msun)
GALS = Q8.load_sparc()
OUT = []
def P(s): print(s, flush=True); OUT.append(s)


def mb_pd1(q, Y):
    VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + Y * q["Vdisk"] ** 2 + 1.4 * Y * q["Vbul"] ** 2
    return max(float(np.max(np.clip(VB2 * q["R"] / G_KPC, 0, None))), 1e3)


def rk_clamped(f, z, lM, k):
    lMc = min(max(lM, RK.MASSES[0]), RK.MASSES[-1]); return RK.rk_kpc(f, z, lMc, k)


RES = dict(lane="XJ1R", part="(b) rotation-curve containment", n_galaxies=len(GALS), note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
# KS4
ks4 = {}
for f in RK.FOOTS:
    rows = []
    for q in GALS:
        Mb = 0.5 * q["meta"]["L36"] * 1e9 + 1.33 * q["meta"]["MHI"] * 1e9; Rl = float(np.max(q["R"]))
        rows.append((Rl / rk_clamped(f, 0.0, math.log10(Mb), 1), q["name"]))
    worst = max(rows); nb = sum(1 for r, _ in rows if r > 1)
    ks4[f] = dict(n_beyond=nb, worst=worst[1], worst_ratio=worst[0], pass_=bool(nb == 0 and worst[1] == "UGC00128" and round(worst[0], 2) == 0.47))
    P(f"KS4 [{f}] FLD1's SPARC line from this lane's R_1 (FLD1's mass and clamp): {nb} beyond; worst {worst[1]} at {worst[0]:.3f} -> {'PASS' if ks4[f]['pass_'] else 'FAIL'}")
RES["KS4"] = ks4
# (b)
B = {}
for f in RK.FOOTS:
    B[f] = {}
    for k in (1, 2, 3):
        B[f][str(k)] = {}
        for Y in (0.5, 0.3, 0.8):
            rows = []
            for q in GALS:
                Mb = mb_pd1(q, Y); Rl = float(np.max(q["R"])); lM = math.log10(Mb); Rk = RK.rk_kpc(f, 0.0, lM, k)
                rows.append(dict(name=q["name"], logMb=lM, R_last=Rl, R_k=Rk, ratio=Rl / Rk if Rk > 0 else math.inf, outside_mass_table=bool(lM < 6.5 or lM > 12)))
            rows.sort(key=lambda r: -r["ratio"])
            beyond = [r for r in rows if r["ratio"] > 1]
            B[f][str(k)][f"Y{Y:g}"] = dict(n_beyond=len(beyond), beyond=beyond, worst5=rows[:5], median_ratio=float(np.median([r["ratio"] for r in rows])),
                                         n_outside_mass_table=sum(r["outside_mass_table"] for r in rows))
        g = B[f][str(k)]["Y0.5"]
        word = ("no galaxy beyond" if g["n_beyond"] == 0 else f"{g['n_beyond']} galaxies beyond") if k > 1 else "(k = 1 reported)"
        P(f"(b) [{f}] k {k}, Y 0.5: {g['n_beyond']} of {len(GALS)} beyond R_{k}(0); worst " + ", ".join(f"{r['name']} {r['ratio']:.3f} (R_last {r['R_last']:.1f} kpc, R_{k} {r['R_k']:.1f} kpc, log M_b {r['logMb']:.2f})" for r in g["worst5"][:3])
          + f"; median ratio {g['median_ratio']:.3f} -> {word}; Y 0.3: {B[f][str(k)]['Y0.3']['n_beyond']} beyond, Y 0.8: {B[f][str(k)]['Y0.8']['n_beyond']} beyond")
        for r in g["beyond"]:
            P(f"    beyond [{f}] k {k}: {r['name']} R_last/R_{k} = {r['ratio']:.3f}")
RES["containment"] = B
RES["gate"] = {f: {str(k): ("NO GALAXY BEYOND" if B[f][str(k)]["Y0.5"]["n_beyond"] == 0 else "GALAXY BEYOND") for k in (2, 3)} for f in RK.FOOTS}
P("(b) gate per footing and k (Y 0.5): " + json.dumps(RES["gate"]))
json.dump(RES, open(os.path.join(HERE, "xj1r_rc.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "xj1r_rc.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
