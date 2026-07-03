#!/usr/bin/env python3
"""
LANE L1b -- THE TWO NAMED CAVEAT KNOBS of the banked hierarchical SPARC arbiter, turned.
Headline convention = the CORRECTED data-space likelihood (VERIFY_L1_inclination_norm_fork.py,
corrected=True: V_obs fixed with published e_V, model mean = V_mod*sqrt(d)*t, t=sin(i)/sin(i0),
NO -2N*ln(t) norm term). Framework nu(y)=sqrt(1+1/y); a0 canonical 9.36e-11, fork 1.13e-10.

KNOB 1: UNLOCK Upsilon_bul -- independent per-galaxy lognormal prior log10 U_bul ~ N(log10 0.7,
        0.10 dex) [variant 0.15 dex], jointly marginalized with U_disk (N(log10 0.5, 0.10)), D, i.
        Banked model had U_bul = 1.4*U_disk LOCKED while the top influencers (UGC06787, IC4202,
        NGC7814) are bulge-heavy.
KNOB 2: sigma_int form -- PER-GALAXY fractional sigma_int f_g (hierarchical: half-normal prior of
        scale tau, truncated+normalized on the f grid, tau profiled) vs the banked GLOBAL profiled
        f. Per-galaxy FREE-profiled f carried as the labeled extreme (Neyman-Scott caveat).

VALIDATION GATES (asserted; exit 0 = all passed):
  V1 corrected-baseline reproduction: full a0_hat=1.37e-10 (+bootstrap ~3.3 sig excl. of 9.36e-11),
     gas-dominated cut a0_hat=9.8e-11 -- the banked arbiter's corrected numbers, same data handling.
  V2 mock injection THROUGH THE UNLOCKED MACHINERY: truth = framework nu, a0=9.36e-11, U_d=0.5,
     U_b=0.7, D=D0, i=i0, noise=e_V -> must recover unbiased with U_bul unlocked.
PRE-REGISTERED READING (fixed before running): if unlocking U_bul COLLAPSES the tension (full-sample
a0_hat in [0.9,1.1]e-10 or Dchi2(9.36e-11) below ~9 bootstrap-honest) -> the full-sample exclusion is
DOWNGRADED to bulge-M/L systematics; if it survives >3 sigma under BOTH knobs -> it HARDENS.
C. Zimmerman lane L1b, 2026-07-02. numpy + local SPARC only.
"""
import numpy as np, glob, os, sys, time

t_start = time.time()
SMOKE = os.environ.get("SMOKE", "0") == "1"
c = 2.998e8; kpc = 3.0857e19; H0 = 2.184e-18; OmL = 0.685
A0FW = (c/2)*np.sqrt(3*OmL*H0**2/(8*np.pi)); A0FORK = 1.13e-10
assert abs(A0FW/9.36e-11 - 1) < 0.005
ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data"

# ----------------------------------------------------------------------------- data (banked loader)
meta = {}
for line in open(os.path.join(ROOT, "SPARC_Lelli2016c.mrt")):
    f = line.split()
    if len(f) < 18: continue
    try:
        D = float(f[2]); eD = float(f[3]); inc = float(f[5]); ei = float(f[6]); Q = int(f[17])
    except ValueError:
        continue
    meta[f[0]] = dict(D0=D, eD=max(eD, 0.05*D), i0=inc, ei=max(ei, 1.0), Q=Q)
gals = []
for fn in sorted(glob.glob(os.path.join(ROOT, "sparc_data", "*_rotmod.dat"))):
    d = np.genfromtxt(fn, comments="#")
    if d.ndim != 2 or d.shape[1] < 6: continue
    name = os.path.basename(fn).split("_rotmod")[0]
    R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    ok = (Vo > 0) & (eV > 0)
    if ok.sum() < 5 or name not in meta: continue
    gals.append(dict(name=name, R=R[ok], Vo=Vo[ok], eV=eV[ok], Vg=Vg[ok], Vd=Vd[ok], Vb=Vb[ok],
                     **meta[name]))
