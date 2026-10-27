#!/usr/bin/env python3
"""X54_cold_de_exchange: build the exchange CLASS (FROZEN_CRITERIA section 1).

Copies the pristine CLASS v3.3.4 tree already on disk (no download) to a build directory OUTSIDE the repository, applies
edits (background.c: analytic exchange background for rho_cdm and rho_lambda; perturbations.c: dilution term on
delta_cdm in synchronous gauge + Newtonian-gauge refusal), writes `x54_exchange.patch` (diff vs pristine) into this lane,
and builds with CLASS's documented C build: `make -j1 class`.

Runtime environment (read once per run):
  X54_XI     exchange strength xi (unset or empty = exchange off = binary identical to vanilla)
  X54_MODEL  "C" (Q = xi H rho_c, default) or "D" (Q = xi H rho_DE)
  X54_BUG    "1" = MUTATE: background exchange sign flipped AND the perturbation dilution term dropped
Sign convention: xi > 0 = energy flows dark energy -> cold dark energy.

Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I x54_make_patch.py
Build dir: $X54_BUILD (default: <system temp>/x54_class_build).
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
PRIS = os.path.join(EXT, "class_public_v3.3.4_2026_10_22", "class_public-3.3.4")
BUILD = os.environ.get("X54_BUILD", os.path.join(tempfile.gettempdir(), "x54_class_build"))
TREE = os.path.join(BUILD, "class_x54")

BG_TOP = r'''#include "background.h"

/* ---- X54 exchange (rebuild_2026_10_22/X54_cold_de_exchange) ----
   d rho_c/dt + 3 H rho_c = +Q, d rho_DE/dt = -Q, xi > 0 = DE -> cold.
   Model C: Q = xi H rho_c  -> rho_c = rho_c0 a^-(3-xi), rho_DE = rho_L0 + xi rho_c0/(3-xi) (a^-(3-xi) - 1).
   Model D: Q = xi H rho_DE -> rho_DE = rho_L0 a^-xi, rho_c = (rho_c0 - B) a^-3 + B a^-xi, B = xi rho_L0/(3-xi).
   Both vanish identically at a = 1 relative to vanilla, so CLASS's budget closure is unchanged.
   X54_BUG=1 (MUTATE): the background uses -xi. */
static int x54_init_done = 0, x54_on_flag = 0, x54_model = 0, x54_bug = 0;
static double x54_xi = 0.;
static void x54_setup(void) {
  const char *s;
  if (x54_init_done) return;
  x54_init_done = 1;
  s = getenv("X54_XI");
  if (s == NULL || s[0] == '\0') { x54_on_flag = 0; return; }
  x54_on_flag = 1;
  x54_xi = atof(s);
  s = getenv("X54_MODEL");
  x54_model = (s != NULL && (s[0] == 'D' || s[0] == 'd')) ? 1 : 0;
  s = getenv("X54_BUG");
  x54_bug = (s != NULL && s[0] == '1') ? 1 : 0;
}
int x54_is_on(void) { x54_setup(); return x54_on_flag; }
int x54_bug_on(void) { x54_setup(); return x54_bug; }
/* background factors (written so that xi = 0 is bit-identical to vanilla):
   rho_c = [Omega0_cdm H0^2 / a^3] * fc,  rho_DE = [Omega0_lambda H0^2] * fl,  dfl = d fl / d ln a */
void x54_bg(double a, double oc, double ol, double *fc, double *fl, double *dfl) {
  double xi, b;
  x54_setup();
  if (!x54_on_flag) { *fc = 1.; *fl = 1.; *dfl = 0.; return; }
  xi = x54_bug ? -x54_xi : x54_xi;
  if (x54_model == 0) {
    *fc = pow(a, xi);
    *fl = 1. + xi*oc/((3.-xi)*ol) * (pow(a, -(3.-xi)) - 1.);
    *dfl = -xi * (oc/ol) * pow(a, -(3.-xi));
  } else {
    b = xi*ol/((3.-xi)*oc);
    /* b > 1 (no physical solution: today's cold dark energy smaller than its exchange-fed part) occurs only at
       shooting trial points far from any fit (h > ~1.4); there the a^-3 term is dropped, rho_c = B a^-xi */
    *fc = (b <= 1.) ? (1. - b + b * pow(a, 3.-xi)) : (b * pow(a, 3.-xi));
    *fl = pow(a, -xi);
    *dfl = -xi * pow(a, -xi);
  }
}
/* perturbations: dilution rate r = a Q / (rho_c aH), so delta_c' -= r aH delta_c; 0 under the bug */
double x54_rate(double rho_c, double rho_l) {
  x54_setup();
  if (!x54_on_flag || x54_bug) return 0.;
  if (x54_model == 0) return x54_xi;
  return x54_xi * rho_l / rho_c;
}
/* ---- end X54 ---- */
'''

BG_CDM_OLD = '''    pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3);
    rho_tot += pvecback[pba->index_bg_rho_cdm];
'''
BG_CDM_NEW = '''    {
      double x54_fc, x54_fl, x54_dfl;
      x54_bg(a, pba->Omega0_cdm, pba->Omega0_lambda, &x54_fc, &x54_fl, &x54_dfl);
      pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3) * x54_fc;
    }
    rho_tot += pvecback[pba->index_bg_rho_cdm];
'''
BG_L_OLD = '''    pvecback[pba->index_bg_rho_lambda] = pba->Omega0_lambda * pow(pba->H0,2);
    rho_tot += pvecback[pba->index_bg_rho_lambda];
    p_tot -= pvecback[pba->index_bg_rho_lambda];
'''
BG_L_NEW = '''    {
      double x54_fc, x54_fl, x54_dfl;
      x54_bg(a, pba->Omega0_cdm, pba->Omega0_lambda, &x54_fc, &x54_fl, &x54_dfl);
      pvecback[pba->index_bg_rho_lambda] = pba->Omega0_lambda * pow(pba->H0,2) * x54_fl;
      dp_dloga += -pba->Omega0_lambda * pow(pba->H0,2) * x54_dfl; /* p_DE = -rho_DE */
    }
    rho_tot += pvecback[pba->index_bg_rho_lambda];
    p_tot -= pvecback[pba->index_bg_rho_lambda];
'''
BG_INIT_OLD = '''  /** - assign values to all indices in vectors of background quantities */
  class_call(background_indices(pba),
             pba->error_message,
             pba->error_message);
'''
BG_INIT_NEW = '''  if (x54_is_on() && pba->background_verbose > 0) printf("X54 exchange ACTIVE%s\\n", x54_bug_on() ? " (MUTATE BUG)" : "");

  /** - assign values to all indices in vectors of background quantities */
  class_call(background_indices(pba),
             pba->error_message,
             pba->error_message);
  class_test(x54_is_on() && ((pba->has_cdm == _FALSE_) || (pba->has_lambda == _FALSE_) || (pba->has_fld == _TRUE_)),
             pba->error_message, "X54 exchange needs cdm + Lambda and no fld");
'''

PT_TOP_OLD = '#include "parallel.h"\n'
PT_TOP_NEW = ('#include "parallel.h"\n/* X54 exchange; perturbations.c is compiled as C++ */\n'
              '#ifdef __cplusplus\nextern "C" {\n#endif\nint x54_is_on(void);\n'
              'double x54_rate(double rho_c, double rho_l);\n#ifdef __cplusplus\n}\n#endif\n')
PT_GAUGE_OLD = '''  class_test((ppt->gauge == synchronous) && (pba->has_cdm == _FALSE_),'''
PT_GAUGE_NEW = '''  class_test(x54_is_on() && (ppt->gauge != synchronous),
             ppt->error_message,
             "X54 exchange is implemented in synchronous gauge only");

  class_test((ppt->gauge == synchronous) && (pba->has_cdm == _FALSE_),'''
PT_CDM_OLD = '''        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */'''
PT_CDM_NEW = '''        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */
        if (x54_is_on()) { /* X54: Q along u_c, deltaQ = 0 on cold-comoving slices -> dilution */
          dy[pv->index_pt_delta_cdm] -= a_prime_over_a
            * x54_rate(pvecback[pba->index_bg_rho_cdm], pvecback[pba->index_bg_rho_lambda])
            * y[pv->index_pt_delta_cdm];
        }'''


def sub(path, old, new):
    s = open(path).read()
    assert s.count(old) == 1, f"anchor not unique in {path}: {old[:60]!r}"
    open(path, "w").write(s.replace(old, new))


def main():
    assert os.path.isdir(PRIS), PRIS
    shutil.rmtree(TREE, ignore_errors=True)
    os.makedirs(BUILD, exist_ok=True)
    shutil.copytree(PRIS, TREE, symlinks=True)
    bg = os.path.join(TREE, "source", "background.c")
    pt = os.path.join(TREE, "source", "perturbations.c")
    sub(bg, '#include "background.h"\n', BG_TOP)
    sub(bg, BG_CDM_OLD, BG_CDM_NEW)
    sub(bg, BG_L_OLD, BG_L_NEW)
    sub(bg, BG_INIT_OLD, BG_INIT_NEW)
    sub(pt, PT_TOP_OLD, PT_TOP_NEW)
    sub(pt, PT_GAUGE_OLD, PT_GAUGE_NEW)
    sub(pt, PT_CDM_OLD, PT_CDM_NEW)
    diff = ""
    for rel in ("source/background.c", "source/perturbations.c"):
        r = subprocess.run(["diff", "-u", "--label", "a/" + rel, "--label", "b/" + rel,
                            os.path.join(PRIS, rel), os.path.join(TREE, rel)], capture_output=True, text=True)
        diff += r.stdout
    open(os.path.join(HERE, "x54_exchange.patch"), "w").write(diff)
    env = dict(os.environ, OMP_NUM_THREADS="1")
    log = open(os.path.join(BUILD, "build_class_x54.log"), "w")
    r = subprocess.run(["nice", "-n", "15", "make", "-j1", "class"], cwd=TREE, stdout=log, stderr=subprocess.STDOUT, env=env)
    assert r.returncode == 0, "build failed; see build_class_x54.log in the build dir"
    h = hashlib.sha256(open(os.path.join(TREE, "class"), "rb").read()).hexdigest()
    hp = hashlib.sha256(diff.encode()).hexdigest()
    print(f"built class_x54; binary sha256 {h}; patch sha256 {hp}; patch lines {diff.count(chr(10))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
