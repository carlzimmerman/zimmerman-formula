import os
import json
import numpy as np

mode = os.environ['ORCH_MODE']
inputs = json.load(open(os.environ['ORCH_INPUTS']))

M = 10.0
d = 0.5
r0 = d / M

def kappa(r):
    if r < r0:
        return M
    else:
        return 0.0

I = M * r0**3 / 3
var_estimate = 2 * I * np.sqrt(M)
bound = 2 * (2 * d)**1.5 / (9 * np.sqrt(M))

if mode == 'main':
    cap_certificate = bool(var_estimate < bound)
elif mode == 'positive':
    cap_certificate = True
else:
    cap_certificate = False

result = {
    'protocol': 2,
    'complete': True,
    'checks': {'cap_certificate': cap_certificate},
    'measurements': {'I': float(I), 'var_estimate': float(var_estimate), 'bound': float(bound)}
}

print(json.dumps(result))