assert len(gals) == 171, f"expected banked 171, got {len(gals)}"
if SMOKE: gals = gals[:20] + [g for g in gals if g["name"] in ("UGC06787", "IC4202", "NGC7814")]
NG = len(gals)
gf = np.array([(lambda n_, d_: n_/max(d_, 1e-30))(np.sum(np.sign(g["Vg"])*g["Vg"]**2),
      np.sum(np.sign(g["Vg"])*g["Vg"]**2) + 0.5*np.sum(g["Vd"]**2) + 0.7*np.sum(g["Vb"]**2))
      for g in gals])
sel_gas = gf > 0.5
hasb = np.array([np.any(g["Vb"] != 0) for g in gals])
if not SMOKE:
    assert sel_gas.sum() == 37, "gas-dom membership drifted"
print(f"sample N={NG}; gas-dom N={sel_gas.sum()}; bulge (Vbul>0 anywhere) N={hasb.sum()}; "
      f"gas-dom WITH bulge N={int((sel_gas & hasb).sum())}")

nu_fw = lambda y: np.sqrt(1.0 + 1.0/y)

# ----------------------------------------------------------------------------- grids (banked + LUB)
A0GRID = np.unique(np.concatenate([np.geomspace(0.6e-10, 3.0e-10, 17),
        np.geomspace(0.85e-10, 1.75e-10, 13), np.geomspace(0.9e-10, 1.55e-10, 19),
        [A0FW, A0FORK, 1.2e-10, 7.7e-11]]))
LNA0 = np.log(A0GRID); NA = len(A0GRID)
IA_FW = int(np.argmin(abs(A0GRID - A0FW))); IA_FORK = int(np.argmin(abs(A0GRID - A0FORK)))
FGRID = np.array([0.0, .01, .02, .03, .04, .05, .055, .06, .065, .07, .08, .09, .105, .12,
                  .135, .155, .17]); NF = len(FGRID)
LU0 = np.log10(0.5); SIGU = 0.10
LUD = LU0 + np.arange(-0.65, 0.6501, 0.05); NUD = len(LUD)          # banked disk axis (27)
LUB0 = np.log10(0.7)
LUB = LUB0 + np.arange(-0.80, 0.8001, 0.05); NUB = len(LUB)         # bulge axis (33), open in cache
TOP3 = ("UGC06787", "IC4202", "NGC7814")

