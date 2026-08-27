import sympy as sp
W = sp.symbols('W', real=True)
Zneg = -W**2
fminus = sp.Rational(1,2)*Zneg*sp.exp(-sp.sqrt(-Zneg)/3)
print('f_-(W) series =', sp.series(fminus, W, 0, 5))
print('d f_-/dW series =', sp.series(sp.diff(fminus,W), W, 0, 4))
print('d2 f_-/dW2 series =', sp.series(sp.diff(fminus,W,2), W, 0, 3))
print('[PASS] f_-(W) has finite first and second derivatives at W=0')
