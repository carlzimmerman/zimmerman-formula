"""AGB1, POST HOC (written after the Part A numbers were seen; not in FROZEN_CRITERIA.md; no frozen word).

The same today / ever questions with NO supernovae at all, so that nothing in the answer depends on any supernova
magnitude or on the age dispute: DESI DR2 BAO alone, and BAO + DESI's compressed CMB prior, flat w0-wa, using the
lane's own fitter. Writes agb1_posthoc_nosn.json; log to agb1_posthoc_nosn.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.argv = ["agb1_run.py", "POSTHOC"]
import agb1_run as R

out = {}
for label, part in (("BAO only", "A"), ("BAO + compressed CMB prior", "C")):
    F = R.Fitter(part, None, R.BAO("all"))
    free = F.fit({}, []); today = F.fit({}, [], "today", extra=(free,)); never = F.fit({}, [], "never", extra=(today, free))
    out[label] = dict(free=free, today=today, never=never, D_today=today["chi2"] - free["chi2"], D_never=never["chi2"] - free["chi2"])
    print(f"{label}: best chi2 {free['chi2']:.3f}  Om {free['Om']:.4f} w0 {free['w0']:+.3f} wa {free['wa']:+.3f} q0 {free['q0']:+.3f}"
          f" (min q {free['qmin']:+.3f} at z {free['z_qmin']:.2f})  edge {free['edge']}", flush=True)
    print(f"   q0 = 0: dchi2 {out[label]['D_today']:.3f};  never accelerated: dchi2 {out[label]['D_never']:.3f}"
          f" (Om {never['Om']:.4f} w0 {never['w0']:+.3f} wa {never['wa']:+.3f} min q {never['qmin']:+.5f}  edge {never['edge']})", flush=True)
json.dump(out, open(os.path.join(HERE, "agb1_posthoc_nosn.json"), "w"), indent=1, default=float)
print("wrote agb1_posthoc_nosn.json")
