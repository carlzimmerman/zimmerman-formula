"""CFG363: lensing kill test of the two-level retention picture. Criteria: FROZEN_CRITERIA.md (35b3aa30d).

Builds on cold_mass cm11 (9f0c92398; matter only). Adds the framework's baryon-sourced nu_mono phantom and places the moved
cold mass in a mass-conserving Gaussian envelope (width R_s) around its host.
Scaffold: colossus planck18 (Tinker08 / Tinker10 / diemer19 / NFW, M200m). Units: Msun/h, comoving Mpc/h, k in h/Mpc.
Run: python3 cfg363_lensing_kill.py ; MUTATE=1 drops the moved cold mass (T0c must fail, rc 1).
"""
import json, math, os, sys, itertools
import numpy as np
trapz = getattr(np, 'trapezoid', None) or np.trapz
from scipy.special import sici
from colossus.cosmology import cosmology
from colossus.lss import mass_function, bias
from colossus.halo import concentration, mass_so

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import CFG4_common as C4  # noqa: E402  (the record's nu_mono)

MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []


def say(s=""):
    print(s)
    lines.append(s)


def check(name, ok, val):
    checks.append({"name": name, "pass": bool(ok), "value": val})
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


cosmo = cosmology.setCosmology("planck18")
h = cosmo.H0 / 100.0
Om = cosmo.Om0
fb = cosmo.Ob0 / cosmo.Om0
fc = 1.0 - fb
S8_ref = cosmo.sigma8 * math.sqrt(Om / 0.3)
rho_m = cosmo.rho_m(0.0) * 1e9                      # Msun/h per (Mpc/h)^3, comoving
G_kpc = 4.30091e-6                                  # kpc (km/s)^2 / Msun
a0_k = 9.3603e-11 * 3.0857e13                       # (km/s)^2 / kpc, canonical, flat in z
c_over_H0 = 2997.92458                              # Mpc/h

lM = np.linspace(8.0, 16.0, 97)
M = 10**lM
dlnM = np.log(10) * (lM[1] - lM[0])
ks = np.logspace(-3, 1.6, 70)
zs = np.concatenate([np.linspace(0.0, 2.0, 11)[:-1], np.linspace(2.0, 6.0, 9)])


def u_nfw(Mv, z):
    c = concentration.concentration(Mv, "200m", z, model="diemer19")
    R = mass_so.M_to_R(Mv, z, "200m") / 1000.0 * (1 + z)          # comoving Mpc/h
    rs = R / c
    x = np.outer(ks, rs)
    si1, ci1 = sici((1 + c) * x)
    si0, ci0 = sici(x)
    m = np.log(1 + c) - c / (1 + c)
    return (np.sin(x) * (si1 - si0) - np.sin(c * x) / ((1 + c) * x) + np.cos(x) * (ci1 - ci0)) / m, R


def phantom(Mv, z, R200, csw, ge=0.0):
    """M_ph total (Msun/h) and normalised Fourier profile u_ph(k, M), from M_ph(<r) = (nu_mono(y) - 1) M_b, truncated at csw R200."""
    Mb_sun = fb * Mv / h                                            # Msun
    Mtot = np.zeros_like(Mv)
    U = np.zeros((len(ks), len(Mv)))
    for j in range(len(Mv)):
        r_c = np.logspace(np.log10(1e-3 * R200[j]), np.log10(csw * R200[j]), 300)   # comoving Mpc/h
        r_phys_kpc = r_c / (1 + z) / h * 1000.0
        y = G_kpc * Mb_sun[j] / (r_phys_kpc**2 * a0_k)
        if ge > 0:                                                  # POST-FREEZE: EFE cap, enclosed phantom frozen once y < g_e/a0
            y = np.maximum(y, ge)
        Mph = (C4.nu_mono(y) - 1.0) * Mb_sun[j] * h                 # Msun/h, enclosed
        dM = np.diff(Mph)
        rm = 0.5 * (r_c[1:] + r_c[:-1])
        Mtot[j] = Mph[-1]
        kr = np.outer(ks, rm)
        U[:, j] = (np.sinc(kr / np.pi) @ dM + np.sinc(np.outer(ks, r_c[:1]) / np.pi)[:, 0] * Mph[0]) / max(Mph[-1], 1e-30)
    return Mtot, U


