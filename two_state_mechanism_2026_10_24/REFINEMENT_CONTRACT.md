# Targeted dwarf resolution follow-up

The explicit dwarf profile failed the original 0.05 bound-fraction difference
criterion: 0.796875 versus 0.87109375. Energy errors passed. Separate timestep
from particle-count sensitivity: run N=256 with dt=0.000025, then N=512 at the
same timestep. Compare the first with the stored N=256/dt=0.00005 run and the
second with the first. Keep the energy tolerance 0.005 and the 0.05 fraction
criterion. Preserve the original failure; do not call it a passing result.

No softening-limit test is attempted, and a successful follow-up would still
support only the specified softened, finite-time experiment. The profile
cluster run lasts 17.72 Gyr; its final snapshot must not be presented as an
age-matched cluster prediction. Earlier samples remain available separately.
