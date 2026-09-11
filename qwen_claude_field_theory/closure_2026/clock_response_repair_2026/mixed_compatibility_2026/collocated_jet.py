#!/usr/bin/env python3
"""An integrable primitive in the projection's actual odd spline space."""
from functools import lru_cache
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.linalg import lu_factor, lu_solve, svdvals


@lru_cache(maxsize=8)
def derivative_operator(grid):
    r=np.asarray(grid,dtype=float)
    if len(r)<4 or r[0]!=0 or np.any(np.diff(r)<=0) or not np.all(np.isfinite(r)):
        raise ValueError('finite increasing radial grid starting at zero required')
    # Column j is the odd spline of a unit rate at positive-radius node j.
    fit=CubicSpline(r[1:]**2,np.eye(len(r)-1)/r[1:,None],axis=0)
    derivative=fit(r*r)+2*(r*r)[:,None]*fit(r*r,1)
    # Nodal derivative collocation has a near-null oscillatory mode (measured
    # condition about 1.3e9 at 513 points). Stagger the positive collocation
    # points between knots while retaining the exact regular-center equation.
    points=np.r_[0.,(r[1:-1]+r[2:])/2]
    square=fit(points*points)+2*(points*points)[:,None]*fit(points*points,1)
    singular=svdvals(square)
    if singular[-1]<=0:raise ValueError('singular clock-rate derivative operator')
    return derivative,lu_factor(square),dict(
        condition_number=float(singular[0]/singular[-1]),
        minimum_singular_value=float(singular[-1]),
        maximum_singular_value=float(singular[0]),
        imposed_derivative_rows=len(r)-1,
        collocation='center and positive-knot midpoints',
        outer_derivative_imposed=False)


def collocated_primitive(r,source):
    r=np.asarray(r,dtype=float);source=np.asarray(source,dtype=float)
    if r.ndim!=1 or source.shape!=r.shape or not np.all(np.isfinite(source)):
        raise ValueError('matching finite radial source required')
    _,factor,_=derivative_operator(tuple(r))
    points=np.r_[0.,(r[1:-1]+r[2:])/2]
    target=CubicSpline(r*r,source)(points*points)
    return np.r_[0.,lu_solve(factor,target)]
