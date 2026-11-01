"""SPARC S, Tl and LITTLE THINGS LT for C1-C4. Sections 2 and 3.1."""
from crg1_core import *
from crg1_zoom import get_nr

UPS = np.round(np.arange(0.30, 1.2000001, 0.01), 2)
BINS = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]

def load_table():
    T = {}
    for l in open(os.path.join(INP, "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) != 19: continue
        try:
            T[t[0]] = dict(Inc=float(t[5]), L36=float(t[7]), MHI=float(t[13]), Vflat=float(t[15]), Q=float(t[17]))
        except ValueError:
            continue
    return T

def load_gal():
    T = load_table(); G = []
    for f in sorted(glob.glob(os.path.join(INP, "sparc", "rotmod", "*_rotmod.dat"))):
        name = os.path.basename(f).replace("_rotmod.dat", "")
        a = np.loadtxt(f, comments="#", ndmin=2)
        t = T[name]
        G.append(dict(name=name, Rk=a[:, 0], R=a[:, 0] * KPC, Vobs=a[:, 1].copy(), eV=a[:, 2], Vgas=a[:, 3], Vdisk=a[:, 4], Vbul=a[:, 5], **t,
                      lgMb=math.log10((0.5 * t["L36"] + 1.33 * t["MHI"]) * 1e9)))
    return G

def gB_mat(g):
    VB2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + UPS[:, None] * g["Vdisk"] ** 2 + 1.4 * UPS[:, None] * g["Vbul"] ** 2
    return VB2 * 1e6 / g["R"]

def fit(G, model):
    """model(g, gB) -> g_p of same shape (nUps, npt). Returns statistics and per-galaxy Ups."""
    wr2, ws, Yb = [], [], []
    skipped = 0
    for g in G:
        gb = gB_mat(g)
        gO = (g["Vobs"] * 1e3) ** 2 / g["R"]
        ok = (gb > 0) & (gO > 0) & np.isfinite(gb) & (g["Vobs"] > 0)
        W = 1 / (np.maximum(g["eV"], 1) / np.maximum(g["Vobs"], 1)) ** 2
        gp = model(g, gb)
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.where(ok, np.log10(np.where(gO > 0, gO, 1.0)) - np.log10(np.maximum(gp, 1e-300)), 0.0)
        a = (W[None, :] * r * r * ok).sum(1); b = (W[None, :] * ok).sum(1)
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.where(b > 0, a / b, np.inf)
        if not np.isfinite(q).any():
            skipped += 1; Yb.append(np.nan); wr2.append(0.0); ws.append(0.0); continue
        i = int(np.argmin(q)); wr2.append(a[i]); ws.append(b[i]); Yb.append(UPS[i])
    Yb = np.array(Yb)
    return dict(rms=math.sqrt(sum(wr2) / sum(ws)), Y_med=float(np.nanmedian(Yb)), Yb=Yb, skipped=skipped)

def tilt(G, Yb):
    q = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in G])
    V = np.array([g["Vflat"] for g in G])
    lo = q & (V > 0) & (V < 100); hi = q & (V > 150)
    out = dict(n_quality=int(q.sum()), n_lo=int(lo.sum()), n_hi=int(hi.sum()),
               Y_lo=float(np.nanmedian(Yb[lo])), Y_hi=float(np.nanmedian(Yb[hi])))
    out["tilt"] = out["Y_lo"] - out["Y_hi"]
    b = {}
    for a, c in BINS:
        s = q & (V >= a) & (V < c)
        b["[%d,%d)" % (a, c)] = dict(n=int(s.sum()), Y=float(np.nanmedian(Yb[s])) if s.any() else "nan")
    out["Y_by_Vflat"] = b
    return out

def m_law(a0):
    def f(g, gb): return law(gb, a0)
    return f

def halo_params(g, b, nr):
    lg = float(b.lgM200(g["lgMb"])); M200 = 10 ** lg * E.Msun
    R2 = R200_of(M200, b.h, E.G, E.Mpc)
    S = nr.S(10 ** lg / f_c, b)
    r0 = solve_r0(M200, R2, S, B_S)
    return M200, R2, S, r0

def m_c1(b, nr, capped):
    def f(g, gb):
        M200, R2, S, r0 = halo_params(g, b, nr)
        Rr = np.minimum(g["R"], R2) if capped else g["R"]
        return gb + E.G * math.pi * S * r0 ** 2 * B_S(Rr / r0) / g["R"] ** 2
    return f

