#!/usr/bin/env python3
"""DW2 part (b): new process rows, each computed to a number. Inputs marked PROVISIONAL are from memory or web reading. kappa = 1/2 FITTED; cold dark energy, never a particle; particle-like rows are stated, not adopted; reinstates nothing."""
import sys
from scipy.integrate import solve_ivp, quad
from scipy.optimize import fsolve
from astropy.io import fits
from dw2_core import *
OUT = []; RES = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
GAL = load(); BY = [[g for g in GAL if binof(g) == i] for i in range(6)]; a0 = A0["canonical"]; YR = 3.156e7; T0 = 1.38e10 * YR; GPC = 4.30091e-3
H0N, OMN = 0.6856, 0.2976; OMX = 0.1197; OMB = 0.0224; RH1 = 3 * (100e3 / MPC) ** 2 / (8 * math.pi * G); RHOB0 = OMB * RH1; RHOX0 = OMX * RH1
# ---- per-bin need and system numbers
RN = {}; SYS = []
for i, gs in enumerate(BY):
    row = {}
    for mass in ("em1", "share"):
        q = psi_bin([item(g, .5, *cold_pair(g, .5, mass), FQ) for g in gs], a0, "N"); row[mass] = 1 - q["psi"]
    RN[BN[i]] = row
    v = lambda f: float(np.median([f(g) for g in gs]))
    Mb = lambda g: Mbtot(g, .5); Rl = lambda g: g["R"].max() / KPC
    SYS.append(dict(bin=BN[i], n=len(gs), Mb=v(Mb), Rl=v(Rl), V=v(lambda g: g["Vflat"]), Ms=v(lambda g: .5 * g["L36"] * 1e9), Mg=v(lambda g: 1.33 * g["MHI"] * 1e9), M200e=v(lambda g: M200_of(g, "em1")), M200s=v(lambda g: M200_of(g, "share")), Mcn=v(lambda g: float(Mc_native(M200_of(g, "em1"), g["R"].max()))), Mcs=v(lambda g: float(Mc_native(M200_of(g, "share"), g["R"].max())))))
RES["need"] = RN; RES["sys"] = SYS
P("R_need (1 - psi, N, f_Q, U .5, canonical): " + " ".join(f"{k}: {v['em1']:.2f}/{v['share']:.2f}" for k, v in RN.items()))
Rq = np.median([RN[b]["em1"] for b in BN[3:5]]); Rqs = np.median([RN[b]["share"] for b in BN[3:5]]); P(f"R_need at 150-250: EM1 {Rq:.2f}, share {Rqs:.2f}")
for s in SYS: P(f"  {s['bin']:8s} n {s['n']} M_b {s['Mb']:.2e} R_last {s['Rl']:.1f} V {s['V']:.0f} M_* {s['Ms']:.2e} M_gas {s['Mg']:.2e} M200 EM1 {s['M200e']:.2e} share {s['M200s']:.2e} M_c(R_last) EM1 {s['Mcn']:.2e} share {s['Mcs']:.2e}")
L = SYS[3]; L2 = SYS[4]
def spec_need(g, mass, R_out=None):
    """Specific energy (m/s)^2 to lift cold out of R_last in log potential at V_flat, mass-weighted."""
    M200 = M200_of(g, mass); Rl = g["R"].max(); rr = np.geomspace(Rl * 1e-3, Rl, 200); Mc = Mc_native(M200, rr); dm = np.gradient(Mc); V2 = g["Vflat"] ** 2 * KMS2; e = float(np.sum(dm * V2 * np.log(Rl / rr))) / float(Mc[-1]); return e, float(Mc[-1])
ROWS = {}
def row(n, label, const, part, text, **k): ROWS[n] = dict(label=label, const=const, particle=part, text=text, **k); P(f"\n[{n}] {label} | constants {const} | particle-like {part}\n    {text}")
# ---- 1 law-field contraction
def contract_law(rg, Mb, M0, F, a):
    """Cold conserves r x (M_i + law mass of its own baryons) with the law's term in both states: initial baryons trace cold, final baryons Mb. Blumenthal is the a -> 0 limit."""
    Mlaw = lambda M, r: law(np.maximum(G * M * MS / r ** 2, 1e-40), a) * r ** 2 / G / MS
    lr = np.log(rg); Rt = rg * (M0 + Mlaw(F * M0, rg)); lo, hi = rg * 1e-3, rg * 1.0001
    for _ in range(40):
        c = np.sqrt(lo * hi); Mg = np.interp(np.log(c), lr, Mb); v = c * (M0 + Mlaw(Mg, c)); lo, hi = np.where(v < Rt, c, lo), np.where(v < Rt, hi, c)
    o = np.maximum.accumulate(np.sqrt(lo * hi)); return np.interp(lr, np.log(o), M0, left=0.0, right=M0[-1])
