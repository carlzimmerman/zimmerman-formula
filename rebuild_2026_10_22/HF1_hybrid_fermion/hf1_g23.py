#!/usr/bin/env python3
"""HF1 gates 2 and 3. Modes: select | run M WF WB | mutate M WF WB.  Writes hf1_g23_<mode>.json/.out. CRG1's graders read-only. A1 R3-R6. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import csv, json, math, os, sys
os.environ.setdefault("OMP_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
import hf1_crgload as HL; HL.crg()
import numpy as np
import crg1_core as CO, crg1_clusters as C, crg1_sparc as SP, crg1_groups as GR, crg1_dwarfs as DW, crg1_efe as EFE
import hf1_fermion as FM
np.seterr(all="ignore")
A0 = CO.A0; MSUN = CO.F.Msun; MPC = CO.F.Mpc; GF = CO.F.G; FEET = ("canonical", "alt")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
RTA = lambda Mt, z=0.0: C.rta_com(Mt) / (1 + z)

# ---------------- clusters
def grid_for(rta, n=420, rmin=1e-3 * MPC):
    return np.geomspace(rmin, max(rta, 1.01 * rmin) * 1.0001, n)
def cluster_fermion(RMg, Mb, Mbt, rta, R500p, Rf, m, a0, gf=2.0, capf=1.0):
    r = grid_for(rta); M = np.interp(np.log(r), np.log(RMg), Mb); s = FM.solve(r, M, rta, R500p * MPC, Rf * Mbt, m, a0, gf=gf, capf=capf)
    Mf = np.exp(np.interp(np.log(RMg), np.log(r), np.log(np.maximum(s["Mf"], 1e-300)))); Mf[RMg > rta] = s["Mf"][-1]; Mf[RMg < r[0]] = s["Mf"][0] * (RMg[RMg < r[0]] / r[0]) ** 3
    return Mf, s
def build_keys(D, CSS, h, Rf, m, fs, gd, foot, gf=2.0, capf=1.0, info=None):
    a0 = A0[foot]; N = D.N; V = np.zeros((N, C.N_BIN)); vC = np.zeros((N, C.N_BIN)); g_ = D.geo[h]; gas = 10 ** gd; CS = CSS["own_" + foot]; nf = 0; RG = C.RG; RM = C.RM
    for i in range(N):
        z = D.z[i]; q = g_["q"][i]; c = C.ctx_of(D, h, i); Mg = D.Mgas[i] * q ** 2.5 * gas; Rp = D.R500[i] * q
        Mbx, Mb, Mbt, rta = C.chain(Mg, Rp, fs, z, MSUN); Mf, s = cluster_fermion(RM, Mb, Mbt, rta, Rp, Rf, m, a0, gf, capf); nf += 0 if s["conv"] else 1
        Mt = Mb + Mf; Msrc = Mt.copy(); pos = Mt > 0; Msrc[pos] = Mt[pos] * CO.nu(GF * Mt[pos] / RM[pos] ** 2 / a0)
        V[i] = C.vec(Msrc, c); vC[i] = C.vec(C.m_cstar(Mb, a0, CS), c)
        if info is not None and h == 0.672: info.append(dict(sig=float(s["sigma"]), cap=float(s["cap"]), Mf500=float(np.interp(Rp * MPC, RM, Mf) / MSUN), Mb500=float(np.interp(Rp * MPC, RM, Mb) / MSUN), Mf1=float(np.interp(MPC, RM, Mf) / MSUN), Mfta=float(Mf[-1] / MSUN), Mbt=float(Mbt / MSUN), rta=float(rta / MPC)))
    return V, vC, nf
def keys_all(D, CSS, Rf, m, fs, gd, foot, tag, gf=2.0, capf=1.0, info=None):
    res = {}; cells = {}
    for h, _, _, hn in C.HS:
        p = os.path.join(CO.CACHE, f"hf1_{tag}_{foot}_f{fs}_g{gd}_h{h}_gf{gf}_cf{capf}.npz")
        if os.path.exists(p) and info is None: z = np.load(p); V, vC, nf = z["V"], z["vC"], int(z["nf"])
        else:
            V, vC, nf = build_keys(D, CSS, h, Rf, m, fs, gd, foot, gf, capf, info); np.savez(p, V=V, vC=vC, nf=nf)
        cells[h] = (V, vC, nf)
    return cells
def k_table(D, cells, foot, B1=False, fac=None):
    tabs = {}
    for h, _, _, hn in C.HS:
        V, vC, _ = cells[h]; M = C.Meas(D, h)
        if B1:
            b = M.g["Bst"][None, :]
            for a in ("n", "nraw", "nx", "nRR"): setattr(M, a, getattr(M, a) / b)
        if fac is not None:
            f = fac(hn)
            for a in ("n", "nraw", "nx", "nRR"): setattr(M, a, getattr(M, a) * f)
        tabs[hn] = C.keys_table(M, V, vC, foot, "template")
    s = C.k_summary(tabs); w = max(((abs(v["Z"]), k, hn, v["Z"]) for hn, t in tabs.items() for k, v in t.items()))
    return dict(n_pass=s["n_pass"], failing=s["failing"], worst=[w[1], w[2], w[3]], Z={hn: {k: v["Z"] for k, v in t.items()} for hn, t in tabs.items()}, A={hn: {k: v["A"] for k, v in t.items()} for hn, t in tabs.items()}, pred={hn: {k: v["pred"] for k, v in t.items()} for hn, t in tabs.items()})
def keyline(lab, T):
    z = T["Z"]["h0672"]; P(f"  {lab}: {T['n_pass']} of 15, over 2 in either h: {', '.join(T['failing']) or 'none'}; worst {T['worst'][0]} ({T['worst'][1]}) {T['worst'][2]:+.2f}; G-OUT-all {z['G-OUT-all']:+.2f}, G-OUT-Mall {z['G-OUT-Mall']:+.2f}, G-OUT-M3 {z['G-OUT-M3']:+.2f}, G-MID-T3 {z['G-MID-T3']:+.2f}, G-IN-Mall {z['G-IN-Mall']:+.2f}")

# ---------------- X-COP
def xcop_rows(XC, Rf, m, foot, fs=0.034, gf=2.0, capf=1.0, law_only=False):
    a0 = A0[foot]; RM = C.RM; rows = []; E = CO.E; info = {}
    for j, c in enumerate(XC):
        Mg = C.li(c["gr"], c["gm"], c["R500"]); Rp = c["R500"] / 1e3
        Mbx, Mb, Mbt, rta = C.chain(Mg, Rp, fs, c["z"], E.Msun, seed=3 * 1.2 * Mg * E.Msun)
        if law_only: Mf = np.zeros_like(Mb); s = dict(sigma=0.0, cap=0.0, conv=True)
        else: Mf, s = cluster_fermion(RM, Mb, Mbt, rta, Rp, Rf, m, a0, gf, capf)
        info[c["name"]] = dict(sigma_kms=float(s["sigma"]) / 1e3, cap=float(s["cap"]), conv=bool(s["conv"]), rta_Mpc=float(rta / MPC), Mf_rta=float(Mf[-1] / E.Msun), Mb_rta=float(Mbt / E.Msun))
        for x in C.XS:
            r = x * c["R500"]; mh, mg, ms = C.li(c["hr"], c["hm"], r), C.li(c["gr"], c["gm"], r), C.li(c["sr"], c["sm"], r)
            if not all(map(np.isfinite, (mh, mg, ms))): continue
            rm = r * 1e3 * E.pc; mf = float(np.interp(rm, RM, Mf)) / E.Msun; Mt = mg + ms + mf; gN = E.G * Mt * E.Msun / rm ** 2; g = float(FM.lawg(gN, a0)); Mm = g * rm ** 2 / E.G / E.Msun
            rows.append(dict(cluster=c["name"], j=j, x=x, d=math.log10(mh / Mm), mf=mf, mb=mg + ms, mh=mh))
    def st(rs): d = np.array([q["d"] for q in rs]); return dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d), passed=bool(abs(d.mean()) <= 0.05 and np.sqrt((d ** 2).mean()) <= 0.10))
    out = dict(all=st(rows), train=st([q for q in rows if q["j"] % 2 == 0]), holdout=st([q for q in rows if q["j"] % 2 == 1]), by_x={str(x): float(np.mean([q["d"] for q in rows if q["x"] == x])) for x in C.XS}, per_cluster={c["name"]: float(np.mean([q["d"] for q in rows if q["cluster"] == c["name"]])) for c in XC}, info=info, mf_over_mb_by_x={str(x): float(np.median([q["mf"] / q["mb"] for q in rows if q["x"] == x])) for x in C.XS})
    return out

# ---------------- discs
def gal_grid(g):
    return np.geomspace(0.05 * g["R"][0], 2e24, 200)
def gal_masses(g, gb, Mt_row, rg):
    """gb (nU, npt) -> Mb on rg, as CRG1's m_c2: r^2 inside, to Mt over 3 R_last outside."""
    R = g["R"]; Mk = np.maximum.accumulate(np.maximum(gb * R ** 2 / GF, 0), axis=-1); out = np.zeros((gb.shape[0], rg.size)); lr = np.log(R); lg = np.log(rg)
    for k in range(gb.shape[0]):
        Mm = max(Mk[k, -1], Mt_row[k]); a = rg < R[0]; c = rg > R[-1]; w = ~(a | c)
        out[k, a] = Mk[k, 0] * (rg[a] / R[0]) ** 2; out[k, w] = np.interp(lg[w], lr, Mk[k]); t = np.clip(np.log(rg[c] / R[-1]) / math.log(3), 0, 1)
        out[k, c] = np.exp((1 - t) * math.log(max(Mk[k, -1], 1e-300)) + t * math.log(max(Mm, 1e-300)))
    return np.maximum.accumulate(out, axis=-1)
