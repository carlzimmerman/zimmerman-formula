#!/usr/bin/env python3
"""CFG265_lean_read.py: frozen-criteria P1. Reads the ChainCert Lean files AS TEXT at the pinned commit (no build, nothing
written into the repo), prints the exact statements the PAPER39 draft paraphrases with their hypotheses, counts theorem
declarations per module, and compares the counts with the draft (331; 47 -> 219; 62 -> 281; 50 -> 331) and with
verify_chain.out / verify_chain_MUTATE.out / Axioms.out. Exit 0 if it completed (a mismatch prints MISMATCH)."""
import re, sys
from CFG265_common import *

C = "fable_independent_2026/lean_2026/ChainCert/"
NAMES = {
    'Ownership': ['ownership_distinguishes', 'ownership_not_field_local', 'noEFE_continuousLinear', 'deep_not_efeFreeRay', 'law_not_efeFreeRay', 'vecLaw_not_efeFree'],
    'Theory': ['ownership_nonlocal'],
    'Dimension': ['no_sqrtM_length_GMc', 'sqrtM_length_iff', 'acc_from_GcX_iff', 'sqrtM_length_iff_acc', 'hbar_admissible', 'not_only_accelerations'],
    'Action': ['gauss_form', 'gauss_iff_kernel', 'spherical_kernel', 'muP2Aqual', 'nuP2_of_action'],
    'CalibrationWall': ['T1_deep_iff', 'T2a_P2_injective', 'T2a_one_point_fails', 'T4_design_bound', 'T4_sigma_floor'],
    'Footing': ['footing_kappaM_iff'],
}
STEP = {'step 1 (Ownership, Theory, A0Numeric, DoorEleven)': (['Ownership', 'Theory', 'A0Numeric', 'DoorEleven'], 47, 219),
        'step 2 (Action, Dimension, FluidLink)': (['Action', 'Dimension', 'FluidLink'], 62, 281),
        'step 3 (CalibrationWall)': (['CalibrationWall'], 50, 331)}


def decl(src, name):
    m = re.search(r'^(theorem|lemma|structure|def|noncomputable def)\s+' + re.escape(name) + r'\b(.*?)(:=|\bwhere\b)', src, re.S | re.M)
    if not m:
        return None
    s = (m.group(1) + ' ' + name + m.group(2)).strip()
    return re.sub(r'\s+', ' ', s)


def main():
    files = [f for f in ls_pin(C) if f.endswith('.lean')]
    counts = {}
    for f in sorted(files):
        t, _ = pin_text(f)
        counts[f.split('/')[-1][:-5]] = len(re.findall(r'^\s*(theorem|lemma)\s', t, re.M))
    print('repo <repo>; ChainCert read at', PIN, '(text only; no lake build, no verify_chain.sh run)')
    print('theorem/lemma declarations per module:', counts)
    print('sum over all modules:', sum(counts.values()), '(the verifier counts the theorems it #print-axioms; see Axioms.out)')
    for k, (mods, n, cum) in STEP.items():
        got = sum(counts.get(m, 0) for m in mods)
        print('  %-50s modules sum %3d  (draft %d, cumulative %d)  %s' % (k, got, n, cum, 'OK' if got == n else 'MISMATCH'))
    v, _ = pin_text(C + 'verify_chain.out'); vm, _ = pin_text(C + 'verify_chain_MUTATE.out'); ax, _ = pin_text(C + 'Axioms.out')
    print('verify_chain.out:', [l for l in v.split('\n') if 'theorems checked' in l or 'VERIFY' in l])
    print('verify_chain_MUTATE.out:', [l for l in vm.split('\n') if 'theorems checked' in l or 'VERIFY' in l])
    nax = len(re.findall(r'depends on axioms', ax))
    nonstd = len([l for l in ax.split('\n') if 'depends on axioms' in l and l.strip().split('[')[-1].strip(']').replace(' ', '') != 'propext,Classical.choice,Quot.sound'])
    print('Axioms.out: %d "depends on axioms" lines; lines with an axiom list other than [propext, Classical.choice, Quot.sound]: %d' % (nax, nonstd))
    print()
    for mod, names in NAMES.items():
        t, _ = pin_text(C + mod + '.lean')
        for n in names:
            d = decl(t, n)
            print('[%s] %s' % (mod, d if d else n + ': NOT FOUND'))
            print()
    # the README's own statements for the two items most likely to be read beyond their premises
    r, _ = pin_text(C + 'README.md')
    for key in ('ownership is non-local', 'why an acceleration scale must exist', 'action → kernel', 'spherical Gauss step'):
        for ln in r.split('\n'):
            if ln.startswith('| ' + key):
                print('README row:', ln[:700])
                print()
    sys.exit(0)


if __name__ == '__main__':
    main()
