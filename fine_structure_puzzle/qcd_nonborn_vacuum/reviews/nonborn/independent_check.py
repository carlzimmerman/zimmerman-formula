"""Independent archived-source parser and nonsingular full-trace convolution."""
import ast
import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path
import mpmath as mp
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

ROOT=Path.cwd()
BASE=Path(__file__).resolve().parent
AUTHOR=ROOT/'fine_structure_puzzle/qcd_nonborn_vacuum/nonborn_proton'
COMMON=ROOT/'fine_structure_puzzle/qcd_nonborn_vacuum/common_response'
mp.mp.dps=50
checks=[]
def check(label, flag):
    if not flag: raise AssertionError(label)
    checks.append(label)
def near(a,b,tol='1e-35'):
    return abs(a-b) < mp.mpf(tol)*max(1,abs(a),abs(b))
def sha(raw): return hashlib.sha256(raw).hexdigest()

# Read from the separately downloaded exact archive, not the author's parser.
with tarfile.open(BASE/'source_work/2005.09518v2.auth.tar') as ar:
    notebook=ar.extractfile('anc/SupplementaryFile_UnpolarizedVVCS.nb').read()
check('archive ancillary exactly matches worker input',notebook==(AUTHOR/'sources/SupplementaryFile_UnpolarizedVVCS.nb').read_bytes())
nb=notebook.decode()
names=[r'\[Alpha]E1plus\[Beta]M1protonLO',r'\[Beta]M1protonLO']

def rhs_box(name):
    start='RowBox[{"'+name+'", "=",'
    check('unique raw assignment '+name,nb.count(start)==1)
    i=nb.index(start)+len(start)
    while nb[i].isspace():i+=1
    begin=i; stack=[]; quoted=False; escaped=False
    while i<len(nb):
        c=nb[i]
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c in '[{':stack.append(c)
        elif c in ']}':
            op=stack.pop();check('balanced box delimiter',op+ c in ('[]','{}'))
            if not stack:return nb[begin:i+1]
        i+=1
    raise ValueError('incomplete box')

def inert_box(raw):
    # Translate only unquoted Mathematica delimiters into Python inert calls.
    chunks=re.split(r'("(?:[^"\\]|\\.)*")',raw)
    converted=''.join(c if n%2 else c.replace('[','(').replace(']',')').replace('{','[').replace('}',']') for n,c in enumerate(chunks))
    tree=ast.parse(converted,mode='eval').body
    def visit(node):
        if isinstance(node,ast.Constant) and isinstance(node.value,str):return node.value
        if isinstance(node,ast.List):return [visit(n) for n in node.elts]
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {'RowBox','FractionBox','SuperscriptBox','SqrtBox'} and not node.keywords:
            return (node.func.id,[visit(n) for n in node.args])
        raise ValueError('non-box node '+ast.dump(node))
    return visit(tree)

def flatten(node):
    if isinstance(node,str):return node
    name,args=node
    if name=='RowBox':return ' '.join(flatten(n) for n in args[0])
    if name=='FractionBox':return '('+flatten(args[0])+')/('+flatten(args[1])+')'
    if name=='SuperscriptBox':return '('+flatten(args[0])+')**('+flatten(args[1])+')'
    if name=='SqrtBox':return 'sqrt('+flatten(args[0])+')'
    raise ValueError(name)

def expression(name):
    s=flatten(inert_box(rhs_box(name)))
    for old,new in [(r'f\[Pi]','fpi'),(r'm\[Pi]','mpi'),(r'\[Mu]','mu'),(r'\[Pi]','Pi')]:s=s.replace(old,new)
    s=s.replace('[','(').replace(']',')').replace('^','**')
    tokens=set(re.findall('[A-Za-z]+',s))
    check('formula identifiers whitelisted '+name,tokens<={'e','gA','fpi','mpi','mu','Pi','ArcTan','ArcTanh','Log','sqrt'})
    syms={v:sp.Symbol(v) for v in ('e','gA','fpi','mpi','mu')}
    syms.update({'Pi':sp.pi,'ArcTan':sp.atan,'ArcTanh':sp.atanh,'Log':sp.log,'sqrt':sp.sqrt})
    formula=parse_expr(s,local_dict=syms,transformations=standard_transformations+(implicit_multiplication_application,))
    stripped=sp.cancel(formula/syms['e']**2)
    check('no charge after exact e2 stripping '+name,syms['e'] not in stripped.free_symbols)
    return stripped,s

