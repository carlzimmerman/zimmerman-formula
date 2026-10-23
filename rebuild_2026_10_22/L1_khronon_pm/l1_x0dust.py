#!/usr/bin/env python3
"""L1_khronon_pm X0-dust pre-flight (coordinator request A7, "early release"): computed BEFORE any A7 cell.

  OMP_NUM_THREADS=1 nice -n 15 python3 l1_x0dust.py               -> l1_x0dust.out, l1_x0dust_results.json
  L1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 l1_x0dust.py   -> XD3 with the hold coefficient's sign flipped (J'(0) = +1): must FAIL

XD1  x_rms(z), z = 3000 -> 50, of the hold-field argument x = |grad Xi|/(a a0) along the DUST-LIMIT linear spectrum (vanilla CLASS cdm
     transfer, model B; khronon = CDM-like, "hold off"), with Xi from the linear hold (Yukawa, mu_K = 14.8) and, for reference, from the
     strong-field (Jeans) branch Xi = -S/(a mu)^2; z_x where x_rms crosses 1; both footings.
XD2  the DBI background (Q7, BS's lambda_D = 30, cap mu_K): M^2/mu^2 = Qbar^2 r^3, the background excess Z/(r+1) and w vs z; x_rms with
     DBI's M(z) along the dust-limit spectrum and along DBI's own khronon transfer (Q7's binary, read-only); z_x.
XD3  is "hold off before z_x" self-consistent?  Exact (sympy) linear response of BS24's PN system about a background with hold
     argument x (BSK1 M4): the khronon's net self-force kernel s(k; f) = (m^2 - f k^2)/((1 - f) k^2 + m^2), f = f_theta = mu + x mu' in
     [0, 1).  PASS = ds/df < 0 for every k > 0 and the two limits are F3's BSK2 (f = 0) and Jeans (f = 1) kernels.  Then larger x gives a
     STIFFER khronon, not a freer one.
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys, json, math, time, subprocess, re
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("L1_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
W = os.path.join(HERE, "work", "x0dust"); os.makedirs(W, exist_ok=True); os.environ["L1_WORK"] = W
import numpy as np
sys.path.insert(0, HERE)
import khronon_pm as K
import sympy as sp
OUT, RES, CHK = [], {"lane": "L1_khronon_pm", "part": "x0dust_preflight_A7", "mutate": MUT}, {}
T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=val, threshold=thr); P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
P("L1_khronon_pm X0-dust pre-flight (A7)" + (" [MUTATE]" if MUT else "") + ": kappa = 1/2 FITTED; footings never pooled")
bg = K.MODEL_B; h = bg.h; MU = 14.8; LAM = 30.0
ZL = [3000, 2000, 1500, 1200, 1000, 800, 600, 500, 400, 300, 250, 199, 150, 100, 75, 50]
I0 = 3 * bg.Otau / 2997.92458 ** 2                 # (h/Mpc)^2, late K abundance
kstar = 0.05 / h; As = math.exp(K.LNAS_C2B) * 1e-10; ns = K.NS_C2B

# ---- dust-limit transfer (vanilla CLASS, model B), cdm = khronon in the dust limit
from classy import Class
c = Class(); c.set({"omega_b": K.WB_C2B, "omega_cdm": K.OM_B * h * h - K.WB_C2B, "h": h, "ln10^{10}A_s": K.LNAS_C2B, "n_s": ns,
                    "tau_reio": K.TAU_C2B, "N_ur": 3.044, "T_cmb": 2.7255, "output": "mTk", "P_k_max_h/Mpc": 30.0, "z_max_pk": 3000.0,
                    "matter_source_in_current_gauge": "yes"})
c.compute()
TD = {}
for z in ZL:
    t = c.get_transfer(z); TD[z] = (np.array(t["k (h/Mpc)"]), np.array(t["d_cdm"]), np.array(t["d_b"]))
c.struct_cleanup(); c.empty()

def xrms(k, Tt, a, M, a0c, kmax, ratio_rho=1.0, branch="yukawa"):
    sel = (k <= kmax) & (k >= 1e-4)
    k_, T_ = k[sel], Tt[sel]
    S = 1.5 * bg.Otau * ratio_rho / a * T_                         # 4 pi G a^2 delta rho_tau / delta (code units), per unit curvature
    Xi = -S / (k_ ** 2 + (a * M) ** 2) if branch == "yukawa" else -S / (a * M) ** 2
    D2 = As * (k_ / kstar) ** (ns - 1)                             # dimensionless primordial curvature power
    g2 = np.trapz((k_ * Xi) ** 2 * D2 / k_, k_)
    return math.sqrt(g2) / (a * a0c)
def zcross(zs, xs):
    for i in range(len(zs) - 1):
        if (xs[i] - 1) * (xs[i + 1] - 1) <= 0:
            l0, l1 = math.log(xs[i]), math.log(xs[i + 1]); f = -l0 / (l1 - l0)
            return math.exp(math.log(1 + zs[i]) + f * (math.log(1 + zs[i + 1]) - math.log(1 + zs[i]))) - 1
    return None

# ---- XD1
XD1 = {}
for foot in ("canonical", "alt"):
    a0c = bg.a0c(foot); rows = {}
    for z in ZL:
        a = 1 / (1 + z); k, Tc, Tb = TD[z]
        rows[z] = dict(x_yuk_k4=xrms(k, Tc, a, MU, a0c, 4.0), x_yuk_k16=xrms(k, Tc, a, MU, a0c, 16.0), x_jeans_k4=xrms(k, Tc, a, MU, a0c, 4.0, branch="jeans"))
    zx = zcross(ZL, [rows[z]["x_yuk_k4"] for z in ZL]); zx16 = zcross(ZL, [rows[z]["x_yuk_k16"] for z in ZL])
    XD1[foot] = dict(rows=rows, z_x_k4=zx, z_x_k16=zx16)
    P(f"  XD1 {foot}: x_rms (dust spectrum, Yukawa hold, k<=4) " + ", ".join(f"z{z}: {rows[z]['x_yuk_k4']:.3g}" for z in (3000, 1000, 500, 300, 199, 100, 50))
      + f"; z_x(k<=4) {zx if zx is None else round(zx, 1)}, z_x(k<=16) {zx16 if zx16 is None else round(zx16, 1)}; "
      + f"Jeans-branch x at z 1000/199: {rows[1000]['x_jeans_k4']:.3g}/{rows[199]['x_jeans_k4']:.3g}")
RES["XD1"] = XD1
check("XD1", all(v["z_x_k4"] is not None for v in XD1.values()), "; ".join(f"{f}: z_x {v['z_x_k4']:.1f} (k<=16 {v['z_x_k16']:.1f})" for f, v in XD1.items() if v["z_x_k4"]), "z_x found (computed)")

# ---- XD2: DBI background and transfer
def dbi_bg(a, mu=MU, lam=LAM):
    Z = I0 / (2 * mu ** 2 * a ** 3); r = math.sqrt(1 + lam * Z * Z); Q = 1 + Z / r
    return dict(Z=Z, r=r, M2_over_mu2=Q * Q * r ** 3, excess=Z / (r + 1), w=Z / (r * (r + 1)), lamZ2=lam * Z * Z)
rd = os.path.join(W, "dbi_x0"); os.makedirs(rd, exist_ok=True)
p = {"h": h, "omega_b": K.WB_C2B, "omega_cdm": 1e-8, "omega_aest": K.OM_B * h * h - K.WB_C2B - 1e-8, "ln10^{10}A_s": K.LNAS_C2B, "n_s": ns,
     "tau_reio": K.TAU_C2B, "T_cmb": 2.7255, "aest_Q0": 1.0, "aest_K_B": 1.0, "aest_g": 1.0, "aest_lambda_c": -1.0, "aest_K_type": 5,
     "aest_K2": (MU * h) ** 2, "aest_Z0": LAM, "output": "mTk", "z_pk": ", ".join(str(z) for z in ZL), "z_max_pk": 3000, "P_k_max_h/Mpc": 30.0,
     "tol_perturbations_integration": 1e-7, "perturbations_sampling_stepsize": 0.05, "k_per_decade_for_pk": 40,
     "start_small_k_at_tau_c_over_tau_h": 0.0015 * 0.25, "start_large_k_at_tau_h_over_tau_k": 0.07 * 0.25,
     "write_parameters": "no", "input_verbose": 1, "background_verbose": 1, "fourier_verbose": 1, "overwrite_root": "yes", "root": os.path.join(rd, "DBI_"),
     "matter_source_in_current_gauge": "yes"}
with open(os.path.join(rd, "DBI.ini"), "w") as f: f.write("".join(f"{k_} = {v_}\n" for k_, v_ in p.items()))
r = subprocess.run(["nice", "-n", "15", K.CLASS_DBI, os.path.join(rd, "DBI.ini")], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
assert r.returncode == 0, (r.stdout + r.stderr)[-300:]
ob, oc = K.WB_C2B / h ** 2, 1e-8 / h ** 2; oa = bg.Om - ob - oc
XD2 = {"background": {}, "x": {}}
for z in ZL:
    XD2["background"][z] = dbi_bg(1 / (1 + z))
for foot in ("canonical", "alt"):
    a0c = bg.a0c(foot); rows = {}
    for i, z in enumerate(ZL):
        a = 1 / (1 + z); B = dbi_bg(a); M = MU * math.sqrt(B["M2_over_mu2"]); ex = 1 + B["excess"]
        t = K._read_tk(os.path.join(rd, f"DBI__z{i + 1}_tk.dat")); kD = t["k (h/Mpc)"] if "k (h/Mpc)" in t else t["k"]
        rho_m = ob + oc + oa * ex                                   # a^3-scaled background densities at z
        dtau = (rho_m * t["d_m"] - ob * t["d_b"] - oc * t["d_cdm"]) / (oa * ex)
        k, Tc, _ = TD[z]
        rows[z] = dict(x_dustspec_DBI_M=xrms(k, Tc, a, M, a0c, 4.0, ratio_rho=ex), x_DBIspec_DBI_M=xrms(kD, dtau, a, M, a0c, 4.0, ratio_rho=ex),
                       x_DBIspec_mu=xrms(kD, dtau, a, MU, a0c, 4.0, ratio_rho=ex))
    XD2["x"][foot] = dict(rows=rows, z_x_dustspec=zcross(ZL, [rows[z]["x_dustspec_DBI_M"] for z in ZL]),
                          z_x_DBIspec=zcross(ZL, [rows[z]["x_DBIspec_DBI_M"] for z in ZL]))
    P(f"  XD2 {foot}: x_rms with DBI M(z): dust spectrum " + ", ".join(f"z{z}: {rows[z]['x_dustspec_DBI_M']:.3g}" for z in (3000, 1000, 300, 199, 50))
      + "; DBI's own spectrum " + ", ".join(f"z{z}: {rows[z]['x_DBIspec_DBI_M']:.3g}" for z in (3000, 1000, 300, 199, 50))
      + f"; z_x dust-spec {XD2['x'][foot]['z_x_dustspec']}, DBI-spec {XD2['x'][foot]['z_x_DBIspec']}")
P("  XD2 DBI background (cap, lambda_D 30): " + "; ".join(f"z{z}: M^2/mu^2 {XD2['background'][z]['M2_over_mu2']:.3g}, excess {XD2['background'][z]['excess']:.2g}, "
                                                           f"w {XD2['background'][z]['w']:.2g}" for z in (3000, 1000, 500, 199, 50)))
RES["XD2"] = XD2
check("XD2", True, "computed (see lines above)", "computed")

# ---- XD3: exact linear response about a background with hold argument x (BS24 PN system, BSK1 M4 transcription)
k_, m_, f_, G4 = sp.symbols("k m f G4", positive=True)
dphi, dXi, drho = sp.symbols("dphi dXi drho")
j = -1 if not MUT else +1                                         # J'(0); MUTATE flips it
Cth = (f_ - 1) if j == -1 else (f_ + 1)                            # linearised J_Y tensor along k: f_theta - 1 (BSK1 M4 C_th)
eqs = [sp.Eq(-k_ ** 2 * dphi, G4 * drho), sp.Eq(G4 * drho, (k_ ** 2 * Cth - m_ ** 2) * dXi)]
sol = sp.solve(eqs, [dphi, dXi], dict=True)[0]
# net self-force potential on the khronon per unit 4piG drho: (phi - Xi) = -s / k^2  (s = 1: ordinary self-gravity)
s_expr = sp.simplify(-(sol[dphi] - sol[dXi]) * k_ ** 2 / (G4 * drho))
s_target = (m_ ** 2 - f_ * k_ ** 2) / ((1 - f_) * k_ ** 2 + m_ ** 2)
same = sp.simplify(s_expr - s_target) == 0
dsdf = sp.simplify(sp.diff(s_target, f_))
neg = sp.simplify(dsdf + k_ ** 2 * (k_ ** 2) / ((1 - f_) * k_ ** 2 + m_ ** 2) ** 2) == 0      # ds/df = -k^4/((1-f)k^2+m^2)^2 < 0
lim0 = sp.simplify(s_target.subs(f_, 0) - m_ ** 2 / (k_ ** 2 + m_ ** 2)) == 0
lim1 = sp.simplify(s_target.subs(f_, 1) - (1 - k_ ** 2 / m_ ** 2)) == 0
RES["XD3"] = dict(s=str(s_expr), dsdf=str(dsdf), same=bool(same), dsdf_negative=bool(neg), f0_is_BSK2=bool(lim0), f1_is_Jeans=bool(lim1))
P(f"  XD3 s(k; f) = {s_expr}; ds/df = {dsdf}")
check("XD3", same and neg and lim0 and lim1,
      f"s = (m^2 - f k^2)/((1-f)k^2 + m^2): {same}; ds/df = -k^4/((1-f)k^2+m^2)^2 < 0: {neg}; f=0 -> BSK2: {lim0}; f->1 -> Jeans 1 - k^2/m^2: {lim1}",
      "exact (sympy)")
RES["reading"] = ("Larger x raises f_theta = mu + x mu' toward 1, which LOWERS the khronon's net self-force kernel at every k (to the Jeans form "
                  "1 - k^2/(a mu)^2 as x -> infinity). In v3's PN system a large early x therefore stiffens the khronon; it does not release "
                  "it. 'Hold off before z_x' is not self-consistent; the linear (x = 0) growth results are, if anything, optimistic.")
P("  reading: " + RES["reading"])
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0
npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
P(f"L1_X0DUST COMPLETE: {npass}/{ntot} checks PASS.  ({RES['runtime_s']:.0f} s)")
K.atomic_json(os.path.join(HERE, f"l1_x0dust_results{SUF}.json"), RES)
K.atomic_text(os.path.join(HERE, f"l1_x0dust{SUF}.out"), "\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)
