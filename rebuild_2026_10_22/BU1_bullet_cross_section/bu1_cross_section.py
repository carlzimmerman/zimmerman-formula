"""BU1_bullet_cross_section -- frozen criteria FROZEN_CRITERIA.md (bcdb19e9e7).

OS1's core law fixes the cold dark energy's self-coupling: n = 2 q_f - 1 and s v = K sigma^(1-n),
K = 9 sigma_ref^(1+n) / (4 pi G t Sigma_a0^2).  Grades s(v) against merger bounds and checks dwarf-scale collapse.
MUTATE=1: n -> -n (cross-section rising with velocity).
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MUTATE = os.environ.get("MUTATE") == "1"; TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

G, YR = 6.674e-11, 3.156e7
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
SREF = 70.50e3; T_AGE = 13.8e9 * YR; VFAC = 4 / math.sqrt(math.pi)
CGS = 10.0  # 1 m^2/kg = 10 cm^2/g
OS1 = json.load(open(os.path.join(REB, "OS1_core_law_out_of_sample", "os1_out_of_sample_results.json")))
QF = {f: OS1["footings"][f]["q_f"] for f in A0}
VS = (10, 50, 200, 1000, 1900, 3000, 4700)
B1, B2, B3, W, C1, C2, C3 = 1.25, 0.47, 0.708, 2.0, 0.35, 0.13, 1.0
C_COLL = 0.75
DW1_KN = {"canonical": {5: 1158, 1000: 653}, "alt": {5: 2048, 1000: 539}}

P(f"kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed{'; MUTATE n -> -n' if MUTATE else ''}")
RES = dict(frozen="bcdb19e9e7", mutate=MUTATE, footings={}, checks={})
ok_all = True
for f in A0:
    a0, q = A0[f], QF[f]; n0 = 2 * q - 1; n = -n0 if MUTATE else n0
    sa = a0 / (2 * math.pi * G)
    K = 9 * SREF ** (1 + n) / (4 * math.pi * G * T_AGE * sa ** 2)
    def s_of_v(v_kms):  # m^2/kg
        sig = v_kms * 1e3 / VFAC
        return K * sig ** (1 - n) / (v_kms * 1e3)
    s = {v: s_of_v(v) * CGS for v in VS}
    P(f"[{f}] q_f {q:.3f} -> n {n:+.3f}; Sigma_a0 {sa:.4f} kg/m^2; s(v_ref = {VFAC*SREF/1e3:.1f} km/s) "
      f"{s_of_v(VFAC*SREF/1e3)*CGS:.4f} cm^2/g")
    P(f"[{f}] s(v) cm^2/g at " + ", ".join(f"{v}: {s[v]:.4g}" for v in VS))

    # checks (computed on the unmutated n as frozen; MUTATE rebuilds them at its own n where meaningful)
    k0 = abs(round(n0, 3) - {"canonical": 0.784, "alt": 0.496}[f]) < 1e-9
    def kn(sig):
        rho0 = 4 * math.pi * G * sa ** 2 * (sig / SREF) ** (2 * q) / (9 * sig ** 2)  # Sigma(sigma) = Sigma_a0 (sigma/sref)^q
        sv = K * sig ** (1 - n); s_ = sv / (VFAC * sig)
        return (1 / (rho0 * s_)) / (sig / math.sqrt(4 * math.pi * G * rho0)), rho0 * sv * T_AGE
    kn_ref_closed = 4 / (3 * math.sqrt(math.pi)) * 2 * a0 * T_AGE / SREF
    knr, gt = kn(SREF)
    k1 = abs(knr / kn_ref_closed - 1) < 0.01
    if not MUTATE:
        k1 = k1 and all(abs(kn(sg * 1e3)[0] / DW1_KN[f][sg] - 1) < 0.01 for sg in DW1_KN[f])
    k2 = abs(gt - 1) < 1e-9
    P(f"[{f}] checks K0 n {'ok' if k0 else 'FAIL'}; K1 Kn_ref {knr:.1f} vs closed {kn_ref_closed:.1f}"
      + ("" if MUTATE else f", Kn(5/1000) {kn(5e3)[0]:.0f}/{kn(1e6)[0]:.0f} vs DW1 {DW1_KN[f][5]}/{DW1_KN[f][1000]}")
      + f" {'ok' if k1 else 'FAIL'}; K2 rho0 s v t {gt:.12f} {'ok' if k2 else 'FAIL'}")
    ok_all &= k0 and k1 and k2

    # merger class
    passes = s[3000] <= B1 and s[1000] <= B2 and s[3000] <= B3
    excl = s[3000] > B1 or s[1000] > W
    mcls = "PASSES BOUNDS" if passes else ("EXCLUDED" if excl else "TENSION")
    c1 = "C1 PASS" if s[1900] <= C1 else "C1 FAIL"
    P(f"[{f}] B1 Bullet s(3000) {s[3000]:.4f} vs 1.25 (x{B1/s[3000]:.1f} margin; s(4700) {s[4700]:.4f}); "
      f"B2 Harvey s(1000) {s[1000]:.4f} vs 0.47 (x{B2/s[1000]:.1f}); B3 CFG725 s(3000) vs 0.708 (x{B3/s[3000]:.1f})")
    P(f"[{f}] C1 Sagunski s(1900) {s[1900]:.4f} vs 0.35 (x{C1/s[1900]:.1f}) -> {c1}; reported only: C2 Andrade 0.13 "
      f"(x{C2/s[1900]:.1f}), C3 Peter 1 (x{C3/s[1900]:.0f}); C4 Kaplinghat fit ~0.1 @1500, ~2 @50 vs ours "
      f"{s_of_v(1500)*CGS:.3f} / {s[50]:.3f}")
    P(f"[{f}] MERGER CLASS: {mcls} ({c1})")

    # dwarfs: collapse closed form t_c/t = (150/C) v/(3 sigma), independent of sigma
    tct = {}
    for sg in (5, 10, 20, 70.5, 1000):
        sig = sg * 1e3
        rho0 = 4 * math.pi * G * sa ** 2 * (sig / SREF) ** (2 * q) / (9 * sig ** 2)
        r0 = sa * (sig / SREF) ** q / rho0
        s_ = K * sig ** (1 - n) / (VFAC * sig)
        tc = 150 / C_COLL / (s_ * rho0 * r0 * math.sqrt(4 * math.pi * G * rho0))
        tct[sg] = tc / T_AGE
    closed = 150 / C_COLL * VFAC / 3
    dcls = ("COLLAPSE RISK" if min(tct.values()) <= 1 else ("EXTREME" if s[10] > 100 else "SANE"))
    P(f"[{f}] dwarfs: s(10) {s[10]:.3f}, s(50) {s[50]:.3f} cm^2/g; t_c/t at sigma 5/10/20/70.5/1000 km/s: "
      + " / ".join(f"{v:.1f}" for v in tct.values()) + f" (closed form {closed:.1f}) -> {dcls}")
    RES["footings"][f] = dict(q_f=q, n=n, K_SI=K, s_cm2g={str(v): s[v] for v in VS}, merger_class=mcls, C1=c1,
                              dwarf_class=dcls, tc_over_t=tct, Kn_ref=knr)

classes = {RES["footings"][f]["merger_class"] for f in A0}
verdict = classes.pop() if len(classes) == 1 else "UNDECIDED"
dw = {RES["footings"][f]["dwarf_class"] for f in A0}
RES["verdict"] = dict(merger=verdict, dwarf=dw.pop() if len(dw) == 1 else "UNDECIDED")
RES["checks"]["all_pass"] = ok_all
P(f"VERDICT: merger {RES['verdict']['merger']}; dwarfs {RES['verdict']['dwarf']}; checks {'all pass' if ok_all else 'FAILED'}")
if MUTATE:
    ins = verdict == "PASSES BOUNDS"
    P(f"MUTATE: {'INSENSITIVE TO n (still PASSES BOUNDS)' if ins else 'class moved -> grade driven by the derived exponent'}")
    RES["mutate_reading"] = "INSENSITIVE TO n" if ins else "class moved"

json.dump(RES, open(os.path.join(HERE, f"bu1_cross_section_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"bu1_cross_section{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (ok_all and not MUTATE) else 1)