def gal_model(g, gb, Y, Rf, m, a0, gf=2.0, capf=1.0, Rsig=None, info=None):
    rg = gal_grid(g); Mt = (Y * g["L36"] + 1.33 * g["MHI"]) * 1e9 * MSUN; Mb = gal_masses(g, gb, Mt, rg); Mtot = np.maximum(Mb[:, -1], Mt); rta = np.array([RTA(x) for x in Mtot])
    s = FM.solve(rg, Mb, rta, g["R"][-1], Rf * Mtot, m, a0, gf=gf, capf=capf, iters=120)
    if Rsig == "obs" and g["Vflat"] > 0:
        s = FM.solve(rg, Mb, rta, g["R"][-1], Rf * Mtot, m, a0, gf=gf, capf=capf * ((g["Vflat"] * 1e3 / math.sqrt(2)) / s["sigma"])[:, None] ** 3, iters=120)
    i0 = np.searchsorted(np.log(rg), np.log(g["R"])) ; i0 = np.clip(i0, 1, rg.size - 1); dl = math.log(rg[1] / rg[0]); t = (np.log(g["R"]) - np.log(rg[i0 - 1])) / dl
    Mfr = s["Mf"][:, i0 - 1] * (1 - t) + s["Mf"][:, i0] * t
    if info is not None: info.append(dict(name=g["name"], conv=s["conv"], sig=np.asarray(s["sigma"]).tolist()[:1]))
    return FM.lawg(gb + GF * Mfr / g["R"] ** 2, a0), Mfr
