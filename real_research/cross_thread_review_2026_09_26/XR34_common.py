#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_common -- shared plumbing for XR34, the kernel-argument re-score of the record's particle-mesh forest lanes.

THE ONE LINE.  Every affected lane evaluates the MOND kernel at |grad_x phi_N| / a^2, where phi_N solves the lane's own
lap_x phi_N = 1.5 Om delta / a and the particles are kicked by dp/dt = -grad_x phi_N with p = a^2 dx/dt.  That makes phi_N
the PHYSICAL peculiar potential and g_N,phys = |grad_x phi_N| / a, so the committed argument is (1+z) g_N,phys
(XR34_kernel_argument.py shows it from the code's own solve and kick).  This module reads a lane's source READ-ONLY,
replaces that ONE line, and executes the result as a fresh module whose __main__ block does not run:
    'none'    the committed line, |grad_x phi_N| / a^2   (= (1+z) g_N,phys)
    'fix'     |grad_x phi_N| / a                          (= g_N,phys)
    'double'  |grad_x phi_N| / a^0                        (the correction applied twice, g_N,phys/(1+z): the MUTATE)
The patch is verified every time: the patched text differs from the committed file in exactly one line, that line.

It also
  * runs a lane's own run() in worker processes (spawn, one run per process -- max_tasks_per_child = 1 -- one thread
    each; a lost worker raises BrokenProcessPool instead of hanging), at most 3 at a time and at most 1 of the large
    256^3-mesh runs (~6.7 GB) at a time; with XR34_SLOTDIR set, a machine-wide Budget shared by concurrently running
    XR34 scripts keeps the total to one heavy + one light run, or three light runs (the machine being shared);
  * extracts a lane's own accel() closure from the patched source (AST) and evaluates it on a prescribed density field:
    the single-halo probe (k1_tables runs it in a child, so a parent never holds the lanes' CLASS tables);
  * keeps the record's output conventions: <name>.out tee, check(), <name>_results.json; MUTATE=1 -> _MUTATE names.
    A spawned worker re-imports the main script; Lane() detects it and does not touch the parent's .out.
Nothing outside this folder is edited.  kappa = 1/2 is FITTED (Z = 5.7888); no XR34 number depends on it.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"                                               # one thread per process (set before numpy loads)
import sys, io, ast, json, time, math, types, textwrap, contextlib, resource, fcntl
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RR = os.path.join(REPO, "real_research")
G03 = os.path.join(RR, "g03_audit_2026")
DEN = os.path.join(RR, "dark_energy_2026")

MAG_LINE = "            mag = np.sqrt(sum((gg / a ** 2) ** 2 for gg in gphi)) + 1e-30"
GN_LINE = "            gN = [-gg / a ** 2 for gg in gphi]"
LANES = {
    "L346": dict(rel=("g03_audit_2026", "L346_switch_forest_gate.py"), line=GN_LINE, runfn="run"),
    "L347": dict(rel=("g03_audit_2026", "L347_switch_forest_flux_power.py"), line=MAG_LINE, runfn="run"),
    "L359": dict(rel=("g03_audit_2026", "L359_vacuum_gated_switch.py"), line=MAG_LINE, runfn="run_gated"),
    "L362": dict(rel=("g03_audit_2026", "L362_forest_pincer_convergence.py"), line=MAG_LINE, runfn="run"),
    "DE11": dict(rel=("dark_energy_2026", "DE11_forest_converged_model.py"), line=MAG_LINE, runfn="run"),
    "DE11b": dict(rel=("dark_energy_2026", "DE11b_forest_convergence.py"), line=MAG_LINE, runfn="run"),
}
PATCH = {"none": "/ a ** 2", "fix": "/ a", "double": "/ a ** 0"}
PATCH_MEANING = {"none": "|grad_x phi_N|/a^2 = (1+z) g_N,phys (committed)", "fix": "|grad_x phi_N|/a = g_N,phys (corrected)",
                 "double": "|grad_x phi_N|/a^0 = g_N,phys/(1+z) (correction applied twice: MUTATE)"}


def rel(path):
    return os.path.relpath(path, REPO)


def lane_path(lane):
    return os.path.join(RR, *LANES[lane]["rel"])


def patched_source(lane, patch):
    """the lane's committed source with ONE line changed; returns (source, [(line number, old, new)])."""
    src = open(lane_path(lane)).read()
    line = LANES[lane]["line"]
    if src.count(line) != 1:
        raise RuntimeError(f"{lane}: the kernel line occurs {src.count(line)} times (expected exactly 1)")
    if line.count("/ a ** 2") != 1:
        raise RuntimeError(f"{lane}: the kernel line must carry '/ a ** 2' once")
    new = src.replace(line, line.replace("/ a ** 2", PATCH[patch]))
    a_, b_ = src.splitlines(), new.splitlines()
    if len(a_) != len(b_):
        raise RuntimeError(f"{lane}: the patch changed the line count")
    diff = [(i + 1, x, y) for i, (x, y) in enumerate(zip(a_, b_)) if x != y]
    if len(diff) != (0 if patch == "none" else 1) or (diff and diff[0][1] != line):
        raise RuntimeError(f"{lane}/{patch}: the patch must change exactly the kernel line, got {diff}")
    return new, diff


_MODS = {}


def module(lane, patch):
    """the lane executed from its (patched) committed source as a fresh module; its __main__ block does not run."""
    key = (lane, patch)
    if key in _MODS:
        return _MODS[key]
    src, _ = patched_source(lane, patch)
    name = f"xr34_{lane}_{patch}"
    mod = types.ModuleType(name)
    mod.__file__ = lane_path(lane)                                      # the lane's own HERE/REPO resolve as committed
    sys.modules[name] = mod
    d = os.path.dirname(lane_path(lane))
    if d not in sys.path:
        sys.path.insert(0, d)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, lane_path(lane), "exec"), mod.__dict__)
    _MODS[key] = mod
    return mod


