"""Tier B: G. Section 3.2-3.3. Background A, set P. C2 is computed as an extra (Tier C in the table)."""
from crg1_core import *
from crg1_zoom import get_nr

XG = np.logspace(-5, 5, 3000); LX = np.log(XG)
RHO_H = 1 / (2 * math.pi * XG * (1 + XG) ** 3); M_H = XG ** 2 / (1 + XG) ** 2
gN_t = M_H / XG ** 2

def load():
    rows = []
    for l in open(os.path.join(INP, "groups", "J_A_A_710_L39.tsv")):
        if l.startswith("#"): continue
        f = l.rstrip("\n").split("\t")
        if len(f) >= 13 and f[0].strip().isdigit() and f[1].strip() == "Galaxy group":
            rows.append((float(f[5]), float(f[7]), float(f[10])))
    return rows

def logsig(lM, Re, dl, cand, a0, nr=None):
    a = Re * (P.pc * 1e3) / 1.8153
    lg = lM + dl; Mb = 10 ** lg * P.Msun; b = bg(BGS[0]); rr = XG * a
    if cand == "none":
        gt = gN_t
    else:
        lgM2 = float(b.lgM200(lg)); M200 = 10 ** lgM2 * P.Msun; R2 = R200_of(M200, b.h, P.G, E.Mpc)
        y0 = a0 / (P.G * Mb / a ** 2) if a0 else None
        if cand == "C1":
            S = nr.S((M200 / E.Msun) / f_c, b); r0 = solve_r0(M200, R2, S, B_S)
            gt = gN_t + math.pi * S * r0 ** 2 * B_S(np.minimum(rr, R2) / r0) / (Mb * XG ** 2)
        elif cand == "C2":
            S = nr.S((M200 / E.Msun) / f_c, b); r0 = solve_r0(M200, R2, S, B_S)
            rg = np.geomspace(min(rr[0], 1e-4 * R2), R2, 800); M0g = math.pi * S * r0 ** 2 * B_S(rg / r0)
            Mbg = np.interp(np.log(rg), np.log(rr), Mb * M_H)
            Mc = contract(rg, Mbg, M0g, Mbg[-1] / M0g[-1])
            gt = gN_t + np.interp(np.log(rr), np.log(rg), Mc) / (Mb * XG ** 2)
        elif cand == "C3":
            M = M200 / E.Msun
            if M > 10 ** 12.3:
                S = S_H(M, a0, eta_C3, b); r0 = solve_r0(M200, R2, S, B_B)
                gt = gN_t + math.pi * S * r0 ** 2 * B_B(np.minimum(rr, R2) / r0) / (Mb * XG ** 2)
            else:
                gt = nu(gN_t / y0) * gN_t
        elif cand == "C4":
            gt = nu(gN_t / y0) * gN_t
    s2 = np.trapz(4 * math.pi * XG ** 2 * RHO_H * XG * gt * XG, LX) / 3 * P.G * Mb / a
    return 0.5 * math.log10(s2) - 3

def stat(rows, cand, a0, nr=None):
    d, sl = [], []
    for ls, lM, Re in rows:
        d.append(ls - logsig(lM, Re, 0.0, cand, a0, nr))
        sl.append((logsig(lM, Re, 0.01, cand, a0, nr) - logsig(lM, Re, -0.01, cand, a0, nr)) / 0.02)
    d = np.array(d); sl = np.array(sl); mean = d.mean(); se = d.std(ddof=1) / math.sqrt(len(d)); sys_ = 0.10 * sl.mean()
    tot = math.sqrt(se ** 2 + sys_ ** 2); Z = mean / tot
    cls = "NOT DIAGNOSTIC" if tot > 0.045 else ("CONSISTENT" if abs(Z) < 2 else ("ABOVE LAW" if Z >= 2 else "BELOW LAW"))
    return dict(n=len(d), mean=mean, se=se, sys=sys_, tot=tot, Z=Z, cls=cls, passed=cls == "CONSISTENT")

def main():
    if have_part("G"): return
    rows = load(); assert len(rows) == 63
    NRa, NRb = get_nr("a"), get_nr("b")
    out = {"C1": {"canonical": stat(rows, "C1", None, NRa), "canonical_A1b": stat(rows, "C1", None, NRb)},
           "C2_extra_TierC": {"canonical": stat(rows, "C2", None, NRa)},
           "C3": {f: stat(rows, "C3", A0[f]) for f in A0}, "C4": {f: stat(rows, "C4", A0[f]) for f in A0},
           "no_halo_Newton": stat(rows, "none", None)}
    save_part("G", out); log("G done")

if __name__ == "__main__": main()
