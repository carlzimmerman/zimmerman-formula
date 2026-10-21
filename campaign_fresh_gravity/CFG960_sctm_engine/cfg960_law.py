#!/usr/bin/env python3
"""CFG960 V-LAW (FROZEN_CRITERIA.md section 2): static isolated host on a 128^3 mesh with the engine's own functions
(radial_edges / bin_of profile, Law, body_points with A3 hybrid painting, deposit_points (the particles' CIC) + outer mesh nodes,
Mesh FFT Poisson, spectral gradient, interp1).
  box A: L 6.4 Mpc/h, M_b 1e12 h^-1 Msun (Plummer a 0.04 Mpc/h), M_c = 20 M_b (deep regime)
  box B: L 0.64 Mpc/h, M_b 1e12 (Plummer a 0.004), M_c = 2 M_b (y ~ 0.1-3)
  both footings, a = 1 (graded); box A at a = 0.5 reported only (unit check of the a-dependence).
Expected radial field g_exp(r) = Cg [M_b(<r) + min((nu_mono(y) - 1) M_b(<r), M_c)] / r^2 - (1.5 Om / a^2) M_tot r / (3 N_ref)
(the second term: the periodic mesh removes k = 0, i.e. a uniform negative background).  K: body off -> the baryons' Newtonian field.
Lines: median |g/g_exp - 1| <= 0.02 and max <= 0.05 over 4 dx <= r <= 0.85 r_e; median <= 0.02 over 1.3 r_e <= r <= min(2.5 r_e, 0.4 L).
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg960_law.py  -> cfg960_law.out / cfg960_law.json
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, time
os.environ.setdefault("CFG596_THREADS", "1"); os.environ.setdefault("CFG596_L", "6.4"); os.environ.setdefault("CFG960_RSSMAX", "1.0")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg960_sctm_pm as S
import numpy as np
E = S.E
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

M = 128; NREF = M ** 3; NB_PART = 200_000
def plummer(n, apl, rng):
    u = rng.random(n); r = apl / np.sqrt(np.maximum(u, 1e-12) ** (-2.0 / 3.0) - 1.0)
    r = np.minimum(r, 50 * apl)
    v = rng.normal(size=(n, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
    return r[:, None] * v
def fib_sphere(n):
    i = np.arange(n) + 0.5; z = 1 - 2 * i / n; rr = np.sqrt(1 - z * z); ph = i * S.GOLD
    return np.stack([rr * np.cos(ph), rr * np.sin(ph), z], 1)

def case(L, Mb_sun, Nc, apl, foot, a, seed=960):
    E.L = float(L); mesh = E.Mesh(M); dx = mesh.dx
    rng = np.random.default_rng(seed)
    mu_unit = L ** 3 / NREF
    Mb = Mb_sun / (E.Om * 2.775e11) / mu_unit                        # own baryons in particle-mass units
    Mc = Nc * Mb
    X = np.full(3, L / 2.0)
    xb = X[None, :] + plummer(NB_PART, apl, rng); wb = np.full(NB_PART, Mb / NB_PART)
    edges = S.radial_edges(dx)
    rb = np.sqrt(((xb - X) ** 2).sum(1))
    prof = np.bincount(S.bin_of(rb, edges), weights=wb, minlength=len(edges))[None, :]
    law = S.Law(a, foot, NREF)
    BB, dg, re = S.body_points(prof, np.array([Mc]), X[None, :], law, edges, dx, M)          # A3: inner CIC points + outer mesh nodes
    bpos, bw = BB["pos"], BB["w"]
    r_e = float(re[0])
    res = {}
    for body in (True, False):
        rho = np.zeros((M, M * M))
        S.deposit_points(rho, mesh, xb % L, wb)
        if body:
            S.deposit_points(rho, mesh, bpos, bw)
            if len(BB["cw"]): np.add.at(rho.reshape(-1), BB["cidx"], BB["cw"])
        delta = (rho.reshape(M, M, M) / (NREF / M ** 3) - 1.0).astype(np.float32)
        dk = mesh.fwd(delta)
        for s in mesh.slabs: dk[s] = ((-1.5 * E.Om / a) * dk[s]) * mesh.ik2_s(s)
        rmax = min(3.0 * r_e, 0.45 * L); radii = np.geomspace(2 * dx, rmax, 40); nv = fib_sphere(64)
        pts = (X[None, None, :] + radii[:, None, None] * nv[None, :, :]).reshape(-1, 3) % L
        grad = np.zeros((len(pts), 3)); b = mesh.cbuf()
        for c in range(3):
            for s in mesh.slabs: b[s] = (1j * mesh.kv_s(c, s)) * dk[s]
            mesh.inv_ip(b); grad[:, c] = E.interp1(mesh, b.view(np.float32), pts)
        gr = ((grad.reshape(len(radii), len(nv), 3) * nv[None, :, :]).sum(2) / a).mean(1)     # inward radial g = (grad phi . n)/a
        Mbr = np.array([wb[rb < r].sum() for r in radii])
        Cg = (1.5 * E.Om / a ** 2) * (L ** 3 / NREF) / (4 * math.pi)
        Mtot = Mb + (Mc if body else 0.0)
        Mph = np.minimum(law.mph(radii, Mbr), Mc) if body else 0.0
        gexp = Cg * (Mbr + Mph) / radii ** 2 - (1.5 * E.Om / a ** 2) * Mtot * radii / (3 * NREF)
        dev = gr / gexp - 1
        inner = (radii >= 4 * dx) & (radii <= 0.85 * r_e); outer = (radii >= 1.3 * r_e) & (radii <= min(2.5 * r_e, 0.4 * L))
        y_in = law.Cy * Mbr[inner] / radii[inner] ** 2
        r_ = dict(r_e=r_e, r_e_dx=r_e / dx, n_points=int(len(bw)), n_nodes=int(len(BB["cw"])), painted_over_Mc=float((bw.sum() + BB["cw"].sum()) / Mc),
                  inner_n=int(inner.sum()), inner_median=float(np.median(np.abs(dev[inner]))), inner_max=float(np.max(np.abs(dev[inner]))),
                  outer_n=int(outer.sum()), outer_median=float(np.median(np.abs(dev[outer]))) if outer.any() else None,
                  y_inner_range=[float(y_in.min()), float(y_in.max())] if len(y_in) else None,
                  radii=radii.tolist(), g_pm=gr.tolist(), g_exp=gexp.tolist())
        r_["PASS"] = bool(r_["inner_median"] <= 0.02 and r_["inner_max"] <= 0.05 and (r_["outer_median"] is not None and r_["outer_median"] <= 0.02))
        res["body" if body else "K_nobody"] = r_
    return res

def main():
    t0 = time.time()
    P("CFG960 V-LAW: static isolated host, engine functions, 128^3 mesh (FROZEN_CRITERIA.md section 2).")
    P("kappa = 1/2 FITTED; footings never pooled; not theory closed.")
    R = dict(lane="CFG960", gate="V-LAW", criteria="FROZEN_CRITERIA.md 6fc440225", engine_sha256=S.hashlib.sha256(open(S.__file__, "rb").read()).hexdigest(), cases={})
    allpass = True
    for name, L, Nc, apl, a, graded in (("A", 6.4, 20.0, 0.04, 1.0, True), ("B", 0.64, 2.0, 0.004, 1.0, True), ("A_a0.5", 6.4, 20.0, 0.04, 0.5, False)):
        for foot in ("canonical", "alt"):
            r = case(L, 1e12, Nc, apl, foot, a)
            R["cases"][f"{name}_{foot}"] = dict(graded=graded, L=L, Nc=Nc, a=a, **r)
            for k in ("body", "K_nobody"):
                v = r[k]
                P(f"  {name:6s} {foot:9s} {k:8s}: r_e {v['r_e']:.4f} Mpc/h ({v['r_e_dx']:.1f} dx), points {v['n_points']} + nodes {v['n_nodes']}, painted/M_c {v['painted_over_Mc']:.15f}; "
                  f"4dx-0.85r_e (n {v['inner_n']}, y {v['y_inner_range'][0]:.3g}-{v['y_inner_range'][1]:.3g}): median {v['inner_median']:.4f} max {v['inner_max']:.4f}; "
                  f"1.3-2.5 r_e (n {v['outer_n']}): median {v['outer_median']:.4f} -> {'PASS' if v['PASS'] else 'FAIL'}" + ("" if graded else " [reported only]"))
                if graded: allpass &= v["PASS"]
    R["V_LAW_PASS"] = bool(allpass); R["runtime_s"] = time.time() - t0; R["maxrss_gb"] = E.rss_gb()
    P(f"V-LAW (boxes A, B; both footings; body and K) -> {'PASS' if allpass else 'FAIL'}; runtime {R['runtime_s']:.0f} s; peak RSS {R['maxrss_gb']:.2f} GB")
    json.dump(R, open(os.path.join(HERE, "cfg960_law.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg960_law.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