def release_modules():
    """drop the modules built in this process (and the lanes they imported) so their CLASS tables can be freed."""
    import gc
    _MODS.clear()
    for n in [n for n in sys.modules if n.startswith("xr34_") or n in (
            "L362_forest_pincer_convergence", "L347_switch_forest_flux_power")]:
        del sys.modules[n]
    gc.collect()


# ------------------------------------------------------------------------------------------------------ the PM runs
def _job(job):
    """one lane run in its own process: job = (lane, patch, cfg); returns the lane's own (name, out) plus wall and peak RSS."""
    lane, patch, cfg = job
    t0 = time.time()
    mod = module(lane, patch)
    name, out = getattr(mod, LANES[lane]["runfn"])(cfg)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_gb = rss / 1e9 if sys.platform == "darwin" else rss / 1e6       # bytes on macOS, kB on Linux
    return dict(lane=lane, patch=patch, name=name, out=out, wall_s=time.time() - t0, peak_rss_gb=rss_gb)


class Budget:
    """An optional machine-wide budget shared by concurrently running XR34 scripts (env XR34_SLOTDIR, a scratch folder).
    Three token files: a light run (128^3 mesh, <= 1.6 GB) holds one, a heavy run (256^3 mesh, ~6.7 GB) holds two, so
    across all scripts at most one heavy + one light, or three light, runs at once: <= 3 processes and <= ~8.3 GB of
    workers.  A heavy run waiting for its two tokens holds the 'gate' exclusively, which stops new light runs from
    starting anywhere until it has them.  Tokens are flock()s: a process that dies releases them.  Without XR34_SLOTDIR
    only the per-script limits apply."""

    def __init__(self):
        self.dir = os.environ.get("XR34_SLOTDIR")
        self.n = int(os.environ.get("XR34_NTOK", 3))
        self.gate = None
        if self.dir:
            os.makedirs(self.dir, exist_ok=True)

    def _fd(self, name):
        return os.open(os.path.join(self.dir, name), os.O_CREAT | os.O_RDWR)

    @staticmethod
    def _try(fd, mode):
        try:
            fcntl.flock(fd, mode | fcntl.LOCK_NB)
            return True
        except OSError:
            return False

    def take(self, heavy, gated=True):
        """non-blocking: the held token fds, or None."""
        if not self.dir:
            return []
        if gated and heavy and self.gate is None:
            fd = self._fd("gate")
            if not self._try(fd, fcntl.LOCK_EX):
                os.close(fd)
                return None
            self.gate = fd
        elif gated and not heavy:
            fd = self._fd("gate")
            ok = self._try(fd, fcntl.LOCK_SH)
            os.close(fd)                                                # closing releases the shared lock
            if not ok:
                return None
        need, got = (2 if heavy else 1), []
        for i in range(self.n):
            fd = self._fd(f"token{i}")
            if self._try(fd, fcntl.LOCK_EX):
                got.append(fd)
                if len(got) == need:
                    break
            else:
                os.close(fd)
        if len(got) < need:
            for fd in got:
                os.close(fd)
            return None
        if heavy and self.gate is not None:
            os.close(self.gate)
            self.gate = None
        return got

    @staticmethod
    def give(fds):
        for fd in fds or []:
            os.close(fd)

    def wait_take(self, heavy=False, poll=5.0):
        while True:
            fds = self.take(heavy)
            if fds is not None:
                return fds
            time.sleep(poll)


