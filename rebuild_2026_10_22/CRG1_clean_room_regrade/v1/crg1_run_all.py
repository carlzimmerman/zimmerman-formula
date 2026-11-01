"""Orchestrator: clean rebuild, K3 repeat, MUTATE, A5(b). Resumable: finished parts are skipped unless --clean."""
import os, sys, subprocess, time, shutil, hashlib, resource, json, numpy, scipy, glob
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
os.environ.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
LOG = open("crg1_run.log", "a")
def L(m):
    s = "%s %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), m); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
def run(script, *args, env=None, expect=0):
    t = time.time(); e = dict(os.environ); e.update(env or {})
    r = subprocess.run([sys.executable, script, *args], env=e, capture_output=True, text=True)
    LOG.write(r.stdout); LOG.flush()
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1048576.0
    L("%s %s rc=%d %.1fs peak-child-so-far %.0fMB%s" % (script, " ".join(args), r.returncode, time.time() - t, peak, " env=%s" % env if env else ""))
    if r.returncode != expect:
        L(r.stderr[-1500:]); sys.exit("STOP: %s rc %d" % (script, r.returncode))
def pipeline(res, env=None):
    for s in ("crg1_zoom.py", "crg1_efe.py", "crg1_k1_math.py", "crg1_k1_shear.py"): run(s, env=env)
    run("crg1_k1_shear.py", "--flip", env=env, expect=1)
    for s in ("crg1_k2.py", "crg1_sparc.py", "crg1_clusters.py", "crg1_groups.py", "crg1_lens.py", "crg1_dwarfs.py"): run(s, env=env)
    run("crg1_aggregate.py", res, env=env)
if __name__ == "__main__":
    t0 = time.time()
    if "--clean" in sys.argv:
        for d in ("partials", "cache", "k3", "oneset", "mutate"): shutil.rmtree(d, ignore_errors=True)
    L("START numpy %s scipy %s python %s" % (numpy.__version__, scipy.__version__, sys.version.split()[0]))
    pipeline("crg1_results.json"); a = hashlib.sha256(open("crg1_results.json", "rb").read()).hexdigest(); L("results sha256 %s" % a)
    t1 = time.time()
    pipeline("crg1_results_K3repeat.json", env=dict(CRG1_PARTIALS="k3/partials", CRG1_CACHE="k3/cache"))
    b = hashlib.sha256(open("crg1_results_K3repeat.json", "rb").read()).hexdigest()
    L("K3 repeat sha256 %s identical=%s" % (b, a == b))
    if a != b: sys.exit("K3 FAILED")
    # MUTATE nu=1
    env = dict(CRG1_MUTATE_NU1="1", CRG1_PARTIALS="mutate/partials", CRG1_CACHE="mutate/cache")
    run("crg1_mutate.py", env=env)
    # A5(b)
    env = dict(CRG1_ONESET="1", CRG1_PARTIALS="oneset/partials", CRG1_CACHE="oneset/cache")
    run("crg1_a5b.py", env=env)
    rt = dict(total_s=time.time() - t0, first_pipeline_s=t1 - t0, peak_child_MB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1048576.0, numpy=numpy.__version__, scipy=scipy.__version__)
    json.dump(rt, open("crg1_runtime.json", "w"), indent=1, sort_keys=True)
    L("DONE %s" % rt)
