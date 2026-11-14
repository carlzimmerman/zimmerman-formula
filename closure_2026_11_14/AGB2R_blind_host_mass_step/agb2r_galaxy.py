"""AGB2R galaxy host-age model (blind re-implementation from AGB2's FROZEN_CRITERIA.md; reading in READING.md).

Childress, Wolf & Zahid (2014) recipe as the criteria state it: main sequence 2.00 e^{1.33 z} (M/1e10)^0.7 Msun/yr,
mass quenching p_Q = 0.5 [1 - erf((log M - log M_Q(z))/1.5)], mass loss f_ml(t) = 0.046 ln(t / 0.276 Myr + 1),
seed 1e6 Msun, flat Om = 0.30, H0 = 70. Progenitor ages weighted by SFR(t - tau) x DTD(tau).
No supernova magnitude is read here.

Usage: python3 agb2r_galaxy.py            builds the tables (base, alt-MQ, T_W DTD) and runs check KG
Writes agb2r_tables.npz and agb2r_KG.json; prints the comparison with the values quoted in the criteria.
"""
import json, os, sys
for _v in ("VECLIB_MAXIMUM_THREADS", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import numpy as np
from scipy.special import erf

HERE = os.path.dirname(os.path.abspath(__file__))
GYR_H0 = 977.7922216807891          # 1/(1 km/s/Mpc) in Gyr
H0, OM = 70.0, 0.30
ZG = np.round(np.arange(0, 1.6 + 1e-9, 0.02), 2)          # 81 redshifts
MG = np.round(np.arange(7.5, 12.4 + 1e-9, 0.05), 2)       # 99 masses


def logmq_c14(z):
    z = np.asarray(z, float)
    return np.where(z <= 1.5, 10.43 + 0.9*np.log10(1 + z), 8.56 + 5.6*np.log10(1 + z))


def logmq_alt(z):
    return 10.077 + 0.636*np.asarray(z, float)


def dtd_c14(t):
    x = np.asarray(t, float)/0.3
    return x**20/(x**21 + 1)


def dtd_w(t):
    t = np.asarray(t, float)
    return np.where(t >= 0.04, np.maximum(t, 1e-30)**-1.13, 0.0)


def fml(age_gyr):
    return 0.046*np.log(np.asarray(age_gyr)*1000.0/0.276 + 1.0)


class Cosmo:
    """t(z) and z(t) for flat Om = 0.30, H0 = 70, no radiation."""
    def __init__(s):
        x = np.linspace(0, np.log(1 + 1e4), 400001); z = np.expm1(x)
        f = 1/np.sqrt(OM*(1 + z)**3 + 1 - OM)
        cum = np.concatenate([[0.0], np.cumsum(0.5*(f[1:] + f[:-1])*np.diff(x))])
        tail = (2/3)/np.sqrt(OM)*(1 + z[-1])**-1.5
        s.z = z; s.t = (cum[-1] - cum + tail)*GYR_H0/H0          # Gyr, decreasing in z
        s.t0 = float(s.t[0])

    def t_of_z(s, z):
        return np.interp(z, s.z, s.t)

    def z_of_t(s, t):
        return np.interp(t, s.t[::-1], s.z[::-1])


def build(dt=0.004, logmq=logmq_c14, dtd=dtd_c14, form_every=0.024, look_first=13.0, n_form=541, nsub=16):
    """Integrate all tracks on one absolute time grid. Returns a dict with the tables and the raw tracks."""
    C = Cosmo()
    nst = int(round(look_first/dt))                    # steps from the first formation time to now
    tb = C.t0 - look_first + dt*np.arange(nst + 1)     # boundaries (absolute time, Gyr)
    zb = C.z_of_t(tb)
    every = int(round(form_every/dt))
    nk = every*np.arange(n_form)                       # start boundary of each track
    K = n_form
    w_surv = 1.0 - fml((np.arange(nst) + 0.5)*dt)      # surviving fraction of a step formed m+1 steps before
    seed_surv = lambda age: 1.0 - fml(np.maximum(age, 0.0))
    formedT = np.zeros((nst, K))                       # formedT[j, k]: mass formed by track k in step j
    S = np.zeros((K, nst + 1))                         # surviving mass at each boundary
    active0 = nk == 0
    S[active0, 0] = 1e6
    for n in range(nst):
        act = nk <= n
        if n > 0:
            sm = w_surv[n - 1::-1]@formedT[:n]
            age_seed = (n - nk)*dt
            S[:, n] = np.where(act, 1e6*seed_surv(age_seed) + sm, 0.0)
        M = S[act, n]
        pq = 0.5*(1 - erf((np.log10(M) - logmq(zb[n]))/1.5))
        inc = 0.3*2.00*np.exp(1.33*zb[n])*pq*1e-7*dt*1e9
        Mend = (M**0.3 + inc)**(1/0.3)
        formedT[n, act] = Mend - M
    sm = w_surv[::-1]@formedT
    formed = np.ascontiguousarray(formedT.T)
    S[:, nst] = np.where(nk <= nst, 1e6*seed_surv((nst - nk)*dt) + sm, 0.0)
    # DTD averaged over each step of delay: step m covers tau in [m dt, (m+1) dt]
    sub = (np.arange(nst)[:, None] + (np.arange(nsub) + 0.5)[None, :]/nsub)*dt
    ph = dtd(sub); phi_bar = ph.mean(1); tphi_bar = (sub*ph).mean(1)
    out = dict(dt=dt, tb=tb, zb=zb, nk=nk, S=S, formed=formed, t0=C.t0, cosmo=C)
    mean_t = np.full((len(ZG), len(MG)), np.nan); med_t = np.full_like(mean_t, np.nan); topflat = []
    for iz, z in enumerate(ZG):
        n = int(round((C.t_of_z(z) - tb[0])/dt))
        ex = np.where(nk < n)[0]                        # tracks with at least one formed step
        F = formed[ex, :n][:, ::-1]                     # column m = delay step m
        wphi = F*phi_bar[:n]; wt = F*tphi_bar[:n]
        norm = wphi.sum(1); ok = norm > 0               # a track younger than the shortest delay has no supernovae yet
        ex, F, wphi, wt, norm = ex[ok], F[ok], wphi[ok], wt[ok], norm[ok]
        mean = wt.sum(1)/norm
        cw = np.cumsum(wphi, 1)/norm[:, None]
        med = np.empty(len(ex))
        for r in range(len(ex)):
            m = int(np.searchsorted(cw[r], 0.5))
            lo = cw[r, m - 1] if m > 0 else 0.0
            med[r] = (m + (0.5 - lo)/(cw[r, m] - lo))*dt
        lm = np.log10(S[ex, n])
        o = np.argsort(lm); lm, mean, med = lm[o], mean[o], med[o]
        if np.any(np.diff(lm) <= 0): raise RuntimeError(f"mass not monotonic in formation time at z {z}")
        mean_t[iz] = np.interp(MG, lm, mean); med_t[iz] = np.interp(MG, lm, med)   # flat beyond the ends
        if lm[-1] < MG[-1]: topflat.append((float(z), float(lm[-1])))
        if lm[0] > MG[0]: raise RuntimeError(f"lightest track above the grid at z {z}")
    out.update(mean=mean_t, median=med_t, topflat=topflat)
    return out


def tables_from_npz(path=os.path.join(HERE, "agb2r_tables.npz")):
    return dict(np.load(path))


class AgeModel:
    """Bilinear tau(log M, z) on the tables; masses clipped to [7.5, 12.4]; shift in dex applied before clipping."""
    def __init__(s, tab, kind="mean", shift=0.0):
        s.T = tab[kind]; s.shift = shift

    def __call__(s, logm, z):
        logm = np.clip(np.asarray(logm, float) + s.shift, MG[0], MG[-1]); z = np.clip(np.asarray(z, float), ZG[0], ZG[-1])
        fz = (z - ZG[0])/0.02; iz = np.minimum(np.floor(fz).astype(int), len(ZG) - 2); uz = fz - iz
        fm = (logm - MG[0])/0.05; im = np.minimum(np.floor(fm).astype(int), len(MG) - 2); um = fm - im
        T = s.T
        return ((1 - uz)*(1 - um)*T[iz, im] + uz*(1 - um)*T[iz + 1, im] + (1 - uz)*um*T[iz, im + 1] + uz*um*T[iz + 1, im + 1])


def formed_quantiles_z0(B, logm_target=11.5, qs=(0.25, 0.5, 0.75)):
    """Lookback (Gyr) by which a fraction q of the formed mass had formed, for the z = 0 track of mass logm_target."""
    nst = B["formed"].shape[1]; lm = np.log10(np.maximum(B["S"][:, nst], 1e-30))
    order = np.argsort(lm); k_hi = order[np.searchsorted(lm[order], logm_target)]; k_lo = order[np.searchsorted(lm[order], logm_target) - 1]
    look_mid = (nst - np.arange(nst) - 0.5)*B["dt"]     # lookback of each step's middle

    def qk(k):
        f = B["formed"][k]; c = np.cumsum(f)/f.sum()
        return np.array([np.interp(q, c, look_mid[:]) for q in qs])  # cumulative rises as lookback falls
    a, b = qk(k_lo), qk(k_hi); u = (logm_target - lm[k_lo])/(lm[k_hi] - lm[k_lo])
    return (1 - u)*a + u*b, float(lm[k_lo]), float(lm[k_hi])


def main():
    res = {}
    base = build()
    # KG (i)
    mq035 = float(logmq_c14(0.35)); b1 = 10.43 + 0.9*np.log10(2.5); b2 = 8.56 + 5.6*np.log10(2.5)
    kg1 = abs(mq035 - 10.55) <= 0.01 and abs(b1 - b2) <= 0.005
    # KG (ii)
    am = AgeModel(dict(mean=base["mean"]), "mean")
    a8, a10, a115, a12 = (float(am(m, 0.0)) for m in (8.0, 10.0, 11.5, 12.0))
    frac = (a115 - a10)/(a12 - a8); kg2 = frac >= 0.5
    # KG (iii)
    q, lmlo, lmhi = formed_quantiles_z0(base)
    half, width = float(q[1]), float(q[0] - q[2])
    kg3 = 8.0 <= half <= 11.5 and width <= 2.0
    # KG (iv)
    fine = build(dt=0.002)
    dmean = float(np.nanmax(np.abs(fine["mean"] - base["mean"]))); dmed = float(np.nanmax(np.abs(fine["median"] - base["median"])))
    kg4 = dmean <= 0.05 and dmed <= 0.05
    res["KG"] = dict(i=dict(logMQ_035=mq035, branch_lo_15=b1, branch_hi_15=b2, passed=bool(kg1)),
                     ii=dict(mean_ages_z0={"8": a8, "10": a10, "11.5": a115, "12": a12}, fraction=frac, passed=bool(kg2)),
                     iii=dict(q25_q50_q75_lookback=[float(v) for v in q], half=half, middle_half_width=width,
                              bracketing_logM=[lmlo, lmhi], passed=bool(kg3)),
                     iv=dict(max_dmean=dmean, max_dmedian=dmed, passed=bool(kg4)),
                     passed=bool(kg1 and kg2 and kg3 and kg4))
    print(f"KG (i) log M_Q(0.35) = {mq035:.4f} (10.55 +- 0.01); branches at z 1.5: {b1:.4f} {b2:.4f} -> {'PASS' if kg1 else 'FAIL'}")
    print(f"KG (ii) z = 0 mean ages at log M 8, 10, 11.5, 12: {a8:.3f} {a10:.3f} {a115:.3f} {a12:.3f}; fraction of the rise in 10-11.5 = {frac:.3f} (>= 0.5) -> {'PASS' if kg2 else 'FAIL'}")
    print(f"KG (iii) log M 11.5 track at z = 0 (between tracks of log M {lmlo:.3f}, {lmhi:.3f}): lookback of 25/50/75 % formed mass"
          f" {q[0]:.3f} {q[1]:.3f} {q[2]:.3f} Gyr; half {half:.3f} in [8, 11.5], middle half {width:.3f} <= 2 -> {'PASS' if kg3 else 'FAIL'}")
    print(f"KG (iv) dt 2 Myr vs 4 Myr: max |d mean| {dmean:.4f}, max |d median| {dmed:.4f} Gyr (<= 0.05) -> {'PASS' if kg4 else 'FAIL'}")
    print(f"KG -> {'PASS' if res['KG']['passed'] else 'FAIL'}")
    print(f"tables flat above the most massive track at: {[(z, round(m, 3)) for z, m in base['topflat']][:6]} ... ({len(base['topflat'])} redshifts)")
    # comparison with the values quoted in the criteria
    crit_mean = {0.0: [1.02, 1.65, 3.07, 4.47, 6.48, 8.71, 10.45], 0.5: [0.68, 1.02, 1.74, 2.42, 3.43, 4.64, 5.73],
                 1.0: [0.48, 0.67, 1.05, 1.40, 1.93, 2.60, 3.28]}
    crit_med0 = [0.77, 1.14, 2.20, 3.87, 7.56, 10.53, 11.42]
    ms = [8, 9, 10, 10.5, 11, 11.5, 12]; amed = AgeModel(dict(median=base["median"]), "median")
    cmp = {}
    for z, vals in crit_mean.items():
        mine = [float(am(m, z)) for m in ms]
        cmp[f"mean_z{z}"] = dict(mine=mine, criteria=vals, diff=[a - b for a, b in zip(mine, vals)])
        print(f"mean age z {z}: mine " + " ".join(f"{v:6.2f}" for v in mine) + " | criteria " + " ".join(f"{v:6.2f}" for v in vals))
    mine = [float(amed(m, 0.0)) for m in ms]
    cmp["median_z0"] = dict(mine=mine, criteria=crit_med0, diff=[a - b for a, b in zip(mine, crit_med0)])
    print("median age z 0: mine " + " ".join(f"{v:6.2f}" for v in mine) + " | criteria " + " ".join(f"{v:6.2f}" for v in crit_med0))
    res["compare_criteria_table"] = cmp
    # model forks
    alt = build(logmq=logmq_alt); tw = build(dtd=dtd_w)
    np.savez(os.path.join(HERE, "agb2r_tables.npz"), z=ZG, logm=MG, mean=base["mean"], median=base["median"],
             mean_altMQ=alt["mean"], median_altMQ=alt["median"], mean_TW=tw["mean"], median_TW=tw["median"])
    res["topflat"] = dict(base=base["topflat"], altMQ=alt["topflat"], TW=tw["topflat"])
    print("alt-MQ mean age z 0: " + " ".join(f"{float(AgeModel(dict(mean=alt['mean']))(m, 0.0)):6.2f}" for m in ms))
    print("T_W    mean age z 0: " + " ".join(f"{float(AgeModel(dict(mean=tw['mean']))(m, 0.0)):6.2f}" for m in ms))
    with open(os.path.join(HERE, "agb2r_KG.json"), "w") as fh: json.dump(res, fh, indent=1)
    print("wrote agb2r_tables.npz, agb2r_KG.json")


if __name__ == "__main__":
    main()