def run_jobs(jobs, heavy=lambda job: False, nproc=3, nheavy=1, log=print):
    """run jobs = [(lane, patch, cfg), ...] in priority order: <= nproc processes, <= nheavy heavy ones at a time, and
    within the machine-wide Budget when XR34_SLOTDIR is set.  Each run gets a fresh spawned process (one thread).
    Returns {(lane, patch, name): result}.  A 256^3-mesh run peaks at ~6.7 GB and a 128^3 one at ~1.3-1.6 GB."""
    nproc = int(os.environ.get("XR34_NPROC", nproc))
    nheavy = int(os.environ.get("XR34_NHEAVY", nheavy))
    release_modules()                                                   # the parent keeps no CLASS tables while workers run
    bud = Budget()
    pending, running, held, res = list(jobs), {}, {}, {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=nproc, mp_context=mp.get_context("spawn"), max_tasks_per_child=1) as ex:
        while pending or running:
            i = 0
            while len(running) < nproc and i < len(pending):
                j = pending[i]
                if heavy(j) and sum(1 for r in running.values() if heavy(r)) >= nheavy:
                    i += 1
                    continue
                fds = bud.take(heavy(j))
                if fds is None:
                    if heavy(j):
                        break                                           # the heavy run waits at the head, holding the gate
                    i += 1
                    continue
                fut = ex.submit(_job, j)
                running[fut], held[fut] = j, fds
                pending.pop(i)
            if not running:
                time.sleep(5)
                continue
            done, _ = wait(list(running), timeout=10, return_when=FIRST_COMPLETED)
            for fut in done:
                j = running.pop(fut)
                bud.give(held.pop(fut))
                r = fut.result()
                res[(r["lane"], r["patch"], r["name"])] = r
                log(f"    run done: {r['lane']:5s} {r['patch']:6s} {r['name']:22s} {r['wall_s']:7.0f} s, peak RSS "
                    f"{r['peak_rss_gb']:.2f} GB   [{time.time() - t0:.0f} s; {len(pending)} queued, {len(running)} running]")
    return res


def _k1_job(lane, fix):
    return halo_summary(halo_table(lane, fix)), halo_summary(halo_table(lane, "none"))


def k1_tables(lane, fix):
    """K1's two single-halo summaries (the corrected line -- or the MUTATE's doubled one -- and the committed line), computed
    in a spawned child holding one Budget token, so the parent never holds the lanes' CLASS tables."""
    bud = Budget()
    fds = bud.wait_take(heavy=False)
    try:
        with ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn")) as ex:
            return ex.submit(_k1_job, lane, fix).result()
    finally:
        bud.give(fds)


# ------------------------------------------------------------------------------------------------ the single-halo probe
def accel_source(lane, patch):
    """the (patched) accel() closure of the lane's run function, dedented, as source text."""
    src, _ = patched_source(lane, patch)
    lines = src.splitlines()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.FunctionDef) and node.name == LANES[lane]["runfn"]:
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef) and sub.name == "accel":
                    code = textwrap.dedent("\n".join(lines[sub.lineno - 1:sub.end_lineno]))
                    want = textwrap.dedent(LANES[lane]["line"].replace("/ a ** 2", PATCH[patch])).strip()
                    if want not in code:
                        raise RuntimeError(f"{lane}/{patch}: the extracted accel() does not carry the patched kernel line")
                    return code
    raise RuntimeError(f"{lane}: accel() not found")


