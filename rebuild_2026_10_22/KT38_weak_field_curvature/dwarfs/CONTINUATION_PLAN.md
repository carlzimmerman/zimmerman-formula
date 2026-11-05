# Adaptive length continuation, declared before its run

The coordinator reports no Milky Way primary pass at the initial lengths.
The ell=1 kpc scan reaches vc=242.42 but misses other cuts, while ell=3 kpc
has maximum vc=215.91 below the unchanged219.9 lower cut. This motivates a
disclosed adaptive continuation at common ell=1.5,1.75,2,2.25,2.5 kpc.
These values are not represented as part of the original blind range.

Run all five lengths for both a0 footings and the same original24objects,
41Upsilon samples, baryons, gas convention and observational cuts. Retain
the full A/B action, all three radial grids, all three independent virial
forms, selected actual-energy finite differences, and original numerical
gates without alteration. Record local negative total force separately
from the unchanged global virial-screen pass flag.

The continuation entrypoint sets only the list of common physical lengths
in a fresh process importing the unchanged KT38 dwarf implementation.
No historical source or run is edited. The complete original KT38 source
closure, entrypoint and this plan are pinned by a fresh contract/manifest.
Wall600s,CPU550s,1MiBlog,one numerical thread,no CPU-affinity request.