# ----------------------------------------------------------------------------- cache builder
def build(sample, nu, unlock, ngrid=13, span=3.5, tag=""):
    """Corrected data-space likelihood; (d,i) marginalized; returns per-galaxy T[NA,NF,NUD,NUBg]
    (NUBg = NUB if unlock and the galaxy has a bulge, else 1 with U_bul irrelevant/locked).
    locked: gbar = gas + U_d*(Vd^2 + 1.4*Vb^2);  unlocked: gbar = gas + U_d*Vd^2 + U_b*Vb^2."""
    out = []; t0 = time.time()
    Ud = 10.0**LUD; Ub = 10.0**LUB
    for k, g in enumerate(sample):
        Rm = g["R"]*kpc; sd = g["eD"]/g["D0"]
        dgr = np.linspace(max(1 - span*sd, 0.15), 1 + span*sd, ngrid)
        ilo = max(g["i0"] - span*g["ei"], 10.0); ihi = min(g["i0"] + span*g["ei"], 89.9)
        igr = np.linspace(min(ilo, ihi - 0.2), ihi, ngrid)
        t = np.sin(np.radians(igr))/np.sin(np.radians(g["i0"]))
        pdi = (((dgr - 1)/sd)**2)[:, None] + (((igr - g["i0"])/g["ei"])**2)[None, :]  # CORRECTED norm
        gas = np.sign(g["Vg"])*g["Vg"]**2
        blg = unlock and np.any(g["Vb"] != 0)
        if blg:
            star = Ud[:, None, None]*(g["Vd"]**2)[None, None, :] \
                 + Ub[None, :, None]*(g["Vb"]**2)[None, None, :]              # [NUD,NUB,j]
            gbar = ((gas[None, None, :] + star)*1e6/Rm[None, None, :]).reshape(NUD*NUB, -1)
            nub = NUB
        else:
            star = g["Vd"]**2 + (0.0 if unlock else 1.4)*g["Vb"]**2
            gbar = (gas[None, :] + Ud[:, None]*star[None, :])*1e6/Rm[None, :]  # [NUD,j]
            nub = 1
        msk = gbar[0] > 0                     # positive at joint U-min => positive on grid
        gb = gbar[:, msk]; Ru = Rm[msk]; Vo = g["Vo"][msk]; eV = g["eV"][msk]
        nU = gb.shape[0]
        sqd = np.sqrt(dgr)
        sdt = sqd[:, None]*t[None, :]; dt2 = dgr[:, None]*(t**2)[None, :]      # [d,i]
        s02 = eV[None, :]**2 + (FGRID[:, None]*Vo[None, :])**2                 # [NF,j]
        iv = 1.0/s02; VoIv = Vo[None, :]*iv
        A_ = (Vo[None, :]**2*iv).sum(1); norm0 = np.log(2*np.pi*s02).sum(1)    # [NF]
        T = np.empty((NA, NF, nU))
        for ia in range(NA):
            Vm0 = np.sqrt(nu(gb/A0GRID[ia])*gb*Ru[None, :])/1e3                # [nU,j]
            B0 = (Vm0[None, :, :]*VoIv[:, None, :]).sum(2)                     # [NF,nU]
            C0 = ((Vm0**2)[None, :, :]*iv[:, None, :]).sum(2)                  # [NF,nU]
            X = ((A_ + norm0)[:, None, None, None] + pdi[None, None, :, :]
                 - 2.0*B0[:, :, None, None]*sdt[None, None, :, :]
                 + C0[:, :, None, None]*dt2[None, None, :, :])                 # [NF,nU,d,i]
            Xf = X.reshape(NF, nU, -1); xm = Xf.min(-1)
            T[ia] = -0.5*xm + np.log(np.mean(np.exp(-0.5*(Xf - xm[..., None])), -1))
        assert np.isfinite(T).all(), f"non-finite lnL for {g['name']}"
        out.append(T.reshape(NA, NF, NUD, nub))
        if (k + 1) % 40 == 0: print(f"    [{tag}] {k+1}/{len(sample)} ({time.time()-t0:.0f}s)")
    print(f"    [{tag}] done: {len(sample)} galaxies, {time.time()-t0:.0f}s")
    return out

# ----------------------------------------------------------------------------- combines
def combine(Tlist, sigUb=0.10, lu0b=LUB0, idxd=None, idxb=None):
    """apply U priors (disk always; bulge only where the axis is open) -> G[gal,NA,NF]"""
    idxd = np.arange(NUD) if idxd is None else idxd
    G = np.empty((len(Tlist), NA, NF))
    pud = ((LUD[idxd] - LU0)/SIGU)**2
    for k, T in enumerate(Tlist):
        W = T[:, :, idxd, :] - 0.5*pud[None, None, :, None]
        if T.shape[3] > 1:
            ib = np.arange(NUB) if idxb is None else idxb
            W = W[:, :, :, ib] - 0.5*(((LUB[ib] - lu0b)/sigUb)**2)[None, None, None, :]
        Wf = W.reshape(NA, NF, -1); wm = Wf.max(-1)
        G[k] = wm + np.log(np.mean(np.exp(Wf - wm[..., None]), -1))
    return G

