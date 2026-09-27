#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG3_kids -- KiDS-1000 WEAK LENSING AROUND ISOLATED LENSES UNDER THE PRINCIPLE (Brouwer et al. 2021, four stellar-mass bins, full
covariance), with FP20's EXACT projector.  esd_of_M, DE8's esd_from_mlens and L352's project_M2 are not used.

THE LENS UNDER THE PRINCIPLE.  An isolated lens is a held-back region of its own.  Inside it the vacuum answers the baryons with
the Bose kernel (CFG3_principle D2), read in the region's own free fall (D7): the web's bulk-flow field drops out, the web's TIDAL
field across the region survives.  At the region's edge r_g the answer stops and its mass is compensated (D6): a negative shell
-M_b (nu(r_g) - 1).  The edge is where the lens's infall flow first fell behind the vacuum's expansion (theta = 3 H_Lambda), computed
for the lens's Lagrangian patch (CFG3_common.gate_radius; the patch's mass from Moster+13 at z = 0.25 with M_* = M_b/1.4, bracketed
by M_b/1.0 and M_b/2.0).  No constant is chosen: H_Lambda, a0 and the linear spectrum fix everything.
THE TIDAL RESIDUAL (the principle's in-region field for an isolated lens): the rms traceless tide of the matter outside the region,
|T r| = 4 pi G rho_m(z) sigma_delta(R_g, z) sqrt(2/9) r (R_g the region's Lagrangian radius; FP1 E's linear spectrum), entered in
the record's stacked-monopole form N(y, e) (FP1 E / BS2) with e = |T r|/a0 at each radius.

MACHINERY (read-only): FP1_static_sector.py's E section (L355's KiDS-1000 machinery: data, covariance in its corrected order, M_b
profiled per bin on 9.8..11.8, the linear 2-halo template with amplitude in [0, A_max]) exec'd from its committed source, with
FP20's exact projector (FP20_esd_projection_fix.py's shell_mats/ESDFix, exec'd) swapped in.

