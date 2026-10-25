#!/usr/bin/env python3
"""X34_recombination_release: build the R1 turn-on CLASS (FROZEN_CRITERIA §1, reading R1).

Copies the pristine CLASS v3.3.4 tree already on disk (no download) to a build directory OUTSIDE the repository,
applies three edits (background.c: S(a) on rho_cdm + vacuum-like reservoir; perturbations.c: dilution term on delta_cdm
in synchronous gauge + Newtonian-gauge refusal), writes `x34_turnon.patch` (diff vs pristine) into this lane, and builds
with CLASS's documented C build: `make -j1 class`.

The turn-on is read from the environment at run time: X34_ZON (z_on; unset = turn-on disabled, binary == vanilla) and
X34_WIDTH (tanh width in ln a; default 0.05).

Run: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I x34_make_patch.py
Build dir: $X34_BUILD (default: <system temp>/x34_class_build).
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
BUILD = os.environ.get("X34_BUILD", os.path.join(tempfile.gettempdir(), "x34_class_build"))
TREE = os.path.join(BUILD, "class_x34")

BG_TOP = r'''#include "background.h"

/* ---- X34 turn-on (rebuild_2026_10_22/X34_recombination_release, reading R1) ----
   rho_cdm(a) = rho_c0 a^-3 S(a), S = 1/(1+exp(-2u)), u = (ln a - ln a_on)/w.
   Reservoir (w_res = -1): rho_res(a) = rho_c0 * I(ln a), I(x) = int_x^inf e^{-3x'} S'(x') dx'. Energy conserved:
   d(rho_c + rho_res)/dln a = -3 rho_c. Read once from X34_ZON / X34_WIDTH (unset = off = vanilla). */
#define X34_NT 40001
static int x34_init_done = 0, x34_on_flag = 0;
static double x34_xon = 0., x34_w = 0.05, x34_xmin = 0., x34_xmax = 0., x34_dx = 1., x34_Itot = 0.;
static double x34_I[X34_NT];
static double x34_Sfun(double x) { return 1./(1.+exp(-2.*(x-x34_xon)/x34_w)); }
static double x34_Spfun(double x) { double s = x34_Sfun(x); return 2./x34_w*s*(1.-s); }
static void x34_setup(void) {
  const char *z, *w; int i;
  if (x34_init_done) return;
  x34_init_done = 1;
  z = getenv("X34_ZON");
  if (z == NULL || z[0] == '\0') { x34_on_flag = 0; return; }
  x34_on_flag = 1;
  x34_xon = -log(1.+atof(z));
  w = getenv("X34_WIDTH");
  if (w != NULL && w[0] != '\0') x34_w = atof(w);
  x34_xmin = x34_xon - 40.*x34_w; x34_xmax = x34_xon + 40.*x34_w;
  x34_dx = (x34_xmax - x34_xmin)/(X34_NT - 1);
  x34_I[X34_NT-1] = 0.;
  for (i = X34_NT-2; i >= 0; i--) {
    double xa = x34_xmin + i*x34_dx, xb = xa + x34_dx;
    x34_I[i] = x34_I[i+1] + 0.5*(exp(-3.*xa)*x34_Spfun(xa) + exp(-3.*xb)*x34_Spfun(xb))*x34_dx;
  }
  x34_Itot = x34_I[0];
}
int x34_is_on(void) { x34_setup(); return x34_on_flag; }
/* returns S; sets dlnS/dlna, rho_res/rho_c0 (H0^2 Omega0_cdm units), d(rho_res/rho_c0)/dlna */
double x34_S(double a, double *dlnS, double *res, double *dres) {
  double x, s, f; int i;
  x34_setup();
  if (!x34_on_flag) { *dlnS = 0.; *res = 0.; *dres = 0.; return 1.; }
  x = log(a);
  s = x34_Sfun(x);
  *dlnS = 2./x34_w/(1.+exp(2.*(x-x34_xon)/x34_w));
  *dres = -exp(-3.*x)*x34_Spfun(x);
  if (x <= x34_xmin) *res = x34_Itot;
  else if (x >= x34_xmax) *res = 0.;
  else { f = (x - x34_xmin)/x34_dx; i = (int)f; if (i > X34_NT-2) i = X34_NT-2; f -= i;
         *res = (1.-f)*x34_I[i] + f*x34_I[i+1]; }
  return s;
}
/* ---- end X34 ---- */
'''

BG_OLD = '''    pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3);
    rho_tot += pvecback[pba->index_bg_rho_cdm];
    p_tot += 0.;
    rho_m += pvecback[pba->index_bg_rho_cdm];
'''
BG_NEW = '''    {
      double x34_dl, x34_r, x34_dr, x34_s;
      x34_s = x34_S(a, &x34_dl, &x34_r, &x34_dr);
      pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3) * x34_s;
      rho_tot += pvecback[pba->index_bg_rho_cdm];
      p_tot += 0.;
      rho_m += pvecback[pba->index_bg_rho_cdm];
      if (x34_is_on()) { /* X34 reservoir, w = -1 */
        rho_tot += pba->Omega0_cdm * pow(pba->H0,2) * x34_r;
        p_tot -= pba->Omega0_cdm * pow(pba->H0,2) * x34_r;
        dp_dloga += -pba->Omega0_cdm * pow(pba->H0,2) * x34_dr;
      }
    }
'''
BG_INIT_OLD = '''  /** - assign values to all indices in vectors of background quantities */
  class_call(background_indices(pba),'''
BG_INIT_NEW = '''  if (x34_is_on() && pba->background_verbose > 0) printf("X34 turn-on ACTIVE (R1)\\n");

  /** - assign values to all indices in vectors of background quantities */
  class_call(background_indices(pba),'''

PT_TOP_OLD = '#include "parallel.h"\n'
PT_TOP_NEW = ('#include "parallel.h"\n/* X34 (R1 turn-on); perturbations.c is compiled as C++ */\n'
              '#ifdef __cplusplus\nextern "C" {\n#endif\nint x34_is_on(void);\n'
              'double x34_S(double a, double *dlnS, double *res, double *dres);\n#ifdef __cplusplus\n}\n#endif\n')
PT_GAUGE_OLD = '''  class_test((ppt->gauge == synchronous) && (pba->has_cdm == _FALSE_),'''
PT_GAUGE_NEW = '''  class_test(x34_is_on() && (ppt->gauge != synchronous),
             ppt->error_message,
             "X34 turn-on (R1) is implemented in synchronous gauge only");

  class_test((ppt->gauge == synchronous) && (pba->has_cdm == _FALSE_),'''
PT_CDM_OLD = '''        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */'''
PT_CDM_NEW = '''        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */
        if (x34_is_on()) { /* X34: released matter born homogeneous on synchronous slices (deltaQ = 0) */
          double x34_dl, x34_r, x34_dr;
          x34_S(pvecback[pba->index_bg_a], &x34_dl, &x34_r, &x34_dr);
          dy[pv->index_pt_delta_cdm] -= a_prime_over_a * x34_dl * y[pv->index_pt_delta_cdm];
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
    sub(bg, BG_OLD, BG_NEW)
    sub(bg, BG_INIT_OLD, BG_INIT_NEW)
    sub(pt, PT_TOP_OLD, PT_TOP_NEW)
    sub(pt, PT_GAUGE_OLD, PT_GAUGE_NEW)
    sub(pt, PT_CDM_OLD, PT_CDM_NEW)
    diff = ""
    for rel in ("source/background.c", "source/perturbations.c"):
        r = subprocess.run(["diff", "-u", "--label", "a/" + rel, "--label", "b/" + rel,
                            os.path.join(PRIS, rel), os.path.join(TREE, rel)], capture_output=True, text=True)
        diff += r.stdout
    open(os.path.join(HERE, "x34_turnon.patch"), "w").write(diff)
    env = dict(os.environ, OMP_NUM_THREADS="1")
    log = open(os.path.join(BUILD, "build_class_x34.log"), "w")
    r = subprocess.run(["nice", "-n", "15", "make", "-j1", "class"], cwd=TREE, stdout=log, stderr=subprocess.STDOUT, env=env)
    assert r.returncode == 0, "build failed; see build_class_x34.log in the build dir"
    h = hashlib.sha256(open(os.path.join(TREE, "class"), "rb").read()).hexdigest()
    hp = hashlib.sha256(diff.encode()).hexdigest()
    print(f"built class_x34; binary sha256 {h}; patch sha256 {hp}; patch lines {diff.count(chr(10))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