exprs=[expression(n) for n in names]
arg_syms=[sp.Symbol(n) for n in ('mu','gA','fpi','mpi')]
source_fns=[sp.lambdify(arg_syms,e[0],'mpmath') for e in exprs]

# Real branches are evaluated from the raw archive formula. The source's
# ArcTanh arguments are imaginary; test both sides of mu=sqrt(2), as well as
# near the endpoints of the open interval on which the real formula is claimed.
def real_forms(mu):
    s=mp.sqrt(4-mu*mu); th=mp.acos(mu/2); l=mp.log(mu)
    A=-44+788*mu**2-1500*mu**4+899*mu**6-215*mu**8+18*mu**10
    B=406-737*mu**2+304*mu**4-36*mu**6+2*(mu**2-4)**2*(9-35*mu**2+18*mu**4)*l
    P=4-492*mu**2+942*mu**4-424*mu**6+54*mu**8
    R=-127+235*mu**2-54*mu**4+(-72+418*mu**2-316*mu**4+54*mu**6)*l
    return (-2*A*th+mu*s*B)/(96*s**5),(P*th-mu*s*R)/(192*s**3)

branch_rows=[]
for raw in ['0.0001','0.01','0.1487524912871561490828865891481130165','0.5','1','1.4142135623730950488','1.5','1.9','1.99']:
    v=mp.mpf(raw); src=[f(v,1,1,1)*mp.pi**3 for f in source_fns]; real=real_forms(v)
    check('independent raw-source vs real branches '+raw,all(near(a,b,'1e-31') for a,b in zip(src,real)))
    check('source formula imaginary residue '+raw,max(abs(mp.im(z)) for z in src)<mp.mpf('1e-40'))
    s=mp.sqrt(4-v*v)
    check('atan branch identity '+raw,near(mp.atan(v/s)-mp.atan((v*v-2)/(v*s)),mp.acos(v/2)))
    branch_rows.append({'mu':raw,'FS':mp.nstr(real[0],35),'FB':mp.nstr(real[1],35)})

# Independent charge coefficient algebra from primary BKSM coefficients.
k=sp.Symbol('kappa_s');
elog=sp.Integer(9)-3; blog=3*((3+k)-(1-k))
econst=(sp.Integer(71)-39)/8; bconst=((sp.Rational(37,2)+6*k)-(sp.Rational(13,2)-6*k))/4
check('BKSM electric difference',(elog,econst)==(6,4))
check('BKSM magnetic difference',sp.expand(blog)==6+6*k and sp.expand(bconst)==3+3*k)
check('scalar nonsinglet log cancellation branch',sp.expand(elog-blog).subs(k,0)==0)
check('SO4 nonsinglet logarithm',sp.expand(sp.Rational(3,32*96)*(elog-blog))==-3*k/512)

# Check full tensor contraction from angular moments and orthogonal E/B trace.
x=sp.Symbol('x'); a,b=sp.symbols('a b')
source_trace=sp.expand(-3*(b-(a+b)*x*x)+(1-x*x)*(a+b))
local_trace=sp.expand(a*(1+2*x*x)-2*b*(1-x*x))
check('two-current vs local polarizability tensor',source_trace==local_trace)
check('angular zero for a=b',sp.expand(source_trace).coeff(x,0).subs(a,b)/2+sp.expand(source_trace).coeff(x,2).subs(a,b)/8==0)

# Finite-band kernel: no author code and no arctangent function.
legendre={}
def gl(n):
    if n not in legendre:
        nodes,weights=mp.gauss_quadrature(n,'legendre')
        legendre[n]=[(mp.mpf(z+1)/2,mp.mpf(w)/2) for z,w in zip(nodes,weights)]
    return legendre[n]

def stable_trace(t,x,n):
    y=x*x;h=1-y;H=mp.sqrt(1+t*y);hp=H+1
    integ=mp.fsum(w*(z-h*z*z)/(mp.sqrt(1+t*(z-h*z*z))*(1+mp.sqrt(1+t*(z-h*z*z)))) for z,w in gl(n))
    rational=y*(2*h+t*y/hp)/(hp*hp*(4*h+t))
    return t*(mp.mpf('0.5')+y*(2/hp+1/(2*hp*hp))+rational-(2+t/2)*integ)

