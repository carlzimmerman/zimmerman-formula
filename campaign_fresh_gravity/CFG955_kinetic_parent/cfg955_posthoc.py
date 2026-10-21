"""CFG955 POST HOC (amendment A1, dated 2026-10-21; no class weight). Run only after cfg955.py MAIN has written cfg955_results.json.
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg955_posthoc.py   -> cfg955_posthoc.out, cfg955_posthoc.json
PH1  a1 convergence: the NGC 3198 stationary-state check with the simple kernel at N = 100001 (frozen), 200001, 400001 table nodes.
PH2  the second hydrostatic equilibrium found by L5 (same T_J, same domain dust mass): its law deviation on NGC 3198's 43 radii and
     at the deep points, and on the toy at r = 2, 5, 8; plus the law deviation along the near-degenerate family C in [C2, 1].
PH3  the central-collapse diagnostics of the K-T spherical toy (IC-L), 200 s wall cap each: frozen settings; N = 40000; softening 0.1;
     fast probe tau/10; relaxation forbidden inside r = 0.24; relaxation off.
PH4  thermostatted linear stability (T-BE): SIS Euler exponents (sympy) and the lowest Sturm-Liouville eigenvalue of
     -(y'/(r^2 rho))' - (4 pi G/(r^2 T_J)) y = omega^2 y/(r^2 rho T_J), y = delta M, Dirichlet at r_in and 0.999 r_e (rigid; conservative),
     on the toy and on NGC 3198 (both footings, both kernels).
PH5  energy books through the collapse onset: frozen K-T toy from IC-L, |E_tot(t) - E_tot(0)|/E_ref and the inner fractions at
     t = 5, 10, 12, 13, 14 (200 s cap).
kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed."""
import os, sys, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg955.py")).read()
head = src.split("# ================================================================================================ K CONTROLS")[0]
g = {"__file__": os.path.join(HERE, "cfg955.py"), "__name__": "cfg955_head"}
exec(compile(head, "cfg955_head", "exec"), g)
np = g["np"]; PchipInterpolator = g["PchipInterpolator"]
OUT = []; RES = {"lane": "CFG955", "part": "POSTHOC A1", "criteria": g["CRIT"]}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


MAIN = json.load(open(os.path.join(HERE, "cfg955_results.json")))
G_SI, KPC, MSUN, MB_N, R_N = g["G_SI"], g["KPC"], g["MSUN"], g["MB_N"], g["R_N"]
r0 = 0.1 * KPC
P("CFG955 POST HOC (A1, 2026-10-21; no class weight)")


def a1_dev(kz, foot, N, C=1.0):
    a0 = g["A0"][foot]
    md = g["ngc_model"](kz, a0)
    m_v, dm_v, law_v, dlaw_v = g["ngc_vec"](kz, a0, md)
    tab = g["hydro_tables"](m_v, dm_v, law_v, dlaw_v, G_SI, r0, md["r_e"], N=N)
    Mend, path = g["rk4_hydro"](tab, [C], keep_path=True)
    xn = tab["x"][::2]; Mdi = PchipInterpolator(np.log(xn), path[:, 0])
    Rin = R_N[R_N > r0]
    gm = G_SI * (m_v(Rin) + Mdi(np.log(Rin))) / Rin ** 2; glw = law_v(G_SI * m_v(Rin) / Rin ** 2)
    dev = np.abs(gm / glw - 1)
    deep = {}
    for y in (1e-2, 1e-3):
        rd = math.sqrt(G_SI * MB_N * MSUN / (y * a0))
        gmd = G_SI * (float(m_v(np.array([rd]))[0]) + float(Mdi(math.log(rd)))) / rd ** 2
        deep[f"y={y:g}"] = abs(gmd / float(law_v(G_SI * MB_N * MSUN / rd ** 2)) - 1)
    return dict(max_dev=float(dev.max()), argmax_kpc=float(Rin[int(np.argmax(dev))] / KPC), deep=deep,
                Mend_over_Mc=float(Mend[0] / md["Mc"]))