def lane_consts(lane):
    """(Om, h, A0_SI, UNIT_ACC, nu_mono) exactly as the lane uses them."""
    m = module(lane, "none")
    base = m.L7 if lane in ("L359", "DE11") else (m.L62 if lane == "DE11b" else m)
    return dict(Om=base.Om, h=base.h, A0_SI=dict(base.A0_SI), UNIT_ACC=base.UNIT_ACC, A0=dict(base.A0), nu_mono=base.nu_mono)


def box_of(lane, L):
    """(L, NG) of the probe box: the lane's own mesh (L346's box is fixed at 50 Mpc/h, 128^3)."""
    if lane == "L346":
        return module(lane, "none").L, module(lane, "none").NG
    return L, 128


def probe(lane, patch, a, rho, xq, foot="canonical", L=25.0, newtonian=False):
    """the lane's own accel() (patched) evaluated at scale factor a on the prescribed mesh density rho (= 1 + delta) at the
    query points xq; returns the kick -grad_x phi at xq (code units).  newtonian=True runs the lane's LCDM branch; otherwise
    the switch is on everywhere (f = 1: full QUMOND), which exercises the same kernel line as the forest runs."""
    mod = module(lane, patch)
    code = accel_source(lane, patch)
    ns = dict(mod.__dict__)
    npart = len(xq)
    L, NG = box_of(lane, L)
    dep = lambda x, w: rho * (npart / NG ** 3)                          # so that the lane's rho = deposit * NG^3/npart = rho
    zero = lambda: {"dph": np.zeros((NG, NG, NG)), "f": np.zeros((NG, NG, NG))}
    if lane == "L362":
        s = mod.Sim(L, NG, NG); s.deposit = dep
        ns.update(s=s, npart=npart, mode="lcdm" if newtonian else "switch", xc=0.0, a0=mod.A0[foot])
    elif lane == "DE11b":
        s = mod.L62.Sim(L, NG, NG); s.deposit = dep
        ns.update(s=s, npart=npart, mode="lcdm" if newtonian else "all", a0=mod.L62.A0[foot], state=zero(), w=0.25)
    elif lane == "DE11":
        bx = mod.L7.Box(L); bx.deposit = dep
        ns.update(bx=bx, npart=npart, mode="lcdm" if newtonian else "l347", xc=0.0, a0=mod.L7.A0[foot], state=zero(), w=0.25)
    elif lane == "L347":
        bx = mod.Box(L); bx.deposit = dep
        ns.update(bx=bx, npart=npart, mode="lcdm" if newtonian else "switch", xc=0.0, a0=mod.A0[foot])
    elif lane == "L359":
        bx = mod.L7.Box(L); bx.deposit = dep
        ns.update(bx=bx, npart=npart, mode="lcdm" if newtonian else "switch", xc0=0.0, p=0.0, a0=mod.L7.A0[foot])
    elif lane == "L346":
        ns.update(npart=npart, mode="lcdm" if newtonian else "switch", a0=mod.A0[foot], xc=0, Rs=0.0, ph_in_x=False,
                  cic_deposit=dep)
    else:
        raise ValueError(lane)
    ns.update(L=L, NG=NG, NP=NG)                                         # run()'s own locals, where the closure reads them
    exec(code, ns)
    out = ns["accel"](xq, a)
    return out[0] if lane == "L346" else out


# SI constants for the analytic halo (independent of the lanes' unit constants)
G_SI, MPC_M, KMS = 6.674e-11, 3.0857e22, 1e3


