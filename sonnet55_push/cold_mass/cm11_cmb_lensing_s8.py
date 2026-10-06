"""cm11: CMB-lensing and S8 shift from the two-level retention (cm08-cm10), halo model, matter only (MOND phantom lensing NOT included -> the shift is an
UPPER BOUND on the suppression; the phantom adds lensing mass inside galaxy halos).
Model (declared before the run): halos (colossus planck18; Tinker08 mass function, Tinker10 bias, NFW with Diemer19 concentration, M200m) carry
M_eff = M [f_b + (1 - f_b) r(M, z)], r = 1 (LCDM) for z >= 2.5, two-level r = 0.13 (M < M_step) / 0.60 (M >= M_step) for z <= 1.5, linear in z between;
M_step = 1e12.5 Msun (cm10 bracket midpoint; 1e12 and 1e13 reported). The removed cold mass is DIFFUSE: it traces the linear field above R_s and is smooth below,
W(k) = exp(-(k R_s)^2/2), R_s = 1 Mpc/h (0.3 and 3 reported). Mass not in halos > 1e6 Msun/h is diffuse with W = 1 (standard consistency term).
P = P_1h + P_lin (I_h + D W)^2, I_h = int dn b (M_eff/rho) u, D = diffuse fraction. Limber: CMB lensing kernel (chi* at z = 1090); cosmic shear with a KiDS-like
n(z) ~ z^2 exp(-(z/0.45)^1.5) (median ~0.7; stated). S8 shift: S8_eff/S8 = <C_ratio>^(1/2.5) over ell 100-1500 (cosmic-shear amplitude ~ S8^2.5, approximate).
Context: KiDS/DES S8 ~ 0.76-0.78 vs Planck 0.83 (about -8%); CMB lensing (ACT DR6/Planck) is consistent with Planck LCDM to ~2-3%.
Run: python3 cm11_cmb_lensing_s8.py | MUTATE=1 sets r = 1 everywhere (shifts must vanish, check L fails)
"""
import os, sys, math, numpy as np
from colossus.cosmology import cosmology
from colossus.lss import mass_function, bias
from colossus.halo import concentration, mass_so
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
cosmo = cosmology.setCosmology("planck18"); h = cosmo.H0 / 100
fb = cosmo.Ob0 / cosmo.Om0
lM = np.linspace(6, 15.8, 120); M = 10**lM; dlnM = np.log(10) * (lM[1] - lM[0])
ks = np.logspace(-3, 1.5, 80)
zs = np.linspace(0.0, 4.0, 33)
def u_nfw(k, Mv, z):
    c = concentration.concentration(Mv, "200m", z, model="diemer19")
    R = mass_so.M_to_R(Mv, z, "200m") / 1000.0 * (1 + z)   # comoving Mpc/h
    rs = R / c; x = np.outer(k, rs)
    from scipy.special import sici
    si1, ci1 = sici((1 + c) * x); si0, ci0 = sici(x)
    m = np.log(1 + c) - c / (1 + c)
    return (np.sin(x) * (si1 - si0) - np.sin(c * x) / ((1 + c) * x) + np.cos(x) * (ci1 - ci0)) / m
def rfun(Mv, z, Mstep):
    if MUTATE: return np.ones_like(Mv)
    w = np.clip((2.5 - z) / 1.0, 0, 1)
    two = np.where(Mv / h >= Mstep, 0.60, 0.13)
    return (1 - w) * 1.0 + w * two