def refine_peak(prof):
    i = int(np.argmax(prof))
    if i == 0 or i == NA - 1: return A0GRID[i]
    x0, x1, x2 = LNA0[i-1:i+2]; y0, y1, y2 = prof[i-1:i+2]
    den = (x0-x1)*(x0-x2)*(x1-x2)
    a = (x2*(y1-y0) + x1*(y0-y2) + x0*(y2-y1))/den
    b = (x2**2*(y0-y1) + x1**2*(y2-y0) + x0**2*(y1-y2))/den
    return float(np.exp(-b/(2*a))) if a < 0 else A0GRID[i]

def dchi2_interval(prof, level=1.0):
    dc = 2*(prof.max() - prof); i = int(np.argmin(dc)); lo = A0GRID[0]; hi = A0GRID[-1]
    for j in range(i, 0, -1):
        if dc[j-1] >= level:
            lo = np.exp(np.interp(level, [dc[j], dc[j-1]], [LNA0[j], LNA0[j-1]])); break
    for j in range(i, NA - 1):
        if dc[j+1] >= level:
            hi = np.exp(np.interp(level, [dc[j], dc[j+1]], [LNA0[j], LNA0[j+1]])); break
    return lo, hi

def analyze(tag, G, verbose=True):
    """global-f profiled scan (banked headline form)"""
    M = G.sum(axis=0); jf = int(np.argmax(M.max(axis=0))); prof = M.max(axis=1)
    dc = 2*(prof.max() - prof); a0hat = refine_peak(prof); lo, hi = dchi2_interval(prof)
    out = dict(a0hat=a0hat, lo=lo, hi=hi, dfw=dc[IA_FW], dfork=dc[IA_FORK], f=FGRID[jf],
               jf=jf, prof=prof, M=M)
    if verbose:
        print(f"  {tag:<52} a0_hat={a0hat:.3e} [{lo:.2e},{hi:.2e}] f={FGRID[jf]:.3f}")
        print(f"    {'':<50} Dchi2(9.36e-11)={dc[IA_FW]:8.2f} (~{np.sqrt(max(dc[IA_FW],0)):4.1f} sig)"
              f"  Dchi2(1.13e-10)={dc[IA_FORK]:7.2f} (~{np.sqrt(max(dc[IA_FORK],0)):4.1f} sig)")
    return out

def bootstrap(tag, G, nb=500, seed=7):
    rng = np.random.default_rng(seed); n = G.shape[0]; hats = np.empty(nb)
    for b in range(nb):
        hats[b] = refine_peak(G[rng.integers(0, n, n)].sum(axis=0).max(axis=1))
    med = np.median(hats); p16, p84 = np.percentile(hats, [16, 84])
    zfw = (med - A0FW)/max(med - p16, 1e-14) if A0FW < med else (A0FW - med)/max(p84 - med, 1e-14)
    zfk = (med - A0FORK)/max(med - p16, 1e-14) if A0FORK < med else (A0FORK - med)/max(p84 - med, 1e-14)
    print(f"  boot {tag:<38} med={med:.3e} [16,84]=[{p16:.2e},{p84:.2e}]  "
          f"P(<=9.36e-11)={np.mean(hats <= A0FW):.3f} (z~{zfw:.1f})  "
          f"P(<=1.13e-10)={np.mean(hats <= A0FORK):.3f} (z~{zfk:.1f})")
    return hats, zfw

# per-galaxy sigma_int (knob 2): truncated half-normal on the f grid, tau profiled
WF = np.empty(NF)
WF[1:-1] = (FGRID[2:] - FGRID[:-2])/2; WF[0] = (FGRID[1]-FGRID[0])/2; WF[-1] = (FGRID[-1]-FGRID[-2])/2
TAUS = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.065, 0.08, 0.10, 0.13, 0.17, 0.22])

def Lg_tau_stack(G):
    """per-galaxy f marginalized under half-normal(tau), normalized on grid -> [ntau,gal,NA]"""
    out = np.empty((len(TAUS), G.shape[0], NA))
    for q, tau in enumerate(TAUS):
        lw = np.log(WF) - 0.5*(FGRID/tau)**2
        lw -= lw.max(); lw -= np.log(np.exp(lw).sum())          # proper truncated prior mass
        W = G + lw[None, None, :]; wm = W.max(-1)
        out[q] = wm + np.log(np.exp(W - wm[..., None]).sum(-1))
    return out

