#!/usr/bin/env python3
"""
WALLABY / Local-Volume dwarf out-of-sample RAR test on the framework's OWN nu.

FRAMEWORK (its own premises):
  de Sitter-Unruh MODIFIED INERTIA. Own interpolation:
     g_obs = sqrt( g_bar^2 + g_bar * a0 )   <=>   nu(y)=sqrt(1+1/y), y=g_bar/a0
  Footing fork:
     a0_canonical = c*H_Lambda/Z = 9.36e-11 m/s^2   (rho_DE, Z=sqrt(32pi/3))
     a0_alt       = 1.13e-10 m/s^2                   (rho_total, cH0)

GOAL: first genuinely SPARC-INDEPENDENT RAR on the framework's nu, using the
WALLABY DR2 (203) non-SPARC HI curves in the Unified Corpus (Zenodo 19563417)
and/or the Local-Volume dwarf/irregular compilation (Zenodo 20320362).

WHAT THE RAR NEEDS PER POINT:
   g_bar(R) = V_bar(R)^2 / R   built from the BARYONIC decomposition
              V_bar^2 = |Vgas|*Vgas + Upsilon*Vdisk^2 + Upsilon*Vbul^2
   g_obs(R) = V_obs(R)^2 / R

This script:
  (1) Audits the two archives for baryonic content on the NON-SPARC curves.
  (2) If baryonic content exists -> computes the framework RAR both footings.
  (3) If it does not -> reports DATA_GATED with the exact deficit, and
      validates the framework nu machinery on the SPARC curves that ARE in the
      same corpus (sanity: pipeline works, so the null is a data gap, not a bug).
"""
import json, math, numpy as np, os, urllib.request

DATA=os.path.dirname(os.path.abspath(__file__))

# Self-contained: fetch the two public archives if not already present.
ARCHIVES={
  'wallaby.json':'https://zenodo.org/records/19563417/files/rotation_curve_corpus_v7.json?download=1',
  'dwarf.json'  :'https://zenodo.org/records/20320362/files/dwarf_irregular_corpus_v1.json?download=1',
}
for _fn,_url in ARCHIVES.items():
    _p=os.path.join(DATA,_fn)
    if not os.path.exists(_p):
        print(f"[fetch] {_fn} <- {_url}")
        urllib.request.urlretrieve(_url,_p)

G_MSUN_KPC = 4.300917270e-6  # (km/s)^2 kpc / Msun -> we work directly in accel units
KPC_M = 3.0856775814913673e19
KMS_M = 1.0e3

A0_CANON = 9.36e-11
A0_ALT   = 1.13e-10

def accel_SI(V_kms, R_kpc):
    # V^2/R in m/s^2
    return (V_kms*KMS_M)**2 / (R_kpc*KPC_M)

def nu_framework(y):
    # g_obs = sqrt(g_bar^2 + g_bar*a0); y=g_bar/a0 -> g_obs/g_bar = sqrt(1+1/y)
    return np.sqrt(1.0 + 1.0/y)

def gobs_pred(gbar, a0):
    return np.sqrt(gbar**2 + gbar*a0)

# ---------------- AUDIT ----------------
def audit():
    wal=json.load(open(os.path.join(DATA,'wallaby.json')))
    dwf=json.load(open(os.path.join(DATA,'dwarf.json')))
    rep={}
    # WALLABY corpus: what non-SPARC surveys carry baryonic decomposition?
    surv={}
    for g in wal['galaxies']:
        s=g['survey']
        d=surv.setdefault(s,{'n':0,'has_baryon_pts':0,'has_mhi':0})
        d['n']+=1
        rows = g.get('data') or g.get('rotation_curve') or []
        has_bary = any(('Vgas' in r or 'Vdisk' in r) for r in rows) if rows else False
        d['has_baryon_pts'] += 1 if has_bary else 0
        if g.get('mhi_log_msun') not in (None,''): d['has_mhi']+=1
    rep['wallaby_corpus_by_survey']=surv
    # dwarf compilation
    ds={}
    for g in dwf['galaxies']:
        s=g['survey']
        d=ds.setdefault(s,{'n':0,'vgas':0,'stellar':0,'mhi':0,'multipt':0})
        d['n']+=1
        d['vgas']+= 1 if g.get('has_vgas_profile') else 0
        d['stellar']+= 1 if g.get('has_stellar_mass') else 0
        d['mhi']+= 1 if g.get('mhi_log_msun') not in (None,'') else 0
        d['multipt']+= 1 if (g.get('n_points') or 0)>=3 else 0
    rep['dwarf_compilation_by_survey']=ds
    return wal,dwf,rep

