"""Landau DRbar-prime vector vacuum functions, Martin hep-ph/0111209v2.

Arguments are squared masses and Q2. Loop factors are stripped.
Master functions implement Martin's renormalized I and J, not bare integrals.
"""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'master_integrals'))
from master_integrals import I, J


def SSV(x,y,z,Q2=1.):
    if z == 0:
        return ((x+y)**2+3*(x+y)*I(x,y,0,Q2)+3*J(x,Q2)*J(y,Q2)
                -2*x*J(x,Q2)-2*y*J(y,Q2))
    return ((-x*x-y*y-z*z+2*x*y+2*x*z+2*y*z)*I(x,y,z,Q2)
            +(x-y)**2*I(0,x,y,Q2)+(y-x-z)*J(x,Q2)*J(z,Q2)
            +(x-y-z)*J(y,Q2)*J(z,Q2)+z*J(x,Q2)*J(y,Q2))/z+2*(x+y-z/3)*J(z,Q2)


def VS(x,y,Q2=1.):
    return 3*J(x,Q2)*J(y,Q2)


def VVS(x,y,z,Q2=1.):
    if x==0 and y==0:
        return -3*I(0,0,z,Q2)+1.5*J(z,Q2)-z/4
    if x==0:
        x,y=y,x
    if y==0:
        return (x/4+z/2-3*z/(4*x)*I(0,0,z,Q2)
                +(3*z/(4*x)-2.25)*I(0,x,z,Q2)+3/(4*x)*J(x,Q2)*J(z,Q2))
    return ((-x*x-y*y-z*z-10*x*y+2*x*z+2*y*z)*I(x,y,z,Q2)
            +(x-z)**2*I(0,x,z,Q2)+(y-z)**2*I(0,y,z,Q2)-z*z*I(0,0,z,Q2)
            +(z-x-y)*J(x,Q2)*J(y,Q2)+y*J(x,Q2)*J(z,Q2)+x*J(y,Q2)*J(z,Q2))/(4*x*y)+.5*(J(x,Q2)+J(y,Q2))


def FFV(x,y,z,Q2=1.):
    if z==0:
        return -(x+y)**2+2*x*J(x,Q2)+2*y*J(y,Q2)
    return ((x*x+y*y-2*z*z-2*x*y+x*z+y*z)*I(x,y,z,Q2)
            -(x-y)**2*I(0,x,y,Q2)+(x-y-2*z)*J(x,Q2)*J(z,Q2)
            +(y-x-2*z)*J(y,Q2)*J(z,Q2)+2*z*J(x,Q2)*J(y,Q2))/z+2*(-x-y+z/3)*J(z,Q2)


def barFFV(x,y,z,Q2=1.):
    return 6*I(x,y,z,Q2)


def gauge(x,y,z,Q2=1.):
    v=sorted([x,y,z])
    if v[2]==0:
        return 0.
    if v[1]==0:
        t=v[2]
        return 13*t*I(0,0,t,Q2)-71/6*t*J(t,Q2)+19/4*t*t
    if v[0]==0:
        x,y=v[1:]
        return (((43*x*x*y+43*x*y*y-7*x**3-7*y**3)*I(0,x,y,Q2)
                 +(2*y+7*x)*x*x*I(0,0,x,Q2)+(2*x+7*y)*y*y*I(0,0,y,Q2)
                 +(34*x*y-7*x*x-7*y*y)*J(x,Q2)*J(y,Q2))/(4*x*y)
                +3*x*x+3*y*y+5.5*x*y-25/3*(x*J(x,Q2)+y*J(y,Q2))
                +5*(y*J(x,Q2)+x*J(y,Q2)))
    def term(x,y,z):
        return ((-x**4-8*x**3*y-8*x**3*z+32*x*x*y*z+18*y*y*z*z)*I(x,y,z,Q2)
                +(y-z)**2*(y*y+10*y*z+z*z)*I(0,y,z,Q2)
                +x*x*(2*y*z-x*x)*I(0,0,x,Q2)
                +(x*x-9*y*y-9*z*z+9*x*y+9*x*z+14*y*z)*x*J(y,Q2)*J(z,Q2)
                +(22*y+22*z-40*x/3)*x*y*z*J(x,Q2))/(4*x*y*z)
    return term(x,y,z)+term(y,x,z)+term(z,y,x)