def m_c2(b, nr):
    def f(g, gb):
        M200, R2, S, r0 = halo_params(g, b, nr)
        R = g["R"]; rg = np.geomspace(0.05 * R[0], R2, 300); lrg = np.log(rg)
        M0g = math.pi * S * r0 ** 2 * B_S(rg / r0)
        out = np.empty_like(gb)
        for k, Y in enumerate(UPS):
            Mk = np.maximum.accumulate(np.maximum(gb[k] * R ** 2 / E.G, 0))
            Mt = max(Mk[-1], (Y * g["L36"] + 1.33 * g["MHI"]) * 1e9 * E.Msun)
            Mb = np.empty_like(rg); a = rg < R[0]; c = rg > R[-1]; w = ~(a | c)
            Mb[a] = Mk[0] * (rg[a] / R[0]) ** 2
            Mb[w] = np.interp(np.log(rg[w]), np.log(R), Mk)
            t = np.clip(np.log(rg[c] / R[-1]) / math.log(3), 0, 1)
            Mb[c] = np.exp((1 - t) * math.log(max(Mk[-1], 1e-300)) + t * math.log(Mt))
            Mb = np.maximum.accumulate(Mb)
            Mf = contract(rg, Mb, M0g, Mt / M200)
            out[k] = gb[k] + E.G * np.interp(np.log(R), lrg, Mf) / R ** 2
        return out
    return f

def m_c3(b, a0, above_list=None):
    def f(g, gb):
        lg = float(b.lgM200(g["lgMb"])); M = 10 ** lg
        if M > 10 ** 12.3:
            M200 = M * E.Msun; R2 = R200_of(M200, b.h, E.G, E.Mpc)
            S = S_H(M, a0, eta_C3, b); r0 = solve_r0(M200, R2, S, B_B)
            return gb + E.G * math.pi * S * r0 ** 2 * B_B(g["R"] / r0) / g["R"] ** 2
        return law(gb, a0)
    return f

def stat(G, model):
    r = fit(G, model); t = tilt(G, r["Yb"])
    return r, t

def line_S(cells):
    return all(c["rms"] <= 0.110 and 0.50 <= c["Y_med"] <= 0.80 for c in cells)
def line_T(cells): return all(abs(c["tilt"]) <= 0.15 for c in cells)
def line_LT(cells): return all(abs(c) <= 0.10 for c in cells)

