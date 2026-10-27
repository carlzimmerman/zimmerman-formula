# Scope correction: no maximal-endpoint classification

2026-10-06. The independent root-only auditor fgf045_root_audit identified this
before correction. Original ROOT_DERIVATION.md remains byte-for-byte preserved
at SHA256 e4c94d7b9019d61c91499bcc818d1f88f2b434a04c35533dace7061e853dd58d.

In the paragraph after (12), withdraw the sentence beginning "If a smooth
evolution is supplied and persists up to a maximal endpoint" insofar as it
claims forced loss of bounded gradients at that endpoint. A solution may have
an earlier endpoint than the Riccati contradiction time; classifying that
endpoint requires an additional continuation theorem not supplied here.

Replace it by: Equations (1)-(12) exclude a positive C1 solution on the whole
specified cone through T_N. If a positive C1 solution is independently supplied,
its interval covering that cone cannot include T_N. Characteristic bounds keep
density positive and finite on any such interval for each fixed N, but this
does not itself classify an earlier failure of continuation or construct a
shock. No local existence or continuation theorem is proved or imported.

All characteristic identities, coefficient bounds, explicit thresholds,
conditional energy identity and cone nonexistence conclusion survive unchanged.
This is a real restriction of an overstrong interpretive sentence, not a new
run or a silently added assumption. The original failure remains visible.

The same auditor identified a notation/units collision: G in sections 2-3
means sup_U |g| (acceleration), whereas C=4piG in the source paragraph means
Newton's constant from the pinned ancestry. Read every force-bound G in the
inequalities as G_force:=sup_U |g|, and the source constant as C=4pi G_Newton.
M=sup_U |g'| is unchanged. This disambiguation preserves the actual source
normalization; an acceleration is never inserted as Newton's constant.
