"""SCS2: KA4's two-resolution clause applied to every background that has a coarse twin (the graded KA4 in scs2_aqual.py
checks the primaries only; this extends it to the axisymmetric brackets, the external-field ones included, and is reported
beside KA4). Criteria FROZEN_CRITERIA.md (158c4cf770), amendments A1-A3.

Per background: the negative halo-charge fraction Q_neg/Q_pos (off-plane cells) and the minimum off-plane D.P on the fine and
the coarse grid, over the same radius (the coarse grid's outer edge); agreement within 20 % (or both zero), as KA4 states it.
Reads the solver caches ($SCS2_CACHE) written by scs2_aqual.py.  TEST lane; adopts nothing.
"""
import os, sys, json, glob, resource, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scs2_aqual as S

CACHE = os.environ.get("SCS2_CACHE", os.path.join(HERE, "_cache"))
t0 = time.time()
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))

def agree(a, b):
    if a is None or b is None:
        return False
    if abs(a) == 0 and abs(b) == 0:
        return True
    return abs(a - b) <= 0.2 * max(abs(a), abs(b))

rows = []
for fc in sorted(glob.glob(os.path.join(CACHE, "*_coarse.npz"))):
    tag = os.path.basename(fc)[: -len("_coarse.npz")]
    ff = os.path.join(CACHE, tag + ".npz")
    if not os.path.exists(ff):
        continue
    kind = "point" if tag.startswith("KA1") else next(t for t in tag.split("_") if t in ("expo", "kuzmin", "expo+bulge", "thick"))
    out = {}
    for lab, path in (("fine", ff), ("coarse", fc)):
        bg = S.load_cache(path); bg["kind"] = kind
        out[lab] = bg
    crop = min(out["fine"]["g"].rf[-1], out["coarse"]["g"].rf[-1])
    sf = S.summarize_map(out["fine"], crop); scm = S.summarize_map(out["coarse"], crop)
    fr_f = sf["frac_neg_over_pos"] or 0.0; fr_c = scm["frac_neg_over_pos"] or 0.0
    mn_f = sf["min_dp_offplane"]; mn_c = scm["min_dp_offplane"]
    neg_f = sf["n_negative_offplane"] > 0; neg_c = scm["n_negative_offplane"] > 0
    ok_frac = agree(fr_f, fr_c)
    ok_min = (mn_f > 0 and mn_c > 0) or agree(mn_f, mn_c)
    rows.append(dict(tag=tag, kind=kind, frac_fine=fr_f, frac_coarse=fr_c, min_dp_fine=mn_f, min_dp_coarse=mn_c,
                     negative_fine=neg_f, negative_coarse=neg_c, sign_agree=bool(neg_f == neg_c),
                     frac_agree=bool(ok_frac), min_agree=bool(ok_min)))
    P_(f"[{tag}] Q_neg/Q_pos fine {fr_f:.4f} coarse {fr_c:.4f} ({'agree' if ok_frac else 'DIFFER'}); min D.P fine {mn_f:.3e} "
       f"coarse {mn_c:.3e} ({'agree' if ok_min else 'DIFFER'}); negative cells on both grids: {neg_f and neg_c}")

n = len(rows)
summary = dict(n=n, sign_agree=sum(r_["sign_agree"] for r_ in rows), frac_agree=sum(r_["frac_agree"] for r_ in rows),
               min_agree=sum(r_["min_agree"] for r_ in rows),
               differ=[r_["tag"] for r_ in rows if not (r_["frac_agree"] and r_["min_agree"] and r_["sign_agree"])])
P_(f"backgrounds with a coarse twin: {n}; sign of the map agrees on {summary['sign_agree']}; charge fraction within 20 % on "
   f"{summary['frac_agree']}; minimum D.P within 20 % (or both positive) on {summary['min_agree']}")
P_(f"differ: {summary['differ']}")
RES = dict(lane="SCS2", script="scs2_resolution.py", criteria="158c4cf770", rows=rows, summary=summary,
           seconds=round(time.time() - t0, 1), peak_rss_GB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3),
           footer="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs2_resolution.json"), "w") as fh:
    json.dump(RES, fh, indent=1)
P_(f"runtime {RES['seconds']} s, peak RSS {RES['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, "scs2_resolution.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
