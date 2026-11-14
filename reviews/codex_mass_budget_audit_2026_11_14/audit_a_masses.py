#!/usr/bin/env python3
"""Independent check of item A (enclosed-mass audit) in SI.
Loads the FZS1 prefix read-only (which loads FRZ1 and CFG556 read-only) for the halo population, R_set, Bar and the layouts;
everything else (constants in SI, v*, active flag, Xsh medians, raw-law charge, budget radii) is recomputed here.
  nice -n 19 python3 -I -B reviews/codex_mass_budget_audit_2026_11_14/audit_a_masses.py
Prints counts and examples to stdout (kept as audit_a_masses.out / audit_a_masses_codeG.out); a JSON copy goes to scratch/ (not committed). Footings reported side by side, never pooled.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "closure_2026_11_10", "FZS1_forest_settled_radius", "fzs1_hm.py")
code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
Z = {"__file__": SRC, "__name__": "fzs1_lib_audit"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), Z)
F, L = Z["F"], Z["L"]

# ---- own SI constants
G = 6.67430e-11; MSUN = 1.98892e30; MPC = 3.0856775814913673e22; KPC = MPC / 1e3
# --msun-code: choose MSUN so that G MSUN equals the halo code's G = 4.30091e-9 Mpc (km/s)^2 / Msun (isolates the constant convention)
CODEG = "--msun-code" in sys.argv
if CODEG: MSUN = 4.30091e-9 * MPC * 1e6 / G
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}       # physical, constant in z (as JNT2 states)
h = 0.6736; ob, oc = 0.02237, 0.1200
FB = ob / (ob + oc); XGRID = oc / ob
XS = 5.41; q = 1 + XS; H0 = 67.4e3 / MPC; OL = 0.6847
E = lambda z: math.sqrt((1 - OL) * (1 + z) ** 3 + OL)
vstar = lambda ft, z: A0[ft] / (10 * q * H0 * E(z))     # m/s
pd1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")))
XSH = {ft: {zk: float(np.median([r["share_over_Mb"] for r in pd1[ft]["share_tables"][zk]])) for zk in ("z0.0", "z1.0")}
       for ft in ("canonical", "alt")}
assert abs(F["FB"] - FB) < 1e-15 and abs(F["h"] - h) < 1e-15

def cold_SI(b_kg, r_m, a0):
    t = b_kg * a0 * r_m ** 2 / G
    return 2 * t / (math.sqrt(b_kg * b_kg + 4 * t) + b_kg)

def phys_m(rcom, z): return rcom * MPC / ((1 + z) * h)

ZS = (0.0, 2.2, 3.0, 4.4); FACS = (1.25, 2.0, 3.0, 5.0)
out = dict(constants=dict(FB=FB, X_grid=XGRID, Xsh=XSH, vstar0_kms={f: vstar(f, 0) / 1e3 for f in A0}))
counts, cons_max, nrows = {}, 0.0, 0
examples = {}
for z in ZS:
    Z["set_z"](z)
    for ft in ("canonical", "alt"):
        X = XSH[ft]["z0.0" if z < 1 else "z1.0"]
        assert abs(X - F["Xsh"](ft)) < 1e-12
        for fac in FACS:
            n_act = n_ret = n_all = 0
            for idx, hb in enumerate(L["HB"]):
                nrows += 1
                M200c_kg = hb["M200c"] / h * MSUN; r200c_m = phys_m(hb["r200c"], z)
                v200c = math.sqrt(G * M200c_kg / r200c_m)
                vstiff = Z["VST"][ft] * 1e3
                galaxy = not (v200c > vstiff)
                assert galaxy == (Z["regime"](hb, ft) == "galaxy")
                Q = (1 - FB) * hb["Mta"] / h * MSUN
                Rc = Z["rset_com"](hb, ft, z, fac); R = phys_m(Rc, z)
                if galaxy:
                    b_ret = Q / X
                    shape = float(F["M_L"](hb, min(Rc, hb["rta"]))) / hb["Mta"]
                    b_all = b_ret + (FB * hb["Mta"] / h * MSUN - b_ret) * shape
                else:
                    b_ret = b_all = float(F["bar_cum"](hb, FB * hb["M200c"], np.array([Rc]), hb["r200c"])[0]) / h * MSUN
                # conservation of the implemented FZS1 layout (all haloes, all f)
                if fac in (2.0,) or idx % 20 == 0:
                    rs, MS, _ = Z["lay_S"](ft, z, fac)(hb)
                    cons_max = max(cons_max, abs(MS[-1] / hb["Mta"] - 1))
                if v200c <= vstar(ft, z):
                    n_act += 1
                    n_ret += cold_SI(b_ret, R, A0[ft]) > Q * (1 + 1e-12)
                    n_all += cold_SI(b_all, R, A0[ft]) > Q * (1 + 1e-12)
                if idx in (120, 160) and fac in (1.25, 3.0):
                    rta = phys_m(hb["rta"], z)
                    # budget radii: point retained source (closed form) and all-Bar (root of C(r) = Q on [0, rta])
                    Rb_ret = math.sqrt(G * Q * (Q + b_ret) / (A0[ft] * b_ret)) if galaxy else None
                    def allbar(rm):
                        rc = rm / MPC * (1 + z) * h
                        if galaxy:
                            sh = float(F["M_L"](hb, min(rc, hb["rta"]))) / hb["Mta"]
                            bb = Q / X + (FB * hb["Mta"] / h * MSUN - Q / X) * sh
                        else:
                            bb = float(F["bar_cum"](hb, FB * hb["M200c"], np.array([rc]), hb["r200c"])[0]) / h * MSUN
                        return cold_SI(bb, rm, A0[ft]) / Q - 1
                    Rb_all = brentq(allbar, 1e-6 * rta, rta, xtol=1e-12 * rta) if allbar(rta) > 0 else None
                    examples[f"{ft}|z{z:g}|i{idx}|f{fac:g}"] = dict(
                        M200m_Msun_h=hb["M"], galaxy=galaxy, active=v200c <= vstar(ft, z),
                        Mb_ret_Msun=b_ret / MSUN, R_set_kpc=R / KPC, rta_kpc=rta / KPC,
                        Rbudget_ret_kpc=None if Rb_ret is None else Rb_ret / KPC,
                        Rbudget_allbar_kpc=None if Rb_all is None else Rb_all / KPC,
                        raw_ret_cold_at_Rset_Msun_h=cold_SI(b_ret, R, A0[ft]) / MSUN * h,
                        patch_cold_Msun_h=Q / MSUN * h)
            counts[f"{ft}|z{z:g}|f{fac:g}"] = dict(active=n_act, retained_exceeds=int(n_ret), allbar_exceeds=int(n_all))
            print(ft, z, fac, counts[f"{ft}|z{z:g}|f{fac:g}"], flush=True)
out.update(n_rows=nrows, counts=counts, FZS1_patch_mass_conservation_max_rel=cons_max, examples=examples,
           note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
out["msun_kg"] = MSUN
os.makedirs(os.path.join(HERE, "scratch"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "scratch", "audit_a_masses_codeG.json" if CODEG else "audit_a_masses.json"), "w"), indent=1)
print("MSUN (kg)", MSUN, "; constants", json.dumps(out["constants"]))
for k, v in examples.items():
    print("EXAMPLE", k, json.dumps({a: (float(f"{b:.7g}") if isinstance(b, float) else b) for a, b in v.items()}))
print("rows", nrows, "conservation", cons_max)
print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
