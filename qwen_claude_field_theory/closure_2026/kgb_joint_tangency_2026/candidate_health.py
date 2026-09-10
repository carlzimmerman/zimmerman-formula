#!/usr/bin/env python3
"""Independent 40-digit numerical health screen for shared-action search rows.

Local frozen Einstein-frame exterior vacuum only. A surviving screen means
needs further verification, never a certified action or empirical fit.
"""
import json
import mpmath as mp
from dataclasses import replace
import refine_joint as ref


def screen(candidate):
    with mp.workdps(40):
        dw,y2,u2,y1=map(lambda v:mp.mpf(str(v)),candidate['parameters'])
        u1,f,j=map(lambda k:mp.mpf(str(candidate[k])),('u1','f','j'))
        aa,bb=ref.p.pair([mp.log(v) for v in (dw,y2,u2)],u1,
                        replace(ref.p.Spec(),y1=str(y1)))
        ref.p.h.check_map(f,aa['F'],aa['X'])
        rows=[ref.audit.normalized(*[row[k] for k in ('eps','y','X','U','w','F')]) for row in (aa,bb)]
        jets=[ref.audit.jets(a,f,j) for a in rows]
        drift=[ref.audit.next_derivatives(a,f,j) for a in rows]
        relative=[abs(x-y)/max(abs(x),abs(y),1) for x,y in zip(*jets)]
        # Normalize the difference by its two physical terms, not a tiny determinant.
        relative += [abs(x-y)/max(abs(x),abs(y),1) for x,y in zip(*drift)]
        healthy=[ref.audit.evaluate(a,f,j) for a in rows]
        matched=max(relative)<mp.mpf('1e-7')
        strict=[bool(a['strict_EF']) for a in healthy]
        return dict(seven_equations_numerically_matched=bool(matched),
                    maximum_relative_residual=float(max(relative)),
                    local_strict_EF=strict,
                    angular_gradient_instability=[bool(a['kinetic']>0 and a['angular']>0) for a in healthy],
                    angular_speed_squared=[float(-a['angular']/a['kinetic']) if a['kinetic'] else None for a in healthy],
                    needs_high_precision=bool(matched and all(strict)),
                    scope='Numerical local necessary screen only; not full physical health, universal theory, or CMB')


if __name__=='__main__':print(json.dumps(screen(ref.SEED),allow_nan=False))
