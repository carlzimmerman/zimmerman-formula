#!/usr/bin/env python3
"""KO2 design toy: PRE-FREEZE, MODEL ONLY.  Run before FROZEN_CRITERIA.md was committed; reads no data file.
Deep-regime own-field band kernels; each window's shape-noise information spread uniformly in ln g_bar; window noise set so that a
one-amplitude fit there has the stated error.  Gives the error of a[outer]/a[inner] (the brief's R_own) and of the tied R_ext.
Output quoted in FROZEN_CRITERIA.md.  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import numpy as np
e = 1e-15*5000**(np.arange(16)/15)
# bands in g: centre [e13,inf), inner [e7,e13), middle [e4,e7), outer [e0,e4)
def kern(g, g1, g2):  # relative to law sqrt(a0 g); deep regime
    s2 = np.sqrt(g/g2)
    inb = 1-2*s2
    beyond = 2*np.sqrt(g)*(1/np.sqrt(g1)-1/np.sqrt(g2))
    return np.where(g>=g2,0.0,np.where(g>=g1,inb,beyond))
def cols(g):
    c = 2*np.sqrt(g/e[13])
    return np.stack([np.full_like(g,0)+c, kern(g,e[7],e[13]), kern(g,e[4],e[7]), kern(g,e[0],e[4])],1)
# fine grid in ln g over bins 0..12; info density uniform in ln g within each window; window noise set so that a one-amplitude fit in that window has error sig_w
def fisher(sig):
    F=np.zeros((4,4)); win={'out':(0,4),'mid':(4,7),'in':(7,13)}
    for w,(b0,b1) in win.items():
        g=np.exp(np.linspace(np.log(e[b0]),np.log(e[b1]),2001)[:-1]+0.5*np.log(e[b1]/e[b0])/2000)
        X=cols(g); n=len(g)
        # one-amplitude fit of law (sum of cols = 1) has info n/v -> v = n*sig^2
        v=n*sig[w]**2
        F+=X.T@X/v
    return F
for lab,sig in (('host-free late KO1',dict(out=.39,mid=.40,inn=.27)),('guess full late',dict(out=.13,mid=.13,inn=.09))):
    sig={'out':sig['out'],'mid':sig['mid'],'in':sig['inn']}
    F=fisher(sig); C=np.linalg.inv(F)
    print(lab,'4 bands: err a_c a_in a_mid a_out',np.sqrt(np.diag(C)).round(3))
    # R_own = a_out/a_in at truth 1: var = C33 + C11 - 2C13
    print('  err R_own(out/in)',np.sqrt(C[3,3]+C[1,1]-2*C[1,3]).round(3),' err R_mid',np.sqrt(C[2,2]+C[1,1]-2*C[1,2]).round(3))
    # tied ext = mid+out
    T=np.array([[1,0,0],[0,1,0],[0,0,1],[0,0,1]],float); F3=T.T@F@T; C3=np.linalg.inv(F3)
    print('  3 bands (ext tied): err',np.sqrt(np.diag(C3)).round(3),' err R_ext',np.sqrt(C3[2,2]+C3[1,1]-2*C3[1,2]).round(3))
    # inner+centre tied, mid, out separately
    T2=np.array([[1,0,0],[1,0,0],[0,1,0],[0,0,1]],float); F2=T2.T@F@T2; C2=np.linalg.inv(F2)
    print('  centre+inner tied: err a_core a_mid a_out',np.sqrt(np.diag(C2)).round(3),' R_out',np.sqrt(C2[2,2]+C2[0,0]-2*C2[0,2]).round(3) if False else np.sqrt(C2[2,2]+C2[0,0]-2*C2[0,2]).round(3))
