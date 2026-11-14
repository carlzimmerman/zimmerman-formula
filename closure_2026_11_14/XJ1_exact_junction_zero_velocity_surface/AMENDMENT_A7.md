# XJ1 AMENDMENT A7 (2026-11-14, written 15:57 EST by the clock): the lens profile inside the settled radius, with FRZ1's leftover term

Post hoc: written after every label of this lane was final and after lane BJ1's builder pointed out a difference. It
adds one reported check. It changes no case, gate, label or lane word.

**The difference.** For the forest, this lane's "law's layout" is FRZ1's mode "B": the law's halo capped at the share,
plus, where the law's halo has not used the whole share by the turnaround radius, the unused share spread in
proportion to radius (rem x r / r_ta). In this lane's lens chain (`xj1_lens.py`, `xj1_lens2.py`, `xj1_lens3.py`) the
inside of the settled radius is the law's capped halo alone, without that leftover term (the term is there only when
R_set is the turnaround radius). The criteria's wording for the lens profile, "the law's halo unscaled", does not say
which, so the reported G4 words were computed for the law's halo without the leftover term. BJ1's lens chain includes
it.

**The check (reported; no label).** `xj1_lens4.py`: a copy of `xj1_lens3.py` with the leftover term included inside
R_set (enclosed cold mass min(M_ph(x), X) + rem x / x_ta, the outside factor t recomputed from it), for Ec2 and Ec3,
with JNT2's anchor unchanged. Reported: the G4 words and early-type z beside the stored ones (Ec2 +0.28 / +0.85, Ec3
+0.57 / +1.04), the share of lens-table cells where the leftover term is not zero, and the largest relative change of
the enclosed cold mass at R_set.

**Hand estimate:** the leftover term is zero for most lenses (CSD1 found the law's charge with and without it equal
to the printed digits at z = 0); the early-type z moves by less than 0.1 and both words stay PASS (85 %).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
