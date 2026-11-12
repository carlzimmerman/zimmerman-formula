#!/usr/bin/env python3
"""SS1 variants B-G (AMENDMENT_A2 2b866ef57a; criteria b5adc7a90b, A1 9aeeb48503). Variant engine:
    python3 ss1v.py ka                    -> parts/v_ka.json            K0, K-B, K-C, K-D, K-F, K-G (+ footing constants)
    python3 ss1v.py local <V> [opt]       -> parts/local_V<V>[opt].json  gates 1, 2, 3, 4 (reported), 5, 10 through ss1.py's
                                             run_local with the variant's component (A's battery, read-only reuse), + gate 5b UMa
    SS1_FOOT=<f> python3 ss1v.py cosmo <V> -> parts/vcosmo_<V>_<f>.json  gates 6, 7 (reading), 8 (growth with streaming daughters)
    python3 ss1v.py bullet <V>            -> parts/vbullet_<V>.json      gate 9 (DB1 child via ss1_bullet.py)
V in B C D E F G and the G MUTATE ids MG1-MG4; opt in obs (bracket B3, G only) and local (G-local bracket).
Retention: root of -ln f + x0^4/4 (1 - f^4) = alpha, uniform over the pre-conversion component (B: radial factor; G-local: per
shell). TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, time, io, contextlib, subprocess
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from scipy.special import erfc
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); sys.path.insert(0, HERE)
import ss1_core as C
AMEND2 = "2b866ef57a"; AMEND3 = "694668618a"
PARTS = os.path.join(HERE, "parts")
G_KPC = 4.3009172706e-6; C_KMS = 299792.458; KMS_GYR_MPC = 1.0227121650537077e-3          # 1 km/s x 1 Gyr = 1.0227 kpc = 1.0227e-3 Mpc
A0H = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; LSTAR_PC = {"canonical": 21.68, "alt": 22.85}
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
F1A = json.load(open(os.path.join(REPO, "closure_2026_11_07", "F1A_primary_cmb_audit", "f1a.json")))
FOOTS = ("canonical", "alt")
def P(s=""): print(s, flush=True)

# ================================================================== retention closed form
def ret(x0, alpha):
    if alpha <= 0: return 1.0
    if x0 <= 0: return math.exp(-alpha)
    a = x0 ** 4 / 4.0
    return brentq(lambda f: -math.log(f) + a * (1 - f ** 4) - alpha, 1e-300, 1.0, xtol=1e-15) if alpha > 0 else 1.0
def y_of_tau(x0, tau): return ret(x0, tau) if tau > 0 else 1.0
def x_crit(alpha): return ((64.0 / 15.0) * (alpha - math.log(2))) ** 0.25

# ================================================================== per-footing constants
def footing(f):
    h = float(Q15["footings"][f]["main"]["h"]); ob = Q15["footings"][f]["main"]["theta"]["omega_b"]; R = float(F1A[f]["R_B2"])
    Om = ob * (1 + R) / h ** 2; Or = 2.469e-5 * (1 + 0.2271 * 3.046) / h ** 2; Ode = 1 - Om - Or
    z_q0 = (2 * Ode / Om) ** (1 / 3) - 1
    def tlb(z):
        zz = np.linspace(0, z, 20001); E = np.sqrt(Om * (1 + zz) ** 3 + Or * (1 + zz) ** 4 + Ode); return 977.792 / (100 * h) * np.trapz(1 / ((1 + zz) * E), zz)
    H0_gyr = 100 * h / 977.792; G0 = 4 * math.pi * H0_gyr * math.sqrt(Ode)
    vst = (A0H[f] * 2.99792458e8 * LSTAR_PC[f] * 3.0857e16) ** (1 / 3) / 1e3
    return dict(h=h, ob=ob, R=R, Om=Om, Ode=Ode, z_q0=z_q0, t_q0=tlb(z_q0), Gamma0_G=G0, alpha_G=G0 * tlb(z_q0), v_stiff=vst, t_055=tlb(0.55))

# ================================================================== subhalo bracket (Jiang & van den Bosch 2016 unevolved SHMF)
def shmf_moments(mu_max=1.0):
    mu = np.geomspace(1e-4, mu_max, 20000); dN = 0.22 * mu ** -0.91 * np.exp(-6 * mu ** 3)          # per dln mu
    l = np.log(mu); return float(np.trapz(mu ** 2 * dN, l)), float(np.trapz(mu * dN, l))
M2_ALL, M1_ALL = shmf_moments(1.0); M2_ISO, M1_ISO = shmf_moments(0.25)
FSUB = dict(field=math.sqrt(M2_ALL) + 0.012, isolated=math.sqrt(M2_ISO) + 0.012)
FSLOSH = dict(field=M2_ALL * (1 + M1_ALL) + 0.008, isolated=M2_ISO * (1 + M1_ISO) + 0.008)   # A3: mu1 = 1/(1 + int mu dN)

# ================================================================== variant definitions
VAR = os.environ.get("SS1V", "G")
OPT = os.environ.get("SS1V_OPT", "")
FCEN = float(os.environ.get("SS1V_FCEN", "0.6"))        # F bracket value for groups / clusters (0.3 reported as a second run)
def vpar(V, f):
    F = footing(f); base = "G" if V.startswith("MG") else ("H" if (V.startswith("MH") or V.startswith("MI") or V.startswith("I")) else V[:1])
    if base in ("B", "C", "D", "E"): p = dict(z_dec=0.55, alpha=3.80, kick={"B": 355.0, "C": 220.0}.get(base, 1150.0))
    else: p = dict(z_dec=F["z_q0"], alpha=F["alpha_G"], kick=4 * F["v_stiff"])
    p.update(base=base, v_stiff=F["v_stiff"], F=F)
    if V == "MG1": p["v_stiff"] *= 1.25
    if V == "MG2": p["v_stiff"] /= 1.25
    if V == "MG3": p["alpha"] = 0.0
    p["force_x0_zero"] = (V == "MG4")
    if base == "H":                                                            # A4: variant H
        p["hfull"] = V.startswith("Hfull"); p["gform"] = "src" if V == "Hsrc" else "halo"
        if p["hfull"]: p["kick"] = 2 * F["v_stiff"]
        if V == "MH1": p["v_stiff"] = 0.0
        if V == "MH2": p["kick"] = 0.0
        p["iform"] = V.startswith("I") or V.startswith("MI")                   # A5: variant I
        if p["iform"]:
            p["kick"] = 0.0 if V == "MI2" else F["v_stiff"]; p["ceil"] = 1.0 if V == "MI1" else 1 / math.sqrt(3.0)
            p["gform"] = "isrc" if V == "Isrc" else "halo"; p["nobound"] = (V == "Inob"); p["R_FS"] = r_fs(F, p["z_dec"], p["kick"])
    return p
def r_fs(F, z_dec, kick):
    """comoving streaming length today of a daughter kicked at onset: integral of kick (a_dec/a) / a dt (A5)."""
    zz = np.linspace(0, z_dec, 4001); Or = 2.469e-5 * (1 + 0.2271 * 3.046) / F["h"] ** 2
    H = 100 * F["h"] * np.sqrt(F["Om"] * (1 + zz) ** 3 + Or * (1 + zz) ** 4 + F["Ode"]); a = 1 / (1 + zz); a_dec = 1 / (1 + z_dec)
    dt_dz = 977.792 / (H * (1 + zz)); return float(np.trapz(kick * (a_dec / a) / a * dt_dz, zz) * KMS_GYR_MPC)

# ================================================================== variant H (AMENDMENT_A4): per-radius escape retention + bound daughters
def h_profile(p, H, tau):
    """shells of the pre-conversion halo: radii, component mass per shell, the retained fraction f(r, tau), the bound flag of
    a daughter made there, and v_vir. SIS: sigma^2 = V^2/2 (g = 0.5); NFW: isotropic Jeans of the untruncated profile;
    gform 'src': the source's g_pot(u) = u/(0.08 + u)/(1 + 2.5 u^1.5)."""
    R5, R2 = H["R500"], H["R200"]; rg = np.geomspace(1e-3 * R5, R2, 300); M0 = H["Menc"](rg); dM = np.diff(np.concatenate([[0.0], M0]))
    M200 = H["M200"]; V2 = G_KPC * M200 / R2; v = math.sqrt(G_KPC * H["M500"] / R5)
    if H.get("c200") is None:
        sig2 = np.full_like(rg, V2 / 2); Phi = -V2 * (1 + np.log(R2 / rg))
    else:
        c = H["c200"]; rs = R2 / c; mu = lambda x: np.log1p(x) - x / (1 + x); A = M200 / mu(c)
        xg = np.geomspace(1e-4, 2000.0, 6000); rho = 1 / (xg * (1 + xg) ** 2); Mx = A * mu(xg); integ = rho * G_KPC * Mx / (xg * rs) ** 2 * rs
        cum = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(xg))[::-1])[::-1], [0.0]])
        sig2 = np.interp(rg / rs, xg, cum / rho); Phi = -(G_KPC * A) * np.log1p(rg / rs) / rg
    g = sig2 / v ** 2
    if p.get("gform") == "src": u = rg / R5; g = u / (0.08 + u) / (1 + 2.5 * u ** 1.5)
    if p.get("gform") == "isrc": u = rg / R5; g = np.maximum((u / (0.07 + u)) * (1 - 0.45 * u), 0.0)
    if p.get("iform"):
        ea = math.exp(-p["alpha"]); ftoday = ea + (p["ceil"] - ea) * np.exp(-3 * (p["v_stiff"] / v) ** 2 / np.maximum(g, 1e-30))
        f = 1 - (1 - ftoday) * (tau / p["alpha"]) if (tau > 0 and p["alpha"] > 0) else np.ones_like(rg)
    else:
        f = np.exp(-(tau / math.pi) * (p["v_stiff"] / v) ** 2 / np.maximum(g, 1e-30)) if tau > 0 else np.ones_like(rg)
    bound = (0.5 * (3 * sig2 + p["kick"] ** 2) + Phi) < 0
    if p.get("nobound"): bound = np.zeros_like(bound)
    return rg, dM, f, bound, v
