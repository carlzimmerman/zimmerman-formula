#!/usr/bin/env python3
"""Q7_bs25_cosmology step P (FROZEN_CRITERIA section 5): the Blanchet-Skordis DBI K(Q) as aest_K_type 5 on Q6's
Khronon variant of C7's patched CLASS v3.3.4.

Usage:  python3 -I q7_make_patch.py PRISTINE_DIR TARGET_DIR [--mutate]
  PRISTINE_DIR = ../_external_data/class_public_v3.3.4_2026_10_22/class_public-3.3.4 (never modified)
  TARGET_DIR   = a new directory (must not exist).
Steps: copy the pristine tree; apply rebuild_2026_10_22/Q6_v3_class/khronon.patch with `patch -p1` (must apply cleanly);
add the DBI case ONLY inside background_aest_K() and perturbations_aest_rhs() (anchor edits, each matching once); write
the unified diff Q6-tree -> DBI-tree (source/include) to dbi.patch (dbi_MUTATE.patch with --mutate, where the
perturbation c_s^2 uses the wrong power K'' = 2 mu^2 / r^3).

DBI (BS24 Eq. 87 = BS25 Eq. 6): K = (2 mu^2/lambda_D)[1 - sqrt(1 - lambda_D (Q-1)^2)], lambda_D = aest_Z0 (C7's input,
unused by the Khronon types 0/3/4). Cancellation-free forms (q7_source.py S2-S4): Z = K'/(2 mu^2) = I0/(2 mu^2 a^3),
r = sqrt(1 + lambda_D Z^2): Qbar = 1 + Z/r, K = 2 mu^2 Z^2/(r(r+1)), K'' = 2 mu^2 r^3, c_ad^2 = Z/(r^2 (r+Z)).
Perturbations: Q6's fluid with rest-frame c_s^2 = Qbar K'/(Qbar^2 K'' - 2 j1 k^2/a^2) (= BS24 Eq. 71, q7_source S7).
"""
import difflib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
Q6PATCH = os.path.join(REPO, "rebuild_2026_10_22", "Q6_v3_class", "khronon.patch")
pristine, target = sys.argv[1], sys.argv[2]
MUT = "--mutate" in sys.argv
assert os.path.isdir(pristine) and not os.path.exists(target)
shutil.copytree(pristine, target)
r = subprocess.run(["patch", "-p1", "--forward", "--no-backup-if-mismatch", "-d", target, "-i", Q6PATCH],
                   capture_output=True, text=True)
print(r.stdout.strip())
assert r.returncode == 0 and "FAILED" not in r.stdout and "offset" not in r.stdout.lower() and "fuzz" not in r.stdout.lower(), \
    r.stdout + r.stderr


def snapshot():
    return {(sub, fn): open(os.path.join(target, sub, fn)).read()
            for sub in ("include", "source") for fn in sorted(os.listdir(os.path.join(target, sub)))}


Q6TREE = snapshot()


def edit_once(path, old, new):
    fp = os.path.join(target, path)
    s = open(fp).read()
    assert s.count(old) == 1, f"anchor x{s.count(old)} in {path}: {old[:80]!r}"
    open(fp, "w").write(s.replace(old, new))


# ------------------------------------------------------------------ 1. background_aest_K(): add case 5 before default
BG_OLD = """  default:
    class_stop(pba->error_message,"Khronon (Q6): aest_K_type = %d not coded (0 DUST, 3 LIT, 4 LOB)",pba->aest_K_type);
  }"""
BG_NEW = """  case 5: /* Q7_bs25_cosmology: BS DBI K = (2 mu^2/lambda_D)[1 - sqrt(1 - lambda_D (Q-1)^2)], lambda_D = aest_Z0;
             Z = K'/(2 mu^2), r = sqrt(1 + lambda_D Z^2): Qbar = 1 + Z/r, K = 2 mu^2 Z^2/(r(r+1)), c_ad^2 = Z/(r^2(r+Z)) */
    {
      double lamD = pba->aest_Z0;
      double Zd = kp/(2.*mu2);
      double rd;
      if (lamD < 0.)
        class_stop(pba->error_message,"Khronon DBI (Q7): lambda_D = aest_Z0 = %e must be >= 0",lamD);
      rd = sqrt(1. + lamD*Zd*Zd);
      *Q = 1. + Zd/rd;
      *Kz = 2.*mu2*Zd*Zd/(rd*(rd + 1.));
      *ca2 = Zd/(rd*rd*(rd + Zd));
    }
    break;
  default:
    class_stop(pba->error_message,"Khronon (Q6/Q7): aest_K_type = %d not coded (0 DUST, 3 LIT, 4 LOB, 5 DBI)",pba->aest_K_type);
  }"""
edit_once("source/background.c", BG_OLD, BG_NEW)

# ------------------------------------------------------------------ 2. perturbations_aest_rhs(): add case 5 before default
kpp = "2.*mu2/(rd*rd*rd)" if MUT else "2.*mu2*rd*rd*rd"
PT_OLD = """  default: /* DUST */
    cs2 = 0.;
  }
  Pi = cs2*"""
PT_NEW = """  case 5: /* Q7_bs25_cosmology: DBI, K'' = 2 mu^2 r^3, r = sqrt(1 + lambda_D Z^2), Z = K'/(2 mu^2); c_s^2 = BS24 Eq. 71 */
    {
      double Zd = Kp/(2.*mu2);
      double rd = sqrt(1. + pba->aest_Z0*Zd*Zd);
      double K2pp = """ + kpp + """;
      cs2 = Q*Kp/(Q*Q*K2pp - 2.*j1*k2/a/a);
    }
    break;
  default: /* DUST */
    cs2 = 0.;
  }
  Pi = cs2*"""
edit_once("source/perturbations.c", PT_OLD, PT_NEW)
print(f"DBI edits applied to {target}{' (MUTATE: K_pp = 2 mu^2 / r^3)' if MUT else ''}")

# ------------------------------------------------------------------ diff Q6 tree -> DBI tree
NEW = snapshot()
out = []
for key in sorted(NEW):
    if NEW[key] != Q6TREE[key]:
        sub, fn = key
        out.extend(difflib.unified_diff(Q6TREE[key].splitlines(keepends=True), NEW[key].splitlines(keepends=True),
                                        fromfile=f"a/{sub}/{fn}", tofile=f"b/{sub}/{fn}"))
pname = os.path.join(HERE, "dbi_MUTATE.patch" if MUT else "dbi.patch")
open(pname, "w").write("".join(out))
print(f"wrote {os.path.basename(pname)}: {sum(1 for l in out if l.startswith('+') and not l.startswith('+++'))} added, "
      f"{sum(1 for l in out if l.startswith('-') and not l.startswith('---'))} removed lines")