def raw_source_trace(t,x):
    # Direct NP source S1/S2 translation, retained only at safe interior points.
    h=1-x*x;v=t*h;w=-t*x*x;q=-t;H=mp.sqrt(1-w);D=4*v+q*q
    J=mp.quad(lambda z:1/mp.sqrt(1+t*z-t*h*z*z),[0,1])
    B1=mp.mpf('1.5')+1/v-(1+1/v)*H-(2+q/v)*J/2
    B2=-(mp.mpf('1.5')+(mp.mpf('0.5')+1/q+1/w)*q/v)-(w*q/D)*(1/v-q/(2*v))+(1/v)*(2-(v/w)*(1-w)+q*w/D)*H+(2+3*q/v+q)*J/2
    return -3*B1-B2

endpoint_rows=[]
for r in ['0.1','0.25','0.5']:
    t=mp.mpf(r)**2
    for xraw in ['0.0001','0.125','0.5','0.875','0.9999']:
        xx=mp.mpf(xraw)
        check('stable source trace '+r+','+xraw,near(stable_trace(t,xx,32),raw_source_trace(t,xx),'1e-32'))
    for xx in [mp.mpf(0),mp.mpf(1)]:
        val=stable_trace(t,xx,32)
        endpoint_rows.append({'r':r,'x':str(xx),'trace':mp.nstr(val,35)})
        check('angular endpoint continuity '+r+','+str(xx),abs(val-stable_trace(t,(mp.mpf('1e-12') if xx==0 else 1-mp.mpf('1e-12')),32))<mp.mpf('1e-12'))

def band(lo,hi,n,nx):
    lo=mp.mpf(lo)**2;hi=mp.mpf(hi)**2
    angular=[(mp.cos(mp.pi*j/(nx+1)),mp.pi/(nx+1)*mp.sin(mp.pi*j/(nx+1))**2) for j in range(1,nx+1)]
    return (hi-lo)*mp.fsum(wt*mp.fsum(wx*stable_trace(lo+(hi-lo)*tt,xx,n) for xx,wx in angular) for tt,wt in gl(n))

frozen=json.loads((AUTHOR/'finite_run_001/result.json').read_text())
band_rows=[]
for target in frozen['bands']:
    lo,hi=target['a'],target['b']; vals=[]
    for n,nx in [(16,32),(32,64),(48,96)]:
        vals.append(band(lo,hi,n,nx))
    ref=mp.mpf(target['J_by_order']['48'])
    check('independent full band agrees '+lo+','+hi,near(vals[-1],ref,'1e-25'))
    check('independent quadrature convergence '+lo+','+hi,near(vals[-2],vals[-1],'1e-23'))
    band_rows.append({'a':lo,'b':hi,'J_independent':[mp.nstr(v,40) for v in vals],'absolute_disagreement':mp.nstr(abs(vals[-1]-ref),10)})

params={'M':mp.mpf('0.93827'),'mpi':mp.mpf('0.13957'),'fpi':mp.mpf('0.09221'),'gA':mp.mpf('1.27')}
mu=params['mpi']/params['M']; fs,fb=real_forms(mu)
scale=params['gA']**2/(mp.pi**3*params['fpi']**2*params['mpi'])
staticC=3*scale*(fs-2*fb)/(32*mp.pi*params['M'])
static=json.loads((AUTHOR/'run_001/result.json').read_text())
check('normalized covariant soft coefficient',near(staticC,mp.mpf(static['source_parameter_evaluation']['C_NB_piN_GeV^-4'])))
pref=params['gA']**2*params['mpi']**3/(128*mp.pi**4*params['M']*params['fpi']**2)
check('finite prefactor dimensions and value',near(pref,mp.mpf(frozen['dimensionful_source_prefactor'])))
result={'checks_passed':len(checks),'checks':checks,'raw_archive_formula_sha256':[sha(s.encode()) for _,s in exprs],'raw_archive_formulas':[s for _,s in exprs],'branch_rows':branch_rows,'endpoint_rows':endpoint_rows,'independent_bands':band_rows,'C_covariant_piN_GeV^-4':mp.nstr(staticC,40),'prefactor':mp.nstr(pref,40),'non_claims':['No full-QCD proton mass or physical uncertainty','No full curved vacuum A or R','No empirical alpha','Quadrature agreement is not a rigorous interval bound','Common-response coefficient was exposed before PRETARGET; not a blind factor check']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks_passed':len(checks),'bands':band_rows,'staticC':mp.nstr(staticC,30)},indent=2))
