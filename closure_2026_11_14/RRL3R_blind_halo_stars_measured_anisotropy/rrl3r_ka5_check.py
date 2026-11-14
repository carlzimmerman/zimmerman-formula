#!/usr/bin/env python3
"""
RRL3R diagnostic after the as-frozen run stopped on KA-5 (a_out of the planted broken mock 3.1 sigma low).
Question: is that one seed a fluctuation, or is the fit biased? Runs the same machinery (rrl3r.py executed up to the
end of the nominal PS1 fit, with its output file redirected so rrl3r.out is not touched) on 40 planted single-law
mocks (a = 4.5) and 40 planted broken mocks (3 / 5 / 35), seeds 331700 + k and 331800 + k, and prints the pulls.
No BHB number beyond rrl3r.py's known answers is computed. Writes rrl3r_ka5_check.out.
Usage: python3 -I -B rrl3r_ka5_check.py <PS1 tsv> <DES tsv> <MWS_BHB.fits>
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "rrl3r.py")).read()
cut = src.index('sec("Null mocks from the best single law')
src = src[:cut].replace('os.path.join(HERE, "rrl3r.out")', 'os.path.join(HERE, "rrl3r_ka5_check_head.out")')
G = {"__name__": "rrl3r_head", "__file__": os.path.join(HERE, "rrl3r.py")}
exec(compile(src, "rrl3r.py (head)", "exec"), G)
np = G["np"]; NOM = G["NOM"]; set_data = G["set_data"]; draw_mock = G["draw_mock"]; fit_both = G["fit_both"]; fit_single = G["fit_single"]
out = open(os.path.join(HERE, "rrl3r_ka5_check.out"), "w")
def say(s): print(s, flush=True); out.write(s + "\n"); out.flush()
say(f"N = {NOM['N']} (nominal PS1). Planted single a = 4.5 (40 seeds 331700+k); planted broken 3 / 5 / 35 (40 seeds 331800+k).")
ps = []
for k in range(40):
    m = dict(NOM); set_data(m, draw_mock(NOM, ("single", 4.5), np.random.default_rng(331700 + k))); s1 = fit_single(m)
    ps.append(((s1["a"] - 4.5) / s1["sig"], s1["a"], s1["sig"]))
ps = np.array(ps)
say(f"single: mean a {ps[:, 1].mean():.4f} (sd over seeds {ps[:, 1].std():.4f}; mean Hessian sigma {ps[:, 2].mean():.4f}); pull mean {ps[:, 0].mean():+.3f}, pull sd {ps[:, 0].std():.3f}; |pull| > 2 in {int(np.sum(np.abs(ps[:, 0]) > 2))} of 40")
pb = []
for k in range(40):
    m = dict(NOM); set_data(m, draw_mock(NOM, ("broken", 3.0, 5.0, 35.0), np.random.default_rng(331800 + k)))
    s1, b1, tl = fit_both(m, (25.0, 75.0)); e = b1["err"]
    pb.append([b1["ain"], b1["aout"], b1["rb"], e[0], e[1], e[2], tl])
    say(f"  seed {331800 + k}: a_in {b1['ain']:.3f} +/- {e[0]:.3f}, a_out {b1['aout']:.3f} +/- {e[1]:.3f}, rb {b1['rb']:.2f} +/- {e[2]:.2f}, 2dlnL {tl:.1f}")
pb = np.array(pb)
for i, (nm, tv) in enumerate((("a_in", 3.0), ("a_out", 5.0), ("rb", 35.0))):
    pull = (pb[:, i] - tv) / pb[:, i + 3]
    say(f"broken {nm}: mean {pb[:, i].mean():.4f} (true {tv}), sd over seeds {pb[:, i].std():.4f}, mean Hessian sigma {pb[:, i + 3].mean():.4f}; "
        f"pull mean {pull.mean():+.3f}, pull sd {pull.std():.3f}; |pull| > 2 in {int(np.sum(np.abs(pull) > 2))} of 40")
allok = np.sum((np.abs(pb[:, 0] - 3) <= 2 * pb[:, 3]) & (np.abs(pb[:, 1] - 5) <= 2 * pb[:, 4]) & (np.abs(pb[:, 2] - 35) <= np.maximum(2 * pb[:, 5], 5.0)))
say(f"seeds passing all three of KA-5's broken-mock parameter tests: {int(allok)} of 40")
say("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
out.close()