def h_puffed(p, H): return p.get("hfull") and math.sqrt(G_KPC * H["M500"] / H["R500"]) < p["v_stiff"] / 2
def h_enc(p, H, r, tau=None):
    tau = p["alpha"] if tau is None else tau; r = np.asarray(r, float)
    if h_puffed(p, H): return H["Mchi0"] * r ** 3 / (r * r + 180.0 ** 2) ** 1.5
    rg, dM, f, b, v = h_profile(p, H, tau); Mc = np.cumsum(dM * (f + (1 - f) * b))
    out = np.interp(r, rg, Mc, left=0.0, right=Mc[-1])
    if p.get("iform"):                                              # A5: unbound daughters in a Gaussian shell, mean R_FS, sigma 0.3 R_FS
        b_true = h_profile(dict(p, nobound=False), H, tau)[3] if p.get("nobound") else b
        esc = float(np.sum(dM * (1 - f) * (~b_true)))                 # I-nob: bound daughters are removed, only the unbound go to the shell
        R0 = 1000.0 * p["R_FS"]; rs = np.linspace(1.0, 4 * R0, 4000); w = rs ** 2 * np.exp(-0.5 * ((rs - R0) / (0.3 * R0)) ** 2); cw = np.cumsum(w); cw /= cw[-1]
        out = out + esc * np.interp(r, rs, cw, left=0.0, right=1.0)
    return out
def h_escaped(p, H, tau):
    if h_puffed(p, H): return 0.0
    rg, dM, f, b, v = h_profile(p, H, tau); return float(np.sum(dM * (1 - f) * (~b)) / np.sum(dM))
def h_bound_fraction(p, H, kick):
    q = dict(p, kick=kick); rg, dM, f, b, v = h_profile(q, H, p["alpha"]); return float(np.sum(dM * b) / np.sum(dM))