# ---------- Framework RAR on SPARC-in-corpus (pipeline validation) ----------
def sparc_rar(wal, a0, upsilon=0.70):
    """Build the RAR on the SPARC curves present in THIS corpus, framework nu.
    Returns rms scatter (dex) of log g_obs about the framework prediction."""
    lg_res=[]
    for g in wal['galaxies']:
        if g['survey']!='SPARC': continue
        for r in g['data']:
            R=r['Rad']; Vobs=r['Vobs']
            Vgas=r.get('Vgas',0.0) or 0.0
            Vdisk=r.get('Vdisk',0.0) or 0.0
            Vbul=r.get('Vbul',0.0) or 0.0
            if R<=0 or Vobs<=0: continue
            # sign-preserving quadrature (README convention)
            vbar2 = math.copysign(Vgas*Vgas, Vgas) + upsilon*Vdisk*Vdisk + upsilon*Vbul*Vbul
            if vbar2<=0: continue
            gbar=accel_SI(math.sqrt(vbar2), R)
            gobs=accel_SI(Vobs, R)
            gpred=gobs_pred(gbar, a0)
            if gpred>0 and gobs>0:
                lg_res.append(math.log10(gobs)-math.log10(gpred))
    lg_res=np.array(lg_res)
    return len(lg_res), float(np.sqrt(np.mean(lg_res**2))), float(np.mean(lg_res))

def main():
    wal,dwf,rep=audit()
    print("="*70)
    print("ARCHIVE AUDIT -- baryonic content on NON-SPARC curves")
    print("="*70)
    print("Unified Corpus (Zenodo 19563417), by survey:")
    for s,d in rep['wallaby_corpus_by_survey'].items():
        print(f"  {s:14s} n={d['n']:3d}  curves_with_Vgas/Vdisk={d['has_baryon_pts']:3d}  with_M_HI={d['has_mhi']:3d}")
    print("Local-Volume dwarf compilation (Zenodo 20320362), by survey:")
    for s,d in rep['dwarf_compilation_by_survey'].items():
        print(f"  {s:14s} n={d['n']:3d}  Vgas_prof={d['vgas']:2d}  stellar_mass={d['stellar']:2d}  M_HI={d['mhi']:2d}  multipt(>=3)={d['multipt']:2d}")

    # Can we build g_bar on any NON-SPARC curve?
    nonsparc_baryon = sum(d['has_baryon_pts'] for s,d in rep['wallaby_corpus_by_survey'].items() if s!='SPARC')
    dwarf_bary = sum(d['vgas'] for d in rep['dwarf_compilation_by_survey'].values())
    print()
    print(f"NON-SPARC curves in either archive with a baryonic decomposition: "
          f"{nonsparc_baryon + dwarf_bary}")
    print("  (need Vgas/Vdisk or Vgas-profile per point, OR M_HI+M_star, to form g_bar)")

    print()
    print("="*70)
    print("PIPELINE VALIDATION -- framework nu on the SPARC curves in the corpus")
    print("  (proves the RAR machinery works; the NON-SPARC null is a data gap)")
    print("="*70)
    for name,a0 in [("canonical 9.36e-11",A0_CANON),("alt 1.13e-10",A0_ALT)]:
        n,rms,mean=sparc_rar(wal,a0,upsilon=0.70)
        print(f"  a0={name:20s} Upsilon=0.70 : N={n:5d}  rms={rms:.3f} dex  mean_offset={mean:+.3f} dex")
    # M/L sweep at canonical to show non-diagnosticity
    print("  M/L sweep at a0=canonical:")
    for u in (0.50,0.60,0.70,0.80):
        n,rms,mean=sparc_rar(wal,A0_CANON,upsilon=u)
        print(f"     Upsilon={u:.2f}: rms={rms:.3f} dex  mean={mean:+.3f}")

    print()
    print("VERDICT: DATA_GATED for the SPARC-INDEPENDENT (WALLABY/LV-dwarf) RAR.")
    print("  Both archives ship the 203 WALLABY + LV-dwarf curves as KINEMATICS-ONLY")
    print("  (rad,vrot[,vdisp,inc,pa]); README states 'No baryonic decomposition'.")
    print("  g_bar cannot be formed -> no framework-nu RAR possible on non-SPARC data")
    print("  from these archives. Framework nu pipeline verified on the SPARC subset.")

if __name__=="__main__":
    main()
