"""SRH1R neighbour term (own code): for every carried lens and g_bar cell, the summed 4 G DeltaSigma of its neighbours'
halos, each laid out with the same case as the lens, on a k grid.  One footing and case per run; checkpointed per k;
stops cleanly on SIGTERM.
Usage: python3 -I srh1r_nb.py <work dir> <footing> <case> [null]     ("null" adds the three permuted-position sums)
Output: <work dir>/nb_<footing>_<case>.npz  (real[k, lens, bin], null[k, lens, bin] = mean of the three permutations).
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, math, signal, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import srh1r_model as m

WORK, FOOT, CASE = sys.argv[1], sys.argv[2], sys.argv[3]; NULL = len(sys.argv) > 4 and sys.argv[4] == "null"
KNB = 0.5 * 2.0 ** (np.arange(7) * 4 / 6)                       # 0.5 ... 8, seven nodes
STOP = [False]; signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__(0, True))
L = np.load(os.path.join(WORK, "lens.npz")); PR = np.load(os.path.join(WORK, "pairs.npz")); T = m.table(FOOT, CASE, cache=os.path.join(WORK, "tables"))
zl, Mg, ged = L["z"], L["Mgal"], L["ged"]; NU, NB = len(zl), len(ged) - 1
R1 = np.sqrt(m.G_SI * Mg[:, None] * m.MSUN / ged[None, 1:]) / m.KPC; R2 = np.minimum(np.sqrt(m.G_SI * Mg[:, None] * m.MSUN / ged[None, :-1]) / m.KPC, 3000.0)

def nb_sum(li, lMj, d, k, chunk=40000):
    """Sum over pairs of the neighbour's cell means, per lens and bin (4 G DeltaSigma, m/s^2)."""
    out = np.zeros(NU * NB); lk = math.log10(k)
    for i0 in range(0, len(li), chunk):
        l_, lm_, d_ = li[i0:i0 + chunk], lMj[i0:i0 + chunk].astype("f8") + lk, d[i0:i0 + chunk]; z_ = zl[l_]
        E, Mt, bf = m.halo_scalars(T, lm_, z_); a, b = R1[l_], R2[l_]; ok = b > a
        sat = ok & (a >= (d_ + E)[:, None])                                       # halo wholly inside the inner circle: point mass
        v = np.where(sat, 2 * Mt[:, None] * np.log(np.where(ok, b, a * 2) / a) / (math.pi * (np.where(ok, b, a * 2) ** 2 - a ** 2)), 0.0)
        act = ok & ~sat & (b > (d_ - E)[:, None]); pi, ci = np.nonzero(act)
        if len(pi):
            v[pi, ci] = m.nb_cells(T, lm_[pi], z_[pi], d_[pi], a[pi, ci][:, None], b[pi, ci][:, None])[:, 0]
        out += np.bincount((l_[:, None] * NB + np.arange(NB)[None, :]).ravel(), v.ravel(), NU * NB)
    return out.reshape(NU, NB) * m.DCONV

OUTP = os.path.join(WORK, f"nb_{FOOT}_{CASE}.npz"); PART = OUTP + ".part.npz"
st = dict(np.load(PART)) if os.path.exists(PART) else {}
t0 = time.time()
for ik, k in enumerate(KNB):
    for tag in ["real"] + (["null0", "null1", "null2"] if NULL else []):
        key = f"{tag}_{ik}"
        if key in st: continue
        if STOP[0]: print("SIGTERM: stopped at a checkpoint", flush=True); sys.exit(0)
        st[key] = nb_sum(PR[f"{tag}_li"], PR[f"{tag}_lM"], PR[f"{tag}_d"], k)
        np.savez(PART + ".tmp.npz", **st); os.replace(PART + ".tmp.npz", PART)
        print(f"{FOOT} {CASE} k {k:.3f} {tag} done, {time.time() - t0:.0f} s", flush=True)
real = np.stack([st[f"real_{ik}"] for ik in range(len(KNB))])
sv = dict(real=real, k=KNB)
if NULL: sv["null"] = np.stack([(st[f"null0_{ik}"] + st[f"null1_{ik}"] + st[f"null2_{ik}"]) / 3 for ik in range(len(KNB))])
np.savez(OUTP + ".tmp.npz", **sv); os.replace(OUTP + ".tmp.npz", OUTP); os.remove(PART)
open(os.path.join(WORK, f"nb_{FOOT}_{CASE}.done"), "w").write("done\n"); print("done", flush=True)