# ---- PH1
PH1 = {}
for foot in ("canonical", "alt"):
    for N in (100001, 200001, 400001):
        t0 = time.time(); d = a1_dev("simple", foot, N)
        PH1[f"{foot}|N={N}"] = d
        P(f"  PH1 [{foot}, simple] N = {N}: max |g/g_law - 1| = {d['max_dev']:.3e} at {d['argmax_kpc']:.2f} kpc; deep {d['deep']}; "
          f"M_d(r_e)/M_c {d['Mend_over_Mc']:.9f} ({time.time() - t0:.0f} s)")
RES["PH1"] = PH1

# ---- PH2
PH2 = {}
for key, v in MAIN["L5"].items():
    if not key.startswith("NGC3198"):
        continue
    _, foot, kz = key.split("|")
    roots = [float(x) for x in v["roots"]]
    rows = {}
    for C in sorted(set([min(roots)] + [0.6, 0.75, 0.9] + roots)):
        d = a1_dev(kz, foot, 100001, C)
        rows[f"C={C:.6f}"] = d
    PH2[key] = rows
    P(f"  PH2 [{foot}, {kz}] roots {['%.6f' % x for x in roots]}: " + "; ".join(
        f"{k}: max dev {d['max_dev']:.3f} at {d['argmax_kpc']:.2f} kpc, M_d/M_c {d['Mend_over_Mc']:.5f}" for k, d in rows.items()))
# toy
ttab = g["hydro_tables"](g["tt_m"] if "tt_m" in g else (lambda x: g["t_Mb"](x)),
                         lambda x: 3 * g["TMB"] * g["TAB"] ** 2 * x * x / (x * x + g["TAB"] ** 2) ** 2.5,
                         lambda gn: g["law_simple"](gn, g["TA0"]), lambda gn: g["dlaw"]("simple", gn, g["TA0"]), g["TG"], 1e-3, g["RSTAR"])
troots = [float(x) for x in MAIN["L5"]["toy"]["roots"]]
TROW = {}
for C in sorted(set(troots + [0.3, 0.6])):
    Mend, path = g["rk4_hydro"](ttab, [C], keep_path=True)
    xn = ttab["x"][::2]; Mdi = PchipInterpolator(np.log(xn), path[:, 0])
    rr = np.array([2.0, 5.0, 8.0])
    TROW[f"C={C:.6f}"] = dict(m_over_Mph=(Mdi(np.log(rr)) / g["t_Mph"](rr)).tolist(), Mend_over_Mc=float(Mend[0] / g["T_MC"]))
P("  PH2 toy: " + "; ".join(f"{k}: M_d/M_ph at r = 2, 5, 8 = {[round(x, 3) for x in d['m_over_Mph']]}, M_d(r_*)/M_c {d['Mend_over_Mc']:.4f}"
                             for k, d in TROW.items()))
PH2["toy"] = TROW
RES["PH2"] = PH2

# ---- PH4: thermostatted linear stability
import sympy as sp
from scipy.linalg import eigh_tridiagonal
ss_ = sp.symbols("s")
roots_s = sp.solve(sp.Eq(-ss_ * (ss_ - 1) - 2, 0), ss_)
spacing = float(2 * sp.pi / sp.sqrt(7)); thr = math.exp(spacing)
P(f"  PH4 (sympy) SIS: -y'' - 2y/r^2 = 0 has y = r^s with s = {roots_s}; zero spacing in ln r = 2 pi/sqrt(7) = {spacing:.4f}; "
  f"a negative omega^2 exists once the deep SIS region spans r_out/r_in > e^(2 pi/sqrt 7) = {thr:.3f}")


