import itertools
for d in (2,3,4):
  for L in (2,3):
    pts=list(itertools.product(range(L),repeat=d))
    sh=lambda x,i:tuple((x[k]+(k==i))%L for k in range(d))
    lc={};vc={};bad=0
    for y in pts:
      for i,j in itertools.combinations(range(d),2):
        links=[(y,i),(sh(y,i),j),(sh(y,j),i),(y,j)]
        if len(set(links))<4: bad+=1
        for l in links: lc[l]=lc.get(l,0)+1
        vs={l[0] for l in links}
        if len(vs)!=3: bad+=1
        for z in vs: vc[z]=vc.get(z,0)+1
    print(d,L,"link-degree",set(lc.values()),"=2(d-1)?",set(lc.values())=={2*(d-1)},"vertex",set(vc.values()),"=3m?",set(vc.values())=={3*d*(d-1)//2},"degenerate plaquettes",bad)
