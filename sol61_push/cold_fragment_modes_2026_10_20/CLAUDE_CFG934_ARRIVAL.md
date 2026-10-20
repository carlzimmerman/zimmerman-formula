# Finalized CFG934 arrival: cooling-floor halos

20 October 2026. Read-only, bounded revision and saved-evidence audit.
**The primary result is PARTIAL and FRAGILE, on both acceleration footings.
It supplies a conditional halo-stock prescription for the faintest dwarfs,
not an energy/angular-momentum transport mechanism or a normalization of
the common scalar action.** No lane was rerun and the earlier
`CLAUDE_UPDATE.md` was not changed.

## Revision identity and audit scope

The frozen criteria were committed alone at
`9782c3df7e4ad2001dcff8333aa6ed367bf7543d`. The primary script/results and
K/mutation outputs are at
`e8bb2ae70ad6b2c86790b9312861ac2269227f71`. The finalized README and
post-hoc diagnostic part 2 are at
`8ee694096f4ef99c7000cd909256e3fe26f837e6`. The primary script has not
changed between those result/README revisions.

| Artifact | SHA256 |
|---|---|
| Criteria | `497db498b967129793d96ab57a61f3bb7b5cff5b8e7cbf035867d714418f2ef7` |
| Script | `746aa6c9274caf77eceecbccb6608455cac880d6470a0ff1fdd7daeb5d1597e1` |
| Main JSON | `6730af214697c8568b6e412c1d41e5f7e9d43aa08820795d5d2f4c57cf9643ab` |
| Main output | `76aee6f0d7b3512d2fec0b64acd7dbbf86795477e8054d9315088e6cd20b5119` |
| README | `2cf6c7858388988cf49a2270d13aba22b214455a5d037f3bb1565604e821e7a0` |

`sources_cfg934.json` pins every current lane artifact and its source commit.
The scope here is saved class arithmetic, formula/interpretation checks and
revision reconciliation. Imported upstream catalogs, the full statistical
estimator and generation-time software/input provenance were not reproduced;
no new bounded-runner manifest for Claude's original execution is asserted.

## Actual verdict and controls

Each footing has 12 corners: two molecular weights, two formation-epoch
rules and three NFW density factors. Independent arithmetic from the JSON
reproduces every class label in all 48 reading/footing/corner combinations.
The saved output and README agree.

| Reading | Canonical footing | Alternate footing |
|---|---|---|
| S, primary leftover sum | PARTIAL; UFD labels 5 consistent / 2 tension / 5 contradicted; LVD labels 0 / 1 / 11 | PARTIAL; UFD labels 4 / 3 / 5; LVD labels 0 / 1 / 11 |
| M, local max alternative | PARTIAL; all six classes consistent at 1/12 corners | PARTIAL; all six classes consistent at 2/12 corners |

Only one corner makes all six classes consistent **on both footings at
once**: ionized `mu=0.59`, `tau50`, `C=6000`. Choosing it is not a
bracket-wide survival. S has no all-consistent corner on either footing.
Its stellar-mass-to-light sensitivity gives FAILS for Upsilon_V=1 and a
corner-selectable PARTIAL for Upsilon_V=4 or the declared Upsilon floor;
FRAGILE is therefore a material qualification.

The separate K JSON reports K1-K6 passing. The low-temperature T001
mutation reports exact recovery of the bare law. The high-temperature T100
mutation **fails its frozen control in seven cells**, as retained in the
README; it must not be summarized as all controls passing. Its
overpredictions have insufficient significance in those cells. Main exit 0
does not erase that failed separate control.

## What the cooling floor assumes

The formula implemented at `cfg934.py:137` is

```
Vvir^2 = 2 k_B T/(mu m_p),
M_cool = (Vvir^2/G)^(3/2) [4pi Delta_vir rho_m(z_f)/3]^(-1/2).
```

This is the ordinary gas virial-temperature criterion. It becomes the new
H-CF rule by assigning every star-forming dwarf **exactly** this minimum
primordial collisionless halo mass at its star-formation epoch. The
temperature threshold T=10000 K, gas ionization/molecular weight,
formation-time proxy, NFW form and `rho_s=C rho_m(z_coll)` convention are
physical assumptions and declared inputs. They are not derived from the
three-field action. Molecular cooling, photoheating/reionization,
metal-dependent cooling, tidal evolution and later assembly are not solved
by this floor assignment. A minimum possible star-forming mass does not
establish each object's actual halo mass.

The use of 0.59 versus 1.22 changes the floor strongly. The preferred
all-class corner uses ionized gas, while the README acknowledges that
neutral gas at the threshold points toward the other bracket. Most UFD
formation times are group defaults: only 3/31 have their own SFH, and the
lookback grid caps the epochs. Thus “zero fitted constants” does not mean
absence of model/input choices or a physically selected successful corner.

## Consequence for Draco, Sextans, Fornax and Leo I

In the primary S reading the inherited allocation rule is

```
f_ex = max[0, 1 - M_phantom(edge)/((1-f_b) M_cool)],
g = g_law + f_ex g_N,cold-floor.
```

It reserves the law's entire edge phantom before allowing extra halo mass.
Consequently even a floor halo can give zero additional central support.
At the reported canonical ionized tau50/C6000 corner, Draco has
`M_phantom(edge)~8.17e8 Msun`, cold floor `~3.42e8 Msun`, and `f_ex=0`.
Its LVD residual remains about +0.73 natural-log sigma units. The alternate
footing also has f_ex=0. The post-hoc mass switch is around 8.7e4 Msun
for the ionized bracket, with SFH-dependent exceptions; it is not a
universal measured cutoff.

This explains why the floor can help the faintest objects while leaving
the intermediate dSph excess. It does not close the requested
Draco/Sextans stock gap, and class-average consistency of classical dwarfs
does not establish the individual Fornax/Leo I mass guards. This audit does
not infer an unreported per-object Sextans endpoint from class means.

The M alternative avoids the global leftover factor through a local max of
law phantom support and floor-halo support. Its one shared successful
corner is an actionable **allocation-law** clue, not proof that the same
matter can be counted independently as both an added halo and canonical
polarization. Connecting S or M to a common action still requires deriving
the gravitational source and avoiding that double counting.

Neither reading transports energy, charge or angular momentum, calculates
fragment production/capture, evolves an envelope, fixes the physical scalar
mass or couplings, or derives a0/kappa. It does not supply the missing
conversion from the dimensionless finite-fragment radiation coefficient to
a dwarf formation rate. Coma UDGs and clusters also receive no predicted
excess under this hypothesis. The new result therefore narrows a possible
stock/selector rule while leaving the same-action transport and four-dwarf
conservation obligations open.
