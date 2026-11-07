#!/usr/bin/env python3
"""GL2 (FROZEN_CRITERIA.md 7a585d8aa9): independent Limber C_L^pp vs CLASS, k^-4 present (kernel K) and dropped (M1).
Own code: imports nothing from QX3 / QX7 / CE2 / CK4. kappa = 1/2 FITTED; not theory closed. One thread."""
import os, sys, json, math, re, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from classy import Class

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}          # a0 does not enter the linear background (criteria)
REC = dict(omega_b=0.0215, omega_d=0.11958060485606123, H0=65.0, n_s=0.95)
CK4_FROZEN = {20: 0.045, 50: 0.239, 200: 5.26, 300: 15.0, 400: 33.0}
LS = np.arange(20, 401); LMAX = 500; ZSTAR_MAX = 1000.0   # disclosed: CLASS refuses z_pk > z_rec; kernel ~0 there

def run(bg, zmax_pk, kmax):
    M = Class()
    M.set({'output': 'tCl,lCl,mPk', 'lensing': 'no', 'l_max_scalars': LMAX, 'h': bg["H0"] / 100, 'omega_b': bg["omega_b"],
           'omega_cdm': bg["omega_d"], 'A_s': 2.0e-9, 'n_s': bg["n_s"], 'tau_reio': 0.06, 'N_ur': 3.046, 'T_cmb': 2.7255,
           'P_k_max_1/Mpc': kmax, 'z_max_pk': zmax_pk})
    M.compute(); return M

def limber(M, zgrid, kgrid, k4=True):
    """C_L^pp = int dchi [2 (chi*-chi)/(chi chi*)]^2 / chi^2 * (3/2 Om H0^2 (1+z))^2 P_m(k,z) / k^4  [k^-4 dropped if not k4].
    P tabulated on kgrid and interpolated in ln k; P = 0 outside kgrid."""
    H0 = M.Hubble(0.0); Om = M.Omega_m()
    zs = M.get_current_derived_parameters(['z_star'])['z_star']
    chis = M.angular_distance(zs) * (1 + zs)
    z = np.asarray(zgrid); chi = np.array([M.angular_distance(x) * (1 + x) for x in z]); H = np.array([M.Hubble(x) for x in z])
    lnk = np.log(kgrid)
    Ptab = np.array([[M.pk_lin(k, x) for x in z] for k in kgrid])          # (nk, nz), Mpc^3
    integ = np.zeros((len(LS), len(z)))
    for j in range(len(z)):
        if chi[j] >= chis: continue
        k = (LS + 0.5) / chi[j]; m = (k >= kgrid[0]) & (k <= kgrid[-1])
        Pk = np.zeros(len(LS)); Pk[m] = np.exp(np.interp(np.log(k[m]), lnk, np.log(Ptab[:, j])))
        src = (1.5 * Om * H0 ** 2 * (1 + z[j])) ** 2 * Pk / (k ** 4 if k4 else 1.0)
        integ[:, j] = (2 * (chis - chi[j]) / (chi[j] * chis)) ** 2 / chi[j] ** 2 * src / H[j]   # dchi = dz / H
    return np.trapz(integ, z, axis=1)

def Q_of(Cl_lim, pp):
    r = Cl_lim / pp[LS]; return r / r[LS == 100][0], float(r[LS == 100][0])

def summary(Q):
    return dict(max_abs_dev=float(np.max(np.abs(Q - 1))), at={str(L): float(Q[LS == L][0]) for L in (20, 50, 100, 200, 300, 400)},
                min=float(Q.min()), max=float(Q.max()))

def read_qx3():
    """Step 3: read iter2.py's limber_ratio as text and state whether the per-slice weight carries 1/k^4 or (chi/L)^4."""
    src = open(os.path.join(REPO, "closure_2026_11_06/QX3_cmb_growth/iter2_kq_dust/iter2.py")).read()
    body = src[src.index("def limber_ratio"):src.index("def enclosed")]
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    wline = next(l for l in lines if l.startswith("w ="))
    acc = next(l for l in lines if "num[m] +=" in l)
    pat = re.compile(r"kk\s*\*\*\s*-?4|kk\s*\*\*\s*4|\*\*\s*-4|chi\[j\]\s*\*\*\s*4|\(Ls\s*\+\s*0\.5\)\s*\*\*\s*4|/\s*kk\s*\*\*")
    present = bool(pat.search(body))
    # per-slice power of chi in the accumulated weight: w has chi^-2, accumulator divides by chi^2 -> chi^-4; with
    # P_Psi = P/k^4 = P chi^4/L^4 the correct net power is chi^0 (times the L^-4 that cancels at fixed L)
    return dict(w_line=wline, accumulate_line=acc, k4_or_chi4_found=present, verdict="PRESENT" if present else "ABSENT",
                net_chi_power_in_weight=-4, correct_net_chi_power=0)