def analyze_fpg(tag, G, verbose=True):
    Lt = Lg_tau_stack(G); S = Lt.sum(axis=1)                     # [ntau,NA]
    q = int(np.argmax(S.max(axis=1))); prof = S.max(axis=0)
    dc = 2*(prof.max() - prof); a0hat = refine_peak(prof); lo, hi = dchi2_interval(prof)
    if verbose:
        print(f"  {tag:<52} a0_hat={a0hat:.3e} [{lo:.2e},{hi:.2e}] tau_hat={TAUS[q]:.3f}")
        print(f"    {'':<50} Dchi2(9.36e-11)={dc[IA_FW]:8.2f} (~{np.sqrt(max(dc[IA_FW],0)):4.1f} sig)"
              f"  Dchi2(1.13e-10)={dc[IA_FORK]:7.2f} (~{np.sqrt(max(dc[IA_FORK],0)):4.1f} sig)")
    return dict(a0hat=a0hat, dfw=dc[IA_FW], dfork=dc[IA_FORK], tau=TAUS[q], Lt=Lt, prof=prof)

def bootstrap_fpg(tag, Lt, nb=500, seed=7):
    rng = np.random.default_rng(seed); n = Lt.shape[1]; hats = np.empty(nb)
    for b in range(nb):
        hats[b] = refine_peak(Lt[:, rng.integers(0, n, n), :].sum(axis=1).max(axis=0))
    med = np.median(hats); p16, p84 = np.percentile(hats, [16, 84])
    zfw = (med - A0FW)/max(med - p16, 1e-14) if A0FW < med else (A0FW - med)/max(p84 - med, 1e-14)
    print(f"  boot {tag:<38} med={med:.3e} [16,84]=[{p16:.2e},{p84:.2e}]  "
          f"P(<=9.36e-11)={np.mean(hats <= A0FW):.3f} (z~{zfw:.1f})  "
          f"P(<=1.13e-10)={np.mean(hats <= A0FORK):.3f}")
    return hats, zfw

# ================================================================= GATE V1: corrected baseline
print("\nGATE V1 -- corrected-likelihood baseline reproduction (U_bul LOCKED = 1.4*U_disk)")
T_lock = build(gals, nu_fw, unlock=False, tag="locked")
G_base = combine(T_lock)
r_base = analyze(f"BASELINE locked, full (N={NG})", G_base)
r_bgas = analyze(f"BASELINE locked, gas-dom (N={sel_gas.sum()})", G_base[sel_gas])
h_base, z_base = bootstrap("BASELINE full", G_base)
if not SMOKE:
    assert abs(np.log(r_base["a0hat"]/1.37e-10)) < 0.02, "V1 FAIL: full optimum drifted"
    assert abs(np.log(r_bgas["a0hat"]/9.8e-11)) < 0.04, "V1 FAIL: gas-dom center drifted"
    assert r_base["dfw"] > 9 and 2.5 < z_base < 4.5, "V1 FAIL: exclusion strength drifted"
    print("GATE V1: PASS (banked corrected numbers reproduced: 1.37e-10 full / 9.8e-11 gas-dom / "
          f"boot z~{z_base:.1f})")

# influence audit (baseline): confirm the named top influencers
jf = r_base["jf"]; ia_hat = int(np.argmax(r_base["M"][:, jf]))
infl = 2*(G_base[:, ia_hat, jf] - G_base[:, IA_FW, jf]); order = np.argsort(infl)[::-1]
print("  top-5 pull-away galaxies (baseline):",
      [(gals[k]["name"], round(float(infl[k]), 1)) for k in order[:5]])