def law_pair(g, a, mass="share", U=.5):
    R = g["R"]; Mb = Mbtot(g, U); M200 = M200_of(g, mass); Rv = r200(M200); rg = np.geomspace(R[0] * .05, Rv * 1.2, 200); M0 = Mc_native(M200, rg); Mbk = np.maximum.accumulate(np.maximum(gbar(g, U) * R ** 2 / G / MS, 0)); Mt = max(Mbk[-1], Mb); Mg = np.where(rg < R[0], Mbk[0] * (rg / R[0]) ** 2, np.interp(np.log(rg), np.log(R), Mbk)); o = rg > R[-1]; t = np.clip(np.log(rg[o] / R[-1]) / math.log(3), 0, 1); Mg[o] = np.exp(np.log(max(Mbk[-1], 1e-30)) * (1 - t) + np.log(Mt) * t); Mg = np.maximum.accumulate(Mg); F = Mt / float(M0[-1]); Mf = contract_law(rg, Mg, M0, F, a); return G * np.interp(np.log(R), np.log(rg), M0) * MS / R ** 2, G * np.interp(np.log(R), np.log(rg), Mf) * MS / R ** 2
rows1 = []
for ft in FEET:
    for i in (1, 3, 4):
        rat = []; its = []
        for g in BY[i]:
            a, b = cold_pair(g, .5, "share"); a2, b2 = law_pair(g, A0[ft]); m = outer(g); rat.append(float(np.mean(b2[m] / b[m]))); its.append(item(g, .5, a2, b2, FQ))
        rows1.append((ft, BN[i], float(np.median(rat)), psi_bin(its, A0[ft], "N")["psi"], psi_bin([item(g, .5, *cold_pair(g, .5, "share"), FQ) for g in BY[i]], A0[ft], "N")["psi"]))
row("1 law-field contraction", "CLOSED AT G1", 0, "no", "Cold conserves r(M_i + law mass) with the law's term in both states, share mass: cold at outer third over Newtonian contraction, psi with it, psi Newtonian: " + "; ".join(f"{a} {b} x{c:.2f} psi {d:.2f} (was {e:.2f})" for a, b, c, d, e in rows1) + ". Removes nothing; it only changes how far the cold falls.", data=rows1)
# ---- 2 streaming
vrel = 30.0  # km/s at z 1000, PROVISIONAL
zz = np.geomspace(1, 1000, 4000); Hz = lambda z: 100 * H0N * np.sqrt(OMN * (1 + z) ** 3 + 1 - OMN)
xc = np.trapz(vrel * ((1 + zz) / 1001) * (1 + zz) / Hz(zz) * 1 / (1 + zz) * (1 + zz) / (1 + zz), zz)
rhom = OMN * RHOC / MSPC3 * (0.6856 / H) ** 2 * 1e18  # Msun/Mpc^3
RLg = [(3 * s["M200e"] / (4 * math.pi * rhom)) ** (1 / 3) for s in SYS]
row("2 streaming velocity", "CLOSED AT G1", 0, "no", f"30 km/s at z 1000 (PROVISIONAL): comoving drift {xc:.3f} Mpc against Lagrangian radius by bin " + " ".join(f"{r:.2f}" for r in RLg) + f" Mpc: ratio {xc / RLg[3]:.3f} at 150-200, {xc / RLg[1]:.3f} at 60-100. Moves baryons relative to cold, removes none, larger for dwarfs. Short x{Rq / (xc / RLg[3]):.0f} even read as a removal fraction.", drift=xc)
# ---- 3 GMC scattering
out3 = []
for s, Mp in ((L, 1e6), (L, 1e7), (L2, 1e7)):
    Rl = s["Rl"] * 1e3; rho_p = s["Mg"] / (4 / 3 * math.pi * Rl ** 3); sig = s["V"] / math.sqrt(2); dv2 = 8 * math.pi * GPC ** 2 * Mp * rho_p * 10.0 / sig * (1.38e10 * YR / (PC * 1e0) * 1e3)  # (km/s)^2
    need = s["V"] ** 2 * 1.0; out3.append((s["bin"], Mp, dv2 / 2, need))
