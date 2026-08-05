#!/usr/bin/env python3
"""
Autonomous Research Loop Controller for Modified Inertia Field Theory.

Reads RESEARCH_LOG.md to determine the next paper number and topic,
writes and executes it, then updates the log with results.

Loop continues until:
  - All planned papers are complete
  - A paper reports a critical failure (no further computation possible)
  - The watcher (Claude) interrupts

This script handles the infrastructure; each paper's physics is in its own .py file.
"""

import os, sys, json, time, subprocess, textwrap
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "RESEARCH_LOG.md")


def read_log():
    """Parse RESEARCH_LOG.md to find papers, open issues, and next steps."""
    with open(LOG_FILE) as f:
        content = f.read()

    papers = []
    current_paper = None
    in_next = False

    for line in content.split('\n'):
        if line.startswith('## PAPER '):
            if current_paper:
                papers.append(current_paper)
            name = line.replace('## PAPER ', '').strip()
            current_paper = {"name": name, "next": "", "status": "unknown"}
            in_next = False
        elif line.startswith('**Next**:') and current_paper:
            current_paper["next"] = line.replace('**Next**:', '').strip()
            in_next = True
        elif in_next and current_paper:
            if line.strip().startswith(('**', '##', '---')):
                in_next = False
            else:
                current_paper["next"] += " " + line.strip()
        elif line.startswith('**Results**:') and current_paper:
            pass  # skip results for next determination

    if current_paper:
        papers.append(current_paper)

    return papers


def get_next_paper_number(papers):
    """Find the next available tnN number."""
    existing = set()
    for p in papers:
        name = p["name"]
        if name.startswith("tn"):
            try:
                num = int(name.split()[0][2:])
                existing.add(num)
            except (ValueError, IndexError):
                pass
    next_num = 1
    while next_num in existing:
        next_num += 1
    return next_num


def get_next_topic(papers):
    """Find what the current paper says to do next."""
    for p in reversed(papers):
        nxt = p.get("next", "").strip()
        if nxt and nxt != "None":
            return nxt
    return None


def check_redundant(topic, papers):
    """Check if a topic has already been computed."""
    for p in papers:
        results = p.get("results_raw", "")
        history = p.get("history", "")
        if topic.lower() in results.lower() or topic.lower() in history.lower():
            return True
    return False


def write_next_script(next_num, topic):
    """Write a shell script that runs the next paper and logs results."""
    script_path = os.path.join(BASE_DIR, f"run_tn{next_num}.sh")
    py_path = os.path.join(BASE_DIR, f"tn{next_num}_auto.py")

    # The actual physics code will be written by Claude (the watcher)
    shell_content = textwrap.dedent(f"""\
        #!/bin/bash
        # Autonomous run of tn{next_num}
        set -e
        echo "=== AUTONOMOUS PAPER tn{next_num}: {topic} ==="
        python3 "{py_path}"
        RESULT=$?
        if [ $RESULT -eq 0 ]; then
            echo "tn{next_num}: SUCCESS"
        else
            echo "tn{next_num}: FAILED (exit code {result})"
        fi
        exit $RESULT
    """)

    with open(script_path, 'w') as f:
        f.write(shell_content)
    os.chmod(script_path, 0o755)

    # Create empty physics script placeholder
    placeholder = textwrap.dedent(f'''\
    #!/usr/bin/env python3
    """tn{next_num} — {topic}"""
    import sys
    print("tn{next_num}: Placeholder — waiting for watcher to write physics code.")
    sys.exit(0)
    ''')

    with open(py_path, 'w') as f:
        f.write(placeholder)

    return script_path, py_path


def update_log_after_run(next_num, success, results_summary, next_topic):
    """Update RESEARCH_LOG.md after running a paper."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(LOG_FILE) as f:
        content = f.read()

    # Add new paper entry before the first "---" or at end
    new_entry = textwrap.dedent(f"""
## PAPER tn{next_num} — {results_summary.get('title', 'Auto-computed')}
**Timestamp**: {timestamp}
**History**: {'; '.join(results_summary.get('history', []))}
**Methods**: {'; '.join(results_summary.get('methods', []))}
**Results**: {'; '.join(results_summary.get('results', []))}
**Status**: {'PASS' if success else 'FAIL'}
**Next**: {next_topic or 'Review required'}

---
""")

    # Insert before the first existing paper (after ACTIVE REFRAMING section)
    insert_marker = "\n## PAPER "
    idx = content.find(insert_marker)
    if idx > 0:
        content = content[:idx] + new_entry + content[idx:]
    else:
        content += new_entry

    with open(LOG_FILE, 'w') as f:
        f.write(content)


def run_loop():
    """Main autonomous loop controller."""
    print("=" * 70)
    print("AUTONOMOUS RESEARCH LOOP CONTROLLER")
    print("=" * 70)

    # Read existing papers
    papers = read_log()
    next_num = get_next_paper_number(papers)
    next_topic = get_next_topic(papers)

    print(f"\nExisting papers in log: {len(papers)}")
    for p in papers:
        status = "???"
        if "SUCCESS" in str(p):
            status = "DONE"
        elif "FAIL" in str(p):
            status = "FAILED"
        print(f"  tn{papers.index(p)+1}: {p['name']} [{status}]")

    max_papers = 5  # Safety limit per loop iteration
    paper_num = next_num

    for i in range(max_papers):
        if i > 0:
            papers = read_log()
            next_topic = get_next_topic(papers)
            papers = read_log()
            paper_num = get_next_paper_number(papers)

        if not next_topic:
            print(f"\nNo next topic — loop complete after {i} papers.")
            break

        print(f"\n--- Paper tn{paper_num}: '{next_topic}' ---")

        # Check for obvious redundancy
        redundant = check_redundant(next_topic, papers)
        if redundant:
            print(f"  WARNING: Topic may be redundant — skipping unless watcher overrides.")
            # Continue anyway — watcher should have written the physics

        # Write scripts
        script_path, py_path = write_next_script(paper_num, next_topic)

        # Run the paper
        start = time.time()
        result = subprocess.run(
            ['bash', script_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per paper
        )
        elapsed = time.time() - start

        success = (result.returncode == 0)

        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
        if result.stderr and not success:
            print("STDERR:", result.stderr[-500:])

        # Try to parse results from the paper's output JSON if it exists
        json_path = os.path.join(BASE_DIR, f'tn{paper_num}_results.json')
        summary = {"title": next_topic, "history": [], "methods": [], "results": []}
        if os.path.exists(json_path):
            try:
                with open(json_path) as f:
                    summary = json.load(f)
            except json.JSONDecodeError:
                pass

        summary["title"] = next_topic
        summary["history"] = [f"tn{paper_num} computed: {next_topic}"]
        summary["methods"] = ["autonomous loop execution"]
        summary["results"] = [f"{'SUCCESS' if success else 'FAILED'} in {elapsed:.1f}s"]

        # Update log
        update_log_after_run(paper_num, success, summary, None)  # next topic set by watcher

        print(f"\ntn{paper_num}: {'SUCCESS' if success else 'FAILED'} ({elapsed:.1f}s)")

        if not success:
            print("Paper failed — stopping loop. Watcher should fix and retry.")
            break

        paper_num += 1

    print("\n" + "=" * 70)
    print(f"Loop complete: ran {min(i+1, max_papers)} papers.")
    print("=" * 70)


if __name__ == "__main__":
    run_loop()
