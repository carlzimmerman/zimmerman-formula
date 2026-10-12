#!/usr/bin/env python3
"""CFG647 POST-FREEZE diagnostics (NOT in FROZEN_CRITERIA.md 2e1ea8c58; reported, never gating).
(1) C1 re-read: the engine's nc counts the background node of catch_labels' graph; count OCCUPIED components instead; R_C vs hand
    count at float32 tolerance (the shell weight is float32: rounding of c_s is 3.0e-8).
(2) Because the frozen C2 failed (256^3 recomputation caps far less than the 1024^3 run), the pooling question is re-asked on the STORED
    1024^3 settled field s = dgrav - dpart (256^3 block means): per host (own-host partition of 256^3 catchments), the settled mass it
    actually received D_h vs its own shell cold mass R_h and its whole own-catchment cold mass A_h.  Import lower bounds
    T_shell = sum max(D_h - R_h, 0) / sum D_h and T_all = sum max(D_h - A_h, 0) / sum D_h: settled mass that cannot have come from the
    host's own cold energy, i.e. that the per-component rule pooled from neighbours.  Rough static P(k) estimate of removing that import.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math
os.environ.setdefault("CFG596_L", "100"); os.environ.setdefault("CFG596_RMIN", "0.78125")
os.environ["CFG596_SPILL"] = "0"; os.environ["CFG596_MODE"] = "lean"; os.environ.setdefault("CFG596_THREADS", "4")
os.environ["CFG596_RELIEF"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import cfg647_audit as A
m = A.m

def c1_reread():
    mesh = m.Mesh(64); dx = mesh.dx; Rg = np.geomspace(dx, 8.0, 14); R = Rg[-1]; a = 1.0; D = A.Dta_of(a, m.dta_table())
    idx = np.array([[20, 32, 32], [28, 32, 32]]); ron = np.array([R, R])
    catch = m.unpack(m.cover_balls(mesh, (idx, ron, Rg), D, 1.0, a, A.BR, A.FOOT))
    r, nc = m.catch_labels(catch)
    occ = np.unique(r)
    from scipy import ndimage
    lab, n = ndimage.label(catch)
    bg_node_isolated = True                                   # node 0 never enters the periodic-merge edge list (l0 > 0 & l1 > 0)
    return dict(nc_engine=int(nc), occupied_components=int(len(occ)), ndimage_labels=int(n), nc_minus_occupied=int(nc - len(occ)),
                PASS_reread=bool(len(occ) == 1))

def posthoc(name, a, dta, mesh):
    z = np.load(A.P1M.format(name)); dp_raw = z["dpart"].astype(np.float32); dg = z["dgrav"].astype(np.float32); z.close()
    s = (dg - dp_raw).astype(np.float32); dp = dp_raw - np.float32(dp_raw.astype(np.float64).mean())
    D = A.Dta_of(a, dta)
    peaks = m.cover_peaks(mesh, dp, D)
    edge = m.unpack(m.cover_balls(mesh, peaks, D, None, a, A.BR, A.FOOT))
    catch = m.unpack(m.cover_balls(mesh, peaks, D, 1.0, a, A.BR, A.FOOT))
    I = dict(peaks=peaks, D=D, rv=np.zeros(1, np.float32), e_raw=np.zeros(1, np.float32))
    # membership() needs rv / e_raw only for its naive sums: give full-size dummies
    I["rv"] = np.zeros(catch.shape, np.float32); I["e_raw"] = I["rv"]
    hosts, mult, emult, host, _ = A.membership(mesh, I, a)
    assert np.array_equal(mult > 0, catch)
    cold = ((1 - m.FB) * (1.0 + dp)).astype(np.float64)
    hm = host[catch]; nh = len(hosts); sp = np.where(s > 0, s, 0).astype(np.float64)
    Dh = np.bincount(hm, weights=sp[catch], minlength=nh)
    Rh = np.bincount(hm, weights=(cold * (catch & ~edge))[catch], minlength=nh)
    Ah = np.bincount(hm, weights=cold[catch], minlength=nh)
    lM = np.array([math.log10(m.M_ta(h[1], D)) for h in hosts]); hi = lM >= 13.5
    r, nc = m.catch_labels(catch); lab = np.full(catch.shape, -1, np.int64); lab[catch] = r
    npk = np.bincount(lab[tuple(np.array([h[0] for h in hosts]).T)], minlength=nc)
    multi_host_cell = np.zeros(catch.shape, bool); multi_host_cell[catch] = npk[r] >= 2
    out = dict(n_hosts=nh, stored_pos_total=float(sp.sum()), stored_pos_in_catch=float(sp[catch].sum()),
               stored_pos_frac_in_multihost_comps=float(sp[multi_host_cell].sum() / sp.sum()),
               T_shell=float(np.maximum(Dh - Rh, 0).sum() / Dh.sum()), T_all=float(np.maximum(Dh - Ah, 0).sum() / Dh.sum()),
               T_shell_hi=float(np.maximum(Dh - Rh, 0)[hi].sum() / max(Dh[hi].sum(), 1e-30)), T_shell_lo=float(np.maximum(Dh - Rh, 0)[~hi].sum() / max(Dh[~hi].sum(), 1e-30)),
               T_all_hi=float(np.maximum(Dh - Ah, 0)[hi].sum() / max(Dh[hi].sum(), 1e-30)),
               settled_frac_hi_mass_hosts=float(Dh[hi].sum() / Dh.sum()), n_hosts_hi=int(hi.sum()),
               hosts_importing_beyond_shell=int((Dh > Rh).sum()), hosts_importing_beyond_all=int((Dh > Ah).sum()),
               settled_over_own_shell_hi=float(Dh[hi].sum() / max(Rh[hi].sum(), 1e-30)), settled_over_own_shell_lo=float(Dh[~hi].sum() / max(Rh[~hi].sum(), 1e-30)))
    if name == "z0":
        # rough static estimate: cap each host's received settled at its own shell cold mass; rescale negative s per 256^3 component
        f = np.where(Dh > Rh, Rh / np.maximum(Dh, 1e-30), 1.0)
        s2 = s.astype(np.float64).copy(); pos = s2 > 0
        cellf = np.ones(catch.shape); cellf[catch] = f[hm]
        s2[pos & catch] *= cellf[pos & catch]
        pC = np.bincount(r, weights=np.where(s > 0, s, 0)[catch].astype(np.float64), minlength=nc)
        p2C = np.bincount(r, weights=np.where(s2 > 0, s2, 0)[catch], minlength=nc)
        nC = np.bincount(r, weights=np.where(s < 0, s, 0)[catch].astype(np.float64), minlength=nc)
        g = np.where(nC < 0, (p2C - pC + (-nC)) / np.maximum(-nC, 1e-30), 1.0)        # keep each component's net unchanged
        neg = (s2 < 0) & catch; s2[neg] *= g[lab[neg]]
        kb, Pp, _, _ = m.measure_pk(mesh, dp)
        _, Pg, _, _ = m.measure_pk(mesh, (dp + s).astype(np.float32))
        _, P2, _, _ = m.measure_pk(mesh, (dp + s2).astype(np.float32))
        v = {}
        for k0 in (0.3, 0.5, 1.0, 2.0):
            pp, kk = A.kval(kb, Pp, k0); pg, _ = A.kval(kb, Pg, k0); p2, _ = A.kval(kb, P2, k0)
            v[f"k{k0}"] = dict(k=kk, boost_stored=pg / pp, boost_import_removed=p2 / pp, ratio=p2 / pg)
        out["static_import_removed"] = v
        out["settled_removed_frac"] = float(1 - np.where(s2 > 0, s2, 0)[catch].sum() / sp[catch].sum())
    return out

def main():
    O = {"lane": "CFG647", "post_freeze": True, "criteria": "2e1ea8c58", "C1_reread": c1_reread()}
    print("C1 re-read:", O["C1_reread"], flush=True)
    mesh = m.Mesh(256); dta = m.dta_table()
    for name, a in (("z1", 0.5), ("z0.5", 2 / 3), ("z0", 1.0)):
        O[name] = posthoc(name, a, dta, mesh); print(f"[{name}]", O[name], flush=True)
        json.dump(O, open(os.path.join(HERE, "cfg647_posthoc.json"), "w"), indent=1)
    O["maxrss_gb"] = A.rss(); json.dump(O, open(os.path.join(HERE, "cfg647_posthoc.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
