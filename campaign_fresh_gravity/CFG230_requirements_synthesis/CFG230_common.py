"""CFG230 shared helpers. No absolute home path is printed: the repo root comes from ZF_REPO or by walking
up from this file; every printed path is rewritten to <repo>. MUTATE=<k> selects a control (main runs leave it unset)."""
import os, sys, json, re, subprocess, math, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    r = os.environ.get("ZF_REPO")
    if r and os.path.isdir(os.path.join(r, "campaign_fresh_gravity")):
        return os.path.abspath(r)
    d = HERE
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(d, ".git")):
            return d
        d = os.path.dirname(d)
    sys.exit("CFG230: set ZF_REPO to the repository root")


REPO = find_repo()


def clean(s):
    s = str(s).replace(REPO, "<repo>").replace(HERE, "<scratch>")
    return re.sub(r"/Us" + r"ers/[^\s/]+", "<home>", s)


def mode():
    return os.environ.get("MUTATE", "")


def git(*args):
    p = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout


def norm(s):
    for a, b in (("−", "-"), ("–", "-"), ("‑", "-"), ("×", "x"), ("≈", "~"), ("²", "^2"),
                 ("≥", ">="), ("≤", "<="), ("≠", "!="), (" ", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s)


_cache = {}


def read_norm(rel):
    if rel not in _cache:
        p = os.path.join(REPO, rel)
        _cache[rel] = norm(open(p, encoding="utf-8", errors="replace").read()) if os.path.isfile(p) else None
    return _cache[rel]


class Run:
    """Records checks. kinds: CITATION-AUDIT, CROSS-CHECK, NEW-DERIVATION, EXPECT (hand expectation; a miss is kept)."""

    def __init__(self, name):
        self.name = name
        self.lines = []
        self.checks = []
        self.res = {}

    def p(self, s=""):
        s = clean(s)
        self.lines.append(s)
        print(s)

    def check(self, kind, label, ok, detail=""):
        self.checks.append({"kind": kind, "label": label, "ok": bool(ok), "detail": clean(detail)})
        self.p(f"  [{'PASS' if ok else 'MISS'}] ({kind}) {label} {detail}")

    def write(self, suffix=""):
        base = os.path.join(HERE, f"{self.name}{suffix}")
        miss = [c for c in self.checks if not c["ok"]]
        self.p(f"SUMMARY {self.name}{suffix}: {len(self.checks)} checks, {len(miss)} MISS; repo=<repo>")
        open(base + ".out", "w").write("\n".join(self.lines) + "\n")
        json.dump({"checks": self.checks, "results": self.res, "misses": len(miss)}, open(base + "_results.json", "w"), indent=1, default=str)


def bite(run, changed, what):
    """MUTATE convention: exit 1 when the control bites (headline changed)."""
    run.p(f"CONTROL {'BITES' if changed else 'DOES NOT BITE'}: {what}")
    run.write(f"_MUTATE_{mode()}")
    sys.exit(1 if changed else 0)


# ---- constants used by several scripts (canonical footing: kappa = 1/2, H0 = 67.4, Omega_L = 0.6847)
G = 6.6743e-11
MSUN = 1.98847e30
CLIGHT = 299792458.0
KPC = 3.0856775814913673e19
MPC = KPC * 1e3
AU = 1.495978707e11
PC = KPC / 1e3
H0 = 67.4e3 / MPC
OMEGA_L = 0.6847
RHO_L = 3 * H0 ** 2 * OMEGA_L / (8 * math.pi * G)
A0 = 0.5 * CLIGHT * math.sqrt(G * RHO_L)


def rM(M_msun, a0=None):
    return math.sqrt(G * M_msun * MSUN / (a0 or A0))