ISO_CLS = {"kids"}; GAL_CLS = {"kids", "sparc", "udg", "mw", "lsb"}
def x0_of(p, H, cls, extra=None):
    """the variant's system gate x0 for a virialized pre-conversion halo H (Delta 500, R_sys = R500)."""
    if p["force_x0_zero"] or p["base"] == "H": return 0.0
    extra = extra or {}; b = p["base"]; R5 = H["R500"]; M5 = H["M500"]; v = math.sqrt(G_KPC * M5 / R5)
    Rsys = extra.get("R_sys", R5); Dsys = extra.get("Delta_sys", 500.0)
    fs = extra.get("f_sub", FSUB["isolated" if cls in ISO_CLS else "field"])
    if b == "B": return (fs / 0.035) * (R5 / 250.0)
    if b in ("C", "D"): return (fs / 0.035) * (Rsys / 250.0) * (Dsys / 500.0) ** 1.5
    if b == "E":
        fsl = extra.get("f_slosh", FSLOSH["isolated" if cls in ISO_CLS else "field"]); vv = extra.get("v_vir", v)
        W = max(0.0, 1 - (260.0 / vv) ** 2); return W * ((fsl / 0.120) * (Rsys / 250.0) + max(0.0, vv - 410.0) / 95.0) * (Dsys / 500.0) ** 1.5
    vv = extra.get("v_vir", v)
    if b == "F":
        if Dsys < 200: return 0.0
        fc = extra.get("f_cen", 1.0 if cls in GAL_CLS else FCEN); return 3.40 * max(0.0, (vv / p["v_stiff"]) ** 2 - 1) * (1 - 0.75 * fc)
    if Dsys < 500: return 0.0
    return 3.0 * max(0.0, (vv / p["v_stiff"]) ** 2 - 1)

# ================================================================== component (interface of ss1.Comp)
class VComp:
    def __init__(self, f, kind="SIS", am=False, zero=False):
        self.f, self.kind, self.am, self.zero = f, kind, am, zero; self.p = vpar(VAR, f); F = self.p["F"]; self.c = dict(h=F["h"], R=F["R"], Om=F["Om"]); self.cache = {}
    def halo_for(self, Mb, cls):
        c = self.c; z = self.p["z_dec"]
        if self.am and cls in GAL_CLS:
            M200 = C.moster_halo(Mb, z); H = C.halo(Mb, c["R"], c["h"], c["Om"], kind=self.kind, M200=M200, Mchi=M200 * c["R"] / (1 + c["R"]), z=z)
        else: H = C.halo(Mb, c["R"], c["h"], c["Om"], kind=self.kind, z=z)
        H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]; return H
    def _sys(self, key):
        if key in self.cache: return self.cache[key]
        Mb, cls = key[0], key[1]; H = self.halo_for(Mb, cls); extra = dict(EXTRA.get((round(Mb, -3), cls), {}))
        if OPT == "obs" and (round(Mb, -3), cls) in OBS: extra["v_vir"] = OBS[(round(Mb, -3), cls)]
        x0 = x0_of(self.p, H, cls, extra); fr = None; host = None
        if len(key) == 4:                                                     # member
            host = self._sys(key[2]); d = key[3]; b = self.p["base"]; xh = host["x0"] if d < host["H"]["R500"] else 0.0
            if b == "B": x0 = max(x0, xh)                                     # bath: the host's f
            elif b in ("C", "D", "E"): x0 = math.sqrt(x0 ** 2 + xh ** 2)
            else: x0 = max(x0, xh)
        fr = ret(x0, self.p["alpha"])
        if self.p["base"] == "H": x0 = 0.0; fr = float(h_enc(self.p, H, H["R200"] * 1.0001)) / H["Mchi0"]       # A4: own halo only
        e = dict(H=H, x0=x0, f=fr, cls=cls); self.cache[key] = e; return e
    def build(self, keys):
        for k in keys:
            if not self.zero: self._sys(k)
    def _Mret(self, r, e):
        H = e["H"]; r = np.asarray(r, float); b = self.p["base"]
        if b == "B" and not self.p["force_x0_zero"]:
            rg = np.geomspace(1e-3 * H["R500"], H["R200"], 400); M0 = H["Menc"](rg); dM = np.diff(np.concatenate([[0.0], M0]))
            g = np.where(rg <= 0.25 * H["R500"], 1.0, (rg / (0.25 * H["R500"])) ** (math.log(0.72) / math.log(4)))
            fr = np.array([ret(e["x0"] * gi, self.p["alpha"]) for gi in g]); Mc = np.cumsum(dM * fr)
            return np.interp(r, rg, Mc, left=0.0, right=Mc[-1])
        if b == "G" and OPT == "local" and not self.p["force_x0_zero"]:
            rg = np.geomspace(1e-3 * H["R500"], H["R200"], 400); M0 = H["Menc"](rg); dM = np.diff(np.concatenate([[0.0], M0]))
            v = math.sqrt(G_KPC * H["M500"] / H["R500"]); vl = v * (1 + (rg / (0.35 * H["R500"])) ** 2) ** -0.25
            fr = np.array([ret(3 * max(0.0, (vi / self.p["v_stiff"]) ** 2 - 1), self.p["alpha"]) for vi in vl]); Mc = np.cumsum(dM * fr)
            return np.interp(r / 1.18, rg, Mc, left=0.0, right=Mc[-1])        # the 18 % expansion (bracket, as given)
        if b == "H": return h_enc(self.p, H, r)
        out = e["f"] * H["Menc"](r)
        if b == "C":                                                          # evicted mass in the shelf (Gaussian shell, mean 1.2 Mpc, sigma 0.3 Mpc)
            rs = np.linspace(1.0, 4000.0, 4000); w = rs ** 2 * np.exp(-0.5 * ((rs - 1200.0) / 300.0) ** 2); cw = np.cumsum(w); cw /= cw[-1]
            out = out + (1 - e["f"]) * H["Mchi0"] * np.interp(r, rs, cw, left=0.0)
        return out
    def M(self, r, key):
        if self.zero: return np.zeros_like(np.asarray(r, float))
        return self._Mret(r, self._sys(key))
    def info(self, key):
        if self.zero: return {}
        e = self._sys(key); H = e["H"]; tot = float(self._Mret(H["R200"] * 1.0001, e)); r5 = float(self._Mret(H["R500"], e)); r25 = float(self._Mret(0.25 * H["R500"], e))
        return dict(M_b=H["M_b"], M200=H["M200"], M500=H["M500"], Mchi0=H["Mchi0"], R200=H["R200"], R500=H["R500"], c200=H["c200"], v_vir=math.sqrt(G_KPC * H["M500"] / H["R500"]),
                    x0_system=e["x0"], ret_total=tot / H["Mchi0"], ret_R500=r5 / float(H["Menc"](H["R500"])), ret_025R500=r25 / float(H["Menc"](0.25 * H["R500"])),
                    reduced_reading=e["f"], frozen_da_bracket=None, retained_over_Mb=tot / H["M_b"])
    def rho(self, r_kpc, key):
        if self.zero: return 0.0
        h = 1e-3 * r_kpc; return float((self.M(r_kpc + h, key) - self.M(r_kpc - h, key)) / (2 * h) / (4 * math.pi * r_kpc ** 2))
