#!/usr/bin/env python3
"""Fix-forward entry point for G240 (2026-11-12).

Historical implementation and outputs are preserved in the correction lane's
archive/. See the top correction notice in README.md before using old claims.
No historical .out or results.json is overwritten by this replacement.
"""
from pathlib import Path
import datetime
import runpy
import sys

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    lane = Path(__file__).resolve().parents[2] / 'research_closure_2026_11_12/combined_route/deepseek_corrections'
    sys.path.insert(0, str(lane))
    def has_option(flag):
        return any(arg == flag or arg.startswith(flag + '=') for arg in sys.argv[1:])
    if not has_option('--ns'): sys.argv += ['--ns', '320']
    if not has_option('--nt'): sys.argv += ['--nt', '96']
    if not has_option('--output-dir'):
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        sys.argv += ['--output-dir', str(lane / ('manual_g240_' + stamp))]
    for index, arg in enumerate(sys.argv[1:], start=1):
        if arg == '--output-dir': destination = Path(sys.argv[index + 1])
        elif arg.startswith('--output-dir='): destination = Path(arg.split('=', 1)[1])
        else: continue
        if (destination / 'results.json').exists():
            raise SystemExit('Refusing to overwrite an existing result; use a fresh --output-dir')
    runpy.run_path(str(lane / 'corrected_aqual.py'), run_name='__main__')
