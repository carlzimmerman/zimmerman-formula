# Global continuation test

The positive-Z exact branch is not real-valued for Z<0 because of sqrt(Z). For a candidate global model we therefore need a separate cosmological branch.

Test continuation used here:

f_-(Z) = (1/2) Z exp(-sqrt(-Z)/3),  Z < 0.

This is NOT claimed to be uniquely preferred. It is used because it has the same first derivative at Z=0 as the MOND branch:

f_-(0)=0,  f_-'(0)=1/2.

Near the crossing, write Z = -W^2. Then

f_-(Z) = -W^2/2 + W^3/6 + O(W^4),

while the positive branch gives

f_+ = 2 W^2 - W^3/6 + O(W^4)

when parameterized with its corresponding positive-Z variable. The relevant regularity question is therefore not whether f_ZZ is finite as a function of Z, but whether the pulled-back action is sufficiently regular in the actual crossing variable W and in the physical perturbations.

This package deliberately does NOT claim that matching f and f' at Z=0 proves stability.