EXTRA = {}; OBS = {}

# ================================================================== known answers
def run_ka():
    out = {}
    rows = []; ok = True
    for alpha in (3.80, 4.39):
        for x0 in (0.5, 1.5, 1.95, 2.4, 3.2):
            s = solve_ivp(lambda t, y: -y / (1 + (x0 * y) ** 4), (0, alpha), [1.0], rtol=1e-12, atol=1e-14); yn = float(s.y[0, -1]); yc = ret(x0, alpha)
            rows.append(dict(alpha=alpha, x0=x0, numeric=yn, closed=yc, dev=abs(yn - yc))); ok &= abs(yn - yc) <= 1e-6
    out["K0_closed_form_vs_ODE"] = dict(rows=rows, pass_=bool(ok))
    out["K_B_reproduction"] = dict(claimed={"1.95": 0.250, "2.10": 0.667, "2.40": 0.852, "0.18-0.64": [0.022, 0.023]},
                                   lane={"1.95": ret(1.95, 3.8), "2.10": ret(2.10, 3.8), "2.40": ret(2.40, 3.8), "0.18": ret(0.18, 3.8), "0.64": ret(0.64, 3.8)})
    out["K_D_xcrit"] = dict(at_3p80=x_crit(3.80), at_4p39=x_crit(4.39), ref=[1.908, 1.99], f_at_xcrit=[ret(x_crit(3.80), 3.80), ret(x_crit(4.39), 4.39)])
    # K-F: orchestrator's checks (v_stiff 286, kT-group with f_cen as the orchestrator took it: back out from its x0 where needed; reported)
    kf = {}
    for v, lab in ((361.5, "kT0.8_M500_R500"), (440.0, "1.8e13"), (521.0, "3e13")):
        x = 3.40 * ((v / 286.0) ** 2 - 1); kf[lab] = dict(v=v, x0_fcen0=x, needed_fcen_for_orchestrator=None, f_380_at_x0_1p27=ret(1.27, 3.8), f_439_at_x0_1p27=ret(1.27, 4.39))
    kf["orchestrator_x0_1p27"] = dict(f_380=ret(1.27, 3.80), f_439=ret(1.27, 4.39), ref=[0.043, 0.024]); kf["x0_0p94"] = dict(f_380=ret(0.94, 3.8), f_439=ret(0.94, 4.39)); kf["x0_0p99"] = dict(f_380=ret(0.99, 3.8), f_439=ret(0.99, 4.39))
    out["K_F"] = kf
    # K-G: z 0.05, 500 rho_c, v_stiff 286, alpha 4.39 (h 0.674, Om 0.3154 as the footing; reported against the orchestrator's table)
    F = footing("canonical"); rc = C.rho_crit(0.05, F["h"], F["Om"]); kg = []; okg = True
    refv = [242, 287, 321, 361, 399, 455, 521]; reff = [0.012, 0.012, 0.014, 0.161, 0.927, 0.990, 0.998]
    for M5, vr, fr in zip([3e12, 5e12, 7e12, 1e13, 1.35e13, 2e13, 3e13], refv, reff):
        R5 = (3 * M5 / (4 * math.pi * 500 * rc)) ** (1 / 3); v = math.sqrt(G_KPC * M5 / R5); x = 3 * max(0, (v / 286.0) ** 2 - 1); f_ = ret(x, 4.39)
        kg.append(dict(M500=M5, v=v, v_ref=vr, f=f_, f_ref=fr)); okg &= abs(v / vr - 1) <= 0.01 and abs(f_ - fr) <= 0.005
    lov = []
    for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")):
        if l.startswith("#") or l.startswith("name"): continue
        c_ = l.rstrip("\n").split("\t"); M5 = float(c_[6]) * 1e13; R5 = float(c_[4]); v = math.sqrt(G_KPC * M5 / R5); lov.append(dict(name=c_[0], v=v, f=ret(3 * max(0, (v / 286.0) ** 2 - 1), 4.39)))
    out["K_G"] = dict(table=kg, pass_=bool(okg), lovisari=lov, lovisari_min_f=min(x["f"] for x in lov), lovisari_all_ge_0p992=bool(min(x["f"] for x in lov) >= 0.992))
    out["footings"] = {f: footing(f) for f in FOOTS}
    out["subhalo_bracket"] = dict(int_mu2_all=M2_ALL, int_mu_all=M1_ALL, int_mu2_iso=M2_ISO, int_mu_iso=M1_ISO, f_sub=FSUB, f_slosh=FSLOSH)
    json.dump(out, open(os.path.join(PARTS, "v_ka.json"), "w"), indent=1, default=float)
    P(f"K0 closed form vs ODE: {'PASS' if ok else 'FAIL'} (max dev {max(r['dev'] for r in rows):.1e})")
    P(f"K-B source claims 1.95/2.10/2.40 -> 25.0/66.7/85.2 %: lane {ret(1.95,3.8):.3f} / {ret(2.10,3.8):.3f} / {ret(2.40,3.8):.3f}; KiDS 0.18-0.64 -> {ret(0.18,3.8):.4f}-{ret(0.64,3.8):.4f}")
    P(f"K-D x_crit {x_crit(3.80):.4f} (3.80) {x_crit(4.39):.4f} (4.39)")
    P(f"K-F x0 1.27 -> {ret(1.27,3.8):.4f} / {ret(1.27,4.39):.4f} (ref 0.043 / 0.024); 0.94 -> {ret(0.94,3.8):.4f}/{ret(0.94,4.39):.4f}; 0.99 -> {ret(0.99,3.8):.4f}/{ret(0.99,4.39):.4f}")
    P("K-G " + ("PASS" if okg else "FAIL") + ": " + "; ".join(f"{r['M500']:.3g}: v {r['v']:.0f} ({r['v_ref']}) f {r['f']:.3f} ({r['f_ref']})" for r in kg) + f"; Lovisari min f {out['K_G']['lovisari_min_f']:.4f}")
    for f in FOOTS:
        F = out["footings"][f]; P(f"[{f}] z_dec(q=0) {F['z_q0']:.4f}, Gamma0 {F['Gamma0_G']:.4f}/Gyr, alpha {F['alpha_G']:.3f}, x_crit {x_crit(F['alpha_G']):.3f}, v_stiff {F['v_stiff']:.1f} km/s, kick {4*F['v_stiff']:.0f}")
    P(f"subhalo bracket: f_sub field {FSUB['field']:.4f}, isolated (mu<=0.25) {FSUB['isolated']:.4f}; f_slosh {FSLOSH['field']:.4f} / {FSLOSH['isolated']:.4f}")

