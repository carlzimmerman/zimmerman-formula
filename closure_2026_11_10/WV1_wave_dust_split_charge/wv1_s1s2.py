#!/usr/bin/env python3
"""WV1 numeric part 1: S1c (FRW health, both variants), S1d (static galaxy), S2 (nu_max from the record's Jeans line),
KA3 (QG1's machinery reproduced), MUTATE M2 (V2's frame given QG1's dust charge).

QG1's own script (toe_2026_11_10/QG1_quantum_health_of_A/qg1.py) is executed unmodified in a temporary directory (its
output files go there, not into QG1's folder) and its functions `backgrounds`, `mode`, `grade_row` are reused.

Run:  python3 wv1_s1s2.py  -> wv1_s1s2.out, wv1_s1s2.json   (exit 0 iff every known answer passes)
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, time, math, tempfile, io, contextlib
import mpmath as mp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
QG1 = os.path.join(ROOT, "toe_2026_11_10", "QG1_quantum_health_of_A", "qg1.py")
KD1 = os.path.join(ROOT, "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")
LINES, RES, KA_OK = [], {"known_answers": {}, "S1c": {}, "S1d": {}, "S2": {}, "M2": {}}, True


def P_(s=""):
    LINES.append(s); print(s, flush=True)


def ka(name, ok, msg):
    global KA_OK
    RES["known_answers"][name] = {"ok": bool(ok), "msg": msg}
    KA_OK = KA_OK and bool(ok)
    P_(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")


P_("WV1 numeric part 1 (S1c, S1d, S2). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.")
P_("")
# ------------------------------------------------------------------ run QG1 unmodified in a temp dir
os.environ.pop("QG1_MUTATE", None)
tmp = tempfile.mkdtemp(prefix="wv1_qg1_")
ns = {"__file__": os.path.join(tmp, "qg1.py"), "__name__": "qg1_reuse"}
buf = io.StringIO()
code = None
with contextlib.redirect_stdout(buf):
    try:
        exec(compile(open(QG1).read(), QG1, "exec"), ns)
    except SystemExit as e:
        code = e.code
P_(f"QG1 re-executed unmodified in a temp dir: exit {code}, {len(buf.getvalue().splitlines())} lines of its own output")
QRES = ns["RES"]
mpf = mp.mpf
qg1_committed = json.load(open(os.path.join(os.path.dirname(QG1), "qg1.json")))

P_("")
P_("=== KA3: QG1's rows reproduced through its own functions ===")
printed = {("FRW1100", "canonical"): 334, ("FRW1100", "alt"): 316, ("FRW1", "canonical"): 1.84e5, ("FRW1", "alt"): 1.74e5}
ok3 = code == 0
msgs = []
for (nm, fo), val in printed.items():
    got = float(mpf(QRES["rows"][nm][fo]["Lambda_s_L"]))
    com = float(mpf(qg1_committed["rows"][nm][fo]["Lambda_s_L"]))
    good = abs(got / val - 1) < 0.01 and abs(got / com - 1) < 1e-9
    ok3 = ok3 and good
    msgs.append(f"{nm}/{fo} Lambda_s L {got:.4g} (printed {val:.3g}, committed json {com:.6g})")
for nm in ("PM-2", "PM0", "PM2"):
    for fo in ("canonical", "alt"):
        lab = QRES["rows"][nm][fo]["label"]
        ok3 = ok3 and lab == "PASS"
        msgs.append(f"{nm}/{fo} {lab} (Lambda_s L {float(mpf(QRES['rows'][nm][fo]['Lambda_s_L'])):.3g})")
oth = {(nm, fo): float(mpf(QRES["reports"]["other_mu_reading"][nm][fo]["Lambda_s_L"])) for nm in ("FRW1100", "FRW1")
       for fo in ("canonical", "alt")}
ok3 = ok3 and all(v == 0 for v in oth.values())
msgs.append("other reading (mu_K = 0) FRW Lambda_s L: " + ", ".join(f"{k[0]}/{k[1]} {v:g}" for k, v in oth.items()))
ka("KA3_QG1_machinery", ok3, "; ".join(msgs))

backgrounds, mode, grade_row, KN = ns["backgrounds"], ns["mode"], ns["grade_row"], ns["KN"]
rho_nat, k_nat, MPC, HBAR, C_SI, EV = ns["rho_nat"], ns["k_nat"], ns["MPC"], ns["HBAR"], ns["C_SI"], ns["EV"]
G_SI = ns["G_SI"]

# ------------------------------------------------------------------ S2: nu_max from the record's Jeans line
P_("")
P_("=== S2: Psi's Jeans scale against the record's line (comoving 2 pi/k_J <= 0.42/h Mpc at z 3, 10, 100, 1089) ===")
kd1 = json.load(open(KD1))
G_MPC = 4.30091e-9          # Mpc (km/s)^2 / Msun
RHOC100 = 3 * 100.0 ** 2 / (8 * math.pi * G_MPC)   # Msun / Mpc^3 for H0 = 100 km/s/Mpc
MPC_M, KMS = 3.0857e22, 1e3
nu_max = {}
for fo in ("canonical", "alt"):
    s = kd1["footings"][fo]["setting"]
    h, od = s["h"], s["omega_d"]
    rho0 = od * RHOC100
    kline = 2 * math.pi * h / 0.42                   # comoving Mpc^-1
    rows = {}
    for zz in (3, 10, 100, 1089):
        a = 1 / (1 + zz)
        nmax = math.sqrt(16 * math.pi * G_MPC * rho0 * a) / kline ** 2      # Mpc km/s
        rows[zz] = nmax * 1e3                                                # kpc km/s
    nm_ = min(rows.values())
    nu_max[fo] = nm_
    nu_SI = nm_ * 3.0857e19 * 1e3            # m^2/s
    mc2 = float(HBAR) * float(C_SI) ** 2 / nu_SI / float(EV)
    # acoustic-peak scale: Jeans k at z 1089 for nu_max, against k = 0.3 /Mpc
    kJ1089 = (16 * math.pi * G_MPC * rho0 / 1090 / (nm_ / 1e3) ** 2) ** 0.25
    kJ0 = (16 * math.pi * G_MPC * rho0 / (nm_ / 1e3) ** 2) ** 0.25
    RES["S2"][fo] = {"h": h, "omega_d": od, "rho_Psi0_Msun_Mpc3": rho0, "k_line_Mpc^-1": kline,
                     "nu_max_by_z_kpc_kms": rows, "nu_max_kpc_kms": nm_, "m_c2_min_eV": mc2,
                     "kJ_com_at_z1089_for_nu_max": kJ1089, "kJ_com_today_for_nu_max": kJ0, "binding_z": min(rows, key=rows.get)}
    P_(f"[{fo}] h {h:.5f}, omega_d {od:.5f}, rho_Psi0 {rho0:.4e} Msun/Mpc^3; line k_J >= {kline:.3f}/Mpc comoving")
    P_("    nu_max by redshift (kpc km/s): " + ", ".join(f"z {zz}: {v:.4g}" for zz, v in rows.items()))
    P_(f"    nu_max = {nm_:.4g} kpc km/s (binding z = {min(rows, key=rows.get)}); m c^2 >= {mc2:.3e} eV; "
       f"k_J(comoving) at z 1089 = {kJ1089:.3g}/Mpc (acoustic peaks need dust at k <= 0.3/Mpc: "
       f"{'kept off' if kJ1089 > 0.3 else 'NOT kept off'}); k_J today = {kJ0:.3g}/Mpc")
P_("    V1: the P sector halves the growth rate at k_J (wv1_sym: rate^2/(4 pi G rho) = 1/2 there, off branch); "
   "V2: plain Psi, omega^2 = 0 at k_J. The same k_J is graded for both (criteria S2).")

# ------------------------------------------------------------------ S1c: FRW frame health
P_("")
P_("=== S1c: the frame scalar on QG1's FRW backgrounds ===")


def kgrid(bg, ntot=400):
    lo = mp.log10(bg["kIR"])
    hi = mp.log10(1 / ns["L_nat"](ns["FOOT"][bg["foot"]]["Lstar_pc"] * ns["PC"])) + 4
    return [mpf(10) ** (lo + (hi - lo) * i / (ntot - 1)) for i in range(ntot)]


def scan(bg, mu_of_k=None, G_override=None):
    """omega^2(k) on both branches; returns (all_zero, ghost, max_rate_over_jeans, rate_increasing_at_large_k)."""
    allzero, ghost, worst, incr = True, False, mpf(0), False
    grid = kgrid(bg)
    ktail = grid[-60]
    for br in ("on", "off"):
        prev = None
        for kk in grid:
            b2 = dict(bg)
            if mu_of_k is not None:
                b2["mu"] = mu_of_k(kk)
            q = mode(b2, kk, mpf(0), br, arm="", G_override=G_override)
            om2 = q["om2"]
            if om2 != 0:
                allzero = False
            if q["a"] <= 0:
                ghost = True
            Gc = q["G"]
            jeans = Gc * KN
            if jeans > 0 and om2 < 0:
                ratio = mp.sqrt(-om2 / jeans)
                worst = max(worst, ratio)
                if prev is not None and kk > ktail and ratio > prev * (1 + mpf("1e-12")):
                    incr = True
                prev = ratio
            else:
                prev = mpf(0) if om2 >= 0 else prev
    return allzero, ghost, worst, incr


S1c_label = {}
for fo in ("canonical", "alt"):
    bg_other = backgrounds(fo, "other")
    bg_grad = backgrounds(fo, "graded")
    for nm in ("FRW1100", "FRW1"):
        # V2: frame uncharged (QG1's other reading: mu_K = 0, G = 0)
        r2 = grade_row(nm, bg_other[nm], arm="", do_loop=False)
        az, gh, wr, inc = scan(bg_other[nm], G_override=mpf(0))
        failV2 = az or float(mpf(r2["Lambda_s_L"])) < 10
        RES["S1c"].setdefault("V2", {}).setdefault(fo, {})[nm] = {
            "G": 0, "omega2_identically_zero": az, "Lambda_s_L_QG1": r2["Lambda_s_L"], "set_by": r2["ii_dominant"],
            "label": "FAIL" if failV2 else "PASS"}
        P_(f"[V2 / {fo} / {nm}] frame charge G = 0: omega^2 = 0 at every k on both branches: {az}; QG1 grade_row: "
           f"Lambda_s L = {r2['Lambda_s_L']} ({r2['ii_dominant']}) -> {'FAIL' if failV2 else 'PASS'}")
        S1c_label[("V2", fo, nm)] = "FAIL" if failV2 else "PASS"
        # M2: V2's frame given QG1's dust charge (= QG1's graded row)
        rm = QRES["rows"][nm][fo]
        RES["M2"].setdefault(fo, {})[nm] = {"Lambda_s_L": rm["Lambda_s_L"], "label_ii": "PASS" if rm["ii"] else "FAIL",
                                            "i": rm["i"]}
        # V1: frame charge = rho_Psi; Psi's stiffness mu_eff^2 = k_J^4/k^2, at nu_max of this footing and the scan values
        for fac in (1, 4, 16, 64, 256, 1024, 4096):
            nu_kpc = nu_max["canonical"] * fac if fac != 1 else nu_max[fo]
            nu_SI = mpf(nu_kpc) * mpf("3.0857e19") * 1000
            m_eV = HBAR * C_SI ** 2 / nu_SI / EV                  # Psi's mass (natural units: nu = 1/m)
            bg1 = dict(bg_grad[nm])
            Gc = bg1["G"]                                           # = rho_bar of the cold component (natural units)
            kJ4 = 4 * KN * Gc * m_eV ** 2                           # 16 pi G rho/nu^2 with K = 4 pi G, nu = 1/m
            az1, gh1, wr1, inc1 = scan(bg1, mu_of_k=lambda kk: mp.sqrt(kJ4) / kk)
            fail1 = az1 or gh1 or wr1 > 1 + mpf("1e-9") or inc1
            RES["S1c"].setdefault("V1", {}).setdefault(fo, {}).setdefault(nm, {})[f"nu_x{fac}"] = {
                "nu_kpc_kms": float(nu_kpc), "m_eV": float(m_eV), "k_J_eV": float(kJ4 ** 0.25),
                "omega2_identically_zero": az1, "ghost": gh1, "max_rate_over_jeans": float(wr1),
                "rate_increasing_at_large_k": inc1, "label": "FAIL" if fail1 else "PASS"}
            if fac == 1:
                S1c_label[("V1", fo, nm)] = "FAIL" if fail1 else "PASS"
                P_(f"[V1 / {fo} / {nm}] nu = nu_max = {nu_kpc:.4g} kpc km/s (m c^2 {float(m_eV):.3e} eV): omega^2 = 0 "
                   f"everywhere: {az1}; ghost (a <= 0): {gh1}; max growth rate / sqrt(4 pi G rho) = {float(wr1):.12f}; "
                   f"rate rising at large k: {inc1} -> {'FAIL' if fail1 else 'PASS'}")
        bad = [k_ for k_, v in RES["S1c"]["V1"][fo][nm].items() if v["label"] != "PASS"]
        P_(f"    V1 at nu_max x {{1, 4, ..., 4096}}: {'all PASS' if not bad else 'FAIL at ' + ', '.join(bad)}")
    P_(f"[M2 / {fo}] V2's frame given QG1's dust charge (mu_K*, G = rho_c): FRW1100 Lambda_s L "
       f"{RES['M2'][fo]['FRW1100']['Lambda_s_L']}, FRW1 {RES['M2'][fo]['FRW1']['Lambda_s_L']} -> "
       f"{'PASS: the V2 FAIL flips (BITES)' if all(v['label_ii'] == 'PASS' and v['i'] for v in RES['M2'][fo].values()) else 'does not flip'}")

RES["M2"]["bites"] = all(RES["M2"][fo][nm]["label_ii"] == "PASS" and RES["M2"][fo][nm]["i"]
                         for fo in ("canonical", "alt") for nm in ("FRW1100", "FRW1")) and \
    all(S1c_label[("V2", fo, nm)] == "FAIL" for fo in ("canonical", "alt") for nm in ("FRW1100", "FRW1"))

# ------------------------------------------------------------------ S1d: static galaxy rows
P_("")
P_("=== S1d: static galaxy (QG1's point-mass rows; Psi absent; V1 with Psi stationary adds m f^2 >= 0 to G) ===")
for fo in ("canonical", "alt"):
    for nm in ("PM-2", "PM0", "PM2"):
        r = QRES["rows"][nm][fo]
        RES["S1d"].setdefault(fo, {})[nm] = {"label": r["label"], "Lambda_s_L": r["Lambda_s_L"]}
        P_(f"[{fo} / {nm}] QG1 label {r['label']} (Lambda_s L {r['Lambda_s_L']})")
S1d_ok = {fo: all(RES["S1d"][fo][nm]["label"] == "PASS" for nm in ("PM-2", "PM0", "PM2")) for fo in ("canonical", "alt")}

# ------------------------------------------------------------------ S1 per variant
P_("")
P_("=== S1 labels (S1c on both FRW rows and S1d on all PM rows) ===")
RES["S1"] = {}
for var in ("V1", "V2"):
    for fo in ("canonical", "alt"):
        ok = all(S1c_label[(var, fo, nm)] == "PASS" for nm in ("FRW1100", "FRW1")) and S1d_ok[fo]
        RES["S1"].setdefault(var, {})[fo] = "PASS" if ok else "FAIL"
        P_(f"S1 {var} {fo}: {'PASS' if ok else 'FAIL'}")
P_(f"MUTATE M2: {'BITES' if RES['M2']['bites'] else 'DOES NOT BITE'} (V2 FRW FAIL -> PASS once the frame carries QG1's dust)")

RES["known_answers_all_pass"] = KA_OK
RES["runtime_s"] = round(time.time() - T0, 1)
P_("")
P_(f"known answers {'all pass' if KA_OK else 'NOT all pass'}; runtime {RES['runtime_s']} s")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "wv1_s1s2.out"), "w").write("\n".join(LINES) + "\n")
json.dump(RES, open(os.path.join(HERE, "wv1_s1s2.json"), "w"), indent=1, default=str)
sys.exit(0 if KA_OK else 1)