i_top3 = np.array([next(i for i, g in enumerate(gals) if g["name"] == n) for n in TOP3])
sel_top3 = np.zeros(NG, bool); sel_top3[i_top3] = True
print(f"  pre-registered bulge-heavy subset: {TOP3}, Dchi2 contribs "
      f"{[round(float(infl[i]),1) for i in i_top3]}, sum={infl[i_top3].sum():.1f} "
      f"of full-sample {r_base['dfw']:.1f}")

# ================================================================= build unlocked (bulge gals only)
print("\nbuilding UNLOCKED U_bul cache (bulge galaxies only; no-bulge reuse locked arrays)...")
ib = np.where(hasb)[0]
T_blg = build([gals[i] for i in ib], nu_fw, unlock=True, tag="unlock-bulge")
T_unl = list(T_lock)
for j, i in enumerate(ib): T_unl[i] = T_blg[j]

# ================================================================= GATE V2: mock through unlocked
print("\nGATE V2 -- mock injection (truth a0=9.36e-11, U_d=0.5, U_b=0.7) through UNLOCKED machinery")
rng = np.random.default_rng(42); mock = []
for g in gals:
    Rm = g["R"]*kpc
    gb = (np.sign(g["Vg"])*g["Vg"]**2 + 0.5*g["Vd"]**2 + 0.7*g["Vb"]**2)*1e6/Rm; ok = gb > 0
    Vm = np.sqrt(nu_fw(gb[ok]/A0FW)*gb[ok]*Rm[ok])/1e3
    g2 = dict(g)
    for key in ("R", "Vg", "Vd", "Vb", "eV"): g2[key] = g[key][ok]
    g2["Vo"] = Vm + rng.normal(0, g2["eV"])
    if (g2["Vo"] > 0).all() and len(g2["Vo"]) >= 5: mock.append(g2)
T_mock = build(mock, nu_fw, unlock=True, tag="mock-unlocked")
r_mock = analyze(f"MOCK unlocked (N={len(mock)}), sigUb=0.10", combine(T_mock, sigUb=0.10))
bias = r_mock["a0hat"]/A0FW - 1
r_mockf = analyze_fpg("MOCK unlocked + per-galaxy sigma_int", combine(T_mock, sigUb=0.10), verbose=False)
print(f"GATE V2: recovered {r_mock['a0hat']:.3e} vs truth {A0FW:.3e} (bias {100*bias:+.1f}%), "
      f"Dchi2(truth)={r_mock['dfw']:.2f}; per-gal-f variant: {r_mockf['a0hat']:.3e}, "
      f"Dchi2(truth)={r_mockf['dfw']:.2f}, tau_hat={r_mockf['tau']:.2f}")
if not SMOKE:
    assert abs(bias) < 0.05 and r_mock["dfw"] < 4.0, "V2 FAIL: unlocked machinery biased"
    assert abs(r_mockf["a0hat"]/A0FW - 1) < 0.05 and r_mockf["dfw"] < 4.0, "V2 FAIL: per-gal-f biased"
    print("GATE V2: PASS (both knob machineries recover the injected framework value unbiased)")
del T_mock

# ================================================================= (1) KNOB 1: U_bul unlocked
print("\n" + "="*100)
print("(1) KNOB 1 -- U_bul UNLOCKED: independent per-galaxy lognormal prior, joint with U_disk,D,i")
print("="*100)
G_u10 = combine(T_unl, sigUb=0.10)
G_u15 = combine(T_unl, sigUb=0.15)
res = {}
for tag, G in (("locked (baseline)", G_base), ("UNLOCKED 0.10 dex", G_u10), ("UNLOCKED 0.15 dex", G_u15)):
    print(f"--- {tag} ---")
    res[tag] = dict(
        full=analyze(f"full (N={NG})", G),
        top3=analyze("top-3 bulge influencers ALONE", G[sel_top3]),
        no3=analyze("full MINUS top-3", G[~sel_top3]),
        gas=analyze(f"gas-dom (N={sel_gas.sum()})", G[sel_gas]))
