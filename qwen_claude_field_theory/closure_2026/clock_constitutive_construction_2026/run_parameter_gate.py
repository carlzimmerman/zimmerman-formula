"""Runner entry point that writes the exact parameter-family result."""
import json
from pathlib import Path

from parameter_family_gate import scalar_family


def main():
    result = scalar_family()
    out = Path(__file__).resolve().parent / "run_002" / "parameter_family_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