pk_cache = {}
def Pk(z, Mstep, Rs):
    key = (round(z, 4), Mstep, Rs)
    if key in pk_cache: return pk_cache[key]
    rho = cosmo.rho_m(z) * 1e9 / (1 + z)**3   # comoving Msun h^2/Mpc^3
    dn = mass_function.massFunction(M, z, mdef="200m", model="tinker08", q_out="dndlnM")
    b = bias.haloBias(M, model="tinker10", z=z, mdef="200m")
    Meff = M * (fb + (1 - fb) * rfun(M, z, Mstep))
    u = u_nfw(ks, M, z)
    I1 = (u * (dn * b * Meff / rho)).sum(1) * dlnM
    P1 = (u**2 * (dn * Meff**2 / rho**2)).sum(1) * dlnM
    Dh = 1.0 - (dn * M / rho).sum() * dlnM               # matter outside halos > 1e6 (smooth, W = 1)
    Dr = ((dn * (M - Meff) / rho).sum() * dlnM)          # removed cold mass (smooth below R_s)
    I_low = 1.0 - (dn * b * M / rho).sum() * dlnM - Dh    # bias consistency remainder (assigned to unresolved low-mass halos, W = 1)
    W = np.exp(-(ks * Rs)**2 / 2)
    Pl = cosmo.matterPowerSpectrum(ks, z)
    P = P1 + Pl * (I1 + Dh + I_low + Dr * W)**2
    pk_cache[key] = P; return P
def Cl(ells, kernel, Mstep, Rs):
    chis = np.array([cosmo.comovingDistance(0.0, z) for z in zs])   # Mpc/h
    out = np.zeros(len(ells))
    for i in range(1, len(zs)):
        z, chi = zs[i], chis[i]; dchi = chis[i] - chis[i - 1]
        P = Pk(z, Mstep, Rs); k = (ells + 0.5) / chi
        out += dchi * kernel(z, chi)**2 / chi**2 * np.interp(np.log(k), np.log(ks), P)
    return out
c_km = 299792.458; H0h = 100.0
chistar = cosmo.comovingDistance(0.0, 1090.0)
def k_cmb(z, chi): return 1.5 * cosmo.Om0 * (H0h / c_km)**2 * (1 + z) * chi * (chistar - chi) / chistar
zn = np.linspace(0.01, 3, 300); nz = zn**2 * np.exp(-(zn / 0.45)**1.5); nz /= np.trapz(nz, zn)
chin = np.array([cosmo.comovingDistance(0.0, z) for z in zn])
def k_shear(z, chi):
    m = chin > chi
    if m.sum() < 2: return 0.0
    g = np.trapz(nz[m] * (chin[m] - chi) / chin[m], zn[m])
    return 1.5 * cosmo.Om0 * (H0h / c_km)**2 * (1 + z) * chi * g
ells = np.logspace(2, np.log10(1500), 12)
ref = {}
saveM = MUTATE
for lab, Mstep, Rs in (("main 1e12.5, Rs 1", 10**12.5, 1.0), ("step 1e12", 1e12, 1.0), ("step 1e13", 1e13, 1.0), ("Rs 0.3", 10**12.5, 0.3), ("Rs 3", 10**12.5, 3.0)):
    MUTATE = True; ck0 = Cl(ells, k_cmb, Mstep, Rs); cs0 = Cl(ells, k_shear, Mstep, Rs); pk_cache.clear()
    MUTATE = saveM; ck = Cl(ells, k_cmb, Mstep, Rs); cs = Cl(ells, k_shear, Mstep, Rs); pk_cache.clear()
    rk, rs_ = ck / ck0, cs / cs0
    s8 = float(np.mean(rs_))**(1 / 2.5)
    ref[lab] = (rk, rs_, s8)
    print(f"   {lab:18s}: CMB-lensing C_L ratio at L = 100/400/1500: {rk[0]:.3f}/{np.interp(400, ells, rk):.3f}/{rk[-1]:.3f};"
          f" shear C_l ratio 100/400/1500: {rs_[0]:.3f}/{np.interp(400, ells, rs_):.3f}/{rs_[-1]:.3f};  S8_eff/S8 = {s8:.3f} ({(s8-1)*100:+.1f}%)")
rk, rs_, s8 = ref["main 1e12.5, Rs 1"]
check("L the two-level rule shifts the lensing spectra (MUTATE r = 1 must give ratios = 1 and fail)", abs(s8 - 1) > 0.005)
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
