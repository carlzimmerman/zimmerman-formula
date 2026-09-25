# -*- coding: utf-8 -*-
"""
sandbox.py -- re-run deepseek_push lanes UNMODIFIED on corrected inputs, without touching the committed tree.

A sandbox is a temporary directory that mirrors the repository root:
  <S>/deepseek_push/   real directory: every top-level FILE is a copy-on-write clone (APFS clonefile via `cp -c`, else a
                       plain copy); every top-level DIRECTORY is a read-only symlink.  The lanes re-run here write only
                       top-level files, so no write reaches the committed tree.
  <S>/glm53_push/data/rotation_curve_corpus_v7.json   the corpus variant under test (a real file)
  every other repository entry                          a symlink (read-only inputs such as real_research/data)
The corpus variants change ONLY the SPARC entries: m2l_disk is set to a stated 3.6-micron disc ratio; the bulge ratio is
applied by rescaling V_bul (and SB_bul) so that the lanes' own expression m2l*(V_disk^2 + V_bul^2) equals
Y_disc V_disk^2 + Y_bul V_bul^2; optionally rings with errV/Vobs >= 0.10 are dropped.  V_obs, V_disk, V_gas, radii,
distances and inclinations are untouched.
"""
import os, sys, re, json, math, shutil, subprocess, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
DS = os.path.join(ROOT, "deepseek_push")
CORPUS = os.path.join(ROOT, "glm53_push", "data", "rotation_curve_corpus_v7.json")


def corpus_variant(ud=None, ub=0.7, qcut=None, keep_corpus_ml=False):
    """None -> the committed corpus unchanged.  keep_corpus_ml=True is the MUTATE control: the quality cut and bulge
    rescaling machinery run, but the SPARC m2l_disk values are left as the corpus has them (the correction is NOT applied)."""
    d = json.load(open(CORPUS))
    if ud is None and qcut is None:
        return d
    for g in d["galaxies"]:
        if g.get("survey") != "SPARC":
            continue
        m_old = g.get("m2l_disk") or 0.0
        m_old = m_old if m_old > 0 else 0.5
        m_new = m_old if keep_corpus_ml else ud
        ub_eff = m_old if keep_corpus_ml else ub
        scale_b = math.sqrt(ub_eff / m_new)            # m_new * (scale_b V_bul)^2 = ub_eff * V_bul^2
        rings = []
        for p in g.get("data") or []:
            if qcut is not None and not (p.get("Vobs", 0) > 0 and p.get("errV", 1e9) / p["Vobs"] < qcut):
                continue
            q = dict(p)
            q["Vbul"] = p["Vbul"] * scale_b
            if "SBbul" in q and q["SBbul"] is not None:
                q["SBbul"] = p["SBbul"] * (ub_eff / m_new)
            rings.append(q)
        g["data"] = rings
        g["n_points"] = len(rings)
        g["m2l_disk"] = m_new
    return d


def _clone(src, dst):
    if sys.platform == "darwin":
        r = subprocess.run(["cp", "-c", src, dst], capture_output=True)
        if r.returncode == 0:
            return
    shutil.copy2(src, dst)


def build(corpus_json, patches=None, tag="sb"):
    """patches: {lane_filename: [(old, new), ...]} applied to the sandbox COPY of a lane (input constants only)."""
    S = tempfile.mkdtemp(prefix=f"D02_{tag}_")
    for e in os.listdir(ROOT):
        if e in ("deepseek_push", "glm53_push", ".git"):
            continue
        os.symlink(os.path.join(ROOT, e), os.path.join(S, e))
    os.makedirs(os.path.join(S, "deepseek_push"))
    for e in os.listdir(DS):
        src = os.path.join(DS, e)
        dst = os.path.join(S, "deepseek_push", e)
        if os.path.isdir(src) and not os.path.islink(src):
            os.symlink(src, dst)
        else:
            _clone(src, dst)
    G = os.path.join(ROOT, "glm53_push")
    os.makedirs(os.path.join(S, "glm53_push", "data"))
    for e in os.listdir(G):
        if e != "data":
            os.symlink(os.path.join(G, e), os.path.join(S, "glm53_push", e))
    for e in os.listdir(os.path.join(G, "data")):
        if e != os.path.basename(CORPUS):
            os.symlink(os.path.join(G, "data", e), os.path.join(S, "glm53_push", "data", e))
    json.dump(corpus_json, open(os.path.join(S, "glm53_push", "data", os.path.basename(CORPUS)), "w"))
    for lane, reps in (patches or {}).items():
        patch(S, lane, reps)
    return S


def run(S, lane, timeout=3600, env=None):
    t0 = time.time()
    e = dict(os.environ, **(env or {}))
    r = subprocess.run([sys.executable, lane], cwd=os.path.join(S, "deepseek_push"), capture_output=True, text=True, timeout=timeout, env=e)
    return dict(lane=lane, rc=r.returncode, seconds=round(time.time() - t0, 1), stdout=r.stdout, stderr=r.stderr[-2000:])


def load(S, fn):
    p = os.path.join(S, "deepseek_push", fn)
    return json.load(open(p)) if os.path.exists(p) else None


def destroy(S):
    """remove the sandbox; symlinks are unlinked, never followed."""
    for dirpath, dirnames, filenames in os.walk(S, topdown=False, followlinks=False):
        for f in filenames:
            os.unlink(os.path.join(dirpath, f))
        for d in dirnames:
            p = os.path.join(dirpath, d)
            if os.path.islink(p):
                os.unlink(p)
            else:
                os.rmdir(p)
    os.rmdir(S)


def patch(S, lane, reps):
    """replace input constants in the SANDBOX copy of a lane (after its upstream lanes have run)."""
    p = os.path.join(S, "deepseek_push", lane)
    s = open(p).read()
    for rep in reps:
        if len(rep) == 3 and rep[0] == "re":                      # ("re", pattern, replacement): every match replaced
            s, n = re.subn(rep[1], lambda m, r=rep[2]: r, s)
            if n == 0:
                raise RuntimeError(f"patch pattern not found in {lane}: {rep[1]!r}")
        else:
            old, new = rep
            if old not in s:
                raise RuntimeError(f"patch anchor not found in {lane}: {old!r}")
            s = s.replace(old, new, 1)
    os.remove(p)                                                   # break the clone before writing (clone is CoW anyway)
    open(p, "w").write(s)
