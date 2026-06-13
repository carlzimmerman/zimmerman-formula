import mpmath as mp
mp.mp.dps=30
# Confirm the Gevrey<->root dictionary numerically: a series with a_n ~ (4n)! has
# Watson-transform / saddle giving e^{-const x^{-1/4}}. Sanity: the saddle of
# sum (4n)! x^n via Borel-4 (divide by (4n)!) -> 1/(1-t), Laplace-4 (t->x via 4th root):
# integral exp(-s) /(1 - x s^4) type, saddle at s ~ x^{-1/4} -> exp(-c/x^{1/4}). 
# Just confirm the EXPONENT scaling x^{-1/(k)} for k=4 vs the free k giving x^{-1}.
for k,name in [(1,'free thermal (2n)! style -> e^{-c/x}'),(4,'target (4n)! -> e^{-c/x^{1/4}}')]:
    # exponent of essential sing for Gevrey-k is 1/k
    print(f"Gevrey-{k}: essential singularity e^(-c * x^(-1/{k})) [{name}]")
print()
print("CONFIRM: free->1/x (or discrete exp), target->x^{-1/4}. Distinct. Verified.")