say("CFG363 lensing kill test" + ("  (MUTATE: moved cold mass dropped)" if MUTATE else ""))
say("=" * 78)
say(f"scaffold planck18: Om {Om:.4f}, f_b {fb:.4f}, sigma8 {cosmo.sigma8:.4f}, S8_ref {S8_ref:.4f}")

# ---------------------------------------------------------------- per-z ingredients (bracket-independent)
ING = {}
for z in zs:
    dn = mass_function.massFunction(M, z, mdef="200m", model="tinker08", q_out="dndlnM")
    b = bias.haloBias(M, z, "200m", model="tinker10")
    uN, R200 = u_nfw(M, z)
    ph = {csw: phantom(M, z, R200, csw) for csw in (1, 3)}
    for ge in (0.01, 0.03):                                         # POST-FREEZE variants (labelled)
        ph[("efe", ge)] = phantom(M, z, R200, 3, ge)
    Plin = cosmo.matterPowerSpectrum(ks, z)
    rem = 1.0 - np.sum(dn * b * M / rho_m) * dlnM
    ING[z] = dict(dn=dn, b=b, uN=uN, R200=R200, ph=ph, Plin=Plin, rem=rem)
    say(f"  z = {z:.2f}: bias remainder {rem:+.3f}; phantom/halo mass (dn-weighted) r_sw=1: "
        f"{np.sum(dn*ph[1][0])/np.sum(dn*M):.3f}, r_sw=3: {np.sum(dn*ph[3][0])/np.sum(dn*M):.3f}")


def Pk(z, model):
    """model: None (LCDM) or dict(Mstep, Rs, zsort, csw, phantom, force_r1)"""
    I = ING[z]
    dn, b, uN = I["dn"], I["b"], I["uN"]
    if model is None:
        comps = M[None, :] * uN
    elif model.get("anchored"):                                     # POST-FREEZE: halos match observed lensing (LCDM M u_NFW) by
        r = np.where(M / h >= model["Mstep"], 0.60, 0.13) if z < model["zsort"] else np.ones_like(M)   # construction; moved cold is EXTRA real mass
        uG = np.exp(-0.5 * (ks * model["Rs"] * h) ** 2)[:, None]
        comps = M * uN + (1 - r) * fc * M * uG
    else:
        if model.get("force_r1") or z >= model["zsort"]:
            r = np.ones_like(M)
        else:
            r = np.where(M / h >= model["Mstep"], 0.60, 0.13)
        uG = np.exp(-0.5 * (ks * model["Rs"] * h) ** 2)[:, None]
        moved = 0.0 if MUTATE else (1 - r) * fc * M
        comps = (fb + r * fc) * M * uN + moved * uG
        if model["phantom"]:
            Mph, Uph = I["ph"][model["csw"]]
            comps = comps + Mph * Uph
    P1 = np.sum(dn * comps**2, axis=1) * dlnM / rho_m**2
    Ib = np.sum(dn * b * comps, axis=1) * dlnM / rho_m + I["rem"]
    return P1 + Ib**2 * I["Plin"], Ib, comps


