import pathlib,subprocess,sys,json
P=pathlib.Path(__file__).resolve().parent;dest=pathlib.Path(sys.argv[1]);dest.mkdir(exist_ok=True)
subprocess.run([sys.executable,str(P/'bench.py'),str(dest/'benchmark.json')],check=True)
assert json.loads((dest/'benchmark.json').read_text())==json.loads((P/'bench.json').read_text())
subprocess.run([sys.executable,str(P/'audit.py'),str(dest/'result.json')],check=True)
