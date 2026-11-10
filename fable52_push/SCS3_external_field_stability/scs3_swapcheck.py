"""SCS3 amendments A2 (63ed365df0) item 2 and A3 (fe9811fe03): the solver-swap check. The MMD-ordered direct LU re-solves PL R1 for canonical expo 9.4 at 0.1 a0 and canonical Kuzmin 10.9 at 0.01 a0; Gamma_L^2 (A2 reading) and min D.P
must equal the COLAMD (frozen) solve's to 1e-3 relative.  Also records the frozen 4 GB probe's outcome (passed in by the caller).
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, time, resource
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
os.environ.update(SCS3_SET="X", SCS3_A2="1", SCS3_ITER="1")
import scs3_maps as m
S = m.S
out = dict(lane="SCS3", script="scs3_swapcheck.py", amendment_A2="63ed365df0", amendment_A3="fe9811fe03",
           probe=dict(background="PL canonical expo 9.4 0.1 a0 R2, frozen direct solver", killed_at_rss_GB=5.97, line_GB=4.0,
                      below_line=False), rows=[])
for kind, lm, ge in (("expo", "9.4", 0.1), ("kuzmin", "10.9", 0.01)):
    d = dict(group="PL", foot="canonical", kind=kind, logm=lm, ge=ge, axis="x")
    tg = m.tag_of(d, 1)
    direct = S.load_cache(os.path.join(m.CACHE, tg + ".npz")); direct["kind"] = kind; m.a1_mask(direct, d)
    t = time.time()
    it = S.background("canonical", kind, lm, ge=ge, axis="x", res=1); m.a1_mask(it, d)
    a = m.route_L(direct, kind)["L"]["Gamma2_max_s2"]; b = m.route_L(it, kind)["L"]["Gamma2_max_s2"]
    da = S.summarize_map(direct)["min_dp_offplane"]; db = S.summarize_map(it)["min_dp_offplane"]
    row = dict(tag=tg, Gamma2_direct=a, Gamma2_iter=b, rel_Gamma2=abs(b / a - 1), min_dp_direct=da, min_dp_iter=db,
               rel_min_dp=abs(db / da - 1), residual_iter=it["residual"], seconds=round(time.time() - t, 1))
    row["pass_"] = bool(row["rel_Gamma2"] <= 1e-3 and row["rel_min_dp"] <= 1e-3)
    out["rows"].append(row); print(row, flush=True)
out["pass_"] = all(r["pass_"] for r in out["rows"])
out["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
out["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
json.dump(out, open(os.path.join(HERE, "scs3_swapcheck.json"), "w"), indent=1)
print("swap check", "PASS" if out["pass_"] else "FAIL", "peak", out["peak_rss_GB"], "GB")
