#!/usr/bin/env python3
"""CFG647 (FROZEN_CRITERIA.md, commit 2e1ea8c58): engineering audit of the settled cold-energy accounting in the CFG596 engine.
Imports cfg596_pm.py UNCHANGED (read only) and re-implements its RES source block with instrumentation (per-cell e, s_c, labels,
ball multiplicity, own-host counterfactual).  Inputs: stored P1 (RES canonical 1024^3 L100) 256^3 block means and the P1 JSON.
Measurement only; no simulation.  kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, json, math, resource
os.environ.setdefault("CFG596_L", "100"); os.environ.setdefault("CFG596_RMIN", "0.78125")
os.environ["CFG596_SPILL"] = "0"; os.environ["CFG596_MODE"] = "lean"; os.environ.setdefault("CFG596_THREADS", "4")
os.environ.setdefault("CFG596_RELIEF", "0")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CFG596_lean_pm_1024"))
import numpy as np
import cfg596_pm as m

W596 = os.path.join(m.EXT, "cfg596_work")
P1J = os.path.join(W596, "P1", "cfg596_RES_canonical_N1024_L100_ns1024_lean.json")
P1M = os.path.join(W596, "P1", "cfg596_RES_canonical_N1024_L100_ns1024_lean_{}_mesh256.npz")
FOOT, BR = "canonical", "FLAT"
OUT = {"lane": "CFG647", "criteria": "2e1ea8c58", "engine": "cfg596_pm.py (6323b630f), imported unchanged", "L": m.L, "rmin": m.RMIN_PHYS}
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def say(*a): print(*a, flush=True)

def Dta_of(a, dta):
    return math.exp(np.interp(math.log(1 / a), np.log1p(dta["z"]), np.log(dta["D"])))

def dfield(arr):
    D = m.DField("delta", arr.shape[0], np.float32); D.write_all(np.array(arr, np.float32, copy=True)); return D

# ---------------------------------------------------------------- instrumented copy of forces() RES (diag, fresh masks)
def instrumented(mesh, delta, a, dta):
    M = mesh.M; D = Dta_of(a, dta); tau = (D - 1.0) / 3.0
    dk = mesh.fwd(delta)
    Dfsw = m.DField("fsw", M, np.float32); m.tidal_lean_fsw(mesh, dk, tau, Dfsw); fsw = np.array(Dfsw.read_all()); Dfsw.close(); del dk
    peaks = m.cover_peaks(mesh, delta, D)
    edge = m.unpack(m.cover_balls(mesh, peaks, D, None, a, BR, FOOT))
    catch_p, code, tab = m.cover_balls(mesh, peaks, D, 1.0, a, BR, FOOT, want_fret=True); catch = m.unpack(catch_p)
    fret = tab[code]
    # MOND input (NOFILT: W = 1)
    phb = mesh.fwd((fret * (1.0 + delta)).astype(np.float32))
    for s in mesh.slabs: phb[s] = ((-1.5 * m.Om / a) * phb[s]) * mesh.ik2_s(s)
    def gb(c):
        b = mesh.cbuf()
        for s in mesh.slabs:
            Wk = (0.0 / (1.0 + mesh.k2_s(s)) + 0.0 / (1.0 + mesh.k2_s(s)) + 1.0).astype(np.float32)
            b[s] = (1j * mesh.kv_s(c, s)) * phb[s] * Wk
        r = mesh.inv_ip(b); out = np.empty(r.shape, np.float32); out[...] = m.FB * (-r); return out
    ysq = np.zeros((M,) * 3, np.float32)
    for c in range(3): g = gb(c); ysq += g ** 2
    a0c = a * m.a0_code(a, BR, FOOT)
    w = np.empty_like(ysq)
    for j in range(M): w[j] = m.nu_mono(np.sqrt(ysq[j:j + 1]) / a0c).astype(np.float32) - 1.0
    del ysq
    divk = mesh.cbuf()
    for c in range(3):
        gw = (w * gb(c)).astype(np.float32); gk = mesh.fwd(gw)
        if c == 0: divk[...] = (1j * mesh.kv_s(0, slice(0, M))) * gk
        else: divk += (1j * mesh.kvec[c]) * gk
    del w, phb
    s_ph = -mesh.inv_copy(divk); del divk
    cs = 1.5 * m.Om * (1.0 - m.FB) / a
    sc = (cs * (1.0 + delta)).astype(np.float32)
    e_raw = (fsw * edge.astype(np.float32)) * np.maximum(s_ph - sc, 0.0); e_raw = (e_raw * catch).astype(np.float32)
    shell = catch & ~edge
    rv = (sc * shell).astype(np.float32)
    r, nc = m.catch_labels(catch)
    lab = np.full(M ** 3, -1, np.int64); lab[catch.reshape(-1)] = r
    cm = catch.reshape(-1)
    E_ = np.bincount(r, weights=e_raw.reshape(-1)[cm].astype(np.float64), minlength=nc)
    C_ = np.bincount(r, weights=rv.reshape(-1)[cm].astype(np.float64), minlength=nc)
    W_ = np.bincount(r, weights=(1.0 + delta).reshape(-1)[cm].astype(np.float64), minlength=nc)
    q = E_ / np.maximum(C_, 1e-30); q_raw = q.copy(); capf = np.where(q > 1.0, 1.0 / np.maximum(q, 1e-30), 1.0); q = np.minimum(q, 1.0)
    e = e_raw.reshape(-1).copy(); e[cm] = (e[cm] * capf[r]).astype(np.float32)
    comp = np.zeros(M ** 3, np.float32); comp[cm] = (rv.reshape(-1)[cm] * q[r]).astype(np.float32)
    src = (e - comp).reshape((M,) * 3)
    # potential exactly as _finish_phik
    dkp = mesh.fwd(delta); srck = mesh.fwd(src.astype(np.float32)); phik = mesh.cbuf()
    for s in mesh.slabs:
        ik2 = mesh.ik2_s(s); phik[s] = ((-1.5 * m.Om / a) * dkp[s]) * ik2; phik[s] = phik[s] - srck[s] * ik2
    del dkp, srck
    return dict(D=D, peaks=peaks, edge=edge, catch=catch, shell=shell, fret=fret, sc=sc, e_raw=e_raw, e=e.reshape((M,) * 3),
                comp=comp.reshape((M,) * 3), src=src, rv=rv, r=r, nc=nc, lab=lab.reshape((M,) * 3), E=E_, C=C_, W=W_, q_raw=q_raw,
                phik=phik, cs=cs)

# ---------------------------------------------------------------- ball membership: multiplicity, own-host assignment, naive sums
def balls(mesh, peaks, D, a, X, xfac=None):
    """per resolved host: centre, r_ON, radius (x = 1 or x_supply).  Returns list (centre idx, R, rb)."""
    idx, ron, Rg = peaks; out = []
    for i in np.nonzero(ron >= m.RMIN_PHYS)[0]:
        R = ron[i]; x = m.x_supply(R, D, a, BR, FOOT) if xfac is None else xfac
        out.append((idx[i], R, x * R))
    return out

def offsets(rb, dx):
    n = int(math.floor(rb / dx)) + 1; g = np.arange(-n, n + 1)
    G = np.stack(np.meshgrid(g, g, g, indexing="ij"), -1).reshape(-1, 3)
    d2 = ((G * dx) ** 2).sum(1); k = d2 <= rb * rb
    return G[k], np.sqrt(d2[k])

def membership(mesh, I, a):
    M, dx = mesh.M, mesh.dx
    hosts = balls(mesh, I["peaks"], I["D"], a, 1.0, 1.0)
    edges = balls(mesh, I["peaks"], I["D"], a, None, None)
    mult = np.zeros((M,) * 3, np.int16); emult = np.zeros((M,) * 3, np.int16)
    best = np.full((M,) * 3, np.inf); host = np.full((M,) * 3, -1, np.int32)
    naive_shell = 0.0; naive_e = 0.0; naive_vol = 0
    oc = {}
    for h, ((c, R, rb), (_, _, rbe)) in enumerate(zip(hosts, edges)):
        key = round(rb, 9)
        if key not in oc: oc[key] = offsets(rb, dx)
        G, d = oc[key]; P = (G + c[None, :]) % M
        ii = (P[:, 0], P[:, 1], P[:, 2])
        mult[ii] += 1
        sc_score = d / R - 1e-9 * R                                  # smallest d/R; ties -> larger host
        upd = sc_score < best[ii]; best[ii] = np.where(upd, sc_score, best[ii])
        host[P[upd, 0], P[upd, 1], P[upd, 2]] = h
        naive_shell += float(I["rv"][ii].astype(np.float64).sum()); naive_e += float(I["e_raw"][ii].astype(np.float64).sum()); naive_vol += len(d)
        if rbe >= 0.5 * dx:
            ke = round(rbe, 9)
            if ke not in oc: oc[ke] = offsets(rbe, dx)
            Ge, _ = oc[ke]; Pe = (Ge + c[None, :]) % M; emult[Pe[:, 0], Pe[:, 1], Pe[:, 2]] += 1
        else:
            emult[c[0], c[1], c[2]] += 1
    return hosts, mult, emult, host, dict(naive_shell=naive_shell, naive_e=naive_e, naive_vol=naive_vol)

def kval(kb, pb, k0):
    kb = np.asarray(kb); return float(np.asarray(pb)[np.argmin(np.abs(kb - k0))]), float(kb[np.argmin(np.abs(kb - k0))])

# ---------------------------------------------------------------- C1 synthetic two-ball test
def c1_synthetic():
    saveL = m.L
    mesh = m.Mesh(64); M, dx = 64, mesh.dx
    Rg = np.geomspace(dx, 8.0, 14); R = Rg[-1]; a = 1.0; dta = m.dta_table(); D = Dta_of(a, dta)
    idx = np.array([[20, 32, 32], [28, 32, 32]]); ron = np.array([R, R])
    catch = m.unpack(m.cover_balls(mesh, (idx, ron, Rg), D, 1.0, a, BR, FOOT))
    edge = m.unpack(m.cover_balls(mesh, (idx, ron, Rg), D, None, a, BR, FOOT))
    r, nc = m.catch_labels(catch)
    cs = 1.5 * m.Om * (1 - m.FB) / a; rv = (cs * np.ones((M,) * 3) * (catch & ~edge)).astype(np.float32)
    C_ = np.bincount(r, weights=rv.reshape(-1)[catch.reshape(-1)].astype(np.float64), minlength=nc)
    # hand count, independent of the engine: lattice balls by explicit distance
    I = np.indices((M,) * 3).transpose(1, 2, 3, 0)
    def ball(c, rb):
        d = np.minimum(np.abs(I - c), M - np.abs(I - c)) * dx; return (d ** 2).sum(-1) <= rb * rb
    xs = m.x_supply(R, D, a, BR, FOOT)
    B = [ball(c, R) for c in idx]; Eb = [ball(c, xs * R) for c in idx]
    uni = (B[0] | B[1]) & ~(Eb[0] | Eb[1])
    hand = cs * float(uni.sum()); naive = cs * float(sum((b & ~(Eb[0] | Eb[1])).sum() for b in B))
    ok = (nc == 1) and abs(C_.sum() - hand) <= 1e-9 * hand and np.array_equal(catch, B[0] | B[1]) and naive > hand
    return dict(n_comp=int(nc), RC_engine=float(C_.sum()), RC_hand=hand, naive_per_ball=naive, overlap_shell_cells=int((B[0] & B[1] & uni).sum()),
                naive_minus_hand_over_cs=(naive - hand) / cs, catch_equals_hand_union=bool(np.array_equal(catch, B[0] | B[1])), PASS=bool(ok))

# ---------------------------------------------------------------- main
def main():
    js = json.load(open(P1J))
    # M1
    M1 = {}
    for n, s in js["snap"].items():
        es = s.get("e_sum", 0.0)
        M1[n] = dict(z=s["z"], e_sum=es, src_sum=s.get("src_sum"), ratio=(abs(s["src_sum"]) / es if es else 0.0), overdraw_mass=s.get("overdraw_mass"),
                     q_max=s.get("q_max"), cap_active=s.get("cap_active"), n_catch=s.get("n_catch"))
    OUT["M1"] = M1; OUT["B3_json"] = bool(max(v["ratio"] for v in M1.values()) > 1e-5)
    say("M1 stored JSON |src_sum|/e_sum:", {k: f"{v['ratio']:.2e}" for k, v in M1.items()}, " B3_json bug:", OUT["B3_json"])
    OUT["C1"] = c1_synthetic(); say("C1 synthetic:", OUT["C1"])
    mesh = m.Mesh(256); dta = m.dta_table(); m.DIAGX = True
    OUT["M2"] = {}
    for name, a in (("z1", 0.5), ("z0.5", 2 / 3), ("z0", 1.0)):
        npz = np.load(P1M.format(name)); dp = npz["dpart"].astype(np.float32); dg = npz["dgrav"].astype(np.float32); npz.close()
        dp = dp - np.float32(dp.astype(np.float64).mean())          # block means of rho/mean - 1: re-zero the mean (float roundoff only)
        R = {}
        # C0: unmodified engine forces vs instrumented copy
        m._INC.update(mask=None, catch=None, fcode=None, ftab=None, calls=0)
        phik_eng, info = m.forces(mesh, [dfield(dp)], a, "RES", BR, FOOT, dta, diag=True)
        I = instrumented(mesh, dp, a, dta)
        dphi = float(np.abs(phik_eng - I["phik"]).max() / np.abs(phik_eng).max())
        es_i = float(I["e"].astype(np.float64).sum()); ss_i = float(I["src"].astype(np.float64).sum())
        c0 = dict(max_rel_dphik=dphi, q_max=(info["q_max"], float(I["q_raw"].max())), n_catch=(info["n_catch"], int(I["nc"])),
                  e_sum=(info["e_sum"], es_i), src_sum=(info["src_sum"], ss_i))
        c0["PASS"] = bool(dphi <= 1e-5 and abs(info["q_max"] - c0["q_max"][1]) <= 1e-5 * info["q_max"] and info["n_catch"] == I["nc"]
                          and abs(info["e_sum"] - es_i) <= 1e-5 * info["e_sum"] and abs(info["src_sum"] - ss_i) <= 1e-5 * info["e_sum"])
        R["C0"] = c0; del phik_eng
        say(f"[{name}] C0 {c0}  rss {rss():.2f} GB")
        js_s = js["snap"][name]
        R["C2"] = dict(cap_active_256=bool((I["q_raw"] > 1).any()), overdraw_256=float(I["W"][I["q_raw"] > 1].sum() / I["W"].sum()),
                       overdraw_1024=js_s["overdraw_mass"], q_max_256=float(I["q_raw"].max()), q_max_1024=js_s["q_max"], n_catch_256=int(I["nc"]), n_catch_1024=js_s["n_catch"])
        R["C2"]["PASS"] = bool(R["C2"]["cap_active_256"] and (1 / 1.5) <= R["C2"]["overdraw_256"] / R["C2"]["overdraw_1024"] <= 1.5)
        # B checks
        cm = I["catch"]; E, C = I["E"], I["C"]
        uni_shell = float(I["rv"][I["shell"]].astype(np.float64).sum()); uni_e = float(I["e_raw"][cm].astype(np.float64).sum())
        b1 = abs(C.sum() - uni_shell) / max(uni_shell, 1e-30); b2 = abs(E.sum() - uni_e) / max(uni_e, 1e-30)
        labels_one = bool(len(I["r"]) == int(cm.sum()) and (I["lab"][cm] >= 0).all() and (I["lab"][~cm] < 0).all())
        srcC = np.bincount(I["r"], weights=I["src"][cm].astype(np.float64), minlength=I["nc"])
        eC = np.bincount(I["r"], weights=I["e"][cm].astype(np.float64), minlength=I["nc"])
        b3 = float(np.max(np.where(C > 0, np.abs(srcC) / np.maximum(E, 1e-30), 0.0)))
        over = float(np.max(np.where(C > 0, eC / np.maximum(C, 1e-30), 0.0)))
        b4 = dict(max_delivered_over_RC=over, comp_in_edge=float(np.abs(I["comp"][I["edge"]]).sum()), e_in_shell=float(np.abs(I["e"][I["shell"]]).sum()),
                  e_outside_catch=float(np.abs(I["e"][~cm]).sum()), edge_outside_catch_cells=int((I["edge"] & ~cm).sum()))
        R["B"] = dict(B1_rel=b1, labels_one_per_cell=labels_one, B2_rel=b2, B3_max_comp=b3, B4=b4,
                      BUG=bool(b1 > 1e-5 or not labels_one or b2 > 1e-5 or b3 > 1e-4 or over > 1 + 1e-5 or b4["comp_in_edge"] > 0 or b4["e_in_shell"] > 0 or b4["e_outside_catch"] > 0))
        say(f"[{name}] B {R['B']}")
        # V1 overlap
        hosts, mult, emult, host, naive = membership(mesh, I, a)
        R["union_matches_engine"] = dict(catch=bool(np.array_equal(mult > 0, cm)), edge=bool(np.array_equal(emult > 0, I["edge"])))
        cv = float(cm.sum()); e_pc = I["e"]
        npk = np.bincount(I["lab"][tuple(np.array([h[0] for h in hosts]).T)], minlength=I["nc"])
        compvol = np.bincount(I["r"], minlength=I["nc"])
        big = int(np.argmax(compvol))
        R["V1"] = dict(n_hosts=len(hosts), n_comp=int(I["nc"]), catch_vol_frac_box=cv / mesh.M ** 3,
                       catch_frac_ge2=float((mult >= 2).sum() / cv), catch_frac_ge3=float((mult >= 3).sum() / cv),
                       edge_frac_ge2=float((emult >= 2).sum() / max(I["edge"].sum(), 1)),
                       settled_e_frac_in_ge2=float(e_pc[mult >= 2].astype(np.float64).sum() / max(e_pc.astype(np.float64).sum(), 1e-30)),
                       shell_supply_frac_in_ge2=float(I["rv"][mult >= 2].astype(np.float64).sum() / max(uni_shell, 1e-30)),
                       comps_with_ge2_hosts=int((npk >= 2).sum()), hosts_in_multi_host_comps=int(npk[npk >= 2].sum()),
                       peaks_per_comp_hist={str(k): int(v) for k, v in zip(*np.unique(npk, return_counts=True))},
                       largest_comp_vol_frac_of_catch=float(compvol[big] / cv), largest_comp_hosts=int(npk[big]),
                       largest_comp_supply_frac=float(C[big] / C.sum()), largest_comp_settled_frac=float(np.minimum(E, C)[big] / np.minimum(E, C).sum()))
        say(f"[{name}] V1 {R['V1']}")
        # V2 accounting (mass units of the mean total density per cell: x * a / (1.5 Om))
        mu = a / (1.5 * m.Om)
        deliv = float(np.minimum(E, C).sum())
        R["V2"] = dict(sum_RC=float(C.sum()), unique_shell=uni_shell, naive_per_ball_shell=naive["naive_shell"], naive_over_unique_shell=naive["naive_shell"] / uni_shell,
                       sum_EC=float(E.sum()), unique_e=uni_e, naive_per_ball_e=naive["naive_e"], naive_over_unique_e=naive["naive_e"] / max(uni_e, 1e-30),
                       naive_vol_over_unique=naive["naive_vol"] / cv,
                       mass_settled_delivered=deliv * mu, mass_demand_E=float(E.sum()) * mu, mass_shell_cold=float(C.sum()) * mu,
                       mass_catch_cold=float(((1 - m.FB) * (1.0 + dp))[cm].astype(np.float64).sum()),
                       mass_retained_baryon_ceiling=float((I["fret"] * (1 - m.FB) * (1.0 + dp))[cm].astype(np.float64).sum()),
                       mass_box_total=float((1.0 + dp).astype(np.float64).sum()))
        v2 = R["V2"]; v2["delivered_over_shell_cold"] = v2["mass_settled_delivered"] / v2["mass_shell_cold"]
        v2["delivered_over_retained_ceiling"] = v2["mass_settled_delivered"] / v2["mass_retained_baryon_ceiling"]
        v2["delivered_over_box_mass"] = v2["mass_settled_delivered"] / v2["mass_box_total"]
        say(f"[{name}] V2 {v2}")
        # V3 pooling: own-host counterfactual
        hm = host[cm]; assert (hm >= 0).all()
        nh = len(hosts)
        Eh = np.bincount(hm, weights=I["e_raw"][cm].astype(np.float64), minlength=nh)
        Ch = np.bincount(hm, weights=I["rv"][cm].astype(np.float64), minlength=nh)
        dh = float(np.minimum(Eh, Ch).sum()); G = deliv / max(dh, 1e-30)
        lM = np.array([math.log10(m.M_ta(h[1], I["D"])) for h in hosts])
        # engine delivery attributed to hosts: e post-cap summed over each host's assigned cells
        eng_h = np.bincount(hm, weights=I["e"][cm].astype(np.float64), minlength=nh)
        hi = lM >= 13.5
        R["V3"] = dict(G=G, delivered_engine=deliv, delivered_own_host=dh, hosts_cap_bound_own=int((Eh > Ch).sum()), n_hosts=nh,
                       hosts_no_own_shell_with_demand=int(((Ch <= 0) & (Eh > 0)).sum()),
                       engine_settled_hi_mass=float(eng_h[hi].sum()), own_settled_hi_mass=float(np.minimum(Eh, Ch)[hi].sum()),
                       engine_settled_lo_mass=float(eng_h[~hi].sum()), own_settled_lo_mass=float(np.minimum(Eh, Ch)[~hi].sum()))
        v3 = R["V3"]
        v3["gain_hi"] = v3["engine_settled_hi_mass"] / max(v3["own_settled_hi_mass"], 1e-30)
        v3["gain_lo"] = v3["engine_settled_lo_mass"] / max(v3["own_settled_lo_mass"], 1e-30)
        v3["class"] = "negligible" if G - 1 < 0.01 else ("minor" if G - 1 < 0.05 else "MATERIAL")
        say(f"[{name}] V3 {v3}")
        # V5 resolution control: stored s vs recomputed
        s256 = (I["src"] * mu).astype(np.float32); sst = (dg - npz_dp_raw(name)).astype(np.float32)
        R["V5"] = dict(stored_pos=float(sst[sst > 0].astype(np.float64).sum()), stored_neg=float(sst[sst < 0].astype(np.float64).sum()),
                       recomp_pos=float(s256[s256 > 0].astype(np.float64).sum()), recomp_neg=float(s256[s256 < 0].astype(np.float64).sum()),
                       pearson=float(np.corrcoef(sst.reshape(-1).astype(np.float64), s256.reshape(-1).astype(np.float64))[0, 1]),
                       stored_s_in_catch_pos=float(sst[cm & (sst > 0)].astype(np.float64).sum()),
                       stored_pos_frac_in_ge2=float(sst[(mult >= 2) & (sst > 0)].astype(np.float64).sum() / max(float(sst[sst > 0].astype(np.float64).sum()), 1e-30)))
        say(f"[{name}] V5 {R['V5']}")
        # V4 static P(k) (z = 0 only)
        if name == "z0":
            capf_h = np.where(Eh > Ch, Ch / np.maximum(Eh, 1e-30), 1.0); q_h = np.minimum(Eh / np.maximum(Ch, 1e-30), 1.0)
            src_h = np.zeros(cm.shape, np.float32)
            src_h[cm] = (I["e_raw"][cm] * capf_h[hm] - I["rv"][cm] * q_h[hm]).astype(np.float32)
            kb, Pp, _, _ = m.measure_pk(mesh, dp)
            _, Pe, _, _ = m.measure_pk(mesh, (dp + s256).astype(np.float32))
            _, Ph, _, _ = m.measure_pk(mesh, (dp + src_h * mu).astype(np.float32))
            _, Pst, _, _ = m.measure_pk(mesh, dg - npz_dp_raw(name) + dp)
            v4 = {}
            for k0 in (0.3, 0.5, 1.0, 2.0):
                pp, kk = kval(kb, Pp, k0); pe, _ = kval(kb, Pe, k0); ph, _ = kval(kb, Ph, k0); ps, _ = kval(kb, Pst, k0)
                v4[f"k{k0}"] = dict(k=kk, Pg_engine_over_Pp=pe / pp, Pg_ownhost_over_Pp=ph / pp, Pg_stored_over_Pp=ps / pp, ownhost_over_engine=ph / pe)
            R["V4"] = v4; say(f"[{name}] V4 {v4}")
            del src_h
        OUT["M2"][name] = R
        del I, mult, emult, host, dp, dg
        json.dump(OUT, open(os.path.join(HERE, "cfg647_audit.json"), "w"), indent=1, default=float)
    OUT["maxrss_gb"] = rss()
    bug = OUT["B3_json"] or any(OUT["M2"][n]["B"]["BUG"] for n in OUT["M2"])
    ctrl = OUT["C1"]["PASS"] and all(OUT["M2"][n]["C0"]["PASS"] for n in OUT["M2"])
    OUT["controls_pass"] = bool(ctrl); OUT["accounting_bug_B1_B4"] = bool(bug)
    json.dump(OUT, open(os.path.join(HERE, "cfg647_audit.json"), "w"), indent=1, default=float)
    say(f"controls pass {ctrl}; accounting bug (B1-B4) {bug}; C2 z0 {OUT['M2']['z0']['C2']}; maxrss {OUT['maxrss_gb']:.2f} GB")

_RAW = {}
def npz_dp_raw(name):
    if name not in _RAW:
        _RAW.clear(); z = np.load(P1M.format(name)); _RAW[name] = z["dpart"].astype(np.float32); z.close()
    return _RAW[name]

if __name__ == "__main__":
    main()