def sparc_fit(G, Rf, m, a0, gf=2.0, capf=1.0, Rsig=None):
    frac = []
    def mod(g, gb):
        gp, Mfr = gal_model(g, gb, SP.UPS, Rf, m, a0, gf, capf, Rsig=Rsig); frac.append(dict(name=g["name"], ratio=float(np.median(Mfr[:, -1] / np.maximum(gb[:, -1] * g["R"][-1] ** 2 / GF, 1e-300))))); return gp
    r = SP.fit(G, mod); t = SP.tilt(G, r["Yb"]); return r, t, frac
def hs_slope(G, Rf, m, a0, gf=2.0, capf=1.0, law_only=False):
    """RQ3's hs_row statistic: mismatch at 2 R_d vs surface brightness at 60 <= V_flat < 120, Upsilon 0.5, 0.7."""
    Tb = {}
    for l in open(os.path.join(CO.INP, "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) == 19:
            try: Tb[t[0]] = (float(t[10]), float(t[11]))
            except ValueError: pass
    X, Y_ = [], []
    for g in G:
        if not (g["Q"] <= 2 and g["Inc"] >= 30 and 60 <= g["Vflat"] < 120) or g["name"] not in Tb or Tb[g["name"]][0] <= 0: continue
        VB2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + .5 * g["Vdisk"] ** 2 + .7 * g["Vbul"] ** 2; gb = VB2 * 1e6 / g["R"]; ok = (gb > 0) & (g["Vobs"] > 0); Rk = g["Rk"]; R2 = 2 * Tb[g["name"]][1]
        if ok.sum() < 2 or R2 < Rk[ok].min() or R2 > Rk[ok].max(): continue
        gu = np.where(ok, gb, 1e-30)
        if law_only: mm = FM.lawg(gu, a0)
        else: mm = gal_model(g, gu[None, :], np.array([0.5]), Rf, m, a0, gf, capf)[0][0]
        Vm = np.sqrt(np.maximum(mm * g["R"], 0)) / 1e3; Y_.append(float(np.interp(math.log(R2), np.log(Rk[ok]), Vm[ok] / g["Vobs"][ok] - 1))); X.append(math.log10(Tb[g["name"]][0]))
    X, Y_ = np.array(X), np.array(Y_); sl = lambda x, y: float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()); rg = np.random.default_rng(1); b = np.array([sl(X[k], Y_[k]) for k in rg.integers(0, len(X), (10000, len(X)))]); s = float((np.nanpercentile(b, 84) - np.nanpercentile(b, 16)) / 2); v = sl(X, Y_)
    return dict(slope=v, sigma=s, Z=v / s, n=len(X), passed=bool(abs(v / s) <= 2))
def bf1_train(G_all, Rf, m, a0, gf=2.0, capf=1.0, part=1):
    """BF1's SPARC statistic, odd names (part 1) or even (part 0), points unweighted, Upsilon 0.5, 0.7. Also the law's."""
    names = sorted(g["name"] for g in G_all); dat = {g["name"]: g for g in G_all}; L, F = [], []
    for i, n in enumerate(names):
        g = dat[n]
        if i % 2 != part or g["Q"] >= 3 or g["Inc"] < 30: continue
        VB2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + .5 * g["Vdisk"] ** 2 + .7 * g["Vbul"] ** 2; gb = VB2 * 1e6 / g["R"]; ok = (gb > 0) & (g["Vobs"] > 0) & (g["Rk"] > 0)
        if not ok.any(): continue
        gO = (g["Vobs"] * 1e3) ** 2 / g["R"]; L += list(np.log10(gO[ok] / FM.lawg(gb[ok], a0)))
        mm = gal_model(g, np.where(ok, gb, 1e-30)[None, :], np.array([0.5]), Rf, m, a0, gf, capf)[0][0]; F += list(np.log10(gO[ok] / mm[ok]))
    L, F = np.array(L), np.array(F); rl, rf = float(np.sqrt((L ** 2).mean())), float(np.sqrt((F ** 2).mean())); return dict(rms=rf, median=float(np.median(F)), rms_law=rl, median_law=float(np.median(L)), n=len(F), passed=bool(rf <= 1.05 * rl and abs(np.median(F)) <= 0.03))
# ---------------- LITTLE THINGS, groups, dwarfs
def lt_row(x, Rf, m, a0, gf=2.0, capf=1.0):
    Mb = x["Mb"] * CO.E.Msun; R = x["R"]; rta = RTA(Mb); r = np.geomspace(1e-3 * R, max(rta, 2 * R), 300); Mg = Mb * np.minimum(r / R, 1) ** 2; s = FM.solve(r, Mg, rta, R, Rf * Mb, m, a0, gf=gf, capf=capf); mf = float(np.interp(math.log(R), np.log(r), s["Mf"])); gN = CO.E.G * (Mb + mf) / R ** 2
    return math.log10(x["V"] ** 2 / R) - math.log10(float(FM.lawg(np.array(gN), a0))), mf / Mb
def groups_stat(rows, Rf, m, a0, gf=2.0, capf=1.0):
    P_ = GR.P; XG = GR.XG; LX = GR.LX; RH = GR.RHO_H; MH = GR.M_H
    def ls(lM, Re, dl):
        a = Re * (P_.pc * 1e3) / 1.8153; Mb = 10 ** (lM + dl) * P_.Msun; rr = XG * a; rta = RTA(Mb); r = np.geomspace(1e-3 * a, max(rta, 4 * a), 300); Mg = Mb * np.interp(np.log(r), LX + math.log(a), MH); s = FM.solve(r, Mg, rta, 3 * a, Rf * Mb, m, a0, gf=gf, capf=capf)
        mf = np.interp(np.log(rr), np.log(r), s["Mf"], left=0.0); U = P_.G * Mb / a ** 2; gt = FM.lawg((Mb * MH + mf) * P_.G / rr ** 2, a0) / U
        return .5 * math.log10(np.trapz(4 * math.pi * XG ** 2 * RH * XG * gt * XG, LX) / 3 * P_.G * Mb / a) - 3
    d = np.array([x[0] - ls(x[1], x[2], 0.0) for x in rows]); sl = np.array([(ls(x[1], x[2], .01) - ls(x[1], x[2], -.01)) / .02 for x in rows]); mean = d.mean(); se = d.std(ddof=1) / math.sqrt(len(d)); sy = .10 * sl.mean(); tot = math.hypot(se, sy); Z = mean / tot
    return dict(n=len(d), mean=float(mean), se=float(se), sys=float(sy), tot=float(tot), Z=float(Z), cls="NOT DIAGNOSTIC" if tot > 0.045 else ("CONSISTENT" if abs(Z) < 2 else ("ABOVE LAW" if Z >= 2 else "BELOW LAW")))
def dwarf_E(rows, Rf, m, a0, gf=2.0, capf=1.0):
    Ev = []
    for q in rows:
        Ms = 10 ** q["lgMs"] * CO.D.Msun; r12 = q["r12"]; rta = RTA(Ms); r = np.geomspace(1e-3 * r12, max(rta, 3 * r12), 200); Mg = np.minimum(Ms / 2 * (r / r12) ** 2, Ms); s = FM.solve(r, Mg, rta, r12, Rf * Ms, m, a0, gf=gf, capf=capf); mf = float(np.interp(math.log(r12), np.log(r), s["Mf"]))
        Ev.append(math.log10(q["gobs"] / float(FM.lawg(np.array(q["gN"] + CO.D.G * mf / r12 ** 2), a0))))
    return DW.boot(rows, np.array(Ev))

# ---------------- merger rows, published aperture masses
def lens_rows(Rf, m, foot):
    rows = list(csv.DictReader(open(os.path.join(RB, "MG1_merger_sample", "mg1_table.csv")))); a0 = A0[foot]; res = []; KPC = 3.0857e19
    AP = {("Bullet", "main"): 300, ("Bullet", "sub"): 300, ("MACS J0025", "SE"): 300, ("MACS J0025", "NW"): 300, ("A2744", "Core"): 250}
    for w in rows:
        k = (w["system"], w["sub"])
        if k not in AP: continue
        Rap = AP[k] * KPC; ML = float(w["M_lens"]); Mgas = float(w["M_gas"] or 0) if w["M_gas"] not in ("", "DEFAULT") else .12 * ML; Mst = float(w["M_star"]) if w["M_star"] not in ("", "DEFAULT") else .02 * ML; ag = float(w["a_gas"] or 300) * KPC; ast = float(w["a_star"] or 200) * KPC
        Mbt = (Mgas + Mst) * MSUN; rta = RTA(Mbt); r = np.geomspace(1 * KPC, rta, 400); hern = lambda M, a: M * (r / (r + a)) ** 2; Mb0 = hern(Mst * MSUN, ast) + hern(Mgas * MSUN, ag); s = FM.solve(r, Mb0, rta, Rap, Rf * Mbt, m, a0); out = {}
        def projected(M3):
            rho = np.gradient(M3, r) / (4 * math.pi * r ** 2); RR = np.geomspace(2 * KPC, Rap, 80); Sg = np.array([2 * np.trapz(np.interp(np.sqrt(RR_ ** 2 + zz ** 2), r, rho, right=0.0), zz) for RR_ in RR for zz in [np.geomspace(1e-3 * KPC, rta, 600)]]); return float(2 * math.pi * np.trapz(Sg * RR ** 2, np.log(RR)) / MSUN)
        Mcol = hern(Mst * MSUN, ast) + s["Mf"]; Eff = Mcol * CO.nu(GF * Mcol / r ** 2 / a0)
        Mall = Mb0 + s["Mf"]; Eff2 = Mall * CO.nu(GF * Mall / r ** 2 / a0)
        res.append(dict(system=w["system"], sub=w["sub"], R_kpc=AP[k], M_lens=ML, M_gas=Mgas, M_star=Mst, sigma_kms=float(s["sigma"]) / 1e3, M_proj_gasdisplaced=projected(Eff), M_proj_gascentred=projected(Eff2), ratio_low=projected(Eff) / ML, ratio_high=projected(Eff2) / ML, Mf_proj=projected(s["Mf"]), note="PROVISIONAL inputs from MG1; spherical; gas displaced counts no gas at the peak"))
    return res

def load_common():
    D = C.Data(); CSS = {"own_canonical": EFE.get("canonical", "own"), "own_alt": EFE.get("alt", "own")}; XC = C.xcop_load(); G = SP.load_gal(); LT = SP.load_lt(); return D, CSS, XC, G, LT

def controls(D, CSS, XC, G, LT):
    ck = {}
    # TG known answer: cap at the test profile's rho0 returns the closed form
    sig, r0 = 1e6, 250 * 3.0857e19; rho0 = 9 * sig ** 2 / (4 * math.pi * FM.G * r0 ** 2); mm = FM.tg_mmin(sig, r0); ck["K_TG"] = dict(m_min_eV=mm, cap_over_rho0=FM.rho_cap(mm, sig) / rho0, passed=abs(FM.rho_cap(mm, sig) / rho0 - 1) < 1e-10)
    # cap never exceeded, fair share holds, on a test cluster; convergence with grid
    c = XC[0]; Mg = C.li(c["gr"], c["gm"], c["R500"]); Rp = c["R500"] / 1e3; Mbx, Mb, Mbt, rta = C.chain(Mg, Rp, 0.034, c["z"], CO.E.Msun, seed=3 * 1.2 * Mg * CO.E.Msun)
    Ms = {}
    for n in (420, 840):
        r = np.geomspace(1e-3 * MPC, rta * 1.0001, n); s = FM.solve(r, np.interp(np.log(r), np.log(C.RM), Mb), rta, Rp * MPC, 5.0 * Mbt, 11.0, A0["canonical"]); Ms[n] = (float(np.interp(Rp * MPC, r, s["Mf"])), float(s["Mf"][-1]), bool(np.all(s["rho"] <= s["cap"] * (1 + 1e-9))), s["conv"], float(s["sigma"]))
    ck["K_solver"] = dict(M500_420=Ms[420][0], M500_840=Ms[840][0], ratio=Ms[420][0] / Ms[840][0], fair=Ms[840][1] / (5.0 * Mbt), cap_ok=Ms[840][2], conv=Ms[840][3], passed=bool(abs(Ms[420][0] / Ms[840][0] - 1) < 0.01 and abs(Ms[840][1] / (5.0 * Mbt) - 1) < 0.01 and Ms[840][2] and Ms[840][3]))
    # law limit: zero fermion on X-COP reproduces BF1's known answer +0.467, 0.476
    x = xcop_rows(XC, 0.0, 11.0, "canonical", law_only=True); ck["K_xcop_law"] = dict(mean=x["all"]["mean"], rms=x["all"]["rms"], record=[0.467, 0.476], passed=bool(abs(x["all"]["mean"] - 0.467) <= 0.01 and abs(x["all"]["rms"] - 0.476) <= 0.01))
    # SPARC, LT, groups, dwarfs with the fermion switched off (Rf 0): the law's CRG1 values
    rec = json.load(open(os.path.join(HL.CRG, "v1", "crg1_results.json")))["C4"]["canonical"]
    r0_, t0, _ = sparc_fit(G, 0.0, 11.0, A0["canonical"]); ck["K_sparc_off"] = dict(rms=r0_["rms"], Y=r0_["Y_med"], tilt=t0["tilt"], rec=[rec["S"]["rows"]["A_c2b_refit"]["rms"] if "rows" in rec["S"] else None], passed=bool(abs(r0_["rms"] - 0.0541) <= 2e-4 and abs(r0_["Y_med"] - 0.52) <= 0.011 and abs(t0["tilt"] - 0.02) <= 0.011))
    lt0 = float(np.median([lt_row(x_, 0.0, 11.0, A0["canonical"])[0] for x_ in LT])); ck["K_lt_off"] = dict(E=lt0, passed=bool(abs(lt0 + 0.025) <= 1e-3))
    g0 = groups_stat(GR.load(), 0.0, 11.0, A0["canonical"]); ck["K_groups_off"] = dict(Z=g0["Z"], cls=g0["cls"], passed=bool(abs(g0["Z"] - 0.31) <= 0.01 and g0["cls"] == "CONSISTENT"))
    d0 = dwarf_E(DW.load("canonical"), 0.0, 11.0, A0["canonical"]); ck["K_dw_off"] = dict(Z={k: v["Z"] for k, v in d0["classes"].items()}, passed=bool(abs(d0["classes"]["MW ultra-faint"]["Z"] - 5.22) <= 0.01))
    hs0 = hs_slope(G, 0.0, 11.0, A0["canonical"], law_only=True); hsr = json.load(open(os.path.join(RB, "RQ3_acceptance_v2", "results", "law.json")))["footings"]["canonical"]["rows"]["A4"]; ck["K_hs_law"] = dict(Z=hs0["Z"], rq3=hsr["Z"], passed=bool(abs(hs0["Z"] - hsr["Z"]) <= 0.01))
    # keys harness: CRG1's C4, its own builder, against its sealed table
    KR = json.load(open(os.path.join(HL.CRG, "v1", "crg1_results.json")))["C4"]["canonical"]["K"]
    def cf(h): return C.load_or_build(f"C4_h{h}", C.fn_C4(D, None, CSS, h))
    kb = C.K_block(D, cf, "V_canonical", "vC_own_canonical", "canonical", mode="given"); fl = sorted(kb["failing"]); ck["K_keys_C4"] = dict(n_pass=kb["n_pass"], failing=fl, rec_failing=sorted(KR["failing"]), m3=kb["tables"]["h0672"]["G-MID-T3"]["Z"], passed=bool(fl == sorted(KR["failing"]) and abs(kb["tables"]["h0672"]["G-MID-T3"]["Z"] - 4.46) <= 0.01))
    # my cell with the fermion off equals the direct law on the chain, through vec
    i = 7; q = D.geo[0.672]["q"][i]; Mbx, Mb, Mbt, rta = C.chain(D.Mgas[i] * q ** 2.5 * 10 ** 0.005, D.R500[i] * q, 0.034, D.z[i], MSUN); Mf, _ = cluster_fermion(C.RM, Mb, Mbt, rta, D.R500[i] * q, 0.0, 11.0, A0["canonical"]); pz = Mb > 0; ck["K_off_zero"] = dict(maxfrac=float(np.max(Mf[pz] / Mb[pz])), max_Msun_where_Mb0=float(np.max(Mf[~pz] / MSUN, initial=0.0)), n_Mb0=int((~pz).sum()), passed=bool(np.max(Mf[pz] / Mb[pz]) < 1e-6 and np.max(Mf[~pz] / MSUN, initial=0.0) < 1.0))
    return ck

def report_gate(lab, Rf, m, wf, wb, D, CSS, XC, G, LT, gf=2.0, capf=1.0, tag="RUN"):
    R = dict(m=m, omega_f=wf, omega_b=wb, Rf=Rf, label=lab)
    P(f"\n=== {lab}: m {m:g} eV, omega_f {wf:.5f}, omega_b {wb:.5f}, omega_f/omega_b {Rf:.3f}, g_f {gf:g}, cap factor {capf:g}")
    R["X"] = {f: xcop_rows(XC, Rf, m, f, gf=gf, capf=capf) for f in FEET}
    for f in FEET:
        x = R["X"][f]; P(f"  X-COP {f}: all mean {x['all']['mean']:+.3f} rms {x['all']['rms']:.3f} {'PASS' if x['all']['passed'] else 'FAIL'}; train {x['train']['mean']:+.3f}, {x['train']['rms']:.3f}; holdout {x['holdout']['mean']:+.3f}, {x['holdout']['rms']:.3f}; by x {[round(v, 3) for v in x['by_x'].values()]}; M_f/M_b {[round(v, 2) for v in x['mf_over_mb_by_x'].values()]}")
    P(f"  per cluster canonical {[(k, round(v, 3)) for k, v in R['X']['canonical']['per_cluster'].items()]}; sigma km/s {[round(v['sigma_kms']) for v in R['X']['canonical']['info'].values()]}")
    R["K"] = {}
    info = []
    FA = json.load(open(os.path.join(RB, "DA1_definition_audit", "da1_keys.json")))["F"]; GRD = np.array([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]); fac = lambda hn: np.interp(D.z, GRD, FA[hn])[:, None]
    for f in FEET:
        cells = keys_all(D, CSS, Rf, m, 0.034, 0.005, f, f"m{m:g}", gf, capf, info=info if f == "canonical" else None); T = k_table(D, cells, f); R["K"][f] = T; keyline(f"Keys {f}, f* 0.034, gas +0.005", T)
    cells = keys_all(D, CSS, Rf, m, 0.034, 0.005, "canonical", f"m{m:g}", gf, capf)
    R["K_B1"] = k_table(D, cells, "canonical", B1=True); keyline("  DA1 B = 1", R["K_B1"]); R["K_nz"] = k_table(D, cells, "canonical", fac=fac); keyline("  DA1 n(z)", R["K_nz"])
    cb = keys_all(D, CSS, Rf, m, 0.0615, 0.005, "canonical", f"m{m:g}", gf, capf); R["K_f0615"] = k_table(D, cb, "canonical"); keyline("  f* 0.0615", R["K_f0615"])
    cx = keys_all(D, CSS, Rf, m, 0.034, 0.111, "canonical", f"m{m:g}", gf, capf); R["K_g111"] = k_table(D, cx, "canonical"); keyline("  gas +0.111, X-COP's scale, reported", R["K_g111"])
    R["K_info"] = {k: float(np.median([q[k] for q in info])) for k in info[0]} if info else {}
    if info: P(f"  median cluster: sigma {R['K_info']['sig'] / 1e3:.0f} km/s, r_ta {R['K_info']['rta']:.2f} Mpc, M_f(R500)/M_b(R500) {np.median([q['Mf500'] / q['Mb500'] for q in info]):.2f}, M_f(r_ta) {R['K_info']['Mfta']:.2e}, share of clusters where the cap holds M_f(r_ta) under fair share {np.mean([q['Mfta'] < 0.99 * Rf * q['Mbt'] for q in info]):.2f}")
    R["gate2_pass"] = {f: bool(R["X"][f]["all"]["passed"] and R["K"][f]["n_pass"] == 15) for f in FEET}
    R["lens_rows"] = {f: lens_rows(Rf, m, f) for f in FEET}
    P("  Lensing mass at the offset peak, published apertures, PROVISIONAL (MG1), canonical, reported; collisionless offsets are by construction, not a test:")
    for q in R["lens_rows"]["canonical"]: P(f"    {q['system']} {q['sub']} <{q['R_kpc']} kpc: M_lens {q['M_lens']:.2e}; model gas displaced {q['M_proj_gasdisplaced']:.2e} ({q['ratio_low']:.2f}), gas centred {q['M_proj_gascentred']:.2e} ({q['ratio_high']:.2f}); sigma {q['sigma_kms']:.0f}")
    # gate 3
    R["G3"] = {}
    gr = GR.load()
    for f in FEET:
        a0 = A0[f]; r, t, fr = sparc_fit(G, Rf, m, a0, gf, capf); lt = [lt_row(x, Rf, m, a0, gf, capf) for x in LT]; E_ = np.array([v[0] for v in lt]); ltm = float(np.median(E_)); ic = float(E_[[i for i, x in enumerate(LT) if x["name"] == "IC 1613"][0]]); g_ = groups_stat(gr, Rf, m, a0, gf, capf); d_ = dwarf_E(DW.load(f), Rf, m, a0, gf, capf); h_ = hs_slope(G, Rf, m, a0, gf, capf); q = np.array([g["Q"] <= 2 and g["Inc"] >= 30 for g in G]); V = np.array([g["Vflat"] for g in G]); fr_ = np.array([x["ratio"] for x in fr])
        C_ = dict(S=bool(r["rms"] <= .110 and .50 <= r["Y_med"] <= .80), Tl=bool(abs(t["tilt"]) <= .15), HS=h_["passed"], LT=bool(abs(ltm) <= .10), G=g_["cls"] == "CONSISTENT", Dw=d_["passed"], IC=bool(abs(ic / .075) < 2))
        R["G3"][f] = dict(rms=r["rms"], Y=r["Y_med"], tilt=t["tilt"], Y_by_V=t["Y_by_Vflat"], DA1_window_S={"0.375-0.625": bool(.375 <= r["Y_med"] <= .625 and r["rms"] <= .11), "0.25-0.75": bool(.25 <= r["Y_med"] <= .75 and r["rms"] <= .11)}, hs=h_, lt=ltm, ic_E=ic, ic_Z=ic / .075, groups=g_, dwarfs={k: v["Z"] for k, v in d_["classes"].items()}, lines=C_, gate3_pass=bool(C_["S"] and C_["Tl"] and C_["HS"] and C_["LT"] and C_["G"]), fermion_over_baryon_at_Rlast=dict(median_all=float(np.median(fr_)), median_V_lt100=float(np.median(fr_[q & (V > 0) & (V < 100)])), median_V_gt200=float(np.median(fr_[q & (V > 200)])), max=float(fr_.max())))
        w = R["G3"][f]; P(f"  Gate 3 {f}: rms {w['rms']:.4f}, Upsilon {w['Y']:.2f}, tilt {w['tilt']:+.2f}, SB slope Z {h_['Z']:+.2f}, LT {ltm:+.3f}, groups Z {g_['Z']:+.2f} {g_['cls']}, Dw {[round(v, 2) for v in w['dwarfs'].values()]}, IC 1613 E {ic:+.3f} (Z {ic / .075:+.1f}); M_f/M_b at R_last, median all {w['fermion_over_baryon_at_Rlast']['median_all']:.3f}, V<100 {w['fermion_over_baryon_at_Rlast']['median_V_lt100']:.4f}, V>200 {w['fermion_over_baryon_at_Rlast']['median_V_gt200']:.3f}; lines {C_}; gate 3 {'PASS' if w['gate3_pass'] else 'FAIL'}; DA1 windows {w['DA1_window_S']}")
    ro, to, _ = sparc_fit(G, Rf, m, A0["canonical"], gf, capf, Rsig="obs"); R["G3_sigma_obs"] = dict(rms=ro["rms"], Y=ro["Y_med"], tilt=to["tilt"]); P(f"  Bracket, A1 R4, cap at measured V_flat / sqrt 2, canonical, reported: rms {ro['rms']:.4f}, Upsilon {ro['Y_med']:.2f}, tilt {to['tilt']:+.2f}")
    a0 = A0["canonical"]; VM = float(FM.lawg(np.array(GF * 6.6e10 * MSUN / (8e19 * 3.0857) ** 2), a0)) ; v2 = (220e3) ** 2; rc = float(FM.rho_cap(m, math.sqrt(v2 / 2), gf)) * capf; dK = 2 * rc * 1.1 * 3.0857e19 / (MSUN / (3.0857e16) ** 2); R["MW"] = dict(rho_cap_kg_m3=rc, rho_cap_Msun_pc3=rc / (MSUN / (3.0857e16) ** 3), dKz_Msun_pc2_at_1p1kpc=dK); P(f"  Milky Way, expected fail: the law's cells are already K_z +4.7 to +6.6 sigma high (READ X5). The cap at sigma 220/sqrt 2 km/s permits rho {R['MW']['rho_cap_Msun_pc3']:.4f} Msun/pc^3, adding up to {dK:.1f} Msun/pc^2 to K_z's column at 1.1 kpc before the law's boost. It only adds. Not a new solve")
    return R

def main():
    mode = sys.argv[1]; D, CSS, XC, G, LT = load_common(); RES = dict(mode=mode); SFX = {"select": "select", "controls": "controls", "run": "RUN", "mutate": "MUTATE"}[mode]
    P(f"HF1 gates 2-3, mode {mode}, criteria 56ab302a4d, A1. kappa = 1/2 FITTED; a0 canonical 9.3603e-11, alt 1.1312e-10, never pooled. QUMOND and AQUAL coincide in spherical symmetry with this nu. Not theory closed.")
    if mode == "controls":
        RES["checks"] = controls(D, CSS, XC, G, LT); RES["all"] = all(v["passed"] for v in RES["checks"].values()); P(json.dumps(RES["checks"], indent=0, default=float)); P(f"ALL {RES['all']}")
    if mode == "select":
        _g = json.load(open(os.path.join(HERE, "hf1_g1_results.json")))["rows"]; g1 = dict(_g["FD"]); g1.update(_g.get("FDY", {})); T = {}
        for n, w in g1.items():
            if w.get("status") != "OK": continue
            Rf = w["omega_f"] / w["omega_b"]; m = w["m"]; x = xcop_rows(XC, Rf, m, "canonical"); s = bf1_train(G, Rf, m, A0["canonical"]); T[n] = dict(m=m, omega_f=w["omega_f"], omega_b=w["omega_b"], gate1=w.get("passed"), S=w.get("S"), xtrain=x["train"], strain=s); P(f"  m {m:g} omega_f {w['omega_f']:.4f} gate1 {w.get('passed')} S-RF5 {w.get('S_minus_RF5')}: X-COP train {x['train']['mean']:+.3f}, {x['train']['rms']:.3f} {x['train']['passed']}; SPARC train rms {s['rms']:.4f} (law {s['rms_law']:.4f}), median {s['median']:+.3f} {s['passed']}")
        pool = [t for t in T.values() if t["gate1"]] or list(T.values()); both = [t for t in pool if t["xtrain"]["passed"] and t["strain"]["passed"]]
        ch = min(both, key=lambda t: t["S"]) if both else min(pool, key=lambda t: abs(t["xtrain"]["mean"])); RES.update(table=T, chosen=ch, rule="both pass, lowest S" if both else "none pass both: smallest |mean| on X-COP train"); P(f"CHOSEN m {ch['m']:g}, omega_f {ch['omega_f']:.5f}, rule: {RES['rule']}, pool {'gate-1 passers' if any(t['gate1'] for t in T.values()) else 'all six (numbers only)'}")
    if mode in ("run", "mutate"):
        m, wf, wb = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]); Rf = wf / wb
        if mode == "run":
            RES["R"] = report_gate("RUN", Rf, m, wf, wb, D, CSS, XC, G, LT); RES["bracket_sigma_obs"] = None
        else:
            r0 = xcop_rows(XC, Rf, m, "canonical"); r1 = xcop_rows(XC, Rf, m, "canonical", gf=32.0); cap0 = list(r0["info"].values())[0]["cap"]; sg0 = list(r0["info"].values())[0]["sigma_kms"]; cap_ratio = FM.rho_cap(m, 1e6, 32.0) / FM.rho_cap(m, 1e6, 2.0); dmn = abs(r1["all"]["mean"] - r0["all"]["mean"]); P(f"MUTATE g_f x 16: cap ratio at fixed sigma {cap_ratio:.6f} (expected 16, power 1); X-COP mean {r0['all']['mean']:+.4f} -> {r1['all']['mean']:+.4f}; M_f/M_b at x=0.1 {r0['mf_over_mb_by_x']['0.1']:.3f} -> {r1['mf_over_mb_by_x']['0.1']:.3f}")
            a0 = A0["canonical"]; rp, tp, _ = sparc_fit(G, Rf, m, a0, capf=300.0); P(f"MUTATE planted over-dense, cap x 300: SPARC rms {rp['rms']:.4f}, Upsilon {rp['Y_med']:.2f}, tilt {tp['tilt']:+.2f}: gate 3 S/Tl {'PASS (BAD)' if (rp['rms'] <= .11 and .5 <= rp['Y_med'] <= .8 and abs(tp['tilt']) <= .15) else 'FAIL as required'}"); RES.update(cap_ratio=cap_ratio, x0=r0["all"], x1=r1["all"], planted=dict(rms=rp["rms"], Y=rp["Y_med"], tilt=tp["tilt"]), m1_ok=abs(cap_ratio - 16) < 1e-9, m2_ok=not (rp["rms"] <= .11 and .5 <= rp["Y_med"] <= .8 and abs(tp["tilt"]) <= .15))
    P("kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.")
    json.dump(CO.fmt(RES), open(os.path.join(HERE, f"hf1_g23_{SFX}.json"), "w"), indent=1, sort_keys=True); open(os.path.join(HERE, f"hf1_g23_{SFX}.out"), "w").write("\n".join(OUT) + "\n")
if __name__ == "__main__": main()