def lowest_modes(tab, Gc, r_in, frac_edge=0.999, npts=4000):
    x = tab["x"]; sel = (x >= r_in) & (x <= frac_edge * tab["r_e"]) & np.isfinite(tab["TJ"]) & (tab["TJ"] > 0) & (tab["rho"] > 0)
    xs = x[sel]; rho = tab["rho"][sel]; T = tab["TJ"][sel]
    idx = np.unique(np.round(np.linspace(0, xs.size - 1, npts)).astype(int))
    r = xs[idx]; rho = rho[idx]; T = T[idx]; l = np.log(r); h = np.diff(l)
    pr = 1.0 / (r * r * rho) / r                                     # (p / r) in the ln-r form
    q = -4 * math.pi * Gc / (r * r * T) * r
    w = 1.0 / (r * r * rho * T) * r
    ph = 0.5 * (pr[1:] + pr[:-1]) / h                                # flux coefficients at half points
    n = r.size - 2                                                   # interior unknowns (Dirichlet ends)
    hm = 0.5 * (h[1:] + h[:-1])
    diag = (ph[:-1] + ph[1:]) / hm + q[1:-1]
    off = -ph[1:-1] / np.sqrt(hm[:-1] * hm[1:])
    Bd = w[1:-1]
    # symmetric form: D^{-1/2} A D^{-1/2}, with A_ii = diag, A_i,i+1 = -ph / hm (made symmetric by the hm scaling)
    A_d = diag / Bd
    A_o = off / np.sqrt(Bd[:-1] * Bd[1:])
    ev = eigh_tridiagonal(A_d, A_o, select="i", select_range=(0, 4), eigvals_only=True)
    return ev, float(r[0]), float(r[-1])


PH4 = {"sympy_roots": [str(x) for x in roots_s], "zero_spacing_lnr": spacing, "threshold_ratio": thr}
ev, ra, rb = lowest_modes(ttab, g["TG"], 1e-3)
PH4["toy"] = dict(eigs=ev.tolist(), n_negative_of_first5=int(np.sum(ev < 0)), r_range=[ra, rb],
                  efold_time_toy_units=(1 / math.sqrt(-ev[0]) if ev[0] < 0 else None))
P(f"  PH4 toy (Plummer, r_* = 10): lowest 5 omega^2 = {[f'{v:+.3e}' for v in ev]}; negative: {int(np.sum(ev < 0))}; "
  f"e-folding time of the fastest mode = {PH4['toy']['efold_time_toy_units']} (toy units; collapse seen at t = 12-18)")
for foot in ("canonical", "alt"):
    for kz in ("simple", "mono"):
        a0 = g["A0"][foot]; md = g["ngc_model"](kz, a0)
        m_v, dm_v, law_v, dlaw_v = g["ngc_vec"](kz, a0, md)
        tab = g["hydro_tables"](m_v, dm_v, law_v, dlaw_v, G_SI, r0, md["r_e"])
        ev, ra, rb = lowest_modes(tab, G_SI, r0)
        ef = (1 / math.sqrt(-ev[0]) / g["GYR_S"]) if ev[0] < 0 else None
        PH4[f"NGC3198|{foot}|{kz}"] = dict(eigs=ev.tolist(), n_negative_of_first5=int(np.sum(ev < 0)), efold_Gyr=ef,
                                           r_range_kpc=[ra / KPC, rb / KPC])
        P(f"  PH4 NGC 3198 [{foot}, {kz}]: lowest 5 omega^2 (s^-2) = {[f'{v:+.3e}' for v in ev]}; negative: {int(np.sum(ev < 0))}; "
          f"fastest e-folding {ef if ef is None else round(ef, 3)} Gyr")
RES["PH4"] = PH4

# ---- PH3: collapse diagnostics (capped)
def variant(npt=10000, eps=0.02):
    h2 = head.replace("RSTAR, RCAT, NPT = 10.0, 30.0, 10000", f"RSTAR, RCAT, NPT = 10.0, 30.0, {npt}")
    h2 = h2.replace("T_RMIN, T_DTMAX, T_CA, T_EPS = 1e-3, 0.02, 0.03, 0.02", f"T_RMIN, T_DTMAX, T_CA, T_EPS = 1e-3, 0.02, 0.03, {eps}")
    gg = {"__file__": os.path.join(HERE, "cfg955.py"), "__name__": "cfg955_variant"}
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(h2, "cfg955_variant", "exec"), gg)
    return gg