# ---------------------------------------------------------------- T0 controls
say("\nT0 controls")
z0 = zs[0]
P_l, Ib_l, comps_l = Pk(z0, None)
i01 = np.argmin(abs(ks - 0.01))
r2h = Ib_l[i01] ** 2
check("T0a LCDM 2-halo reproduces P_lin at k = 0.01 h/Mpc to 3%", abs(r2h - 1) < 0.03, f"[I_b]^2 = {r2h:.4f}")
base = dict(Mstep=1e12, Rs=1.0, zsort=2.0, csw=1, phantom=False, force_r1=True)
P_b, _, _ = Pk(z0, base)
check("T0b r = 1, phantom OFF equals LCDM to 1e-6", np.max(abs(P_b / P_l - 1)) < 1e-6, f"max |ratio-1| = {np.max(abs(P_b/P_l-1)):.1e}")
r_t = np.where(M / h >= 1e12, 0.60, 0.13)
moved_t = 0.0 if MUTATE else (1 - r_t) * fc * M
mass_err = np.max(abs(((fb + r_t * fc) * M + moved_t) / M - 1))  # profile weights at k -> 0 (u -> 1), phantom excluded
check("T0c per-halo real mass conserved (k -> 0 profile sum / M = 1) to 1e-6", mass_err < 1e-6, f"max |sum/M - 1| = {mass_err:.1e}")

# ---------------------------------------------------------------- Limber
chi_of = lambda z: cosmo.comovingDistance(0.0, z)                 # Mpc/h
chis = np.array([chi_of(z) for z in zs])
chi_star = chi_of(1100.0)


def interp_P(Ptab, chi, ell):
    """P at k = (ell+0.5)/chi for each z row, log-interpolated in k."""
    out = np.zeros(len(zs))
    for i in range(len(zs)):
        if chis[i] <= 0:
            continue
        k = (ell + 0.5) / chis[i]
        out[i] = np.exp(np.interp(np.log(k), np.log(ks), np.log(Ptab[i]))) if k <= ks[-1] else 0.0
    return out


W_cmb = 1.5 * Om / c_over_H0**2 * chis * (chi_star - chis) / chi_star * (1 + zs)
zg = np.linspace(0.001, 4.0, 400)
nz = zg**2 * np.exp(-(zg / 0.5) ** 1.5)
nz /= trapz(nz, zg)
chig = np.array([chi_of(z) for z in zg])
q_sh = np.array([1.5 * Om / c_over_H0**2 * chis[i] * (1 + zs[i]) *
                 trapz(np.where(chig > chis[i], nz * (chig - chis[i]) / np.maximum(chig, 1e-9), 0.0), zg) for i in range(len(zs))])


def Cl(Ptab, W, ells):
    out = []
    for ell in ells:
        Pv = interp_P(Ptab, None, ell) if False else interp_P(Ptab, chis, ell)
        integ = np.where(chis > 0, W**2 / np.maximum(chis, 1e-9) ** 2 * Pv, 0.0)
        out.append(trapz(integ, chis))
    return np.array(out)


L_cmb = np.unique(np.round(np.logspace(np.log10(40), np.log10(763), 24)))
L_sh = np.unique(np.round(np.logspace(np.log10(150), np.log10(1500), 24)))
P_lcdm = np.array([Pk(z, None)[0] for z in zs])
C_cmb_ref, C_sh_ref = Cl(P_lcdm, W_cmb, L_cmb), Cl(P_lcdm, q_sh, L_sh)
C100 = Cl(P_lcdm, W_cmb, [100])[0]
check("T0d LCDM C_L^kk(L=100) within 1e-7 .. 3e-7 (order-of-magnitude sanity)", 1e-7 < C100 < 3e-7, f"{C100:.2e}")

