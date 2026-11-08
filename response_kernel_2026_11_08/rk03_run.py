#!/usr/bin/env python3
"""Serialization-only adapter for RK03; preserve original failed run/code."""
import argparse
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import rk03_test as experiment


def numpy_scalar(value):
    if isinstance(value,np.generic):return value.item()
    raise TypeError(f'Unsupported result type: {type(value).__name__}')


def dumps(value,**kwargs):
    return json.dumps(value,default=numpy_scalar,**kwargs)


if __name__=='__main__':
    assert json.loads(dumps({'fixture':np.bool_(True)}))=={'fixture':True}
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    experiment.json=SimpleNamespace(loads=json.loads,dumps=dumps)
    experiment.main(args.output)
