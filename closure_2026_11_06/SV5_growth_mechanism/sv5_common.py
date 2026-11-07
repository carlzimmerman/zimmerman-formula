"""SV5 shared loaders (read-only reuse, executed from source exactly as QX7 iter_4 and QX10 iter_2 load them).
kappa = 1/2 FITTED; not theory closed."""
import os, sys, math, io, contextlib
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
CL = os.path.join(REPO, "closure_2026_11_06")
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}

def load_growth():
    """QX3 iter3 (up to '# K: beta = 0') + QX7 iter_3's generalised solver g2gen(kJ)."""
    D3 = os.path.join(CL, "QX3_cmb_growth", "iter3_barotropic_family")
    s3 = open(os.path.join(D3, "iter3.py")).read(); c3 = s3.index("# K: beta = 0")
    cwd = os.getcwd(); os.chdir(D3); os.environ.pop("QX3_MUTATE", None)
    argv0, sys.argv = sys.argv, [os.path.join(D3, "iter3.py")]
    N3 = {"__file__": os.path.join(D3, "iter3.py"), "__name__": "iter3_reused"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(s3[:c3], os.path.join(D3, "iter3.py"), "exec"), N3)
    os.chdir(cwd); sys.argv = argv0
    S3 = open(os.path.join(CL, "QX7_unified_cold_switch", "iter_3_de_fraction_switch", "qx7_iter3.py")).read()
    blk = S3[S3.index("# ---- generalised G2' solver"):S3.index("d_iter3 = g2(")]
    MC = N3["M"]; OL0 = MC.Omega_Lambda(); H0c_ = MC.Hubble(0.0)
    def ode(z): return OL0 / (MC.Hubble(z) / H0c_) ** 2
    LOC = dict(np=np, N3=N3, I2=N3["I2"], MC=MC, H0=N3["H0"], ode=ode); exec(blk, LOC)
    N3["g2gen"] = LOC["g2gen"]; N3["solve_gen"] = LOC["solve_gen"]
    return N3

def load_qx10():
    Q = os.path.join(CL, "QX10_window_hardening", "iter_2_capture_dynamics", "qx10_i2.py")
    argv0, sys.argv = sys.argv, [Q]
    NS = {"__file__": Q, "__name__": "qx10_reused"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(open(Q).read(), Q, "exec"), NS)
    sys.argv = argv0
    return NS

def sigma_A_rel(N3):
    """T0.4: PR4 amplitude error of the X0 fit, 1/(A sqrt(b))."""
    I2 = N3["I2"]; LIB = I2.LIB; D = I2.D; X = N3["X0"]
    u = LIB.wsum(D["W"], X) + LIB.wsum(D["M"], X)
    a = LIB.qform(u, D["Cinv"], D["d"] + D["F"]); b = LIB.qform(u, D["Cinv"]); A = a / b
    return float(1.0 / (A * math.sqrt(b))), float(A)
