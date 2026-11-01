"""Tier B: Dw. Section 6. Set D."""
from crg1_core import *
from crg1_zoom import get_nr
CLASSES = ["MW ultra-faint", "bright M31", "M31 others", "MW classical", "LG field"]

def load(foot):
    arr = {}
    for r in csv.DictReader(open(os.path.join(INP, "dwarfs", "arroyo_polonio2026_tableA1.csv"))):
        try:
            v = float(r["sig_free"]) / float(r["sig_f0"])
        except ValueError:
            continue
        arr[r["lvd_name"]] = v
    med = float(np.median(list(arr.values())))
    rows = []
    for r in csv.DictReader(open(os.path.join(INP, "dwarfs", "x1_per_system_inputs.csv"))):
        if r["footing"] != foot: continue
        mv = r["M_V"].strip()
        pres = mv not in ("", "nan") and np.isfinite(float(mv))
        b = arr[r["name"]] if r["name"] in arr else (med if pres and float(mv) > -7.7 else 1.0)
        sc = float(r["sigma"]) * b; r12 = 4.0 / 3 * float(r["rh_pc"]) * D.pc; Ms = 10 ** float(r["logMstar"])
        rows.append(dict(name=r["name"], host=r["host"], cls=r["cls"], lgMs=float(r["logMstar"]), r12=r12,
                         gobs=3 * (sc * 1e3) ** 2 / r12, gN=D.G * (Ms / 2) * D.Msun / r12 ** 2, s=float(r["sdMC[Newton]"])))
    return rows

def boot(rows, Ev):
    rng = np.random.default_rng(20261026); out = {}; ok = True
    for c in CLASSES:
        ii = [i for i, r in enumerate(rows) if r["cls"] == c]; E_ = Ev[ii]; s = np.array([rows[i]["s"] for i in ii]); N = len(ii)
        ix = rng.integers(0, N, (10000, N)); z = rng.standard_normal((10000, N))
        sd = float(np.std(np.median(E_[ix] + s[ix] * z, axis=1)))
        md = float(np.median(E_)); Z = md / sd
        out[c] = dict(N=N, median=md, sd=sd, Z=Z); ok &= abs(Z) < 2
    return dict(classes=out, passed=bool(ok))

def Mcool(b):
    rc = rho_crit0(b.h, D.G, D.Mpc); rm0 = ((b.wb + b.wc) / b.h ** 2) * rc
    K = (3 / (4 * math.pi * 18 * math.pi ** 2 * rm0 * 9 ** 3)) ** (1.0 / 3)
    M = (1e4 * 2 * 1.380649e-23 * K / (0.59 * 1.67262192e-27 * D.G)) ** 1.5
    return M

def c3(rows, a0, flag):
    b = bg(BGS[0]); mc = Mcool(b); E_ = []
    for r in rows:
        M200 = max(10 ** float(b.lgM200(r["lgMs"])) * D.Msun, mc)
        halo = (r["host"] in ("MW", "M31")) if flag == "host" else (M200 / D.Msun > 10 ** 12.3)
        if halo:
            R2 = R200_of(M200, b.h, D.G, D.Mpc); S = a0 / (2 * math.pi * D.G); r0 = solve_r0(M200, R2, S, B_B)
            Mh = math.pi * S * r0 ** 2 * float(B_B(min(r["r12"], R2) / r0))
            gp = r["gN"] + D.G * Mh / r["r12"] ** 2
        else:
            gp = float(nu(np.array([r["gN"] / a0]))[0]) * r["gN"]
        E_.append(math.log10(r["gobs"] / gp))
    return boot(rows, np.array(E_))

def c4(rows, a0):
    E_ = [math.log10(r["gobs"] / (float(nu(np.array([r["gN"] / a0]))[0]) * r["gN"])) for r in rows]
    return boot(rows, np.array(E_))

def c1(rows, nr=None, unit=None):
    """Ceiling over M200. nr None: ND1's anchors (A14a); else NR2's table (A14b)."""
    b = bg(BGS[0]); LMG = np.arange(4, 14 + 1e-9, 0.02); n = len(LMG)
    unit = unit or E
    Sv, R2v, r0v = np.zeros(n), np.zeros(n), np.zeros(n)
    et = SC["ce1_a4_eta_med"]; r10, r11 = SC["x80"]["r10"], SC["x80"]["r11"]
    for i, lm in enumerate(LMG):
        Mt = 10 ** lm / f_c; lg = math.log10(Mt)
        if nr is None:
            S = f_c * float(np.interp(lg, [12, 13, 14], [et["12"], et["13"], et["14"]])) * 10 ** float(np.interp(lg, [10, 11, 12], [math.log10(r10), math.log10(r11), 0.0]))
        else:
            S = f_c * float(nr.eta(Mt)) * float(nr.lowfac(Mt))
        S *= float(b.sigcoll(max(Mt, 10 ** (7 + math.log10(2)))))
        S *= unit.Msun / unit.pc ** 2
        M200 = 10 ** lm * D.Msun; R2 = R200_of(M200, b.h, D.G, D.Mpc); Sv[i], R2v[i] = S, R2; r0v[i] = solve_r0(M200, R2, S, B_S)
    E_ = []
    for r in rows:
        C = float((math.pi * Sv * r0v ** 2 * B_S(np.minimum(r["r12"], R2v) / r0v)).max())
        E_.append(math.log10(r["gobs"] / (r["gN"] + D.G * C / r["r12"] ** 2)))
    return boot(rows, np.array(E_))

def main():
    if have_part("Dw"): return
    Rw = {f: load(f) for f in A0}
    out = {"C4": {f: c4(Rw[f], A0[f]) for f in A0}, "C3": {f: c3(Rw[f], A0[f], "host") for f in A0},
           "C3_A13b_mass_flag": {f: c3(Rw[f], A0[f], "mass") for f in A0},
           "C1": {"canonical": c1(Rw["canonical"])}, "C1_A14b_NR2": {"canonical": c1(Rw["canonical"], get_nr("a"))},
           "C1_NA2b_unit_set_D": {"canonical": c1(Rw["canonical"], None, D)}}
    save_part("Dw", out); log("Dw done")

if __name__ == "__main__": main()
