# k=0 / k!=0 sector gate

`sector_rank_gate.py` rederives the selected linear Euler-symbol matrix and
computes its determinant and ranks in four sectors: homogeneous static,
homogeneous dynamic, nonzero-k static, and the derived clock characteristic. The
gate does not insert a rank or determinant. It only checks derived relations:
the determinant factorization, degeneracy of the homogeneous static sector,
regularity of a nonzero-k static mode, rank loss on the derived clock characteristic,
and the fact that the homogeneous dynamic sector is not the nonzero-k sector.

The result is a concrete warning against extrapolating a nonzero-mode
Dirac count to FLRW k=0. The pseudoinverse must be defined by kernel removal
and the homogeneous constraints must be varied independently. This is an
exact finite-dimensional Fourier-symbol result at the stated witness, not a
curved-background theorem.

Run:

```sh
python3 -B sector_rank_gate.py \
  --output run_002/sector_rank_results.json
python3 -B -m unittest -v test_sector_rank_gate.py
```