def plummer_setup(L, NG, b_cells=4.0, rq_cells=range(8, 17)):
    """a Plummer sphere centred on a mesh node; returns (delta_shape, xq, r_q [Mpc/h], b [Mpc/h], centre).
    delta_shape integrates to 1 (Mpc/h)^3 over the continuum; the mesh field is multiplied by the chosen mass."""
    d = L / NG
    c = (NG // 2) * d
    b = b_cells * d
    ax = np.arange(NG) * d - c
    ax = (ax + L / 2) % L - L / 2                                        # minimum image
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    r2 = X ** 2 + Y ** 2 + Z ** 2
    shape = 3.0 / (4 * math.pi * b ** 3) * (1 + r2 / b ** 2) ** -2.5
    rq = np.array([n * d for n in rq_cells])
    pts = []
    for n in rq_cells:
        for ax_ in range(3):
            for sgn in (1, -1):
                v = np.full(3, c); v[ax_] += sgn * n * d; pts.append(v)
    return shape, np.array(pts), rq, b, c


def plummer_gN_SI(Mc, rq, b, a, h, Om):
    """G M(<r)/r_phys^2 in m/s^2 for a Plummer of Mc (Mpc/h)^3 of mean matter density, from SI constants alone."""
    H0 = 100.0 * h * KMS / MPC_M
    rho_m0 = Om * 3 * H0 ** 2 / (8 * math.pi * G_SI)                    # kg/m^3, the physical mean matter density today
    Lm = MPC_M / h                                                       # 1 Mpc/h in m
    Menc = rho_m0 * Mc * Lm ** 3 * rq ** 3 / (rq ** 2 + b ** 2) ** 1.5  # kg; the excess mass is conserved (comoving)
    return G_SI * Menc / (a * rq * Lm) ** 2


SCALE = {"none": lambda z: 1 + z, "fix": lambda z: 1.0, "double": lambda z: 1 / (1 + z)}   # argument / g_N,phys


def halo_table(lane, patch, L=25.0, zs=(3.0, 2.0, 0.0), foots=("canonical", "alt"), y12=0.2, b_cells=4.0,
               rq_cells=range(8, 17)):
    """the single-halo probe of one lane and one variant of the kernel line.
    A Plummer sphere (b = 4 cells) centred on a mesh node, its mass set so that y = g_N/a0 = 0.2 at r = 12 cells, z = 3,
    canonical footing (y ~ 0.1-0.4 at z = 3, 0.06-0.2 at z = 2, 0.006-0.02 at z = 0 over r = 8-16 cells: the MOND regime).
    For each z and footing, over r = 8-16 cells (averaged over the six axis directions, on mesh nodes):
      newton   the lane's own Newtonian kick / a  over  G M(<r)/r_phys^2 from SI constants        (1 if phi_N is physical)
      ratio    the lane's own QUMOND kick / a     over  nu_mono(g_N/a0) g_N (analytic, the lane's nu_mono and a0)
      pred     this variant's predicted ratio     nu_mono(s y)/nu_mono(y), s = (1+z) | 1 | 1/(1+z)
    """
    C = lane_consts(lane)
    Lb, NG = box_of(lane, L)
    shape, xq, rq, b, c = plummer_setup(Lb, NG, b_cells, rq_cells)
    r12 = 12 * Lb / NG
    Mc = y12 * C["A0_SI"]["canonical"] / plummer_gN_SI(1.0, np.array([r12]), b, 0.25, C["h"], C["Om"])[0]
    dm = Mc * shape
    rho = 1.0 + (dm - dm.mean())                                          # the lane's zero-mean contrast
    nr = len(rq)
    out = {"box": [Lb, NG], "b_cells": b_cells, "r_cells": list(rq_cells), "Mc_Mpch3": Mc, "rows": {}}
    for z in zs:
        a = 1.0 / (1.0 + z)
        gN = plummer_gN_SI(Mc, rq, b, a, C["h"], C["Om"])
        kN = probe(lane, patch, a, rho, xq, newtonian=True)
        gcN = np.linalg.norm(kN, axis=1).reshape(nr, 6).mean(1) * C["UNIT_ACC"]
        for foot in foots:
            y = gN / C["A0_SI"][foot]
            kM = probe(lane, patch, a, rho, xq, foot=foot)
            gM = np.linalg.norm(kM, axis=1).reshape(nr, 6).mean(1) / a * C["UNIT_ACC"]
            ana = C["nu_mono"](y) * gN
            pred = C["nu_mono"](SCALE[patch](z) * y) / C["nu_mono"](y)
            out["rows"][f"z{z:g}/{foot}"] = dict(z=z, foot=foot, y=y.tolist(), newton=(gcN / a / gN).tolist(),
                                                 newton_a2=(gcN / a ** 2 / gN).tolist(), ratio=(gM / ana).tolist(),
                                                 pred=pred.tolist())
    return out


def halo_summary(tab):
    """max |newton - 1|, max |ratio - 1|, max |ratio/pred - 1| per row."""
    s = {}
    for k, r in tab["rows"].items():
        s[k] = dict(newton=float(np.max(np.abs(np.array(r["newton"]) - 1))), ratio=float(np.max(np.abs(np.array(r["ratio"]) - 1))),
                    vs_pred=float(np.max(np.abs(np.array(r["ratio"]) / np.array(r["pred"]) - 1))),
                    ratio_min=float(np.min(r["ratio"])), ratio_max=float(np.max(r["ratio"])),
                    y_min=float(np.min(r["y"])), y_max=float(np.max(r["y"])))
    return s


# ------------------------------------------------------------------------------------------------------- bookkeeping
class Tee:
    def __init__(self, path):
        self.f = open(path, "w"); self.o = sys.stdout

    def write(self, s):
        self.o.write(s); self.f.write(s)

    def flush(self):
        self.o.flush(); self.f.flush()


class Lane:
    """one XR34 script's bookkeeping: its .out tee, its checks, its JSON (MUTATE -> _MUTATE names)."""

    def __init__(self, slug, mutate):
        self.slug, self.mutate = slug, mutate
        self.t0 = time.time()
        self.checks, self.out = [], {"lane": slug, "mutate": mutate, "checks": {}, "numbers": {}}
        self.dir = os.environ.get("XR34_OUTDIR", HERE)                  # smoke runs write elsewhere, never for the record
        # a spawned worker re-imports the main script: it must not re-open (truncate) the parent's .out.  (During that
        # re-import mp.parent_process() is still None; the process name is already the child's.)
        self.child = mp.current_process().name != "MainProcess" or mp.parent_process() is not None
        if not self.child:
            os.makedirs(self.dir, exist_ok=True)
            self.tee = Tee(os.path.join(self.dir, f"{slug}{'_MUTATE' if mutate else ''}.out"))
            sys.stdout = self.tee

    def P(self, *a):
        print(*a, flush=True)

    def banner(self, t):
        self.P("\n" + "=" * 116 + "\n" + t + "\n" + "=" * 116)

    def check(self, name, measured, ok, reading="", load_bearing=True):
        ok = bool(ok)
        self.checks.append((name, ok, load_bearing))
        self.out["checks"][name.split(" ")[0]] = {"title": name, "ok": ok, "measured": str(measured), "load_bearing": load_bearing}
        self.P(f"  [{'PASS' if ok else 'FAIL'}] {name}{'' if load_bearing else '  (reported, not load-bearing)'}")
        self.P(f"         measured: {measured}")
        if reading:
            self.P(f"         reading:  {reading}")
        return ok

    def el(self):
        return f"[{time.time() - self.t0:.0f} s]"

    def finish(self):
        n_fail = sum(1 for _, ok, lb in self.checks if lb and not ok)
        self.out["n_checks"] = len(self.checks)
        self.out["n_pass"] = sum(1 for _, ok, _ in self.checks if ok)
        self.out["n_fail_load_bearing"] = n_fail
        self.out["wall_s"] = round(time.time() - self.t0, 1)
        name = f"{self.slug}_results{'_MUTATE' if self.mutate else ''}.json"
        with open(os.path.join(self.dir, name), "w") as f:
            json.dump(self.out, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        self.P(f"\n  {self.out['n_pass']}/{len(self.checks)} checks pass; load-bearing failures: {n_fail}; wrote {name}   {self.el()}")
        self.P(f"rc={0 if n_fail == 0 else 1}")
        self.tee.flush()
        return 0 if n_fail == 0 else 1


def worst_p1d(res_run, res_ref, zs=("3.0", "2.0"), kmin=0.2, kmax=2.0):
    """the record's statistic (L347 rule): max |P1D/P1D_ref - 1| over k_par in [kmin, kmax] h/Mpc and the given redshifts."""
    w = 0.0
    for z in zs:
        kp = np.array(res_ref[z]["kpar"]); r = np.array(res_run[z]["p1d"]) / np.array(res_ref[z]["p1d"])
        m = (kp >= kmin) & (kp <= kmax)
        w = max(w, float(np.max(np.abs(r[m] - 1))))
    return w


def max_abs_diff_p1d(run_a, run_b, zs=("3.0", "2.0")):
    """max |P1D_a/P1D_b - 1| over all k_par and redshifts (the exactness of a reproduction)."""
    return max(float(np.max(np.abs(np.array(run_a[z]["p1d"]) / np.array(run_b[z]["p1d"]) - 1))) for z in zs)
