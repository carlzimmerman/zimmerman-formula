# MK2 AMENDMENT A3 (POST HOC: written after a known answer failed; committed alone)

**What failed.** KA4's groups leg, alt footing. With no dust, the capped model's group bracket is
[+0.1583, +0.3226]. QX5's is [+0.158, +0.320]. The difference, 0.0026, is above the frozen 2e-3. Canonical passes
(+0.3597 against +0.359).

**Why.** It is not the machinery. Two gas-only group brackets already have their charge capped at R500 with no dust:
- NGC3402 (canonical and alt): M_L at R500 is 0.91 / 0.83 of the law's.
- RXCJ1840.6-7709 (alt): 0.97 of the law's.

Their law charge reaches 5.41 M_b,tot (A2's global cap) just inside R500. The same code with the cap switched off gives
[+0.1955, +0.3586] / [+0.1583, +0.3203]: QX5's numbers to 1e-4. KA4 was written assuming no cap acts inside the gate
radii at no dust. For these two groups that assumption is false. That is a property of form B's cap, not an error.

**The change (post hoc).**
- KA4's groups leg is checked on the no-dust law with the cap off. That is the machinery's reproduction of QX5.
- The capped no-dust bracket is reported as a model result.
- KA4's X-COP leg is unchanged; it passes on both footings (+0.4675 / +0.4345), and no cap acts inside 0.7 R500.

**What is reported anyway.**
- As frozen, the lane's label would be NO VERDICT, because a frozen known answer failed.
- RESULT.md states this in its first lines, beside the amended label.
- The groups row (d) has no passing c_s on either footing in any case. Its bracket fails by more than 0.15 dex at every
  c_s that has a static state, so the 0.0026 does not touch any interval.

No line, gate or grid changes.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