# ---------- LITTLE THINGS
def load_lt():
    rows = []
    for r in csv.DictReader(open(os.path.join(INP, "little_things", "oh2015_table2.csv"))):
        if all(r[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun")):
            Mb = (float(r["Mgas_1e7Msun"]) + float(r["MSED_1e7Msun"])) * 1e7
            rows.append(dict(name=r["name"], R=float(r["Rmax_kpc"]) * 3.0857e22 / 1e3 if not ONESET else float(r["Rmax_kpc"]) * E.Mpc / 1e3,
                             V=float(r["V_kms"]) * 1e3, Mb=Mb, lg=math.log10(Mb)))
    return rows

def lt_law(rows, a0):
    E_ = [math.log10(x["V"] ** 2 / x["R"]) - math.log10(float(law(np.array([E.G * x["Mb"] * E.Msun / x["R"] ** 2]), a0)[0])) for x in rows]
    return float(np.median(E_))

def lt_halo(rows, b, nr, resp):
    out = []
    for x in rows:
        lg = float(b.lgM200(x["lg"])); M200 = 10 ** lg * E.Msun; R2 = R200_of(M200, b.h, E.G, E.Mpc)
        S = nr.S(10 ** lg / f_c, b); r0 = solve_r0(M200, R2, S, B_S); R = x["R"]
        rg = np.geomspace(1e-3 * R, R2, 600); M0g = math.pi * S * r0 ** 2 * B_S(rg / r0); Mbk = x["Mb"] * E.Msun
        if resp:
            Mbg = Mbk * np.minimum(rg / R, 1) ** 2
            prof = contract(rg, Mbg, M0g, Mbk / M200)
        else:
            prof = M0g
        Mc = float(np.interp(math.log(R), np.log(rg), prof))
        out.append(math.log10(x["V"] ** 2 / R) - math.log10(E.G * Mbk / R ** 2 + E.G * Mc / R ** 2))
    return float(np.median(out))

def lt_c3b(rows, b, a0):
    out = []
    for x in rows:
        lg = float(b.lgM200(x["lg"])); M = 10 ** lg; R = x["R"]; gN = E.G * x["Mb"] * E.Msun / R ** 2
        if M > 10 ** 12.3:
            M200 = M * E.Msun; R2 = R200_of(M200, b.h, E.G, E.Mpc); S = S_H(M, a0, eta_C3, b); r0 = solve_r0(M200, R2, S, B_B)
            gm = gN + E.G * math.pi * S * r0 ** 2 * float(B_B(R / r0)) / R ** 2
        else:
            gm = float(law(np.array([gN]), a0)[0])
        out.append(math.log10(x["V"] ** 2 / R) - math.log10(gm))
    return float(np.median(out))

def n_sat(G, b, fn):
    """Galaxies whose solve_r0 saturates, counted once per galaxy."""
    c0 = COUNT["saturated"]
    for g in G: fn(g)
    return COUNT["saturated"] - c0

def strip(r):
    return {k: v for k, v in r.items() if k != "Yb"}

def main():
    G = load_gal(); LT = load_lt(); assert len(G) == 175
    NRa, NRb = get_nr("a"), get_nr("b")
    res = {}
    def put(name, val):
        res[name] = val
    # C4 / C3 law values first
    for foot in ("canonical", "alt"):
        if have_part("sparc_C4_" + foot): continue
        a0 = A0[foot]
        r, t = stat(G, m_law(a0)); lt = lt_law(LT, a0)
        rows = {bg_: dict(S=strip(r), Tl=t, LT=lt, tags=["[recomputed]", "same on both backgrounds: no background enters"]) for bg_ in BGS}
        passes = dict(S=line_S([r, r]), Tl=line_T([t, t]), LT=line_LT([lt, lt]))
        save_part("sparc_C4_" + foot, dict(rows=rows, passes=passes)); log("C4 %s done" % foot)
    # C1
    if not have_part("sparc_C1_canonical"):
        rows = {}; sc, tc, ltc = [], [], []; diffs = []
        for tag in BGS:
            b = bg(tag)
            r1 = fit(G, m_c1(b, NRa, False)); r2 = fit(G, m_c1(b, NRa, True))
            t2 = tilt(G, r2["Yb"]); t1 = tilt(G, r1["Yb"]); lt = lt_halo(LT, b, NRa, False)
            rb = fit(G, m_c1(b, NRb, False)); tb = tilt(G, fit(G, m_c1(b, NRb, True))["Yb"]); ltb = lt_halo(LT, b, NRb, False)
            rows[tag] = dict(S=strip(r1), Tl=t2, LT=lt, reading="A1a,A4a",
                             A4b_S_with_capped_form=strip(r2), A4b_tilt_with_uncapped_form=t1,
                             A4_max_abs_diff_Yb=float(np.nanmax(np.abs(r1["Yb"] - r2["Yb"]))),
                             A1b=dict(eta12=NRb.eta12, rho10=NRb.rho10, rho11=NRb.rho11, cf12=NRb.cf[0], S=strip(rb), Tl=tb, LT=ltb),
                             n_saturated_r0=n_sat(G, b, lambda g: halo_params(g, b, NRa)), A1a_values=dict(eta12=NRa.eta12, rho10=NRa.rho10, rho11=NRa.rho11, cf12=NRa.cf[0]), tags=["[recomputed]", "[INPUT AS GIVEN: em1 map, cf(1e13), cf(1e14)]"])
            sc.append(r1); tc.append(t2); ltc.append(lt)
            log("C1 %s done" % tag)
        save_part("sparc_C1_canonical", dict(rows=rows, passes=dict(S=line_S(sc), Tl=line_T(tc), LT=line_LT(ltc))))
    # C2
    if not have_part("sparc_C2_canonical"):
        rows = {}; sc, tc, ltc = [], [], []
        for tag in BGS:
            b = bg(tag)
            r, t = stat(G, m_c2(b, NRa)); lt = lt_halo(LT, b, NRa, True)
            rb, tb = stat(G, m_c2(b, NRb)); ltb = lt_halo(LT, b, NRb, True)
            rows[tag] = dict(S=strip(r), Tl=t, LT=lt, reading="A1a", A1b=dict(S=strip(rb), Tl=tb, LT=ltb), tags=["[recomputed]", "[INPUT AS GIVEN: em1 map, cf(1e13), cf(1e14)]"])
            sc.append(r); tc.append(t); ltc.append(lt); log("C2 %s done" % tag)
        save_part("sparc_C2_canonical", dict(rows=rows, passes=dict(S=line_S(sc), Tl=line_T(tc), LT=line_LT(ltc))))
    # C3
    for foot in ("canonical", "alt"):
        if have_part("sparc_C3_" + foot): continue
        a0 = A0[foot]; rows = {}; sc, tb_, ltb_ = [], [], []
        law_r, law_t = stat(G, m_law(a0)); law_lt = lt_law(LT, a0)
        for tag in BGS:
            b = bg(tag)
            r = fit(G, m_c3(b, a0)); tA3b = tilt(G, r["Yb"]); ltA3b = lt_c3b(LT, b, a0)
            nab = sum(1 for g in G if float(b.lgM200(g["lgMb"])) > 12.3)
            rows[tag] = dict(S=strip(r), Tl=law_t, LT=law_lt, reading="A3a: Tl, LT are the law's values on all systems (FG1's stated approximation)",
                             share_SPARC_above_T=nab / 175.0, n_above_T=nab, A3b_basin_consistent=dict(Tl=tA3b, LT=ltA3b),
                             tags=["[recomputed]", "[INPUT AS GIVEN: em1 map, x48 A2 cf]", "C3 floor is a disclosed departure"])
            sc.append(r); log("C3 %s %s done" % (foot, tag))
        save_part("sparc_C3_" + foot, dict(rows=rows, passes=dict(S=line_S(sc), Tl=line_T([law_t, law_t]), LT=line_LT([law_lt, law_lt]))))

if __name__ == "__main__":
    main()