# ---------------------------------------------------------------- brackets
say("\nBrackets (CMB ratio = mean over L 40-763; S8_eff from shear mean ratio over l 150-1500, exponent 2.5 [2.0, 3.0])")
rows = []
for ph_on in (True, False):
    for Mstep, Rs, zsort in itertools.product((1e12, 1e13), (1.0, 3.0, 10.0), (1.0, 2.0)):
        for csw in ((1, 3) if ph_on else (1,)):
            mod = dict(Mstep=Mstep, Rs=Rs, zsort=zsort, csw=csw, phantom=ph_on)
            Pm = np.array([Pk(z, mod)[0] for z in zs])
            rc = float(np.mean(Cl(Pm, W_cmb, L_cmb) / C_cmb_ref))
            rs_ = float(np.mean(Cl(Pm, q_sh, L_sh) / C_sh_ref))
            S8s = {e: S8_ref * rs_ ** (1 / e) for e in (2.0, 2.5, 3.0)}
            t1 = "PASS" if abs(rc - 1) <= 0.05 else ("KILL" if abs(rc - 1) > 0.10 else "tension")
            t2 = "PASS" if 0.74 <= S8s[2.5] <= 0.85 else ("KILL" if not (0.70 <= S8s[2.5] <= 0.89) else "tension")
            rows.append(dict(phantom=ph_on, Mstep=Mstep, Rs=Rs, zsort=zsort, csw=csw if ph_on else None, cmb_ratio=rc,
                             shear_ratio=rs_, S8=S8s, T1=t1, T2=t2))
            say(f"  phantom {'ON ' if ph_on else 'OFF'} Mstep {Mstep:.0e} Rs {Rs:>4} Mpc zsort {zsort} "
                f"{('r_sw ' + str(csw) + 'R200') if ph_on else '          '}: CMB {rc:.3f} [{t1}]  shear {rs_:.3f} "
                f"S8 {S8s[2.5]:.3f} [{S8s[2.0]:.3f}, {S8s[3.0]:.3f}] [{t2}]")

say("\nPOST-FREEZE robustness (labelled; NOT part of the frozen verdict)")
post = []
def run(mod, label):
    Pm = np.array([Pk(z, mod)[0] for z in zs])
    rc = float(np.mean(Cl(Pm, W_cmb, L_cmb) / C_cmb_ref)); rs_ = float(np.mean(Cl(Pm, q_sh, L_sh) / C_sh_ref))
    S8e = S8_ref * rs_ ** (1 / 2.5)
    post.append(dict(label=label, cmb_ratio=rc, shear_ratio=rs_, S8=S8e))
    say(f"  {label}: CMB {rc:.3f}  shear {rs_:.3f}  S8 {S8e:.3f}")
for ge in (0.01, 0.03):
    for Rs in (1.0, 10.0):
        run(dict(Mstep=1e12, Rs=Rs, zsort=2.0, csw=("efe", ge), phantom=True), f"EFE-capped phantom g_e={ge}a0, two-level, Mstep 1e12, Rs {Rs}")
    run(dict(Mstep=1e12, Rs=1.0, zsort=2.0, csw=("efe", ge), phantom=True, force_r1=True), f"EFE-capped phantom g_e={ge}a0, NO sorting (r=1)")
for Rs in (1.0, 3.0, 10.0):
    run(dict(Mstep=1e12, Rs=Rs, zsort=2.0, anchored=True), f"anchored halos (= observed lensing) + moved cold extra, Rs {Rs}")

on = [r for r in rows if r["phantom"]]
killed = all(r["T1"] == "KILL" or r["T2"] == "KILL" for r in on)
surv = [r for r in on if r["T1"] == "PASS" and r["T2"] == "PASS"]
verdict = "KILLED" if killed else ("SURVIVES (scaffold)" if surv else "TENSION")
off = [r for r in rows if not r["phantom"]]
say(f"\nPOST-FREEZE cross-check (labelled): phantom-OFF S8 shift range {min(r['S8'][2.5] for r in off)/S8_ref-1:+.1%} .. "
    f"{max(r['S8'][2.5] for r in off)/S8_ref-1:+.1%} vs cm11 (matter only) -12% .. -19%")
say(f"\nVERDICT: {verdict}" + (f" -- passing brackets: " + "; ".join(
    f"Mstep {r['Mstep']:.0e}, Rs {r['Rs']}, zsort {r['zsort']}, r_sw {r['csw']}R200" for r in surv) if surv else ""))
say("Scaffold result on a LCDM halo population; the framework-native test is CFG359/CFG361's PM machinery.")
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} controls pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG363", "mutate": MUTATE, "S8_ref": S8_ref, "verdict": verdict, "rows": rows, "checks": checks,
           "C100_lcdm": C100, "postfreeze": post}, open(os.path.join(HERE, f"cfg363_lensing_kill_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg363_lensing_kill{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