if __name__ == "__main__":
    t0 = time.time(); RES = dict(lane="GL2", criteria="7a585d8aa9", note="kappa = 1/2 FITTED; not theory closed")
    # ---- record background, full domain
    M = run(REC, ZSTAR_MAX, 60.0)
    KA1 = dict(Om_b0=M.Omega_b(), Om_d0=M.Omega0_cdm() if hasattr(M, "Omega0_cdm") else M.Omega_m() - M.Omega_b())
    KA1["pass"] = abs(KA1["Om_b0"] - 0.05089) <= 1e-4 and abs(KA1["Om_d0"] - 0.28303) <= 1e-4
    P(f"KA1 Om_b0 {KA1['Om_b0']:.5f} Om_d0 {KA1['Om_d0']:.5f} -> {'PASS' if KA1['pass'] else 'FAIL'}")
    pp = M.raw_cl(LMAX)['pp']
    zfull = np.concatenate([np.logspace(-3, 0, 200)[:-1], np.logspace(0, math.log10(ZSTAR_MAX), 400)])
    kfull = np.logspace(-5, math.log10(55.0), 300)
    CK = limber(M, zfull, kfull, k4=True); QK, absK = Q_of(CK, pp)
    KA2 = dict(abs_ratio_L100=absK, pass_=bool(abs(absK - 1) <= 0.05))
    P(f"KA2 absolute Limber/CLASS at L 100 = {absK:.4f} -> {'PASS' if KA2['pass_'] else 'FAIL'}")
    sK = summary(QK); P(f"kernel K (k^-4 present, full domain): max|Q-1| {sK['max_abs_dev']:.4f}; Q at", sK["at"])
    # reported: kernel K on QX3's domain
    zq = np.linspace(0.02, 20.0, 120); kq = np.logspace(-4, 1, 70)
    QKq, absKq = Q_of(limber(M, zq, kq, k4=True), pp); sKq = summary(QKq)
    P(f"kernel K on QX3 domain (z 0.02-20, k <= 10): max|Q-1| {sKq['max_abs_dev']:.4f}; Q at", sKq["at"])
    # ---- MUTATE M1: k^-4 dropped, QX3's domain
    QM, absM = Q_of(limber(M, zq, kq, k4=False), pp); sM = summary(QM)
    rep = {str(L): dict(Q=float(QM[LS == L][0]), ck4=v, rel=float(QM[LS == L][0] / v - 1)) for L, v in CK4_FROZEN.items()}
    M1 = dict(summary=sM, reproduce=rep, leaves_line=bool(sM["max_abs_dev"] > 0.02),
              reproduces_ck4=bool(all(abs(x["rel"]) <= 0.10 for x in rep.values())))
    P(f"M1 (k^-4 dropped, QX3 domain): Q at", sM["at"], "range", f"{sM['min']:.3f}-{sM['max']:.2f}")
    P("   vs CK4 frozen-kernel run:", {L: f"{x['Q']:.3f} vs {x['ck4']} ({x['rel']:+.3f})" for L, x in rep.items()},
      "-> leaves line", M1["leaves_line"], "reproduces", M1["reproduces_ck4"])
    QMf, _ = Q_of(limber(M, zfull, kfull, k4=False), pp)
    P(f"   M1 on the full domain (reported): Q at", summary(QMf)["at"])
    M.struct_cleanup()
    RD = read_qx3(); P("READING iter2.py limber_ratio:", RD["verdict"]); P("   ", RD["w_line"]); P("   ", RD["accumulate_line"])
    # ---- labels per footing (same background; graded separately)
    lab = {}
    for f in FOOT:
        if not (KA1["pass"] and KA2["pass_"]) or sK["max_abs_dev"] > 0.02: L_ = "UNDECIDED"
        elif RD["verdict"] == "PRESENT" or not M1["leaves_line"]: L_ = "REFUTED"
        elif M1["reproduces_ck4"] and RD["verdict"] == "ABSENT": L_ = "CONFIRMED"
        else: L_ = "UNDECIDED"
        lab[f] = L_; P(f"LABEL {f} (a0 {FOOT[f]}): {L_}")
    lane = lab["canonical"] if lab["canonical"] == lab["alt"] else "UNDECIDED"; P("LANE LABEL:", lane)
    # ---- reported: second background (QX3 G1 corner 0.0230 / 75 / 0.98 at its own omega_d_best)
    g1 = json.load(open(os.path.join(REPO, "closure_2026_11_06/QX3_cmb_growth/iter2_kq_dust/iter2.json")))["G1"]
    c2 = next(r for r in g1 if r["omega_b"] == 0.0230 and r["H0"] == 75.0 and r["n_s"] == 0.98)
    BG2 = dict(omega_b=0.0230, omega_d=c2["omega_d_best"], H0=75.0, n_s=0.98)
    M2 = run(BG2, ZSTAR_MAX, 60.0); pp2 = M2.raw_cl(LMAX)['pp']
    Q2, a2 = Q_of(limber(M2, zfull, kfull, k4=True), pp2); Q2m, _ = Q_of(limber(M2, zq, kq, k4=False), pp2); M2.struct_cleanup()
    P(f"reported BG2 {BG2}: kernel K max|Q-1| {np.max(np.abs(Q2 - 1)):.4f} (abs L100 {a2:.4f}); M1 Q at", summary(Q2m)["at"])
    RES.update(background=REC, footings=FOOT, KA1=KA1, KA2=KA2, kernel_K=sK, kernel_K_qx3_domain=sKq, M1=M1,
               M1_full_domain=summary(QMf), reading=RD, labels=lab, lane_label=lane,
               BG2=dict(bg=BG2, kernel_K=summary(Q2), abs_L100=a2, M1=summary(Q2m)),
               Q_kernel_K={int(L): float(q) for L, q in zip(LS, QK)}, Q_M1={int(L): float(q) for L, q in zip(LS, QM)},
               runtime_s=time.time() - t0, peak_rss_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9)
    P(f"runtime {RES['runtime_s']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")
    json.dump(RES, open(os.path.join(HERE, "gl2.json"), "w"), indent=1); open(os.path.join(HERE, "gl2.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(dict(lane="GL2", mutate="M1: k^-4 dropped, QX3 domain", M1=M1, M1_full_domain=RES["M1_full_domain"],
                   BG2_M1=RES["BG2"]["M1"], Q_M1=RES["Q_M1"], note=RES["note"]),
              open(os.path.join(HERE, "gl2_MUTATE.json"), "w"), indent=1)
    open(os.path.join(HERE, "gl2_MUTATE.out"), "w").write("\n".join(l for l in OUT if "M1" in l or "CK4" in l) + "\n")