h_u10, z_u10 = bootstrap("UNLOCKED 0.10 full", G_u10)
h_u15, z_u15 = bootstrap("UNLOCKED 0.15 full", G_u15)
h_no3, z_no3 = bootstrap("UNLOCKED 0.10 minus top-3", G_u10[~sel_top3])

# U_bul posterior modes for the top-3 (at joint a0_hat vs at 9.36e-11), edge-pinning check
print("\n  U_bul posterior modes (unlocked 0.10; d,i marginalized), grid span 0.7x10^[-0.8,+0.8]:")
pud = ((LUD - LU0)/SIGU)**2; pub10 = ((LUB - LUB0)/0.10)**2
r1 = res["UNLOCKED 0.10 dex"]["full"]; ia1 = int(np.argmin(abs(LNA0 - np.log(r1["a0hat"]))))
nedge = 0
for j, i in enumerate(ib):
    W = T_blg[j] - 0.5*pud[None, None, :, None] - 0.5*pub10[None, None, None, :]
    for ia, lab in ((ia1, "a0_hat"), (IA_FW, "9.36e-11")):
        ud, ubb = np.unravel_index(int(np.argmax(W[ia, r1["jf"]])), (NUD, NUB))
        if ubb in (0, NUB - 1): nedge += 1
        if gals[i]["name"] in TOP3:
            print(f"    {gals[i]['name']:<10} at {lab:<9}: U_d={10**LUD[ud]:.2f}  U_b={10**LUB[ubb]:.2f}")
print(f"  bulge-galaxy U_b modes pinned at grid edge: {nedge}/{2*len(ib)} evaluations")

# ================================================================= (2) KNOB 2: sigma_int form
print("\n" + "="*100)
print("(2) KNOB 2 -- sigma_int: GLOBAL profiled (banked) vs PER-GALAXY hierarchical half-normal(tau)")
print("="*100)
r_fpg_lock = analyze_fpg("locked + PER-GALAXY f (half-normal, tau profiled)", G_base)
r_fpg_unl  = analyze_fpg("UNLOCKED 0.10 + PER-GALAXY f (JOINT: both knobs)", G_u10)
Gfree = G_base.max(axis=2, keepdims=True)  # per-galaxy FREE f (extreme; Neyman-Scott caveat)
r_free = analyze("locked + per-galaxy f FREE-profiled (extreme)", Gfree)
h_fpgl, z_fpgl = bootstrap_fpg("locked + per-gal f", r_fpg_lock["Lt"])
h_fpgu, z_fpgu = bootstrap_fpg("JOINT both knobs", r_fpg_unl["Lt"])

# ================================================================= (3) gas-dom under both knobs
print("\n" + "="*100)
print("(3) GAS-DOMINATED cut under both knobs (expected insensitive)")
print("="*100)
print(f"  baseline: {r_bgas['a0hat']:.3e} | unlocked 0.10: {res['UNLOCKED 0.10 dex']['gas']['a0hat']:.3e} "
      f"| unlocked 0.15: {res['UNLOCKED 0.15 dex']['gas']['a0hat']:.3e}")
r_gasf  = analyze_fpg("gas-dom, locked + per-galaxy f", G_base[sel_gas])
r_gasfu = analyze_fpg("gas-dom, JOINT both knobs", G_u10[sel_gas])

# ================================================================= convergence checks
print("\n--- grid convergence ---")
r_full10 = res["UNLOCKED 0.10 dex"]["full"]
rc1 = analyze("U_b grid step 0.05->0.10 (column subsample)",
              combine(T_unl, sigUb=0.10, idxb=np.arange(0, NUB, 2)), verbose=False)
rc2 = analyze("U_d grid step 0.05->0.10 (column subsample)",
              combine(T_unl, sigUb=0.10, idxd=np.arange(0, NUD, 2)), verbose=False)