def collapse_run(gg, mode, fac, rfloor, cap=200.0):
    S = gg["ShellSim"]("L", mode, fac)
    if rfloor > 0:
        base = gg["ShellSim"].relax

        def relax_floor(Dt, S=S, base=base):
            inner = S.r < rfloor
            v0 = S.v[inner].copy(); L0 = S.L[inner].copy()
            base(S, Dt)
            if inner.any():
                dK = 0.5 * gg["T_MU"] * float(np.sum(S.v[inner] ** 2 + S.L[inner] ** 2 / S.r[inner] ** 2 - v0 ** 2 - L0 ** 2 / S.r[inner] ** 2))
                S.a[inner] += (L0 ** 2 - S.L[inner] ** 2) / S.r[inner] ** 3
                S.v[inner] = v0; S.L[inner] = L0; S.E_R += dK
        S.relax = relax_floor
    t0 = time.time(); first = None; nextc = 0.0
    while S.t < 40.0 and time.time() - t0 < cap:
        dt = S.choose_dt()
        if S.t >= nextc:
            if first is None and float(np.mean(S.r < 0.05)) > 0.01:
                first = S.t
            nextc += 0.5
        S.step(dt)
    return dict(first_t_frac05_gt_1pct=first, t_reached=S.t, frac_lt_0p01=float(np.mean(S.r < 0.01)), frac_lt_0p05=float(np.mean(S.r < 0.05)),
                frac_lt_0p5=float(np.mean(S.r < 0.5)), law_frac_lt_0p5=float(gg["t_Mph"](0.5) / gg["T_MC"]), wall_s=time.time() - t0)


PH3 = {}
for name, (npt, eps, mode, fac, rfl) in {"frozen": (10000, 0.02, "KT", 1.0, 0.0), "N40000": (40000, 0.02, "KT", 1.0, 0.0),
                                         "eps0.1": (10000, 0.1, "KT", 1.0, 0.0), "fast_x0.1": (10000, 0.02, "KT", 0.1, 0.0),
                                         "floor0.24": (10000, 0.02, "KT", 1.0, 0.24), "relax_off": (10000, 0.02, "off", 1.0, 0.0)}.items():
    d = collapse_run(variant(npt, eps), mode, fac, rfl)
    PH3[name] = d
    P(f"  PH3 {name:10s}: first t with > 1% of shells inside r < 0.05: {d['first_t_frac05_gt_1pct']}; reached t {d['t_reached']:.2f} in "
      f"{d['wall_s']:.0f} s; frac(<0.01) {d['frac_lt_0p01']:.4f}, frac(<0.05) {d['frac_lt_0p05']:.4f}, frac(<0.5) {d['frac_lt_0p5']:.4f} "
      f"(law {d['law_frac_lt_0p5']:.4f})")
RES["PH3"] = PH3

# ---- PH5: energy books through the collapse onset
gg = variant(10000, 0.02)
S = gg["ShellSim"]("L", "KT", 1.0)
E0 = S.KE() + S.V_grav(); Eref = abs(S.KE()) + abs(S.V_grav())
marks = [5.0, 10.0, 12.0, 13.0, 13.5, 14.0]; PH5 = {}; t0 = time.time(); mi = 0
while mi < len(marks) and time.time() - t0 < 200.0:
    dt = min(S.choose_dt(), marks[mi] - S.t + 1e-12)
    S.step(dt)
    if S.t >= marks[mi] - 1e-9:
        E = S.KE() + S.V_grav() + S.E_R
        PH5[f"t={marks[mi]}"] = dict(eps_E=abs(E - E0) / Eref, E_R=S.E_R, frac_lt_0p05=float(np.mean(S.r < 0.05)),
                                      frac_lt_0p5=float(np.mean(S.r < 0.5)))
        mi += 1
P("  PH5 energy books through the onset (frozen K-T, IC-L): " + "; ".join(
    f"{k}: eps_E {v['eps_E']:.1e}, E_R {v['E_R']:+.2f}, frac(<0.05) {v['frac_lt_0p05']:.4f}, frac(<0.5) {v['frac_lt_0p5']:.4f}" for k, v in PH5.items()))
RES["PH5"] = PH5
json.dump(g["jsonable"](RES), open(os.path.join(HERE, "cfg955_posthoc.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg955_posthoc.out"), "w").write("\n".join(OUT) + "\n")
P(f"  runtime {time.time() - g['T0']:.0f} s")
