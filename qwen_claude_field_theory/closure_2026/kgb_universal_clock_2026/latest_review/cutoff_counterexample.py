#!/usr/bin/env python3
"""An exact logical counterexample, NOT a cosmological matter model."""
from fractions import Fraction as Q


def cluster_proxy(k,cutoff):
    """Only the idealized cutoff membership predicate used in the inference."""
    if k<=0 or cutoff<=0:raise ValueError('positive wavenumber and cutoff required')
    return k<cutoff


def ordered_counterexample():
    kc,early,late,kg=Q(1,10),Q(1,5),Q(1),Q(10)
    return dict(values=dict(k_cmb=kc,early=early,late=late,k_gal=kg),
        ordered_cutoffs=early<late,cmb_early=cluster_proxy(kc,early),
        cmb_late=cluster_proxy(kc,late),galaxy_late=cluster_proxy(kg,late),
        strict_margin=min(early-kc,late-early,kg-late))


def literal_law_counterexample():
    ar,an,v0=Q(1,1091),Q(1),Q(1,1000000)
    early,late=ar/v0,an/v0;kc,kg=Q(1),Q(2000000)
    return dict(a_early=ar,a_late=an,v0=v0,early=early,late=late,k_cmb=kc,k_gal=kg,
        same_mode_transfer=bool(ar<an and cluster_proxy(kc,early) and cluster_proxy(kc,late)),
        galaxy_late=cluster_proxy(kg,late))


def instantaneous_cutoff(a,H,v):
    """Jeans-like comoving scaling only; omit the constant sqrt(3/2)."""
    return a*H/v


def serial(value):
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [serial(v) for v in value]
    if isinstance(value,Q):return str(value)
    return value
