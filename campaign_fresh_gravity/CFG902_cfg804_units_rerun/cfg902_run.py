"""CFG902 -- CFG804 rerun with the f_ret(M_ta) mass convention CFG416 declared (Msun/h).
Criteria: FROZEN_CRITERIA.md (b35efa722).
Usage: python3 cfg902_run.py MODE FOOT    MODE in {orig, declared, mutate}; FOOT in {canonical, alt}.
CFG804's committed cfg804.py is read as text (blob-hash checked) and executed with the frozen replacements R1-R3 only:
  R1  N_of: log M_ta[Msun/h] = log M_b - log10(f_ret f_b) + SHIFT_DEX   (SHIFT_DEX = log10 h, h = 0.674 from CFG416)
  R2  CFG804's internal K1 target 12.30 -> 12.30 + SHIFT_DEX (same convention)
  R3  outputs redirected into this lane (nothing is written into CFG804's directory)
Watchdog: exits if the process exceeds 1 GB RSS or 15 min.  kappa = 1/2 FITTED; not theory closed.
"""
import hashlib, json, math, os, resource, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "CFG804_catchment_supply_derived", "cfg804.py"))
BLOB = "b1749cb85e224d5a78927a061aa2832126b5b1ec"          # cfg804.py as committed in 67774ce37
H_DECL, H_PM = 0.674, 0.6736                                # CFG416 conversion h (cfg416_pm.py l.277); PM cosmology h (report only)
SHIFTS = {"orig": 0.0, "declared": math.log10(H_DECL), "mutate": 2 * math.log10(H_DECL), "declared_h6736": math.log10(H_PM)}
MODE, FOOT = sys.argv[1], sys.argv[2]
assert MODE in ("orig", "declared", "mutate") and FOOT in ("canonical", "alt")
T0 = time.time(); LIM_RSS, LIM_T = 1.0e9, 900.0

def rss():                                                  # macOS ru_maxrss is in bytes
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024)
def watchdog():
    while True:
        if rss() > LIM_RSS or time.time() - T0 > LIM_T:
            sys.stderr.write(f"CFG902 WATCHDOG: rss {rss() / 1e6:.0f} MB, t {time.time() - T0:.0f} s -> STOP\n"); os._exit(3)
        time.sleep(2)
threading.Thread(target=watchdog, daemon=True).start()

raw = open(SRC, "rb").read()
blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
assert blob == BLOB, f"cfg804.py blob {blob} != committed {BLOB}"
src = raw.decode()
REPL = [
    ("lMta = logMb - math.log10(f * FB); fn = fret_of(lMta)",
     "lMta = logMb - math.log10(f * FB) + SHIFT_DEX; fn = fret_of(lMta)"),                      # R1
    ("abs(lk - 12.30) < 0.01", "abs(lk - (12.30 + SHIFT_DEX)) < 0.01"),                          # R2
    ('os.path.join(HERE, f"cfg804_results{sfx}.json")', 'os.path.join(OUTDIR, f"cfg902_results_{MODE}{sfx}.json")'),  # R3
    ('os.path.join(HERE, f"cfg804{sfx}.out")', 'os.path.join(OUTDIR, f"cfg902_{MODE}{sfx}.out")'),                   # R3
]
for a, b in REPL:
    assert src.count(a) == 1, f"replacement target not unique/present: {a}"
    src = src.replace(a, b)

os.environ.pop("CFG804_MUTATE", None)
sys.argv = [SRC] + (["alt"] if FOOT == "alt" else [])
ns = dict(__name__="__main__", __file__=SRC, SHIFT_DEX=SHIFTS[MODE], OUTDIR=HERE, MODE=MODE)
rc = 0
try:
    exec(compile(src, "cfg804.py[CFG902 R1-R3]", "exec"), ns)
except SystemExit as e:
    rc = e.code
t_run = time.time() - T0

# extras (no new physics): the exec'd N_of evaluated under each convention at fixed masses
N_of, NGRID, edge_of, Gpc, a0 = ns["N_of"], ns["NGRID"], ns["edge_of"], ns["Gpc"], ns["a0"]
sfx = "_alt" if FOOT == "alt" else ""
own = json.load(open(os.path.join(HERE, f"cfg902_results_{MODE}{sfx}.json")))
rec = json.load(open(os.path.join(HERE, "..", "CFG804_catchment_supply_derived", f"cfg804_results{sfx}.json")))
MASSES = {"cfg804_primary": rec["primary"]["logMb"], "cfg804_all": rec["all"]["logMb"],
          "own_primary": own["primary"]["logMb"], "own_all": own["all"]["logMb"]}
def table(shift):
    ns["SHIFT_DEX"] = shift; out = {}
    for k, ms in MASSES.items():
        rows = []
        for m in ms:
            N, lM = N_of(m); Ns = float(NGRID[abs(NGRID - N).argmin()]); rM = math.sqrt(Gpc * 10 ** m / a0) / 1e3
            rows.append(dict(logMb=m, N=N, N_snap=Ns, logMta=lM, f_ret=1 / N, edge_rM=edge_of(N), edge_kpc=edge_of(N) * rM))
        out[k] = rows
    Nk, lk = N_of(10.5); out["K3_logMb_10.5"] = dict(N=Nk, logMta=lk)
    return out
EX = dict(lane="CFG902", mode=MODE, footing=FOOT, shift_dex=SHIFTS[MODE], blob=blob, rc=rc,
          tables={k: table(v) for k, v in SHIFTS.items()})
ns["SHIFT_DEX"] = SHIFTS[MODE]
EX.update(runtime_s=round(t_run, 1), maxrss_MB=round(rss() / 1e6, 1))
json.dump(EX, open(os.path.join(HERE, f"cfg902_extras_{MODE}{sfx}.json"), "w"), indent=1, default=float)
print(f"CFG902 run {MODE} {FOOT}: rc {rc}, {t_run:.0f} s, max RSS {rss() / 1e6:.0f} MB", flush=True)
sys.exit(0)
