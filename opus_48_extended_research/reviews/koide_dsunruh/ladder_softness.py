import mpmath as mp
mp.mp.dps = 40
me  = mp.mpf("0.51099895000"); mmu = mp.mpf("105.6583755"); mta = mp.mpf("1776.86")
smu = mp.sqrt(mmu/me); sta = mp.sqrt(mta/me)
Kexp = (1+smu**2+sta**2)/(1+smu+sta)**2
def ladder(d_):
    d_=mp.mpf(d_); e_small=abs(mp.mpf(1)/3-d_); e_big=mp.mpf(1)/3+d_
    sd=(1+d_)/(1-d_); mu=(e_big/e_small)*sd; ta=(e_big/e_small)*sd*sd
    return mu,ta
def K(d_):
    mu,ta=ladder(d_); s=[mp.mpf(1),mu,ta]; return sum(x**2 for x in s)/sum(s)**2

print("K_exp (PDG, from real masses) =", mp.nstr(Kexp,8))
print("\ndelta    K_ladder     sqrt(mu/e)  dev%      sqrt(ta/e)  dev%")
for d_ in ["0.580","0.59","0.60","0.60851","0.6124","0.62","0.63"]:
    mu,ta=ladder(d_); kk=K(d_)
    dm=(mu/smu-1)*100; dt=(ta/sta-1)*100
    tag=""
    if d_=="0.6124": tag="  <- sqrt(3/8) MAJORANA (Singh keeps)"
    if d_=="0.60851": tag="  <- tuned to K=2/3"
    print(f"{d_:8s} {mp.nstr(kk,7):11s} {mp.nstr(mu,7):11s} {mp.nstr(dm,3):8s}  {mp.nstr(ta,7):11s} {mp.nstr(dt,3):6s}{tag}")

print("\nKEY: sqrt(3/8)=%s. The K=2/3 ladder-point delta=0.6085 is" % mp.nstr(mp.sqrt(mp.mpf(3)/8),6))
print("     %.2f%% away from sqrt(3/8); NEITHER is forced to 2/3 — both are interior," % ((0.60851/float(mp.sqrt(mp.mpf(3)/8))-1)*100))
print("     and the ALGEBRA forces sqrt(3/8)=0.6124 (giving K=0.66916, NOT 2/3).")
print("     The 'K=2/3 at delta=0.6085' is a TUNED point, not an algebra output.")
print("\n  Compare: does the REAL PDG mass triple even sit at the Majorana ladder prediction?")
muM,taM = ladder("0.6124")
print("   Majorana ladder: sqrt(mu/e)=%s vs PDG %s ; sqrt(ta/e)=%s vs PDG %s" %
      (mp.nstr(muM,6), mp.nstr(smu,6), mp.nstr(taM,6), mp.nstr(sta,6)))
print("   -> Singh's Majorana ladder MISSES the real PDG sqrt-mass ratios by ~0.6-2%,")
print("      so its K=0.66916 (not the PDG K=0.66666) — the 0.38%% overshoot is REAL, not 2/3.")
