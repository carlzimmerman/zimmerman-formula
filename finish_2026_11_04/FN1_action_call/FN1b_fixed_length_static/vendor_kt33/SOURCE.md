# vendor_kt33: two KT33 modules, copied unchanged

`rebuild_2026_10_22/KT33_reciprocal_filter/` and `KT34_reciprocal_epsilon_scan/` were **not committed** when FN1b ran
(2026-11-04). They are another session's working tree. FN1b's frozen criteria name KT33's engines, so the two modules it
uses are copied here byte for byte, and FN1b imports these copies. Nothing in KT33 was edited.

| file here | copied from | SHA-256 (both, equal) |
|---|---|---|
| `mw_reciprocal.py` | `rebuild_2026_10_22/KT33_reciprocal_filter/mw/mw_reciprocal.py` | a6c3980eac47d27830c8c30aee9001fc54be484bb6c4caa202b47c90d3b446b5 |
| `cassini_v2.py` | `rebuild_2026_10_22/KT33_reciprocal_filter/cassini/cassini_v2.py` | 7d928d700ea4c371b4ac3551a19fa3fbda4f6bb8acac1d9842b4a689f13ac1bf |

- `mw_reciprocal.py` finds UX5's core through a path relative to its own folder, which does not exist here. FN1b loads
  `ux5_core` from `rebuild_2026_10_22/UX5_mw_stellar_mass/` first, so the import resolves to the committed core.
- KT33's stored known answers (its MW grid run and its Cassini run 002) are snapshotted in `../fn1b_ka_snapshot.json`
  by `../fn1b_ka_snapshot.py`, with the SHA-256 of each source file. No value there is computed.
- FN1b cites no KT33 or KT34 result as its own. It uses KT33's code as an engine and reproduces KT33's stored numbers as
  known answers (KA2, KA5a).
