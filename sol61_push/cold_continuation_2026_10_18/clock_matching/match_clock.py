"""Bounded tree-level host-clock matching and exact four-field dispersion.

The response action is the CE-FM-079 ansatz; only the host clock is matched.
No microscopic derivation of the response sector or UV completion is claimed.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from numpy.polynomial import Polynomial as Poly
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1])
assert OUT.is_dir()
SOURCE = ROOT / "sol61_push/closure_particle_bridge_2026_10_16"
phases = json.loads((SOURCE / "mediator_phase_matching_run_002/results.json").read_text())
checks = []


def check(name, passed):
    checks.append({"name": name, "passed": bool(passed)})
    assert passed, name


# Exact algebra is independent of the floating eigensystem implementation.
Ar, Bh, hh, X, kap, sig = sp.symbols("Ar Bh h X kappa s", positive=True)
H = sp.Matrix([[Ar, hh], [hh, Bh]])
R = (H + sig * sp.eye(2)).inv()[0, 0]
Q = (Ar + sig) * (Bh + sig) - hh**2
check("resolvent rational identity", sp.simplify(R - (Bh + sig) / Q) == 0)
Aeff = Ar - hh**2 / Bh
check("adiabatic PXX to delta", sp.simplify(4 * kap * X * R.subs(sig, 0) - 4 * kap * X / Aeff) == 0)
check("resolvent derivative", sp.simplify(-sp.diff(R, sig).subs(sig, 0) - (H.inv() ** 2)[0, 0]) == 0)
A, C, E, d, z, q, t = sp.symbols("A C E d z k2 t", real=True)
Qz = Q.subs(sig, q-z)
quartic = (A*z-C*q)*((kap*z-E*q)*Qz+4*kap*X*z*(Bh+q-z))-d*d*z*q*t*Qz
check("full dispersion quartic", sp.Poly(quartic, z).degree() == 4)
check("homogeneous physical gaps", sp.simplify(quartic.subs(q, 0)/(A*kap*z*z) - ((Ar-z+4*X)*(Bh-z)-hh*hh)) == 0)
g, Z, y = sp.symbols("gamma Z0 y", positive=True)
delta0 = 4*kap*X*Bh/(Ar*Bh-hh*hh)
subs = {A: Z+2*g*y, C: g*y*(1+t), E: kap-(Z+g*y)*y*y*t/X, d*d: (Z+g*y)**2*y*y/X}
cone = sp.factor(quartic.subs(z, q).subs(subs)/(q*q*(Ar*Bh-hh*hh)))
expected = delta0*(Z+g*y-g*y*t)-g*(Z+g*y)*y**3*t*t/X
check("exact lightcone test equals adiabatic margin at every k", sp.simplify(cone-expected) == 0)
check("canonical radial principal obstruction", sp.simplify(expected.subs({t:1, delta0:0}) + g*(Z+g*y)*y**3/X) == 0)
# Stationary branch X=V_I; dX/dI=2 lambda-a^2/B=Ar/(2I)-h^2/(2I B).
I, lam, aa = sp.symbols("I lambda a", positive=True)
check("microscopic PXX identity", sp.simplify((1/(2*lam-aa*aa/Bh)).subs({lam:Ar/(4*I),aa*aa:hh*hh/(2*I)}) - 2*I/Aeff) == 0)
delta1, b, c = sp.symbols("Delta1 b c", real=True)
f = A*(kap+delta0)*z*z-(A*E+(kap+delta0)*C+d*d*t)*z+C*E
low = (A*z-C)*((kap+delta0)*z-E-delta1*z*(1-z)*q)-d*d*z*t
series_q = sp.diff(low.subs(z,c+b*q),q).subs(q,0)
check("first dispersive correction", sp.simplify(series_q-(sp.diff(f,z).subs(z,c)*b-delta1*(A*c-C)*c*(1-c))) == 0)


def background(row):
    mass = row["M_over_m"]
    density, omega2, x = row["phase_I_exact"], row["omega_squared_exact"], row["phase_negative_chi"]
    ar = 4*(2-1/mass)*density
    bh = mass*mass+.75*mass*x+3*x*x
    h = 2*mass*math.sqrt(2*density)
    mat = np.array([[ar,h],[h,bh]])
    eig = np.linalg.eigvalsh(mat)
    actual = np.linalg.eigvalsh(mat+np.diag([4*omega2,0]))
    ke = 2*density
    ae = ar-h*h/bh
    de = 4*ke*omega2/ae
    return dict(M=mass,I=density,X=omega2,Ar=ar,Bh=bh,h=h,H=mat,
                static_eigenvalues=eig,physical_gap_squared=actual,kappa=ke,
                Aeff=ae,Delta0=de,Delta1=4*ke*omega2*(bh*bh+h*h)/(ar*bh-h*h)**2,
                cs2=ae/(ae+4*omega2),cutoff=.1*math.sqrt(float(eig[0])))


def response(bg,y,t):
    ke,X=bg["kappa"],bg["X"]
    return 1+2*y,y*(1+t),ke-(1+y)*y*y*t/X,(1+y)*y/math.sqrt(X)


def eft_roots(bg,y,t,canonical=False):
    a,c,e,d=response(bg,y,t)
    b=bg["kappa"]+(0 if canonical else bg["Delta0"])
    su=a*e+b*c+d*d*t
    hi=(su+math.sqrt(su*su-4*a*b*c*e))/(2*a*b)
    lo=c*e/(a*b*hi)
    return np.array([lo,hi])


def modes(bg,y,t,k):
    """Canonical normalized phase psi=sqrt(kappa)*pi, amplitudes a,b, response f.

    M qddot+G qdot+K q=0. G is anti-Hermitian, K positive for E>0.
    Group derivatives use the Hermitian quadratic pencil, independently of D.
    """
    a,c,e,d=response(bg,y,t)
    mass=np.diag([1.,1.,1.,a])
    stiff=np.diag([k*k+bg["Ar"],k*k+bg["Bh"],e/bg["kappa"]*k*k,c*k*k])
    stiff[0,1]=stiff[1,0]=bg["h"]
    gyro=np.zeros((4,4),complex)
    gyro[0,2]=-2*math.sqrt(bg["X"])
    gyro[2,0]=2*math.sqrt(bg["X"])
    gyro[2,3]=gyro[3,2]=-1j*d/math.sqrt(bg["kappa"])*k*math.sqrt(t)
    generator=np.block([[np.zeros((4,4)),np.eye(4)],[-np.linalg.solve(mass,stiff),-np.linalg.solve(mass,gyro)]])
    ev,vec=np.linalg.eig(generator)
    found=[]
    for j,v in enumerate(ev):
        if v.imag>=0:
            continue
        w=-float(v.imag)
        u=vec[:4,j]
        dk=2*k*np.diag([1.,1.,e/bg["kappa"],c])
        dg=np.zeros((4,4),complex)
        dg[2,3]=dg[3,2]=-1j*d/math.sqrt(bg["kappa"])*math.sqrt(t)
        dw=-2*w*mass-1j*gyro
        derivative=-(np.vdot(u,(dk-1j*w*dg)@u)/np.vdot(u,dw@u))
        pencil=stiff-w*w*mass-1j*w*gyro
        residual=np.linalg.norm(pencil@u)/(np.linalg.norm(stiff)+w*w*np.linalg.norm(mass)+w*np.linalg.norm(gyro))/np.linalg.norm(u)
        found.append({"omega":w,"phase_speed":w/k,"group_speed":float(derivative.real),"group_imaginary":abs(float(derivative.imag)),"residual":float(residual)})
    return sorted(found,key=lambda r:r["omega"]),float(max(abs(ev.real)))


def independent_quartic(bg,y,t,k):
    a,c,e,d=response(bg,y,t)
    zz=Poly([0.,1.]);ss=k*k-zz
    qq=(bg["Ar"]+ss)*(bg["Bh"]+ss)-bg["h"]**2
    det=(a*zz-c*k*k)*((bg["kappa"]*zz-e*k*k)*qq+4*bg["kappa"]*bg["X"]*zz*(bg["Bh"]+ss))-d*d*zz*k*k*t*qq
    roots=det.roots()
    check("quartic roots real positive",max(abs(roots.imag))<1e-6 and min(roots.real)>0)
    return np.sqrt(np.sort(roots.real))


backgrounds={int(r["M_over_m"]):background(r) for r in phases["rows"]}
cases=[(1,.1),(1,.6),(10,.1),(10,1.),(10,1.5),(100,1.),(100,3.),(100,3.6)]
low_rows=[]
for mm,yy in cases:
    bg=backgrounds[mm]
    r=(1+yy)*yy*yy/bg["X"]
    cone=bg["Delta0"]-yy*r
    check("allowed radial energy "+str((mm,yy)),bg["kappa"]>r)
    check("allowed radial common-cone margin "+str((mm,yy)),cone>0)
    largest_phase=largest_group=all_group=max_imag=max_residual=eft_error=kernel_error=0.
    count=0
    for tt in np.linspace(0,1,9):
        ef=eft_roots(bg,yy,float(tt))
        for kk in bg["cutoff"]*np.geomspace(.001,1.,17):
            full,growth=modes(bg,yy,float(tt),float(kk))
            check("four positive modes",len(full)==4)
            max_imag=max(max_imag,growth,max(r["group_imaginary"] for r in full))
            max_residual=max(max_residual,max(r["residual"] for r in full))
            largest_phase=max(largest_phase,max(r["phase_speed"] for r in full[:2]))
            largest_group=max(largest_group,max(r["group_speed"] for r in full[:2]))
            all_group=max(all_group,max(r["group_speed"] for r in full))
            exact=np.array([r["omega"] for r in full[:2]])
            approx=kk*np.sqrt(ef)
            eft_error=max(eft_error,float(max(abs(exact/approx-1))))
            for rr in full[:2]:
                ss=kk*kk-rr["omega"]**2
                resolvent=np.linalg.solve(bg["H"]+ss*np.eye(2),np.array([1.,0.]))[0]
                rational=(bg["Bh"]+ss)/((bg["Ar"]+ss)*(bg["Bh"]+ss)-bg["h"]**2)
                check("independent resolvent evaluation",abs(resolvent/rational-1)<5e-12)
                kernel_error=max(kernel_error,abs(4*bg["kappa"]*bg["X"]*resolvent/bg["Delta0"]-1))
            count+=1
    check("low-band stability",max_imag<1e-7)
    check("quadratic pencil residual",max_residual<1e-10)
    check("exact two low-mode phase speeds below one",largest_phase<1)
    check("tested low-band group speeds below one",all_group<1)
    check("resolvent norm error bound",kernel_error<=.01/.99+1e-9)
    # Independent determinant and centered finite difference of eigenfrequencies.
    for tt in (0.,.5,1.):
        kk=bg["cutoff"]
        full,_=modes(bg,yy,tt,kk)
        roots=independent_quartic(bg,yy,tt,kk)
        check("quartic versus first-order spectrum",max(abs(roots/np.array([rr["omega"] for rr in full])-1))<1e-7)
        left,_=modes(bg,yy,tt,kk*(1-1e-4))
        right,_=modes(bg,yy,tt,kk*(1+1e-4))
        for j in range(2):
            fd=(right[j]["omega"]-left[j]["omega"])/(2e-4*kk)
            check("group derivative finite difference",abs(fd-full[j]["group_speed"])<2e-6)
    low_rows.append(dict(M=mm,y=yy,epsilon=1.,cutoff=bg["cutoff"],radial_spatial_margin=bg["kappa"]-r,
                         radial_cone_margin=cone,spectra=count,max_low_phase_speed=largest_phase,
                         max_low_group_speed=largest_group,max_all_group_speed=all_group,
                         max_low_frequency_relative_EFT_error=eft_error,max_kernel_relative_error=kernel_error,
                         max_real_generator_eigenvalue=max_imag,max_pencil_relative_residual=max_residual))

# One discriminating continuation beyond the gap, not a fresh old cone table.
bg=backgrounds[10]
scan=[]
for kk in np.geomspace(1e-3,1e4,121):
    full,growth=modes(bg,1.,1.,float(kk))
    check("extended scan spectral stability",growth<1e-7)
    scan.append(dict(k=float(kk),max_group_speed=max(rr["group_speed"] for rr in full),modes=full))
first=next(j for j in range(1,len(scan)) if scan[j-1]["max_group_speed"]<1 and scan[j]["max_group_speed"]>1)
lo,hi=scan[first-1]["k"],scan[first]["k"]
cross=brentq(lambda kk:max(rr["group_speed"] for rr in modes(bg,1.,1.,kk)[0])-1,lo,hi,xtol=1e-11)
at_cross,_=modes(bg,1.,1.,cross)
front=np.sqrt(eft_roots(bg,1.,1.,canonical=True))
check("canonical front superluminal",front[1]>1)
check("full spectrum approaches canonical front",abs(scan[-1]["modes"][-1]["phase_speed"]-front[1])<1e-7)
check("first detected group crossing above static cutoff",cross>bg["cutoff"])

summary=[]
for mm,bg in backgrounds.items():
    summary.append({kk:(vv.tolist() if isinstance(vv,np.ndarray) else vv) for kk,vv in bg.items() if kk!="H"})
result={"claim_id":"CE-CONT-CLOCK-MATCH-001","checks":checks,"check_count":len(checks),
        "backgrounds":summary,"low_band_rows":low_rows,
        "extended_M10_y1_radial":{"scan_bracket_for_first_group_crossing":[lo,hi],"k_at_crossing":cross,
          "modes_at_crossing":at_cross,"canonical_front_speeds":front.tolist(),"scan":scan},
        "sampling":{"cases":8,"angles_t":[j/8 for j in range(9)],"k_per_angle":17,"low_spectra":8*9*17,
                    "extended_spectra":121,"randomness":False},
        "non_claims":["The phase-response derivative action is retained from CE-FM-079, not derived from the mediator.",
          "Finite group-speed sampling is not a proof of a uniform finite-band group-velocity bound.",
          "Massive phase speed greater than one is not itself a causality diagnosis; the front and group velocities are reported separately.",
          "The response ansatz above the host gap is a conditional extrapolation, not a UV-matched theory.",
          "No loops, quantum protection, response formation, metric/lensing, population transport or original theory closure."]}
(OUT/"results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"checks":len(checks),"backgrounds":summary,"low_band_rows":low_rows,
                  "first_group_crossing":cross,"canonical_front_speeds":front.tolist(),"sampling":result["sampling"]},indent=2))
