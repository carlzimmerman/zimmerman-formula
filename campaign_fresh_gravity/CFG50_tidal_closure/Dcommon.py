# -*- coding: utf-8 -*-
"""Dcommon -- shared helpers for attack D (tidal-tensor-of-an-auxiliary-potential coupling).  Imports the CFG44 profile/target machinery READ-ONLY (Bcommon writes nothing unless its Report is used; not used here)."""
import os, sys, json, time, math
import numpy as np
sys.dont_write_bytecode = True
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CFG44_fluid_target")
sys.path.insert(0, REPO)
from Bcommon import G, A0, KPC_M, exp_sphere, point_mass, target_fields, nu_p2, law_u   # noqa
HERE = os.path.dirname(os.path.abspath(__file__))

class Report:
    def __init__(self, slug, mutate):
        self.slug = slug + ("_MUTATE_" + mutate if mutate else "")
        self.lines, self.checks, self.numbers, self.t0 = [], [], {}, time.time()
    def P(self, s=""):
        print(s, flush=True); self.lines.append(s)
    def banner(self, s):
        self.P("\n" + "=" * 110 + "\n" + s + "\n" + "=" * 110)
    def check(self, name, detail, ok):
        self.checks.append(dict(name=name, detail=detail, ok=bool(ok)))
        self.P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")
    def num(self, k, v): self.numbers[k] = v
    def write(self):
        nf = sum(not c["ok"] for c in self.checks)
        self.P(f"\n  {sum(c['ok'] for c in self.checks)}/{len(self.checks)} checks pass; failures: {nf}   ({time.time()-self.t0:.0f} s)")
        def clean(o):
            if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
            if isinstance(o, (list, tuple)): return [clean(v) for v in o]
            if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else str(o)
            if isinstance(o, np.integer): return int(o)
            if isinstance(o, (np.bool_, bool)): return bool(o)
            return o if isinstance(o, (int, str)) or o is None else str(o)
        json.dump(clean(dict(slug=self.slug, failures=nf, checks=self.checks, numbers=self.numbers)), open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        return nf

def baryon_fields(prof, h_or_none=None, r0=None, r1=None, n=6001):
    """target fields plus the baryonic tidal data on the target grid.  Returns dict with r, rho_c, g_tot, gN, rho_b, beta, Prr, Pp (target Jeans stress), Trr, Tp (tidal eigenvalues of Phi_b)."""
    f = target_fields(prof, r0=r0, r1=r1, n=n)
    r, rho, g, uN = f["r"], f["rho"], f["g"], f["uN"]
    gN = uN / r**2
    rb = prof.rho_b(r)
    rbar = 3 * (uN / G) / (4 * math.pi * r**3)
    beta = -1.5 * rb / rbar
    Prr = rho * r * g / 2.0                 # sigma_r^2 = V_c^2/2 = r g_tot/2   (CFG44 B1)
    Pp = (1 - beta) * Prr                   # anisotropy beta = -(3/2) rho_b/rhobar_b
    Trr = 2 * gN / r                        # tidal tensor of Phi_b:  T_ij = (delta_ij lap - d_i d_j) Phi_b :  radial eigenvalue
    Tp = 4 * math.pi * G * rb - gN / r      # transverse eigenvalue
    return dict(r=r, rho=rho, g=g, gN=gN, rho_b=rb, beta=beta, Prr=Prr, Pp=Pp, Trr=Trr, Tp=Tp, uN=uN, w=f["w"], u=f["u"])
