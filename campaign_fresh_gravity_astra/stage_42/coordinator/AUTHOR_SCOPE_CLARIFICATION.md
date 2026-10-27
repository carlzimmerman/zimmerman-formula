# Preserved author clarification after frozen-source review

The author replied in collaboration after root identified the section6 scope
ambiguity. Frozen DERIVATION SHA256 is
289b493bbfba4613cf95f939e343bcdd00f0caf55037d107467c15e525e07b5f.
Original run bytes, self-review, result and inventory remain unchanged.

Exact intended replacement supplied by the author:

> Neither [Sf-Sf0] nor Fm is set to zero. By the smooth chart and the full-cone field estimate (3.5), throughout I one has Sf-Sf0=O(e) and mf=O(e). Separately, on the exterior fluid wedges, and hence at A,D, (4.4) gives nv²=O(e^4) and c²(n-rho)=O(e²). Thus Fm=int_I mf=O(e²), and the time-integrated endpoint field stress may be O(e²).

Author explicitly confirms initial nv² is O(1) in the packet core; no core
fluid smallness is used. Section5 pressure/kinetic brackets are endpoint-only;
its bulk bound uses full-cone amplitude control. This correction is necessary
for a literal reading of the frozen section6 sentence, but changes no stated
bounded cone theorem or downstream estimate.
