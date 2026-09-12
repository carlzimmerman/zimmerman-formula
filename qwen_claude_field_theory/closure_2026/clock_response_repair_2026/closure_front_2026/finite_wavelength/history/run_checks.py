#!/usr/bin/env python3
"""Run the exact reduction and its actual Lean certificate, retaining output."""
import argparse
import json
from pathlib import Path
import subprocess
from derive_history import derive


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args(); here=Path(__file__).resolve().parent
    result=derive()
    lean_cwd=here.parents[3]/'clock_constitutive_construction_2026/lean_formalization_2026'
    command=['lake','env','lean',str(here/'HistorySigns.lean')]
    proc=subprocess.run(command,cwd=lean_cwd,capture_output=True,text=True,timeout=90)
    (args.output_dir/'lean.stdout.txt').write_text(proc.stdout)
    (args.output_dir/'lean.stderr.txt').write_text(proc.stderr)
    assert proc.returncode==0,(proc.returncode,proc.stdout,proc.stderr)
    assert proc.stdout.count('[propext, Classical.choice, Quot.sound]')==4
    assert 'sorryAx' not in proc.stdout
    result['lean']={'argv':command,'cwd':str(lean_cwd),'exit_status':proc.returncode,'axiom_sets':4}
    (args.output_dir/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
