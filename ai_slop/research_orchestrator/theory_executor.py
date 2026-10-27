"""Legacy symbolic score gate retired; use the autonomous v2 executor."""
def run_and_score_theory(*args,**kwargs):
    raise RuntimeError('Legacy scoring disabled; use orchestrator.py run')
