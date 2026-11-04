"""FN3b Stage 1 (criteria s4): FN3's tested driver with Sigma_HI held at 6.0 and FN3b's readings. Written before any data.

Readings: R0 (drift 1), R1 (drift 0.5), R2 (no drift), R3b (Sigma_HI x 10^-0.25), R4b (x 10^+0.25), R5 (mu x 0.5),
R6 (mu x 2), R7 (delta_MS = 1); every reading holds Sigma_HI fixed. Context laws and MUTATE hold it at 6.0 too.
  python3 fn3b_stage1.py RUN <cutout_dir>      only after the owner's yes for FN3's cutouts and a K2'' PASS
  python3 fn3b_stage1.py SELFTEST <scratch>    plumbing test on synthetic cutouts
kappa = 1/2 FITTED; not theory closed.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FN3 = os.path.join(HERE, "..", "FN3_musedark_law_refit")
sys.path.insert(0, FN3)
import fn3_stage1 as S1  # noqa: E402

SIG_HI = 6.0
S1.READINGS = {"R0": dict(drift=1.0, sighi=SIG_HI), "R1": dict(drift=0.5, sighi=SIG_HI), "R2": dict(drift=0.0, sighi=SIG_HI),
               "R3b": dict(sighi=SIG_HI * 10 ** -0.25), "R4b": dict(sighi=SIG_HI * 10 ** 0.25),
               "R5": dict(mu=0.5, sighi=SIG_HI), "R6": dict(mu=2.0, sighi=SIG_HI), "R7": dict(dms=False, sighi=SIG_HI)}
_orig = S1.law_fit


def law_fit_fixed(P, a0, mu_scale=1.0, drift=1.0, sighi=None, dms=True, start=None, lo_ext=0.0):
    return _orig(P, a0, mu_scale=mu_scale, drift=drift, sighi=SIG_HI if sighi is None else sighi, dms=dms,
                 start=start, lo_ext=lo_ext)


S1.law_fit = law_fit_fixed
S1.OUTJ = os.path.join(HERE, "fn3b_stage1.jsonl")


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "SELFTEST":
        ok = S1.selftest(sys.argv[2])
        src = os.path.join(FN3, "fn3_stage1_selftest.out")
        txt = open(src).read() if os.path.exists(src) else ""
        open(os.path.join(HERE, "fn3b_stage1_selftest.out"), "w").write("FN3b (Sigma_HI fixed at 6.0)\n" + txt)
        sys.exit(0 if ok else 1)
    if len(sys.argv) > 2 and sys.argv[1] == "RUN":
        if not json.load(open(os.path.join(HERE, "fn3b_k2pp.json"))).get("pass_"):
            print("refusing: K2'' did not pass")
            sys.exit(2)
        sys.argv = [sys.argv[0], "RUN", sys.argv[2]]
        S1.main()
        return
    print(__doc__)


if __name__ == "__main__":
    main()
