#!/usr/bin/env python3
"""CFG640 split-rule design table (no simulation): the condensed retention f_c = f_floor + (f_ret - f_floor) chi that the engine's
phase law assigns to a catchment, over turnaround mass and redshift, both footings.  Uses cfg640_pm.py's own functions (imported).
Brackets (reported only, not used by the engine): hot-gas truncation at the census MOND radius r_M = sqrt(G M_ret / a0) instead of
the catchment radius; primordial cooling (bremsstrahlung term of the same fit only); cooling against the age t = 1/H instead of r/V.
  python3 cfg640_split.py -> cfg640_split.out / cfg640_split.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
os.environ.setdefault("CFG596_RELIEF", "0")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg640_pm as E  # noqa: E402

D = E.dta_table()
def Dta_at(a):
    return math.exp(E.np.interp(math.log(1 / a), E.np.log1p(D["z"]), E.np.log(D["D"])))
def R_of(lM, Dta):                                    # invert M_ta(R, Dta) = 10^lM (Msun/h)
    return (10 ** lM / ((4 * math.pi / 3) * Dta * 0.315 * 2.775e11)) ** (1 / 3)
def chi_variant(R, Dta, a, foot, radius="R", cool="TN", tref="dyn"):
    Mta = E.M_ta(R, Dta); fr = E.fret_of(math.log10(Mta))
    if fr <= E.F_FLOOR: return 0.0
    Mret = fr * E.FB * Mta / 0.674 * E.CMSUN; Mhot = (fr - E.F_FLOOR) * E.FB * Mta / 0.674 * E.CMSUN
    a0 = E.a0_code(a, "FLAT", foot) * E.ACC_UNIT * 100.0
    V = (E.CG * Mret * a0) ** 0.25; T = E.C_MU * E.CMP * V * V / (2 * E.CKB)
    Rp = a * R / 0.674 * E.CMPC if radius == "R" else math.sqrt(E.CG * Mret / a0)
    kT = min(max(E.CKB * T / E.CKEV, 0.01), 20.0)
    lam = E.lam_cool(T) if cool == "TN" else 5.8e-2 * kT ** 0.5 * 1e-22
    A = 3 * E.C_N_NH * E.CKB * T * E.C_MU * E.CMP * E.C_N_NH * 4 * math.pi * Rp / (2 * E.C_NE_NH * lam * Mhot)
    if tref == "dyn": rc = 1.0 / (A * V)
    else:
        H = 100 * 0.674 * 1e5 / E.CMPC * E.E(a); rc = math.sqrt(1.0 / (H * A))
    return min(1.0, rc / Rp)

OUT = []; RES = dict(lane="CFG640 split design table", rows=[])
def P(s): print(s, flush=True); OUT.append(s)
P("CFG640 split rule: f_c = 0.10 + (f_ret - 0.10) chi;  chi = min(1, r_cool/R), t_cool = r/V, hot gas ~ r^-2 to the catchment radius")
P(f"{'foot':9s} {'z':>4s} {'logM_ta':>7s} {'f_ret':>6s} {'T[keV]':>7s} {'chi':>9s} {'f_c':>7s} | brackets chi: r_M-trunc  primordial  t=1/H")
for foot in ("canonical", "alt"):
    for z in (0.0, 0.5, 1.0, 2.0):
        a = 1 / (1 + z); Dt = Dta_at(a)
        for lM in (12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0):
            R = R_of(lM, Dt); fr = E.fret_of(lM); chi = E.chi_cool(R, Dt, a, "FLAT", foot); fc = E.fcond_of(R, Dt, a, "FLAT", foot)
            Mret = fr * E.FB * 10 ** lM / 0.674 * E.CMSUN; V = (E.CG * Mret * E.a0_code(a, "FLAT", foot) * E.ACC_UNIT * 100) ** 0.25
            kT = E.C_MU * E.CMP * V * V / 2 / E.CKEV
            br = [chi_variant(R, Dt, a, foot, "rM"), chi_variant(R, Dt, a, foot, cool="ff"), chi_variant(R, Dt, a, foot, tref="age")]
            RES["rows"].append(dict(foot=foot, z=z, logM_ta=lM, R_cMpch=R, f_ret=fr, kT_keV=kT, chi=chi, f_c=fc,
                                    chi_rM=br[0], chi_primordial=br[1], chi_age=br[2]))
            P(f"{foot:9s} {z:4.1f} {lM:7.2f} {fr:6.3f} {kT:7.3f} {chi:9.2e} {fc:7.4f} | {br[0]:9.2e} {br[1]:10.2e} {br[2]:9.2e}")
mx = max(r["f_c"] - 0.10 for r in RES["rows"]); RES["max_fc_minus_floor"] = mx
mxb = max(max(r["chi_rM"], r["chi_primordial"], r["chi_age"]) * (r["f_ret"] - 0.10) for r in RES["rows"]); RES["max_bracket_fc_minus_floor"] = mxb
P(f"max (f_c - 0.10) over the table = {mx:.2e}; largest bracket value of (f_ret - 0.10) chi = {mxb:.2e}")
json.dump(RES, open(os.path.join(HERE, "cfg640_split.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg640_split.out"), "w").write("\n".join(OUT) + "\n")
