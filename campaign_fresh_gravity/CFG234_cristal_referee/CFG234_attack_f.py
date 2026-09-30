"""CFG234 attack (f): Monte Carlo through the table's own asymmetric errors (split-normal, independent, truncated), N = 20,000 per disc, seed 234. Exit 0."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG234_common import *

t = start("CFG234_attack_f")
N = 20000
rng = np.random.default_rng(234)
df = load_cristal()


def split_normal(med, ehi, elo, n, lo_bound, hi_bound):
    """split-normal about med with upper scale ehi, lower scale elo; NaN error -> fixed. rejection sampling into [lo_bound, hi_bound]."""
    if not np.isfinite(ehi) and not np.isfinite(elo):
        return np.full(n, med)
    ehi = ehi if np.isfinite(ehi) else elo
    elo = elo if np.isfinite(elo) else ehi
    out = np.empty(0)
    tries = 0
    while len(out) < n and tries < 60:
        u = rng.standard_normal(3 * n)
        x = np.where(u > 0, med + u * ehi, med + u * elo)
        x = x[(x > lo_bound) & (x < hi_bound)]
        out = np.concatenate([out, x]); tries += 1
    if len(out) < n:
        out = np.concatenate([out, np.full(n - len(out), np.clip(med, lo_bound + 1e-6, hi_bound - 1e-6))])
    return out[:n]


R = {}
per = {}
draws = {}
for i in ID14:
    r = df.loc[i]; e = r.e
    Re = split_normal(r.Re, e["Re"][0], e["Re"][1], N, 0.05, np.inf)
    Vr = split_normal(r.Vrot, e["Vrot"][0], e["Vrot"][1], N, 0.0, np.inf)
    sg = split_normal(r.sig, e["sig"][0], e["sig"][1], N, 1.0, np.inf)
    fd = split_normal(r.fDM, e["fDM"][0], e["fDM"][1], N, 0.0, 0.999)
    D = 1.0 / (1.0 - fd)
    Vc2 = Vr ** 2 + K0 * sg ** 2
    gb = gacc(np.sqrt(Vc2), Re) / D
    z = r.z
    dl_f = np.log10(D) - np.log10(nu_mono(gb / A0["canonical"]))
    dl_r = np.log10(D) - np.log10(nu_mono(gb / (A0["canonical"] * E_of_z(z))))
    draws[i] = (dl_f, dl_r)
    # point estimate
    pf = cell(df.loc[[i]])[0][0]; pr = cell(df.loc[[i]], rival=True)[0][0]
    per[i] = dict(point_flat=float(pf), point_rival=float(pr), mc_med_flat=float(np.median(dl_f)), mc_med_rival=float(np.median(dl_r)),
                  rival_p16=float(np.percentile(dl_r, 16)), rival_p84=float(np.percentile(dl_r, 84)),
                  P_rival_lt0=float(np.mean(dl_r < 0)), P_flat_gt0=float(np.mean(dl_f > 0)))
print("id     point_flat  MCmed_flat  P(flat>0) | point_rival MCmed_rival [16,84]      P(rival<0)")
for i in ID14:
    p = per[i]
    print(f"{i:5s}  {p['point_flat']:+8.3f}  {p['mc_med_flat']:+8.3f}   {p['P_flat_gt0']:.3f}   | {p['point_rival']:+8.3f}  {p['mc_med_rival']:+8.3f} [{p['rival_p16']:+.3f},{p['rival_p84']:+.3f}]   {p['P_rival_lt0']:.3f}{'  (EXCLUDED)' if i in EXCL else ''}")
R["per"] = per

for nm, ids in (("12", ID12), ("14", ID14)):
    mf = np.median(np.stack([draws[i][0] for i in ids]), axis=0)
    mr = np.median(np.stack([draws[i][1] for i in ids]), axis=0)
    pt_f = float(np.median([per[i]["point_flat"] for i in ids])); pt_r = float(np.median([per[i]["point_rival"] for i in ids]))
    out = {}
    for law, m, pt in (("flat", mf, pt_f), ("rival", mr, pt_r)):
        p16, p50, p84, p025, p975 = np.percentile(m, [16, 50, 84, 2.5, 97.5])
        cls = "under" if p975 < 0 else ("over" if p025 > 0 else "CONS")
        out[law] = dict(point=pt, mc_median=float(p50), p16=float(p16), p84=float(p84), p025=float(p025), p975=float(p975), cls=cls,
                        point_in_16_84=bool(p16 <= pt <= p84), bias=float(p50 - pt), P_lt0=float(np.mean(m < 0)), P_gt0=float(np.mean(m > 0)))
        print(f"n={nm} {law}: point-estimate median {pt:+.3f}; MC sample-median {p50:+.3f} [16-84 {p16:+.3f}, {p84:+.3f}; 95 % {p025:+.3f}, {p975:+.3f}]; bias {p50 - pt:+.3f}; point in 16-84: {p16 <= pt <= p84}; class of the 95 % range: {cls}; P(median<0) {np.mean(m < 0):.3f}")
    R[f"sample{nm}"] = out
n2 = sum(per[i]["P_rival_lt0"] > 0.975 for i in ID12)
n1 = sum(per[i]["P_rival_lt0"] > 0.84 for i in ID12)
print(f"discs individually excluding the rival (delta_rival < 0 in > 97.5 % of draws): {n2} of 12; > 84 % of draws: {n1} of 12")
R["n_indiv_2sigma"] = int(n2); R["n_indiv_1sigma"] = int(n1)
pass_f = R["sample12"]["rival"]["point_in_16_84"] and R["sample12"]["rival"]["cls"] == "under" and abs(R["sample12"]["rival"]["bias"]) <= 0.03
print("frozen pass line (rival: point in MC 16-84, class unchanged (under), |bias| <= 0.03):", "PASS" if pass_f else "FAIL/NARROW")
R["pass"] = bool(pass_f)

# ------------------------------------------------------------------------------------------------------------------------------
# F2 -- POST-HOC (written after F1 above showed a +0.044 bias in the rival median; NOT part of the frozen procedure, never a verdict).
# F1 rejects split-normal draws that leave the physical range, but the table's quantiles are already those of the bounded posterior, so
# the rejection shifts each disc's median (e.g. f_DM 0.07 with a lower error 0.06 loses its lower tail). F2 draws from the quantile function
# through (0, bound), (16 %, med-elo), (50 %, med), (84 %, med+ehi) with a Gaussian-scale tail above 84 % (bounded by 1 for f_DM), so each
# disc's own median is reproduced exactly.
def quantile_draw(med, ehi, elo, n, lb, ub):
    if not np.isfinite(ehi) and not np.isfinite(elo):
        return np.full(n, med)
    ehi = ehi if np.isfinite(ehi) else elo
    elo = elo if np.isfinite(elo) else ehi
    u = rng.uniform(size=n)
    x = np.empty(n)
    q16 = max(lb, med - elo); q84 = min(ub, med + ehi)
    a = u < 0.1587; b = (u >= 0.1587) & (u < 0.5); c = (u >= 0.5) & (u < 0.8413); d = u >= 0.8413
    x[a] = lb + (q16 - lb) * (u[a] / 0.1587)
    x[b] = q16 + (med - q16) * ((u[b] - 0.1587) / (0.5 - 0.1587))
    x[c] = med + (q84 - med) * ((u[c] - 0.5) / (0.8413 - 0.5))
    if np.isfinite(ub):
        x[d] = q84 + (ub - q84) * ((u[d] - 0.8413) / (1 - 0.8413))
    else:
        from scipy.special import ndtri
        zt = ndtri(u[d])          # >= 1
        x[d] = med + zt * ehi
    return x


draws2 = {}
per2 = {}
for i in ID14:
    r = df.loc[i]; e = r.e
    Re = quantile_draw(r.Re, e["Re"][0], e["Re"][1], N, 0.05, np.inf)
    Vr = quantile_draw(r.Vrot, e["Vrot"][0], e["Vrot"][1], N, 0.0, np.inf)
    sg = quantile_draw(r.sig, e["sig"][0], e["sig"][1], N, 1.0, np.inf)
    fd = quantile_draw(r.fDM, e["fDM"][0], e["fDM"][1], N, 0.0, 0.999)
    D = 1.0 / (1.0 - fd)
    gb = gacc(np.sqrt(Vr ** 2 + K0 * sg ** 2), Re) / D
    z = r.z
    draws2[i] = (np.log10(D) - np.log10(nu_mono(gb / A0["canonical"])), np.log10(D) - np.log10(nu_mono(gb / (A0["canonical"] * E_of_z(z)))))
    per2[i] = dict(P_rival_lt0=float(np.mean(draws2[i][1] < 0)), mc_med_rival=float(np.median(draws2[i][1])), mc_med_flat=float(np.median(draws2[i][0])))
print("\n== F2 (POST-HOC, quantile-function draws; not frozen) ==")
R2 = {}
for nm, ids in (("12", ID12), ("14", ID14)):
    for law, k in (("flat", 0), ("rival", 1)):
        m = np.median(np.stack([draws2[i][k] for i in ids]), axis=0)
        pt = float(np.median([per[i]["point_flat" if law == "flat" else "point_rival"] for i in ids]))
        p16, p50, p84, p025, p975 = np.percentile(m, [16, 50, 84, 2.5, 97.5])
        cls = "under" if p975 < 0 else ("over" if p025 > 0 else "CONS")
        R2[f"{nm}|{law}"] = dict(point=pt, mc_median=float(p50), p16=float(p16), p84=float(p84), p025=float(p025), p975=float(p975), cls=cls, bias=float(p50 - pt))
        print(f"n={nm} {law}: point {pt:+.3f}; MC sample-median {p50:+.3f} [16-84 {p16:+.3f}, {p84:+.3f}; 95 % {p025:+.3f}, {p975:+.3f}]; bias {p50 - pt:+.3f}; point in 16-84: {p16 <= pt <= p84}; class {cls}")
n2b = sum(per2[i]["P_rival_lt0"] > 0.975 for i in ID12)
print("F2 discs individually excluding the rival at > 97.5 %:", n2b, "of 12;", {i: round(per2[i]["P_rival_lt0"], 3) for i in ID12})
R["F2_posthoc"] = dict(sample=R2, per=per2, n_indiv_2sigma=int(n2b))

print("Caveats: independent draws (no covariance between V_rot, sigma_0, f_DM, R_e is available); table errors are those of the posterior summary; M_bary (logMtot) is not an input of D or g_bar here.")
savejson("CFG234_attack_f", R)
sys.exit(0)