print(f"  LUB step x2:  a0_hat {r_full10['a0hat']:.3e} -> {rc1['a0hat']:.3e}; "
      f"Dchi2(fw) {r_full10['dfw']:.1f} -> {rc1['dfw']:.1f}")
print(f"  LUD step x2:  a0_hat -> {rc2['a0hat']:.3e}; Dchi2(fw) -> {rc2['dfw']:.1f}")
T_dense = build([gals[i] for i in ib], nu_fw, unlock=True, ngrid=17, span=4.0, tag="dense-bulge")
T_unl_d = list(T_lock)
for j, i in enumerate(ib): T_unl_d[i] = T_dense[j]
rc3 = analyze("dense (d,i) 13->17, span 3.5->4.0 on bulge gals",
              combine(T_unl_d, sigUb=0.10), verbose=False)
print(f"  dense (d,i):  a0_hat -> {rc3['a0hat']:.3e}; Dchi2(fw) -> {rc3['dfw']:.1f}; "
      f"Dchi2(fork) -> {rc3['dfork']:.1f}")
conv_ok = (abs(np.log(rc1["a0hat"]/r_full10["a0hat"])) < 0.02 and
           abs(np.log(rc2["a0hat"]/r_full10["a0hat"])) < 0.02 and
           abs(np.log(rc3["a0hat"]/r_full10["a0hat"])) < 0.03 and
           abs(rc3["dfw"] - r_full10["dfw"]) < 0.15*max(r_full10["dfw"], 10))
print(f"  convergence: {'OK' if conv_ok else 'NOT CONVERGED'}")
if not SMOKE: assert conv_ok, "grids not converged"

# ================================================================= pre-registered verdict
print("\n" + "="*100); print("PRE-REGISTERED VERDICT"); print("="*100)
u10, u15 = res["UNLOCKED 0.10 dex"]["full"], res["UNLOCKED 0.15 dex"]["full"]
collapse = ((0.9e-10 <= u10["a0hat"] <= 1.1e-10) or u10["dfw"] < 9 or z_u10 < 3 or
            (0.9e-10 <= r_fpg_lock["a0hat"] <= 1.1e-10) or r_fpg_lock["dfw"] < 9 or z_fpgl < 3)
hard = (u10["dfw"] > 9 and z_u10 > 3 and u15["dfw"] > 9 and
        r_fpg_lock["dfw"] > 9 and z_fpgl > 3 and r_fpg_unl["dfw"] > 9 and z_fpgu > 3)
print(f"  knob1 U_bul 0.10: a0_hat={u10['a0hat']:.3e} Dchi2(fw)={u10['dfw']:.1f} boot-z~{z_u10:.1f}; "
      f"0.15: {u15['a0hat']:.3e}/{u15['dfw']:.1f}")
print(f"  knob2 per-gal f:  a0_hat={r_fpg_lock['a0hat']:.3e} Dchi2(fw)={r_fpg_lock['dfw']:.1f} "
      f"boot-z~{z_fpgl:.1f}; JOINT: {r_fpg_unl['a0hat']:.3e}/{r_fpg_unl['dfw']:.1f}/z~{z_fpgu:.1f}")
print(f"  minus-top-3 (unlocked): a0_hat={res['UNLOCKED 0.10 dex']['no3']['a0hat']:.3e} "
      f"Dchi2(fw)={res['UNLOCKED 0.10 dex']['no3']['dfw']:.1f} boot-z~{z_no3:.1f}")
if hard and not collapse:
    print("  => SURVIVES >3 sigma under BOTH knobs (and jointly): the full-sample exclusion of "
          "9.36e-11 HARDENS per pre-registration; Sec 3 update note warranted.")
elif collapse:
    print("  => COLLAPSES per pre-registration: downgrade the full-sample exclusion to "
          "bulge-M/L / error-model systematics.")
else:
    print("  => MIXED: neither pre-registered branch cleanly met -- report numbers as stated.")
print(f"\ntotal runtime {time.time()-t_start:.0f}s")
print("EXIT 0 = all gates + convergence passed")
