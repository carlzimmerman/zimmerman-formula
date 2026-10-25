"""POST-RUN DIAGNOSTIC (not frozen, not graded): which Burkert core radii r0 let a Sigma_a0 halo match each dwarf's
route-E requirement within 2 sd at r12, and is there one r0 shared by most dwarfs?  Reads cd1_dwarf_ceiling.json."""
import json, math, numpy as np
G, PC = 6.674e-11, 3.0857e16
A0 = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
def B(x): return np.log1p(x*x) + 2*np.log1p(x) - 2*np.arctan(x)
J = json.load(open('cd1_dwarf_ceiling.json')); out = []
r0g = np.logspace(math.log10(10), math.log10(3e5), 2000)   # pc
for f in ('canonical', 'alt'):
    Sig = A0[f]/(2*math.pi*G); ok = np.zeros_like(r0g); n = 0; wins = []
    for o in J['footings'][f]['rows']:
        if not o['graded'] or o['gh'] <= 0: continue
        r12 = 4/3*o['rh']*PC; sdh = o['sd']*10**o['D']/(10**o['D'] - 1)
        gh = G*math.pi*Sig*(r0g*PC)**2*B(r12/(r0g*PC))/r12**2
        z = (np.log10(gh) - math.log10(o['gh']))/sdh; good = np.abs(z) <= 2
        ok += good; n += 1
        wins.append((o['name'], r0g[good].min() if good.any() else None, r0g[good].max() if good.any() else None))
    i = ok.argmax()
    out.append(f'[{f}] dwarfs {n}; best shared r0 = {r0g[i]:.0f} pc fits {int(ok[i])}/{n}; '
               f'r0 fitting >= 80%: ' + (f'{r0g[ok >= 0.8*n].min():.0f}-{r0g[ok >= 0.8*n].max():.0f} pc' if (ok >= 0.8*n).any() else 'none'))
    nowin = [w[0] for w in wins if w[1] is None]
    out.append(f'   no allowed r0 at all: {len(nowin)} ({", ".join(nowin)})')
    med_lo = np.median([w[1] for w in wins if w[1]]); med_hi = np.median([w[2] for w in wins if w[2]])
    out.append(f'   median allowed window {med_lo:.0f}-{med_hi:.0f} pc')
print('\n'.join(out)); open('cd1_postrun_r0_window.out', 'w').write('\n'.join(out) + '\n')
