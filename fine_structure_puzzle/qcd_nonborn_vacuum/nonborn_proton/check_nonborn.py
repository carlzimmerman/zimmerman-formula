"""Finite no-alpha non-Born calculation; never executes Mathematica code."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys
import mpmath as mp
import sympy as sp
from sympy.parsing.mathematica import parse_mathematica

BASE = Path(__file__).resolve().parent
cfg = json.loads((BASE / 'INPUTS.json').read_text())
mp.mp.dps = cfg['mpmath_decimal_digits']
out = Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
checks = []


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    checks.append(name)


def near(x, y):
    return abs(x-y) < mp.mpf(cfg['relative_absolute_comparison_tolerance']) * max(1, abs(x), abs(y))


class Boxes:
    """Tiny, whitelisted parser of strings/lists/box calls, not an evaluator."""
    def __init__(self, text):
        self.text, self.i = text, 0

    def space(self):
        while self.i < len(self.text) and self.text[self.i].isspace():
            self.i += 1

    def parse(self):
        self.space()
        if self.text[self.i] == '"':
            j = self.i + 1
            while j < len(self.text):
                if self.text[j] == '\\':
                    j += 2
                elif self.text[j] == '"':
                    raw = self.text[self.i+1:j]
                    self.i = j+1
                    return raw
                else:
                    j += 1
            raise ValueError('unclosed source string')
        if self.text[self.i] == '{':
            self.i += 1
            args = self.args('}')
            return args
        match = re.match(r'[A-Za-z]+', self.text[self.i:])
        if not match:
            raise ValueError('unexpected source token '+self.text[self.i:self.i+30])
        head = match.group()
        self.i += len(head)
        self.space()
        if self.text[self.i] != '[':
            raise ValueError('expected source box opening')
        self.i += 1
        args = self.args(']')
        return (head, args)

    def args(self, closing):
        vals = []
        while True:
            self.space()
            if self.text[self.i] == closing:
                self.i += 1
                return vals
            vals.append(self.parse())
            self.space()
            if self.text[self.i] == ',':
                self.i += 1
            elif self.text[self.i] != closing:
                raise ValueError('unexpected source delimiter')


def render(box):
    if isinstance(box, str):
        return box
    head, args = box
    if head == 'RowBox':
        return ' '.join(map(render, args[0]))
    if head == 'FractionBox':
        return '(('+render(args[0])+')/('+render(args[1])+'))'
    if head == 'SuperscriptBox':
        return '(('+render(args[0])+')^('+render(args[1])+'))'
    if head == 'SqrtBox':
        return 'Sqrt['+render(args[0])+']'
    raise ValueError('source box is outside whitelist: '+head)


notebook = (BASE/'sources/SupplementaryFile_UnpolarizedVVCS.nb').read_text()
source_exprs, source_strings = {}, {}
for symbol in cfg['source_assignments']:
    needle = 'RowBox[{"'+symbol+'", "=",'
    check('exactly one source assignment '+symbol, notebook.count(needle) == 1)
    start = notebook.index(needle) + len(needle)
    box = Boxes(notebook[start:]).parse()
    string = render(box)
    for a, b in [(r'f\[Pi]', 'fpi'), (r'm\[Pi]', 'mpi'), (r'\[Mu]', 'mu'), (r'\[Pi]', 'Pi')]:
        string = string.replace(a, b)
    expr = parse_mathematica(string)
    check('source expression whitelist '+symbol, {str(v) for v in expr.free_symbols} == {'e','gA','fpi','mpi','mu'})
    e = sp.Symbol('e')
    stripped = sp.cancel(expr/e**2)
    check('source e squared stripped '+symbol, e not in stripped.free_symbols)
    source_exprs[symbol] = stripped
    source_strings[symbol] = string

mu = sp.Symbol('mu', positive=True)
s = sp.sqrt(4-mu**2)
theta = sp.acos(mu/2)
A = -44+788*mu**2-1500*mu**4+899*mu**6-215*mu**8+18*mu**10
B = 406-737*mu**2+304*mu**4-36*mu**6+2*(mu**2-4)**2*(9-35*mu**2+18*mu**4)*sp.log(mu)
P = 4-492*mu**2+942*mu**4-424*mu**6+54*mu**8
R = -127+235*mu**2-54*mu**4+(-72+418*mu**2-316*mu**4+54*mu**6)*sp.log(mu)
FS = (-2*A*theta+mu*s*B)/(96*s**5)
FB = (P*theta-mu*s*R)/(192*s**3)
FC = FS-2*FB
expected_FS = 11*sp.pi/768+mu*(3*sp.log(mu)/16+sp.Rational(1,4))-507*sp.pi*mu**2/2048
expected_FB = sp.pi/768+mu*(3*sp.log(mu)/32+sp.Rational(21,128))-327*sp.pi*mu**2/2048
expected_FC = 3*sp.pi/256-5*mu/64+147*sp.pi*mu**2/2048
for name,expr,expected in [('FS',FS,expected_FS),('FB',FB,expected_FB),('FC',FC,expected_FC)]:
    check(name+' chiral expansion through mu squared', sp.simplify(sp.series(expr,mu,0,3).removeO()-expected) == 0)
check('leading chiral logarithm cancels in difference', sp.expand(expected_FC).coeff(sp.log(mu)) == 0)

# Exact angular moments; use x=sin(t) to avoid branch ambiguity.
t = sp.Symbol('t', real=True)
angular_moments = [sp.integrate(sp.sin(t)**(2*k)*sp.cos(t)**2,(t,-sp.pi/2,sp.pi/2)) for k in (0,1)]
check('zeroth angular moment', angular_moments[0] == sp.pi/2)
check('second angular moment', angular_moments[1] == sp.pi/8)
a,b,M,L = sp.symbols('a b M L', real=True)
trace_angle = 8*sp.pi*M*(-3*b*angular_moments[0]+(a+b)*(angular_moments[0]+2*angular_moments[1]))
K = sp.simplify(trace_angle*L**4/2/(32*sp.pi**3*M**2))
expectedK = 3*(a-b)*L**4/(32*sp.pi*M)
check('full two amplitude contraction', sp.simplify(K-expectedK) == 0)
Ksub = -3*b*L**4/(16*sp.pi*M)
Kdisp = 3*(a+b)*L**4/(32*sp.pi*M)
check('subtraction plus dispersive', sp.simplify(Ksub+Kdisp-K) == 0)

# Independent local E^2/B^2 photon contraction: <q0^2>=Q^2/4.
Etrace = 3*sp.Rational(1,4)+sp.Rational(3,4)
Btrace = 2*sp.Rational(3,4)
ball_volume = L**4/(32*sp.pi**2)
Klocal = 2*sp.pi*(a*Etrace-b*Btrace)*ball_volume/M
check('independent local polarizability operator', sp.simplify(Klocal-K)==0)
for av,bv in cfg['angular_test_a_b']:
    av,bv = mp.mpf(av),mp.mpf(bv)
    angle = mp.quad(lambda y: mp.sqrt(1-y*y)*(-3*bv+(av+bv)*(1+2*y*y)),[-1,0,1])
    check('numerical angular case '+str((av,bv)), near(angle,3*mp.pi*(av-bv)/4))

funcS = sp.lambdify(mu,FS,'mpmath')
funcB = sp.lambdify(mu,FB,'mpmath')
sourceS = sp.lambdify((sp.Symbol('mu'),sp.Symbol('gA'),sp.Symbol('fpi'),sp.Symbol('mpi')),source_exprs[cfg['source_assignments'][0]],'mpmath')
sourceB = sp.lambdify((sp.Symbol('mu'),sp.Symbol('gA'),sp.Symbol('fpi'),sp.Symbol('mpi')),source_exprs[cfg['source_assignments'][1]],'mpmath')
params = {k:mp.mpf(v) for k,v in cfg['source_parameter_decimals'].items()}
physical_mu = params['mpi_GeV']/params['M_GeV']
rows=[]
for raw in cfg['dimensionless_mu_values']:
    v = physical_mu if raw=='source_ratio' else mp.mpf(raw)
    fs,fb=funcS(v),funcB(v)
    srcs,srcb=sourceS(v,1,1,1)*mp.pi**3, sourceB(v,1,1,1)*mp.pi**3
    check('parsed source vs real FS at '+raw,near(srcs,fs))
    check('parsed source vs real FB at '+raw,near(srcb,fb))
    check('magnetic source imaginary residue at '+raw,abs(mp.im(srcb))<mp.mpf('1e-60'))
    rows.append({'mu':mp.nstr(v,55),'label':raw,'FS':mp.nstr(fs,55),'FB':mp.nstr(fb,55), 'FC':mp.nstr(fs-2*fb,55), 'FC_over_HB':mp.nstr((fs-2*fb)/(3*mp.pi/256),55)})

scale = params['gA']**2/(mp.pi**3*params['fpi_GeV']**2*params['mpi_GeV'])
polar_s,polar_b = scale*funcS(physical_mu),scale*funcB(physical_mu)
polar_c = polar_s-2*polar_b
c4 = 3*polar_c/(32*mp.pi*params['M_GeV'])
c4hb = 9*params['gA']**2/(8192*mp.pi**3*params['M_GeV']*params['fpi_GeV']**2*params['mpi_GeV'])
result={'assertion_tested':'source-derived non-Born soft coefficient and isolated covariant piN-loop sector; no full mass or R', 'checks':checks, 'number_checks':len(checks), 'source_extracted_mathematica_rhs':source_strings, 'symbolic':{'K_NB_leading':str(K),'K_sub_leading':str(Ksub),'K_disp_leading':str(Kdisp),'FC_series':str(expected_FC)}, 'mu_table':rows, 'source_parameter_evaluation':{'a_plus_b_piN_GeV^-3':mp.nstr(polar_s,55),'b_piN_GeV^-3':mp.nstr(polar_b,55),'a_minus_b_piN_GeV^-3':mp.nstr(polar_c,55),'C_NB_piN_GeV^-4':mp.nstr(c4,55),'C_NB_HB_leading_GeV^-4':mp.nstr(c4hb,55),'covariant_over_HB':mp.nstr(c4/c4hb,55)}, 'non_claims':['No numerical alpha imported','No full polarizability uncertainty','No full current tensor or mass matching','No physical finite-Lambda remainder bound','No full R or alpha determination']}
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'source_parameter_evaluation':result['source_parameter_evaluation']},indent=2))