row("3 GMC and cluster scattering", "CLOSED AT G1", 0, "no", "All gas in clumps of M_p, smeared over R_last, lnL 10, 13.8 Gyr (generous; PROVISIONAL clump mass): specific energy, (km/s)^2 / need V^2: " + "; ".join(f"{a} M_p {b:.0e}: {c:.0f} / {d:.0f} = {c / d:.2f}" for a, b, c, d in out3) + ". Clump lives 10-30 Myr so x 0.3 duty at best is not applied; a clump of 1e7 is at the top end. Rises with gas, not V, and gas-rich dwarfs get it first.", data=out3)
# ---- 4 spirals
rd = []
for s in (L, L2):
    Md = s["Mb"]; Rd = s["Rl"] * 1e3 / 4; Jd = 2 * Md * Rd * s["V"]; Om = s["V"] / (2.2 * Rd); e_tot = s["Mcs"] * 1.0 * s["V"] ** 2; rd.append((s["bin"], e_tot * Rqs / (Om * Jd), s["Mcn"] * s["V"] ** 2 * Rq / (Om * Jd)))
row("4 transient spirals", "CLOSED AT G1", 0, "no", "J budget: fraction of the disc's J the cold must absorb to pay lifting at corotation Omega_p = V/2.2 R_d, share / EM1: " + "; ".join(f"{a} {b:.2f} / {c:.2f}" for a, b, c in rd) + ". So about all of the disc's J or more, while observed discs keep most of theirs (retention near 0.6-1, PROVISIONAL): at most 0.4 of J can go, short x2.6 or more at perfect delivery. LC1 has no spirals; the exchange efficiency itself isn't computed, and it reaches cold only at resonances. Bars with stronger torque leave unbarred discs at the same miss (BT1), and spirals are not stronger than bars.", data=rd)
# ---- 5 tides
rt = [(s["bin"], 1000 * (s["M200e"] / (3 * 1e12)) ** (1 / 3) / s["Rl"]) for s in SYS]
Mhost = [(s["bin"], s["M200e"] * (1000 / s["Rl"]) ** 3 / 3) for s in SYS]
row("5 tides", "CLOSED AT G2", 0, "no", "Jacobi radius at 1 Mpc from a 1e12 host over R_last: " + " ".join(f"{a} x{b:.0f}" for a, b in rt) + ". Host mass at 1 Mpc that strips to R_last: " + " ".join(f"{a} {b:.1e}" for a, b in Mhost) + ". SPARC spirals aren't all within 1 Mpc of a rich cluster. Backsplash 'few %' of field (PROVISIONAL). Smaller systems first.", data=rt)
# ---- 6 vacuum
rl = (1 - OMN) * 3 * (100e3 * H0N / MPC) ** 2 / (8 * math.pi * G)
rta = [(s["bin"], (3 * s["M200e"] * MS / (8 * math.pi * rl)) ** (1 / 3) / KPC / s["Rl"]) for s in SYS]
row("6 vacuum repulsion", "CLOSED AT G1", 0, "no", "Zero-force radius (3M/8 pi rho_v)^1/3, native background, over R_last: " + " ".join(f"{a} x{b:.0f}" for a, b in rta) + ". Force ratio at R_last order (R_last/r)^3, under 1e-3.", data=rta)
# ---- 7 selection
scat = 0.15  # dex, PROVISIONAL
dM = -math.log10(1 - Rq); from scipy.stats import norm
Blr = json.load(open(os.path.join(RB, "BL1_blue_lens_halo_mass", "bl1_results.json")))["k"]["law"]["canonical"]
row("7 population selection", "CLOSED AT G1", 0, "no", f"If discs were a low-cold tail, psi {1 - Rq:.2f} is {dM:.2f} dex at fixed M_b, {dM / scat:.1f} sigma on 0.15 dex scatter (PROVISIONAL): P {norm.sf(dM / scat):.1e}, while discs are most systems at these masses. Share row: {-math.log10(1 - Rqs):.2f} dex, {-math.log10(1 - Rqs) / scat:.1f} sigma, P {norm.sf(-math.log10(1 - Rqs) / scat):.1e}. Blue lenses are the whole blue population and reach A {Blr['blue']['A']:.3f}+-{Blr['blue']['sA']:.3f} of the law alone (BL1), so the room isn't a SPARC selection. Note: this works against removal out of R_last only: blue lens window reaches 100s of kpc, so removal must go to about R200, MC1's x69-300 row.")
# ---- 8 BH
bh = []
for i in (3, 4):
    gs = BY[i]; ratio = np.median([0.002 * 0.5 * 1.4 * max(np.max(np.abs(g["Vb"]) ** 2 * g["R"] / G * KMS2 / MS), 1e0) / float(Mc_native(M200_of(g, "share"), g["R"].max())) for g in gs]); bh.append(float(ratio))