# ================================================================== local gates through ss1.run_local
def run_local(V):
    import ss1 as S
    # record-native extras: observed M500 bracket (Lovisari groups, X-COP) keyed by the system's M_b as ss1.run_local passes it
    GB = S.J.load_prefix(os.path.join(S.CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
    lov = {}
    for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")):
        if l.startswith("#") or l.startswith("name"): continue
        c_ = l.rstrip("\n").split("\t"); lov[c_[0]] = (float(c_[6]) * 1e13, float(c_[4]))
    for gp in GB["GR"]:
        if gp["name"] in lov:
            M5, R5 = lov[gp["name"]]
            for fst in (0, 1): OBS[(round(gp["g5"] * (1 + fst), -3), "group")] = math.sqrt(G_KPC * M5 / R5)
    from astropy.io import fits
    for z in GB["XC"]:
        name = z["name"]
        with fits.open(os.path.join(GB["DATA"], "xcop", name, f"{name}_fgas_profile.fits")) as h: R5 = float(h[1].header["R500"])
        F = footing("canonical"); M5 = 500 * C.rho_crit(0.05, F["h"], F["Om"]) * 4 / 3 * math.pi * R5 ** 3
        OBS[(round(z["Mb_last"][0], -3), "xcop")] = math.sqrt(G_KPC * M5 / R5)
    S.Comp = VComp; S.RES = {}; S.SUFFIX = f"_V{V}" + (f"_{OPT}" if OPT else "") + (f"_fcen{FCEN}" if VAR == "F" and FCEN != 0.6 else "")
    if V.startswith("MG") or V.startswith("MH") or V.startswith("MI") or V in ("Isrc", "Inob") or OPT: S.MUT = "primary-only"
    S.run_local()
    # gate 5b, Ursa Major (EV1 W1): members' pointwise shift minus the field's, primary halos
    out = {}
    for f in FOOTS:
        a0 = S.A0H[f]; Sx, _, _ = GB["build"](f, a0); CP = VComp(f); sparc_meta = {}
        sys.path.insert(0, os.path.join(S.CL6, "QX8_sparc_exact_field")); a_ = sys.argv; sys.argv = [a_[0]]
        with contextlib.redirect_stdout(io.StringIO()):
            import qx8 as Q8
        sys.argv = a_
        for q in Q8.load_sparc(): sparc_meta[q["name"]] = q["meta"]
        per = {}
        names = [g_["name"] for g_ in GB["SP"] for _ in range(len(g_["R"]))]; assert len(names) == len(Sx)      # GB1 build() appends points galaxy by galaxy
        for nm_, pnt in zip(names, Sx): per.setdefault(nm_, []).append(pnt)
        Msys = {n: (pts[0]["feat"]["r"] / pts[0]["feat"]["rrM"]) ** 2 * a0 / S.G_SI / S.MS for n, pts in per.items()}
        uma = [n for n in per if sparc_meta.get(n, {}).get("fD") == 4]; fld = [n for n in per if n not in uma]
        # host: the members' summed primary halos; f_sub record-native (largest member as i = 1); R_sys 1.5 Mpc (source), Delta from it
        Hm = {n: CP.halo_for(Msys[n], "sparc") for n in uma}; Mh = sum(H["M200"] for H in Hm.values()); ms = sorted((H["M200"] / Mh for H in Hm.values()), reverse=True)
        fsub = math.sqrt(sum(m * m for m in ms[1:])) + 0.012; rc = C.rho_crit(CP.p["z_dec"], CP.c["h"], CP.c["Om"]); Rsys = 1500.0; Dsys = 3 * Mh / (4 * math.pi * Rsys ** 3 * rc)
        Mbh = Mh / (1 + C.F_CAP * CP.c["R"]); Hh = CP.halo_for(Mbh, "uma_host")
        v_geo = math.sqrt(G_KPC * Mh / Rsys)
        xh_geo = x0_of(CP.p, Hh, "uma_host", dict(R_sys=Rsys, Delta_sys=Dsys, f_sub=fsub, f_slosh=sum(m * m for m in ms[1:]) / ms[0] + 0.008, v_vir=v_geo, f_cen=ms[0]))
        xh_bound = x0_of(CP.p, Hh, "uma_host", dict(f_sub=fsub, f_slosh=sum(m * m for m in ms[1:]) / ms[0] + 0.008, f_cen=ms[0]))
        b = CP.p["base"]
        def shift_for(names, xhost):
            vals = []
            for n in names:
                H = CP.halo_for(Msys[n], "sparc"); xo = x0_of(CP.p, H, "sparc")
                if xhost is not None: xo = max(xo, xhost) if b in ("B", "F", "G") else math.sqrt(xo ** 2 + xhost ** 2)
                fr = ret(xo, CP.p["alpha"]); s_ = []
                for pnt in per[n]:
                    r = pnt["feat"]["r"] / S.KPC; Mb = pnt["feat"]["Mb"]; gN = GB["need"](pnt["feat"], "x") * a0
                    bb = 1 + (float(h_enc(CP.p, H, r)) if b == "H" else fr * float(H["Menc"](r))) / Mb
                    s_.append(math.log10(S.glaw(bb * gN, a0) / S.glaw(gN, a0)))
                vals.append(float(np.mean(s_)))
            return float(np.mean(vals))
        d_geo = shift_for(uma, xh_geo) - shift_for(fld, None); d_bound = shift_for(uma, xh_bound) - shift_for(fld, None)
        out[f] = dict(N_uma=len(uma), N_field=len(fld), M_host=Mh, f_sub_record_native=fsub, Delta_sys=Dsys, x_host_geometry=xh_geo, f_host_geometry=ret(xh_geo, CP.p["alpha"]),
                      x_host_bound_reading=xh_bound, f_host_bound=ret(xh_bound, CP.p["alpha"]), Delta_pred=d_geo, Delta_pred_bound_reading=d_bound, EV1_d=-0.024, EV1_sigma=0.064,
                      status="PASS" if abs(d_geo + 0.024) <= 0.128 else "FAIL")
        P(f"[{f}] 5b UMa ({len(uma)} vs {len(fld)}): host M200 {Mh:.3g}, f_sub {fsub:.3f}, Delta {Dsys:.1f}; x_host {xh_geo:.3f} (f {ret(xh_geo, CP.p['alpha']):.3f}) -> Delta_pred {d_geo:+.3f} vs EV1 -0.024 +- 0.064: {out[f]['status']}; bound reading x {xh_bound:.2f} -> {d_bound:+.3f}")
    json.dump(out, open(os.path.join(PARTS, f"uma_V{V}{('_' + OPT) if OPT else ''}.json"), "w"), indent=1, default=float)

# ================================================================== cosmology: growth with streaming daughters
def run_cosmo(V):
    f = os.environ.get("SS1_FOOT", "canonical"); src = open(os.path.join(HERE, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
    ns = {"__file__": os.path.join(HERE, "ss1_cosmo.py"), "__name__": "ss1c_v"}; a_ = sys.argv; sys.argv = ["ss1_cosmo.py"]
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
    sys.argv = a_
    p = vpar(V, f); M = ns["M"]; KG, ZG = ns["KG"], ns["ZG"]; REFBG = ns["REFBG"]; OD, OB = ns["OD"], ns["OB"]; Q3 = ns["Q3"]; X0 = ns["X0"]; c0 = ns["c0"]
    # PS nodes at the variant's z_dec
    kk = ns["kk"]; Pk = np.array([M.pk_lin(k, p["z_dec"]) for k in kk]); RHO_M0 = ns["RHO_M0"]
    def sig(Mm):
        Rr = (3 * Mm / (4 * math.pi * RHO_M0)) ** (1 / 3); x = kk * Rr; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; return math.sqrt(np.trapz(Pk * W * W * kk ** 3 / (2 * math.pi ** 2), np.log(kk)))
    MED = np.logspace(6, 16, 41); MN = np.sqrt(MED[:-1] * MED[1:]); Fc = erfc(1.686 / (math.sqrt(2) * np.array([sig(m) for m in MED]))); dF = Fc[:-1] - Fc[1:]
    MMIN = float(os.environ.get("SS1V_MMIN", "1e6")); dF = np.where(MN >= MMIN, dF, 0.0)        # A2: M_min 1e10 bracket (halos below M_min stay cold, C-G)
    CPn = VComp.__new__(VComp); CPn.f = f; CPn.kind = "SIS"; CPn.am = False; CPn.zero = False; CPn.p = p; F = p["F"]; CPn.c = dict(h=F["h"], R=F["R"], Om=F["Om"]); CPn.cache = {}
    x0n = []
    for m in MN:
        Mb = m / (1 + C.F_CAP * F["R"]); H = C.halo(Mb, F["R"], F["h"], F["Om"], M200=m, Mchi=m * C.F_CAP * F["R"] / (1 + C.F_CAP * F["R"]), z=p["z_dec"]); H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]
        x0n.append(H if p["base"] == "H" else x0_of(p, H, "node" if m >= 1e13 else "sparc"))
    if p["base"] == "H":
        TG = np.linspace(0, p["alpha"], 41); ESC = np.array([[h_escaped(p, Hn, tg) for tg in TG] for Hn in x0n])
    # background clock (unchanged background) and tau(a)
    z = REFBG["z"]; t = REFBG["t"]; tdec = float(np.interp(p["z_dec"], z, t)); t0 = float(t[0])
    def tau_of_z(zz): return np.where(zz < p["z_dec"], p["alpha"] * (np.interp(zz, z, t) - tdec) / (t0 - tdec), 0.0)
    def Fconv(zz):
        ta = float(tau_of_z(np.array([zz]))[0])
        if ta <= 0: return 0.0
        halo = float(sum(d * np.interp(ta, TG, ESC[i]) for i, d in enumerate(dF))) if p["base"] == "H" else float(sum(d * (1 - y_of_tau(x, ta)) for d, x in zip(dF, x0n)))
        field = (1 - Fc[0]) * (1 - math.exp(-ta)) if p["base"] == "B" else 0.0
        return halo + field
    # streaming length (comoving Mpc) for a daughter produced at onset: integral of v (a_dec/a) / a dt
    a_dec = 1 / (1 + p["z_dec"])
    def lam_of_z(zz):
        if p["base"] == "B": return 5.0
        if zz >= p["z_dec"]: return 0.0
        zs = np.linspace(zz, p["z_dec"], 400); ts = np.interp(zs, z, t); a = 1 / (1 + zs); integ = p["kick"] * (a_dec / a) / a
        return float(abs(np.trapz(integ, ts)) * KMS_GYR_MPC)
    # growth (record's two-fluid ODE, WD1's k-dependent form) with fc(k, a) = Fconv (1 - T(k)), T = 1/(1 + (k lam)^2)
    lna_t = np.log(1 / (1 + z)); o = np.argsort(lna_t); lna_t = lna_t[o]; lnH = np.log(REFBG["H"][o]); dlnH = np.gradient(lnH, lna_t)
    ai = 1 / 3401.0; adec = 1 / 1091.0; nk = len(KG); ZF = np.linspace(0.0, 1.2, 241)                 # fine low-z epochs for fsigma8 (A4 disclosure: replaces the coarse-grid spline derivative)
    grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), np.log(1 / (1 + ZG)), np.log(1 / (1 + ZF))])); tset = {float(x): i for i, x in enumerate(np.log(1 / (1 + ZG)))}; tsetF = {float(x): i for i, x in enumerate(np.log(1 / (1 + ZF)))}
    I4 = np.eye(4)[None, :, :]; zgrid_fc = np.linspace(0, p["z_dec"] + 0.01, 120); Fc_tab = np.array([Fconv(x) for x in zgrid_fc]); lam_tab = np.array([lam_of_z(x) for x in zgrid_fc])
    def solve(on):
        y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai; rec = {}; recF = {}
        for n in range(len(grid) - 1):
            h_ = grid[n + 1] - grid[n]; lm = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lm); zz = 1 / a - 1
            E2 = math.exp(2 * np.interp(lm, lna_t, lnH)) / 100.0 ** 2; dl = float(np.interp(lm, lna_t, dlnH))
            fc = np.zeros(nk)
            if on and zz < p["z_dec"]:
                Fv = float(np.interp(zz, zgrid_fc, Fc_tab)); lv = float(np.interp(zz, zgrid_fc, lam_tab)); fc = Fv * (1 - 1 / (1 + (KG * lv) ** 2))
            Od = OD * a ** -3 / E2 * (1 - fc); Ob = OB * a ** -3 / E2
            A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od; A[:, 1, 1] = -(2 + dl)
            if a > adec: A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
            y = np.linalg.solve(I4 - 0.5 * h_ * A, ((I4 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
            if float(grid[n + 1]) in tset: rec[tset[float(grid[n + 1])]] = y.copy()
            if float(grid[n + 1]) in tsetF: recF[tsetF[float(grid[n + 1])]] = y.copy()
        def fcz(zz): return float(np.interp(zz, zgrid_fc, Fc_tab)) * (1 - 1 / (1 + (KG * float(np.interp(zz, zgrid_fc, lam_tab))) ** 2)) if (on and zz < p["z_dec"]) else np.zeros(nk)
        outF = np.array([OB * recF[j][:, 2] + OD * (1 - fcz(ZF[j])) * recF[j][:, 0] for j in range(len(ZF))]).T
        outv = np.empty((nk, len(ZG)))
        for jz in range(len(ZG)):
            a = 1 / (1 + ZG[jz]); zz = ZG[jz]; fc = np.zeros(nk)
            if on and zz < p["z_dec"]: fc = float(np.interp(zz, zgrid_fc, Fc_tab)) * (1 - 1 / (1 + (KG * float(np.interp(zz, zgrid_fc, lam_tab))) ** 2))
            outv[:, jz] = OB * rec[jz][:, 2] + OD * (1 - fc) * rec[jz][:, 0]
        return outv, outF
    (o1, f1), (o0, f0) = solve(True), solve(False); Rr = o1 / o0; RF_ = f1 / f0
    # sigma8 / fsigma8 (WD1 / CE2 form), lensing reading
    hh = F["h"]; R8 = 8.0 / hh; lk = np.log(KG); W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; w2k3 = W8(KG * R8) ** 2 * KG ** 3 / (2 * np.pi ** 2); Pref = ns["PREF"]
    sig8 = lambda RR: np.sqrt(np.trapz(Pref * RR ** 2 * w2k3[:, None], lk, axis=0)); s_sw = sig8(Rr); s_rf = sig8(np.ones_like(Rr))
    from scipy.interpolate import CubicSpline
    lna_z = np.log(1 / (1 + ZG)); oo = np.argsort(lna_z)
    d_sw = CubicSpline(lna_z[oo], s_sw[oo]).derivative()(lna_z); d_rf = CubicSpline(lna_z[oo], s_rf[oo]).derivative()(lna_z); rr_spline = d_sw / d_rf
    PrefF = np.array([[M.pk_lin(k_, z_) for z_ in ZF] for k_ in KG]); s8F = lambda RR: np.sqrt(np.trapz(PrefF * RR ** 2 * w2k3[:, None], lk, axis=0))
    lnaF = np.log(1 / (1 + ZF)); rrF = np.gradient(s8F(RF_), lnaF) / np.gradient(s8F(np.ones_like(RF_)), lnaF)
    rr = np.interp(ZG, ZF, rrF)                     # fine-grid central differences (graded); the coarse spline kept as rr_spline (reported)
    rows = []
    for (tb, zb, r1, p1, m1, r2, p2, m2) in ns["DESI"]:
        e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = float(np.interp(zb, ZF, rrF)); rows.append(dict(bin=tb, z=zb, Rf=x, Rf_coarse_spline_reported=float(np.interp(zb, ZG, rr_spline)), in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2), s8dir=bool(x <= 1.001)))
    fs_pass = all(r_["in_sf"] and r_["in_sfb"] and r_["s8dir"] for r_ in rows)
    sig8_ref0 = float(M.sigma8()); s8r0 = float(s_sw[0] / s_rf[0]); Om = F["Om"]
    Sx = ns["limber4_bg"](REFBG, Rr); cl, A = Q3["best_amp_chi2"](X0 * Sx)
    FD = ns["forest_setup"](); fr = ns["forest_eval"](FD, REFBG, Rr)
    out = dict(variant=V, footing=f, z_dec=p["z_dec"], alpha=p["alpha"], kick=p["kick"], v_stiff=p["v_stiff"], F_conv_today=float(Fc_tab[0]), F_coll_gt_1e6=float(Fc[0]),
               lambda_today_Mpc=float(lam_tab[0]), x0_nodes=(dict(zip([f"{m:.3g}" for m in MN], x0n)) if p["base"] != "H" else dict(zip([f"{m:.3g}" for m in MN], [float(e[-1]) for e in ESC]))),
               G6=dict(status="PASS", note="mass kept: background identical to the reference (B: 2e-4 mass loss, |Delta chi2| < 1e-2 by A's integrator scale)"),
               sigma8_ratio_z0=s8r0, sigma8_ref=sig8_ref0, sigma8=sig8_ref0 * s8r0, S8=sig8_ref0 * s8r0 * math.sqrt(Om / 0.3), S8_ref=sig8_ref0 * math.sqrt(Om / 0.3),
               fs8=dict(rows=rows, pass_=bool(fs_pass)), forest=fr, G8=dict(status="PASS" if (fs_pass and fr["status"] == "PASS") else "FAIL"),
               lensing_reading=dict(chi2=float(cl), baseline=float(c0), S_L={f"L {L}": float(Sx[L]) for L in (100, 300, 1000) if L < len(Sx)}, status="NO VERDICT (no validated method; A's rule)"),
               criteria=C.CRIT, amendment2=AMEND2)
    out["M_min"] = MMIN; json.dump(out, open(os.path.join(PARTS, f"vcosmo_{V}_{f}" + ("_mmin1e10" if MMIN > 1e6 else "") + ".json"), "w"), indent=1, default=float)
    P(f"[{f}] {V} cosmo: z_dec {p['z_dec']:.3f} alpha {p['alpha']:.3f} kick {p['kick']:.0f}; converted share today {Fc_tab[0]:.3f} (F_coll {Fc[0]:.3f}); lambda {lam_tab[0]:.2f} Mpc; sigma8 {out['sigma8']:.4f} (ref {sig8_ref0:.4f}) S8 {out['S8']:.4f}; "
      f"fsigma8 Rf " + " ".join(f"{r_['bin']} {r_['Rf']:.3f}" for r_ in rows) + f" -> {'PASS' if fs_pass else 'FAIL'}; forest {fr['dchi2']:.3f}; lensing reading {cl:.2f} (base {c0:.2f})")

# ================================================================== Bullet
def run_bullet(V):
    import ss1_bullet as SB
    def call(arg):
        cp = subprocess.run(["nice", "-n", "10", sys.executable, os.path.join(HERE, "ss1_bullet.py"), "--child", arg], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1"))
        line = [l for l in cp.stdout.splitlines() if l.startswith("SS1CHILD ")]
        if cp.returncode != 0 or not line: raise RuntimeError(cp.stderr[-1500:])
        return json.loads(line[0][9:])
    o0 = call("{}"); m = o0["masses"]; Mb = [m["M_gas_sub"][j] + m["M_star_sub"][j] for j in range(2)]; mu = Mb[1] / Mb[0]
    Mret = {}; info = {}
    for f in FOOTS:
        CP = VComp(f); r_ = []; inf = []
        for j, cls in enumerate(("bullet_main", "bullet_sub")):
            H = CP.halo_for(Mb[j], cls); ex = dict(f_sub=mu + 0.012, f_slosh=mu * mu + 0.008) if j == 0 else {}
            x = x0_of(CP.p, H, cls, ex); fr = ret(x, CP.p["alpha"])
            if CP.p["base"] == "H": x = 0.0; fr = float(h_enc(CP.p, H, H["R200"] * 1.0001)) / H["Mchi0"]
            r_.append(fr * H["Mchi0"])
            inf.append(dict(M_b=Mb[j], x0=x, f=fr, v_vir=math.sqrt(G_KPC * H["M500"] / H["R500"]), retained_over_Mb=fr * H["Mchi0"] / Mb[j]))
        Mret[f] = r_; info[f] = inf
    o = call(json.dumps(Mret)); out = dict(variant=V, KA6=o0["KA"], subclusters=info, child_peak_rss_MB=max(o0["child_peak_rss_MB"], o["child_peak_rss_MB"]))
    for f in FOOTS:
        b = o[f]["row"]; out[f] = dict(status="PASS" if b["label"] == "PASS" else "FAIL", row=b)
        P(f"[{f}] {V} Bullet: {b['label']} cls {b['cls']}; M300 {b['M300'][0]/1e14:.2f}, {b['M300'][1]/1e14:.2f} e14 (Z {b['ZM'][0]:+.2f}, {b['ZM'][1]:+.2f}); retained/M_b " + ", ".join(f"{x['retained_over_Mb']:.2f} (x0 {x['x0']:.2f})" for x in info[f]))
    json.dump(out, open(os.path.join(PARTS, f"vbullet_{V}.json"), "w"), indent=1, default=float)

if __name__ == "__main__":
    W = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 else VAR
    if V != VAR: os.environ["SS1V"] = V; VAR = V
    P(f"SS1 variant {V} {W}{(' ' + OPT) if OPT else ''}. A2 {AMEND2}. kappa = 1/2 FITTED; not theory closed; adopts nothing.")
    {"ka": lambda: run_ka(), "local": lambda: run_local(V), "cosmo": lambda: run_cosmo(V), "bullet": lambda: run_bullet(V)}[W]()