CHECKS
  K1 CONTROL: with FP20's projector the harness reproduces FP20's corrected numbers: isolated P2 at FP0's pair 139.800 / 133.948
     (FP20 R6, E3 KiDS_ref) and isolated nu_mono at L355's pair 162.600 / 154.890 (FP20 R8, L355 K1), to < 1e-3.
  S1 [HEADLINE; load-bearing; MUTATE must fail] THE PRINCIPLE'S LENS PASSES KiDS: with the phantom gated at each lens's own r_g,
     compensated, and the rms tidal residual in the kernel's argument, d chi^2 <= +9 against the isolated Bose law (the record's
     gate, CFG4's convention), with the 2-halo template (A <= 2) on both sides; both footings, all three M_b/M_* brackets.
  S2 (reported) the same without the 2-halo term, and with the tide set to zero (a perfectly quiet region).
  S1b, S1c (reported; ADDED AFTER THE FIRST DEVELOPMENT RUN, disclosed): S1b the own-matter reading (iii') -- no external tide in the
     argument -- as the best variant; S1c half the rms tide (the environment's uncertainty, reported as a bracket).
  S3 (reported) the numbers: r_g and the tidal field at 1 Mpc per bin mass; the chi^2 values.
PRE-DECLARED HYPOTHESES (written before the first run of this script):
  H1 K1 reproduces FP20 to < 1e-3.  EXPECT TRUE.
  H2 S1 passes: r_g(z = 0.25) = 1.2-4 Mpc for the bins' patch masses (CFG4 found the phantom must reach >= 0.5 Mpc with a 2-halo
     term, >= 0.84 without), and the rms tide at <= 1 Mpc is ~1e-3 a0 or less.  UNCERTAIN: the tide is comparable to KiDS's
     tolerated field (FP20: e_KiDS ~ 2-5e-4 a0) at 0.3-1 Mpc.
  H3 S2: without the 2-halo term the compensation shell costs more; with zero tide the law is the isolated law up to the shell.
MUTATE=1: the free-fall frame removed -- the web's full (bulk-flow) field enters the kernel's argument (FP1 E's all-matter Maxwell
stack, the record's 'all-matter kernel'): S1 must FAIL (rc = 1).
Run from the repository root (MUTATE first):  MUTATE=1 python3 campaign_fresh_gravity/CFG3_kids.py; python3 campaign_fresh_gravity/CFG3_kids.py
"""
import os, sys, math, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG3_common as C
import numpy as np

R = C.Run("CFG3_kids", __doc__)
P, check = R.P, R.check
if C.MUTATE:
    P("\n  *** MUTATE=1: the web's full field enters the kernel (no free-fall frame): S1 must FAIL ***")

# ================================================================================================ the harness
t0 = time.time()
GK = {"np": np, "math": math, "os": os, "REPO": C.REPO, "G_SI": 6.67430e-11, "_trap": C._trap}
GK, _ = C.exec_slices(os.path.join(C.CHAIN, "FP1_static_sector.py"),
                      [("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")], ns=GK, name="fp1_kids_ro")
F20, _ = C.exec_slices(os.path.join(C.CHAIN, "FP20_esd_projection_fix.py"), [("def shell_mats(edges, Rv):", "class M2Fix:")],
                       ns={"np": np, "math": math}, name="fp20_ro")
FIX = F20["ESDFix"](GK["rrK"], GK["Rp"], GK["PCm2"], GK["MS"])
RRK, RPK, MPCK, MSK = GK["rrK"], GK["Rp"], GK["MPCm"], GK["MS"]
LM, NPB, ES = GK["LM"], GK["npb"], GK["ES"]
W0 = np.zeros(len(ES)); W0[0] = 1.0
GN = 6.67430e-11
ZL = GK["ZL"]
P(f"    FP1 E's KiDS machinery and FP20's exact projector loaded ({time.time() - t0:.0f} s); lens redshift z_l = {ZL}")


def table(Mfun, foot, a0):
    T = np.zeros((len(ES), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, a0, lm), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return {foot: T}


def chi2(Mfun, foot, a0, Amax=0.0, wts=None, TAB=None):
    TAB = table(Mfun, foot, a0) if TAB is None else TAB
    return GK["kfit"](TAB, foot, W0 if wts is None else wts, Amax)[0]


# ================================================================================================ K1
R.banner("K1  CONTROL: FP1 E's harness with FP20's exact projector reproduces FP20's corrected numbers")
f20 = json.load(open(os.path.join(C.CHAIN, "FP20_esd_projection_fix_results.json")))["numbers"]
A0_FP1 = {"canonical": C.A0["canonical"], "alt": C.A0["alt"]}
A0_L355 = GK["A0_L355"]
k1 = {}
for foot in C.FOOTS:
    p2 = chi2(lambda Mb, a0, lm: Mb * C.nu_p2(GN * Mb / RRK ** 2 / a0), foot, A0_FP1[foot])
    mo = chi2(lambda Mb, a0, lm: Mb * C.nu_mono(GN * Mb / RRK ** 2 / a0), foot, A0_L355[foot])
    k1[foot] = (p2, mo, f20["R6_FP1E"]["E3"][foot]["KiDS_ref"][1], f20["R8_L355"]["K1"][foot][1])
    P(f"    {foot:9s}: isolated P2 {p2:.3f} (FP20 {k1[foot][2]:.3f});  isolated nu_mono at L355's a0 {mo:.3f} (FP20 {k1[foot][3]:.3f})")
dk1 = max(max(abs(v[0] - v[2]), abs(v[1] - v[3])) for v in k1.values())
check("K1 CONTROL: FP1 E's KiDS-1000 harness (exec'd read-only) with FP20's exact projector (exec'd) reproduces FP20's corrected isolated "
      "P2 (139.800 / 133.948) and isolated nu_mono (162.600 / 154.890) chi^2", f"max |d chi^2| {dk1:.1e}", dk1 < 1e-3)
R.num("K1", k1)

# ================================================================================================ the principle's lens
R.banner("S1  THE PRINCIPLE'S LENS: the Bose answer gated at the lens's own r_g, compensated, with the tidal residual")
MU = np.linspace(-1.0, 1.0, 801)


def N_field(y, e):
    """the stacked monopole of the QUMOND flux with a field e (per radius), FP1 E's N_of vectorised over (y, e) pairs."""
    y = np.asarray(y, float); e = np.asarray(e, float)
    out = C.nu_bose(y).copy()
    m = e > 0
    if m.any():
        yy, ee = y[m][:, None], e[m][:, None]
        w = np.sqrt(np.maximum(yy ** 2 + ee ** 2 - 2 * yy * ee * MU[None, :], 1e-300))
        out[m] = 0.5 * C._trap(C.nu_bose(w) * (yy - ee * MU[None, :]), MU, axis=1) / y[m]
    return out


RHOM_Z = C.OM_K * C.RHO_CRIT_K * (1 + ZL) ** 3                           # physical mean matter density at z_l [kg/m^3]
DZL = C.growth_D(1 / (1 + ZL))
GATE = {}


def gate_for(lm, fac):
    key = (round(lm, 3), fac)
    if key not in GATE:
        Ms = 10 ** lm / fac
        Mh = float(C.mh_of_mstar(Ms, ZL))
        g = C.gate_radius(Mh, ZL)
        sig = math.sqrt(C.sigma2_cross(g["R_g"], g["R_g"])) * DZL
        T = 4 * math.pi * C.G_SI * RHOM_Z * sig * math.sqrt(2 / 9)          # 1/s^2
        GATE[key] = dict(Mh=Mh, r_g=g["r_g"], R_g=g["R_g"], r_ta=g["r_ta"], sigma=sig, T=T)
    return GATE[key]


def law_factory(fac, tide=1.0, gated=True, web_field=None):
    def Mfun(Mb, a0, lm):
        y = GN * Mb / RRK ** 2 / a0
        g = gate_for(lm, fac)
        e = np.zeros_like(RRK) if web_field is None else np.full_like(RRK, web_field / a0)
        if tide > 0:
            e = np.hypot(e, tide * g["T"] * RRK / a0)
        M = Mb * N_field(y, e)
        if gated:
            M = np.where(RRK < g["r_g"] * C.MPC, M, Mb)                   # the compensating shell at r_g
        return M
    return Mfun


S1 = {}
LYT = GK["LYT"]; YT = 10 ** LYT
NT_MUT = {}
if C.MUTATE:                                                                  # FP1 E's (y, e) table for the uniform-field stack
    NT_MUT = {e: N_field(YT, np.full_like(YT, e)) for e in ES}
for foot in C.FOOTS:
    a0 = C.A0[foot]
    TABref = table(lambda Mb, a0_, lm: Mb * C.nu_bose(GN * Mb / RRK ** 2 / a0_), foot, a0)
    ref = {A: chi2(None, foot, a0, Amax=A, TAB=TABref) for A in (0.0, 2.0)}
    for fac in (1.0, 1.4, 2.0):
        if C.MUTATE:
            TAB = {foot: np.zeros((len(ES), len(LM), 4, NPB))}
            wts = GK["stack_weights"](GK["maxwell_e"](GK["SIG_ALL"] / a0))  # the web's 3-D rms field (all matter), uniform
            for ie, e in enumerate(ES):
                for im, lm in enumerate(LM):
                    Mb = 10 ** lm * MSK
                    yv = GN * Mb / RRK ** 2 / a0
                    gg = gate_for(lm, fac)
                    M = Mb * np.interp(np.log10(yv), LYT, NT_MUT[e])
                    M = np.where(RRK < gg["r_g"] * C.MPC, M, Mb)
                    dS = FIX(M, Mb)
                    TAB[foot][ie, im] = [np.interp(GK["Rd"][b_], RPK / MPCK, dS) for b_ in range(4)]
            for (lab, tide) in (("rms tide", 1.0), ("half tide", 0.5), ("no tide", 0.0)):
                for A in (2.0, 0.0):
                    c2 = chi2(None, foot, a0, Amax=A, wts=wts, TAB=TAB)
                    S1[f"{foot}|{fac}|{lab}|A{A:g}"] = dict(chi2=c2, ref=ref[A], d=c2 - ref[A])
        else:
            for (lab, tide) in (("rms tide", 1.0), ("half tide", 0.5), ("no tide", 0.0)):
                TAB = table(law_factory(fac, tide), foot, a0)
                for A in (2.0, 0.0):
                    c2 = chi2(None, foot, a0, Amax=A, TAB=TAB)
                    S1[f"{foot}|{fac}|{lab}|A{A:g}"] = dict(chi2=c2, ref=ref[A], d=c2 - ref[A])
        P(f"    {foot:9s} M_b/M_* = {fac}: " + "; ".join(f"{k.split('|', 2)[2]}: {v['chi2']:.1f} (d {v['d']:+.1f})"
                                                        for k, v in S1.items() if k.startswith(f"{foot}|{fac}|")) + f"   [ref A=2 {ref[2.0]:.1f}, A=0 {ref[0.0]:.1f}]")
head = [v["d"] for k, v in S1.items() if k.endswith("|rms tide|A2")]
check("S1 [HEADLINE; MUTATE must fail] THE PRINCIPLE'S LENS PASSES KiDS-1000: gated at each lens's own r_g, compensated, with the rms tidal "
      "residual in the kernel's argument and the 2-halo template (A <= 2), d chi^2 <= +9 against the isolated Bose law on both footings and "
      "all three M_b/M_* brackets", f"d chi^2 = {', '.join(f'{d:+.1f}' for d in head)}", max(head) <= 9.0)
R.num("S1", S1)
S2a = [v["d"] for k, v in S1.items() if k.endswith("|A0")]
check("S2 (reported) without the 2-halo term and/or with a perfectly quiet region (tide zero): d chi^2 against the isolated law, same "
      "gate", "; ".join(f"{k}: {v['d']:+.1f}" for k, v in S1.items() if not k.endswith("|rms tide|A2")), max(S2a) <= 9.0, load_bearing=False)
vb = [v["d"] for k, v in S1.items() if k.endswith("|no tide|A2")]
vh = [v["d"] for k, v in S1.items() if k.endswith("|half tide|A2")]
check("S1b (reported; the BEST VARIANT, a post-hoc amendment disclosed: added after the first development run showed S1 failing) THE "
      "OWN-MATTER READING (iii'): the answer reads only the field of the region's own matter, so external tides drop out as the bulk field "
      "does -- gated at r_g, compensated, 2-halo A <= 2: d chi^2 <= +9 on both footings and all three brackets",
      f"d chi^2 = {', '.join(f'{d:+.1f}' for d in vb)}", max(vb) <= 9.0, load_bearing=False,
      reading="the variant changes only external tides (satellites, group members, the Local Group's pair and Chae's bound neighbours are the "
              "region's own matter under both readings); it is the one amendment this lane proposes, and it must be re-tested before adoption")
check("S1c (reported; environmental-uncertainty bracket, not a knob) the declared reading with half the rms tide", 
      f"d chi^2 = {', '.join(f'{d:+.1f}' for d in vh)}", max(vh) <= 9.0, load_bearing=False)

R.banner("S3  THE NUMBERS PER LENS MASS: the region edge and the tide")
rows = []
for lm in (10.0, 10.5, 11.0, 11.5):
    g = gate_for(lm, 1.4)
    e1 = g["T"] * C.MPC / C.A0["canonical"]
    rows.append(dict(logMb=lm, logMh=math.log10(g["Mh"]), r_g=g["r_g"], r_ta=g["r_ta"], R_g=g["R_g"], sigma=g["sigma"], e_1Mpc=e1))
    P(f"    log M_b = {lm}: log M_patch = {math.log10(g['Mh']):.2f}; r_ta = {g['r_ta']:.2f}, r_g = {g['r_g']:.2f} Mpc (physical); sigma(R_g = "
      f"{g['R_g']:.1f} Mpc) = {g['sigma']:.3f}; tide at 1 Mpc = {e1:.2e} a0 (canonical)")
check("S3 (reported) the gate radii of the bins' lenses lie at 1-4 Mpc (beyond CFG4's KiDS reach of 0.5-0.84 Mpc) and the rms tide at 1 Mpc is "
      "below 3e-3 a0", "; ".join(f"logMb {r_['logMb']}: r_g {r_['r_g']:.2f} Mpc, tide {r_['e_1Mpc']:.1e} a0" for r_ in rows),
      all(1.0 <= r_["r_g"] <= 4.5 for r_ in rows) and all(r_["e_1Mpc"] < 3e-3 for r_ in rows), load_bearing=False)
R.num("S3", rows)

R.banner("W  THE LEDGER")
R.ledger("KD1", "PASS" if max(head) <= 9 else "FAIL", "KiDS-1000 isolated lenses, the principle's lens (gated, compensated, rms tide, 2-halo): "
         f"d chi^2 {min(head):+.1f} .. {max(head):+.1f} vs the isolated law", "S1")
R.ledger("KD2", "DERIVED", "the web's bulk field drops out (free-fall frame): the record's all-matter kernel (+528 / +542, FP20) is not this law's", "S1, MUTATE")
sys.exit(R.finish())
