#!/usr/bin/env python3
"""DB1 physical-existence gates (a)-(e), FROZEN_CRITERIA.md. Order-of-magnitude; literature inputs PROVISIONAL, several from memory, labelled.
Amounts from the fitted arms on X-COP at 300 kpc and from the Bullet rows. cgs inside. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
sys.dont_write_bytecode = True
import numpy as np
import db1_core as C
OUT = open("db1_phys.out", "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
G = 6.674e-8; MP = 1.6726e-24; KB = 1.380649e-16; ME = 9.109e-28; CL = 2.998e10; MSUN = 1.989e33; KPCc = 3.0857e21; MPCc = 3.0857e24
TH = 13.97e9 * 3.15576e7  # 1/H0, H0 70 km/s/Mpc (raw local value class; not a LCDM input)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; LJ = json.load(open("db1_lambda.json")); GR = json.load(open("db1_grade.json"))
res = {}
# ---------- amounts: X-COP clusters at r = 300 kpc, 3D, per arm, canonical and alt
from astropy.io import fits
def at300(name, foot, arm):
    T = C.xcop_table()[name]; p = os.path.join(C.XDIR, name); r = 300.0
    with fits.open(os.path.join(p, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    mg = float(C.mgas_interp(T, r * 1e3 * C.PCm)) / C.MS; ms = float(10 ** np.interp(np.log10(r), np.log10(st["RADIUS"]), np.log10(st["MSTAR"])))
    rr = r * 1e3 * C.PCm; gg = C.G * mg * C.MS / rr ** 2; gs = C.G * ms * C.MS / rr ** 2; gb = gg + gs; a = A0[foot]
    Q = dict(gb=np.array([gb]), gg=np.array([gg]), gs=np.array([gs]), r=np.array([rr]), r500=np.array([T["r5"]]), a0=a, sample="cluster")
    tot = float(C.g(Q, arm)[0]); gx = tot * tot / (tot + a) - gb; return dict(Mgas=mg, Mstar=ms, Mcb=gx * rr ** 2 / C.G / C.MS, Mtot=tot * rr ** 2 / C.G / C.MS)
names = sorted(n for n, t in C.xcop_table().items() if t["ms5"] is not None)
say("== amounts at 300 kpc (3D), X-COP 7 clusters; M_cb from law(g_b + g_cb) = model g. Median over clusters.")
AM = {}
for arm in ("P1", "P1G", "P2", "P3"):
    for f in ("canonical", "alt"):
        v = [at300(n, f, arm) for n in names]; Mcb = np.median([x["Mcb"] for x in v]); Mg = np.median([x["Mgas"] for x in v]); Mt = np.median([x["Mtot"] for x in v]); fr = np.median([x["Mcb"] / x["Mtot"] for x in v]); rg = np.median([x["Mcb"] / x["Mgas"] for x in v])
        AM[f"{arm}|{f}"] = dict(Mcb=Mcb, Mgas=Mg, Mtot=Mt, frac=fr, cb_over_gas=rg)
        say(f"  {arm:4s} {f:9s} M_cb {Mcb:.2e} Msun, M_gas {Mg:.2e}, M_cb/M_gas {rg:.2f}, M_cb/M_model {fr:.2f}")
res["amounts_300kpc"] = AM
# The governing case for (a)-(d): the arm that passes X-COP with a fit, P1G canonical. Others scale with M_cb.
ref = AM["P1G|canonical"]; R3 = 300 * KPCc; Mcb = ref["Mcb"] * MSUN
Sig_cb = Mcb / (math.pi * R3 ** 2)  # 3D mass inside 300 kpc over pi R^2: a lower bound on the projected column at R < 300 kpc
rho_cb = Mcb / (4 / 3 * math.pi * R3 ** 3)
say(f"\n== governing case P1G canonical: M_cb(<300 kpc) {ref['Mcb']:.2e} Msun, mean Sigma_cb >= {Sig_cb:.3e} g/cm^2, rho_cb {rho_cb:.2e} g/cm^3")
# (a) X-ray absorption
NH_mean = 0.75 * Sig_cb / MP; lim = 2e20
say(f"(a) mean excess N_H if spread: {NH_mean:.2e} cm^-2 against {lim:.0e} (PROVISIONAL, Chandra/XMM N_H agreeing with Galactic HI at about that level, from memory): {'diffuse ALLOWED' if NH_mean <= lim else 'diffuse EXCLUDED, must be clumped'}")
Sa = max(Sig_cb / 0.10, 1e22 * MP / 0.75)
say(f"    clumped and grey (N_c >= 1e22) with covering f_c <= 0.10 needs Sigma_c >= {Sa:.3e} g/cm^2 (N_c >= {0.75 * Sa / MP:.2e})")
# (b) Bullet: swept column, self-gravity against ram pressure
M_g, a_g = 2.0e14 * MSUN, 565 * KPCc; rho_icm = 3 * M_g / (4 * math.pi * a_g ** 3); v = 4.7e8; Sig_sw = rho_icm * 1000 * KPCc
Sb1 = 3 * Sig_sw; Sb2 = math.sqrt(rho_icm * v * v / G); Sb = max(Sb1, Sb2)
say(f"(b) Bullet main gas central rho {rho_icm:.2e} g/cm^3 (n_e {rho_icm / (1.17 * MP):.1e}), UX6 model; swept column over 1 Mpc {Sig_sw:.3e}; need Sigma_c >= 3x = {Sb1:.3e}; self-gravity G Sigma^2 >= rho v^2 at 4700 km/s needs Sigma_c >= {Sb2:.3e}")
# (c) conduction, saturated; collisions
T = 1e8; ne = 3e-3; kT = KB * T; qsat = 0.4 * ne * kT * math.sqrt(2 * kT / (math.pi * ME)); h = 2.5 * kT / (0.6 * MP); Sc1 = qsat * TH / h; Sc1m = Sc1 / 100
sv = 1e8; Sc2 = rho_cb * sv * TH; Sc = max(Sc1, Sc2)
say(f"(c) saturated heat flux {qsat:.2e} erg/cm^2/s at T 1e8 K, n_e 3e-3 (Cowie and McKee 1977 form); mass evaporated over 1/H0: {Sc1:.3e} g/cm^2 (x 1/100 magnetic suppression: {Sc1m:.1e}, reported only)")
say(f"    cloud-cloud collisions, t_coll = Sigma_c/(rho_cb sigma_v) >= 1/H0 at sigma_v 1000 km/s: Sigma_c >= {Sc2:.3e} g/cm^2 (sigma/m <= {1 / Sc2:.2f} cm^2/g)")
# (d) microlensing threshold
Dg = 1000 * MPCc; Scr = CL ** 2 / (4 * math.pi * G * Dg)
say(f"(d) a cloud is a microlens when Sigma_c > Sigma_cr = c^2/(4 pi G D), D 1 Gpc: {Scr:.3f} g/cm^2. CBDM share of the model mass at 300 kpc: {ref['frac']:.2f} (gate 0.10, PROVISIONAL reading of Oguri+2018)")
lo = max(Sa, Sb, Sc); win = lo < Scr
say(f"\n== cloud window: survival needs Sigma_c >= {lo:.3f} g/cm^2 (max of a, b, c); not a microlens needs Sigma_c < {Scr:.3f}. Window {'OPEN' if win else 'CLOSED'}: ratio {lo / Scr:.2f}")
lo_m = max(Sa, Sb, Sc2, Sc1m); say(f"   with conduction suppressed 100x: need >= {lo_m:.3f}; window {'OPEN' if lo_m < Scr else 'CLOSED'}, ratio {lo_m / Scr:.2f}")
for arm in ("P1", "P2", "P3"):
    Ma = AM[f"{arm}|canonical"]["Mcb"] * MSUN; s_ = Ma / (math.pi * R3 ** 2); r_ = Ma / (4 / 3 * math.pi * R3 ** 3); l_ = max(s_ / 0.10, 1e22 * MP / 0.75, Sb, Sc1, r_ * sv * TH); say(f"   {arm} canonical: need >= {l_:.3f}, ratio {l_ / Scr:.2f}")
# Jeans at the floor, for the cloud class
Tc = 2.73; cs = math.sqrt(KB * Tc / (2.33 * MP)); mJ = cs ** 4 / (G * G * lo); aJ = math.sqrt(mJ / (math.pi * lo)); rho_c = lo / (4 / 3 * aJ); tff = math.sqrt(3 * math.pi / (32 * G * rho_c))
say(f"   a cloud at the window's lower edge, T 2.73 K: bound mass c_s^4/(G^2 Sigma) {mJ / MSUN:.1e} Msun, radius {aJ / 1.496e13:.0f} AU, free-fall {tff / 3.156e7:.1e} yr; heavier clouds collapse unless supported, and would make stars or brown dwarfs")
# compact classes
say("\n== object classes (gates a-e)")
CL_ = []
def cls(name, a, b, c, d, e, note):
    ok = all(x == "pass" for x in (a, b, c, d, e)); CL_.append(dict(cls=name, a=a, b=b, c=c, d=d, e=e, survives=ok, note=note)); say(f"  {name:34s} a {a:6s} b {b:6s} c {c:6s} d {d:10s} e {e:9s} -> {'SURVIVES' if ok else 'does not survive'}; {note}")
fr = ref["frac"] > 0.10
cls("dense cold H2 clouds (sub-critical)", "pass" if win else "fail", "pass" if win else "fail", "pass" if win else "fail", "pass", "pass", f"window {'open' if win else 'closed'} at ratio {lo / Scr:.2f} (need/limit); collisions alone need {Sc2:.2f} against Sigma_cr {Scr:.2f}")
cls("dense cold H2 clouds (super-critical)", "pass", "pass", "pass", "fail" if fr else "pass", "pass", "compact enough to microlens; caustic-crossing limit 1e-5-1e2 Msun (Oguri+2018, PROVISIONAL)")
cls("sub-Earth H/He bodies (< 1e-5 Msun)", "pass", "pass", "untested", "pass", "pass", "below caustic-crossing range; survival of H/He solids not computed here (PROVISIONAL: thought to sublimate), NOT ESTABLISHED")
cls("Jupiters, brown dwarfs (1e-3-0.08)", "pass", "pass", "pass", "fail" if fr else "pass", "pass", "inside the caustic-crossing mass range at a high share of the core mass")
cls("stellar remnants (WD, NS, stellar BH)", "pass", "pass", "pass", "fail", "pass", "microlensing range, and progenitors' metals: ~2 % yield on 4.8x the gas gives ~0.1 of the gas mass in metals against the ICM's ~0.004 (0.3 solar), ~25x over (PROVISIONAL)")
# massive BHs: heating and Bondi
rho = rho_cb; vv = 1e8; heat = lambda M, sig: 8 * math.pi * G * G * rho * M * 10 / vv * TH / sig ** 2
Mh = {s: (s ** 2) / (8 * math.pi * G * G * rho * 10 / vv * TH) / MSUN for s in (2e7, 5e6)}
cs_icm = 1.5e8; rho_g = rho_icm
def Lbondi(M): Md = 4 * math.pi * G * G * (M * MSUN) ** 2 * rho_g / (cs_icm ** 2 + vv ** 2) ** 1.5; return 0.1 * Md * CL * CL
Ltot = {m: Lbondi(m) * (ref["Mcb"] / m) for m in (1e2, 1e4, 1e6)}
say(f"  massive BHs: heating of cluster galaxies over 1/H0 reaches sigma^2 at M_BH {Mh[2e7]:.1e} Msun (sigma 200 km/s), {Mh[5e6]:.1e} (50 km/s); total Bondi-Hoyle L at efficiency 0.1: " + ", ".join(f"{m:.0e} Msun {L:.1e} erg/s" for m, L in Ltot.items()))
cls("massive black holes (1e2 to ~1e7 Msun)", "pass", "pass", "pass", "pass", "pass", f"above the caustic range, below galaxy heating; accretion luminosity {Ltot[1e6]:.0e} erg/s at 1e6 against a core L_X ~1e44-1e45; no known channel makes ~5x the gas in BHs without stars or metals; millilensing not computed")
# (e) budget, raw data only
ob = 0.02166; rho_b = ob * 1.878e-29  # g/cm^3, BBN with D/H (Cooke+2018, PROVISIONAL, from memory)
say(f"\n(e) BBN with D/H: Omega_b h^2 {ob} (Cooke+2018, PROVISIONAL, from memory; not Planck) -> rho_b {rho_b:.2e} g/cm^3, h-free")
for share in (0.04, 0.10):
    for arm in ("P1G", "P3"):
        k = AM[f"{arm}|canonical"]["cb_over_gas"]; say(f"    hot cluster gas {share:.0%} of cosmic baryons (PROVISIONAL census range) x M_cb/M_gas {k:.1f} at 300 kpc ({arm}): CBDM {share * k:.0%} of all baryons, clusters only")
say("    FRB dispersion measures (Macquart+2020, PROVISIONAL, from memory) find the ionized baryons consistent with BBN to roughly +-40 %; cold compact baryons don't add dispersion, so a 20-50 % hidden share is inside those errors: (e) reads pass within errors only, weak")
say("    If the same lambda applies to the hot gas of groups (the rule's reading, which B1 already fails), the hidden share grows with the group gas, not computed here")
res.update(window=dict(need=lo, Sigma_cr=Scr, open=bool(win), need_suppressed=lo_m), classes=CL_, gates=dict(a=Sa, b=Sb, c_cond=Sc1, c_coll=Sc2, Sig_cb=Sig_cb, NH_mean=NH_mean))
surv = [c["cls"] for c in CL_ if c["survives"]]; say("\nclasses that survive all five:", surv or "none")
json.dump(res, open("db1_phys.json", "w"), indent=1, default=float)