row("8 black hole accretion", "CLOSED AT G1", 0, "no", f"M_BH = 0.002 M_bulge (PROVISIONAL), M_BH / M_c(R_last, share): 150-200 {bh[0]:.1e}, 200-250 {bh[1]:.1e}. All mass ever eaten is below M_BH. Short x{Rqs / max(bh):.0f}.", data=bh)
# ---- X-COP numbers
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m))) if r[0] <= t <= r[-1] else np.nan
XC = []; DX = os.path.join(REPO, "real_research", "data", "xcop")
for n in sorted(os.listdir(DX)):
    p_ = os.path.join(DX, n)
    if not (os.path.isdir(p_) and os.path.exists(os.path.join(p_, f"{n}_mstar.fits"))): continue
    with fits.open(os.path.join(p_, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg5 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{n}_mstar.fits")) as h: st = h[2].data.copy()
    XC.append({x: (x * r5, li(hm["RADIUS"], hm["M_FORW"], x * r5), li(ga["RADIUS"] * rg5, ga["MGAS"], x * r5), li(st["RADIUS"], st["MSTAR"], x * r5)) for x in (.1, .3, .5)})
xq = {x: tuple(np.nanmedian([c[x][j] for c in XC]) for j in range(4)) for x in (.1, .3, .5)}; P("X-COP medians (r kpc, M_HSE, M_gas, M_*): " + str({k: tuple(f"{a:.3g}" for a in v) for k, v in xq.items()}))
GN_err = {.1: .38 / 6.73, .3: .51 / 5.94, .5: .63 / 4.80}  # MC1's Gamma_N error / value: X-COP's own fractional error
# ---- 9 universal decay
gdec = {x: Rq for x in xq}
row("9 universal decay", "CLOSED AT G5", 1, "yes", f"Rate from removal R {Rq:.2f}/{Rqs:.2f}, tau {13.8 / -math.log(1 - Rq):.1f}/{13.8 / -math.log(1 - Rqs):.1f} Gyr. No place selector, so clusters lose the same: X-COP inner share down x{1 / (1 - Rq):.1f}/x{1 / (1 - Rqs):.1f} against own error {GN_err[.1]:.2f}, so over by x{Rq / GN_err[.1]:.0f}/x{Rqs / GN_err[.1]:.0f}. Decay into a non-gravitating channel also drops the matter budget.")
# ---- 10, 11 exposure
def rbar(M, Rkpc): return M / (4 / 3 * math.pi * (Rkpc * 1e3) ** 3)
Or = 9.1e-5 * 0.6856 ** -2 * 0 + 4.15e-5 / H0N ** 2
def expos_cmb(z0=3e4, z1=1090):
    zg = np.geomspace(z1, z0, 3000); H_ = 100e3 * H0N / MPC * np.sqrt(OMN * (1 + zg) ** 3 + Or * (1 + zg) ** 4); return float(np.trapz(RHOB0 / MSPC3 * (1 + zg) ** 3 / (H_ * (1 + zg)), zg)) / YR
Ecmb = expos_cmb(); Ecmb2 = expos_cmb(z0=1e6)
Ed = [rbar(s["Mb"], s["Rl"]) * 13.8e9 for s in SYS]; Ecl = {x: rbar(v[2] + v[3], v[0]) * 8e9 for x, v in xq.items()}
sig10 = -math.log(1 - Rq) / np.median(Ed[3:5]); sig10s = -math.log(1 - Rqs) / np.median(Ed[3:5])
row("10 conversion on baryon density", "CLOSED AT G7", 1, "yes", f"Exposure rho_b t, Msun/pc^3 yr. Disc, mean inside R_last by bin: " + " ".join(f"{e:.1e}" for e in Ed) + f". X-COP M_b, 8 Gyr, x .1 .3 .5: " + " ".join(f"{Ecl[x]:.1e}" for x in Ecl) + f". CMB era, z 3e4 to 1090: {Ecmb:.2e}; from 1e6: {Ecmb2:.2e}. Rate set by R at 150-250 EM1 / share: cold lost before last scattering {1 - math.exp(-sig10 * Ecmb):.3f} / {1 - math.exp(-sig10s * Ecmb):.3f} against the 1 % gate: over x{(1 - math.exp(-sig10 * Ecmb)) / 0.01:.0f} / x{(1 - math.exp(-sig10s * Ecmb)) / 0.01:.0f}. X-COP inner lost {1 - math.exp(-sig10 * Ecl[.1]):.3f}. Disc exposure hardly varies by bin, so no trend.", E_cmb=Ecmb, E_disc=Ed, E_cl=Ecl)
# 11 stars
def retained_star(g, sg, mass="em1"):
    Rl = g["R"].max(); rr = np.geomspace(g["R"][0] * .2, Rl, 80); Mc = Mc_native(M200_of(g, mass), rr); Ms = .5 * g["L36"] * 1e9
    Mst_r = np.maximum.accumulate(np.interp(np.log(rr), np.log(g["R"]), np.maximum(((np.abs(g["Vd"]) * g["Vd"] * .5 + np.abs(g["Vb"]) * g["Vb"] * .7) * KMS2 * g["R"] / G / MS), 0), left=0)); rho = Mst_r / (4 / 3 * math.pi * (rr / PC) ** 3); dm = np.diff(Mc, prepend=0); return float(np.sum(dm * np.exp(-sg * rho * 13.8e9)) / Mc[-1])
def fit11(R, mass):
    lo, hi = 1e-14, 1e-6
    for _ in range(40):
        c = math.sqrt(lo * hi); v = np.median([retained_star(g, c, mass) for g in BY[3] + BY[4]]); lo, hi = (c, hi) if v > 1 - R else (lo, c)
    return c
for mass, R_ in (("em1", Rq), ("share", Rqs)):
    sg = fit11(R_, mass); ret = [float(np.median([retained_star(g, sg, mass) for g in gs])) for gs in BY]; need = [1 - RN[b][mass] for b in BN]
    Ecs = {x: (v[3] / (4 / 3 * math.pi * (v[0] * 1e3) ** 3)) * 13.8e9 for x, v in xq.items()}; lost = {x: 1 - math.exp(-sg * e) for x, e in Ecs.items()}; lost8 = {x: 1 - math.exp(-sg * e * 8 / 13.8) for x, e in Ecs.items()}
    RES[f"star_{mass}"] = dict(sigma=sg, retained=ret, need=need, cl_lost=lost, cl_lost8=lost8)
    P(f"  [11 {mass}] sigma {sg:.2e} (Msun/pc^3 yr)^-1; retained by bin " + " ".join(f"{a:.2f}" for a in ret) + " | allowed psi " + " ".join(f"{a:.2f}" for a in need) + " | X-COP lost, 13.8 Gyr x .1 .3 .5 " + " ".join(f"{a:.3f}" for a in lost.values()) + " ; at 8 Gyr " + " ".join(f"{a:.3f}" for a in lost8.values()) + " | own error " + " ".join(f"{GN_err[x]:.3f}" for x in xq))
s_ = RES["star_em1"]; s2 = RES["star_share"]
row("11 conversion on stellar density", "NO CHANNEL (G3); other gates in dw2_second.out", 1, "yes", f"Exposure rho_*(<r) t shell by shell; no stars before z about 20, so CMB untouched (G7 clear). Numbers above. X-COP's BCG region sits at comparable stellar density, EM1 row loses {s_['cl_lost8'][.1]:.2f} at x .1 at 8 Gyr, share {s2['cl_lost8'][.1]:.2f}, own error {GN_err[.1]:.2f}. Couples cold to stars non-gravitationally; solar neighbourhood implies a stellar energy or momentum signal, not computed.")
# ---- 12 kick, log-potential estimate
Vcl = 1200.0
def vk_need(s, Rv=None): return s["V"] * math.sqrt(2 * math.log(r200(s["M200s"]) / KPC / s["Rl"]))
vk = max(vk_need(s) for s in (SYS[3], SYS[4])); RES["Rtight"] = max(RN[b]["em1"] for b in BN[3:5]); fr = {x: None for x in xq}
for x, v in xq.items():
    Mt = lambda r: float(Mc_native(v[1] * 1.3, r * KPC)); f_ = math.exp(vk ** 2 / (2 * Vcl ** 2)); fr[x] = Mt(v[0] / f_) / Mt(v[0])
RES["kick"] = dict(vk=vk, frac=fr)
P(f"  [12] v_k to leave R200 from R_last at 150-250: {vk:.0f} km/s; mean radius factor in cluster V {Vcl:.0f}: {math.exp(vk ** 2 / (2 * Vcl ** 2)):.3f}; M(<r/f)/M(<r) x .1 .3 .5 " + " ".join(f"{a:.3f}" for a in fr.values()) + f"; cluster cold loss at decayed share R {Rq:.2f}: " + " ".join(f"{Rq * (1 - a):.3f}" for a in fr.values()) + f"; share R {Rqs:.2f}: " + " ".join(f"{Rqs * (1 - a):.3f}" for a in fr.values()) + " against own error " + " ".join(f"{GN_err[x]:.3f}" for x in xq))
row("12 decay with a kick", "NEAR MISS, see dw2_second.out", 2, "yes", f"tau {13.8 / -math.log(1 - Rq):.1f}/{13.8 / -math.log(1 - Rqs):.1f} Gyr, v_k {vk:.0f} km/s. Collisionless, passes the Bullet in principle. Dust through the CMB: decay later. Published, PROVISIONAL, on a CDM frame: Peter et al. 2010 exclude v_k > 100 and tau under a few t0 on clusters; Wang et al. 2013 forest tau under 10 Gyr for v_k above 30-70. Red lens need at the same mass has no selector.")
# ---- 13 compact
s = L; rho_c = s["Mcn"] * 3 / (4 * math.pi * (s["Rl"] * 1e3) ** 3); rho_loc = rho_c / 3; sig = s["V"] / math.sqrt(2); xi = 0.0074
tneed = 13.8e9 * YR * xi / -math.log(1 - Rq)  # t_rel so evaporation removes R: dM/M = xi dt/t_rel
Mo = 0.34 * (sig * 1e3) ** 3 / (G ** 2 * rho_loc * MSPC3 * 10 * tneed) / MS
Mo_fast = 0.34 * (sig * 1e3) ** 3 / (G ** 2 * rho_loc * MSPC3 * 10 * (13.8e9 * YR)) / MS
row("13 compact objects", "CLOSED AT G1 via disc heating", 1, "yes", f"Object mass for evaporation (xi {xi}, lnL 10, rho {rho_loc:.1e} Msun/pc^3, sigma {sig:.0f}) to remove R {Rq:.2f}: M_o {Mo:.1e} Msun; t_rel = 13.8 Gyr alone would need {Mo_fast:.1e}. Published disc-heating limit about 3e6 (Lacey and Ostriker 1985, from memory, PROVISIONAL): over x{Mo / 3e6:.0f}. Friction sinks such objects inward first, adds central mass.", Mo=Mo)
# ---- 14 self-interaction
gO = lambda s: s
s = L; rho_R = rho_loc * MSPC3 * 1e-3  # g/cm^3
sm = 1 / (rho_R * (s["V"] * 1e5) * 13.8e9 * YR); P(f"  [14] sigma/m for Gamma t = 1 at R_last, 150-200: {sm:.2f} cm^2/g; published limit 0.47-1.25 (Harvey 2015; Randall 2008, PROVISIONAL)")
# isothermal Jeans with baryons, typical galaxy at 150-200; match M, rho at r1 = k R_last
g = sorted(BY[3], key=lambda q: abs(q["Vflat"] - L["V"]))[0]; M200 = M200_of(g, "em1"); Rl = g["R"].max()
MbF = lambda r: float(np.interp(math.log(r), np.log(g["R"]), np.maximum.accumulate(np.maximum(gbar(g, .5) * g["R"] ** 2 / G / MS, 0)), left=0.0)) if r < g["R"][0] else float(np.interp(math.log(r), np.log(g["R"]), np.maximum.accumulate(np.maximum(gbar(g, .5) * g["R"] ** 2 / G / MS, 0))))
sidm = []
for k in (1.0, 2.0, 4.0):
    r1 = k * Rl; rr = np.array([r1 * .99, r1 * 1.01]); M1 = float(Mc_native(M200, np.array([r1]))[0]); M_ = Mc_native(M200, rr); rho1 = (M_[1] - M_[0]) * MS / (4 / 3 * math.pi * (rr[1] ** 3 - rr[0] ** 3))
    def shoot(p):
        rho0, s2 = math.exp(p[0]), math.exp(p[1])
        def f(r, y): return [4 * math.pi * r ** 2 * y[1], -y[1] * G * (y[0] + MbF(r) * MS) / (r ** 2 * s2)]
        sol = solve_ivp(f, (1e18, r1), [4 / 3 * math.pi * 1e54 * rho0, rho0], method="RK45", rtol=1e-5, atol=[1e30, 1e-30], max_step=r1 / 40)
        return sol, np.array([math.log(max(sol.y[0, -1], 1e-300) / (M1 * MS)), math.log(max(sol.y[1, -1], 1e-300) / rho1)])
    x, _, ier, _ = fsolve(lambda p: shoot(p)[1], [math.log(rho1 * 30), math.log((g["Vflat"] * 1e3) ** 2 / 2)], full_output=True, xtol=1e-3, maxfev=60)
    sol, res = shoot(x); M_RL = float(np.interp(Rl, sol.t, sol.y[0])) / MS; M_n = float(Mc_native(M200, np.array([Rl]))[0]); sidm.append((k, M_RL / M_n, float(np.abs(res).max())))
P("  [14] isothermal Jeans in the baryon well, M(<R_last)/native, match at k R_last: " + " ".join(f"k {a:.0f}: {b:.2f} (res {c:.0e})" for a, b, c in sidm)); RES["sidm"] = sidm
row("14 self-interaction", "CLOSED AT G1", 1, "yes", f"Needs sigma/m {sm:.2f} cm^2/g to thermalise to R_last at 150-200, against Bullet 0.47-1.25 (PROVISIONAL). Mass conserved at the match radius; removal at R_last read above, against need {Rq:.2f}. In a baryon well it doesn't take mass out.", data=sidm)
# ---- 15 ultralight
def retained_sol(s, m22, M200k):
    M = s[M200k]; rc = 1.6 / m22 * (M / 1e9) ** (-1 / 3); rho0 = 0.019 / m22 ** 2 / rc ** 4  # Msun/pc^3, Schive+ 2014 PROVISIONAL
    Ms_ = lambda r: quad(lambda x: 4 * math.pi * (x * 1e3) ** 2 * 1e3 * rho0 / (1 + 0.091 * (x / rc) ** 2) ** 8, 0, r)[0]; Rl = s["Rl"]; rt = 3.3 * rc; Mn = lambda r: float(Mc_native(M, np.array([r * KPC]))[0])
    return (Ms_(Rl) if Rl <= rt else Ms_(rt) + max(Mn(Rl) - Mn(rt), 0)) / Mn(Rl)
mg = [1e-3, 3e-3, .01, .03, .1, .3, 1, 3, 10]; tab = {m: [retained_sol(s, m, "M200e") for s in SYS] for m in mg}
P("  [15] m22: M(<R_last)/native by bin, EM1 mass, core-halo fit extrapolated")
for m in mg: P(f"     {m:7.3f} " + " ".join(f"{a:8.2f}" for a in tab[m]))
RES["sol"] = tab; best = min(tab[m][3] for m in mg); bm = min(mg, key=lambda m: tab[m][3])
row("15 ultralight scalar core", "CLOSED AT G1 in the baryon well, see dw2_second.out", 1, "yes", f"Least retained at 150-200 over the grid {best:.2f} at m22 {bm}. Requires {1 - Rq:.2f}/{1 - Rqs:.2f}.")
RES["rows"] = ROWS
json.dump(RES, open(os.path.join(HERE, f"dw2_proc_results{TAG}.json"), "w"), indent=1, default=float, sort_keys=True); open(os.path.join(HERE, f"dw2_proc{TAG}.out"), "w").write("\n".join(OUT) + "\n")
