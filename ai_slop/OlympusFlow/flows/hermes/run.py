#!/usr/bin/env python3
"""
HermesFlow - Autonomous Z² Research Agent
==========================================

One command to run autonomous scientific discovery.

Usage:
    python run.py                    # Run autonomous agent
    python run.py --mcp              # Start MCP server
    python run.py --domain cosmology # Research specific domain
    python run.py --reset            # Reset agent state and start fresh

Author: Carl Zimmerman
Date: May 3, 2026
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="HermesFlow Autonomous Research")
    parser.add_argument("--mcp", action="store_true", help="Start MCP server")
    parser.add_argument("--domain", type=str, help="Research specific domain")
    parser.add_argument("--reset", action="store_true", help="Reset agent state")
    parser.add_argument("--iterations", type=int, default=20, help="Max iterations")

    args = parser.parse_args()

    if args.reset:
        # Reset agent state
        state_file = Path(__file__).parent / "agent_state.json"
        learning_file = Path(__file__).parent / "learning_log.json"
        if state_file.exists():
            state_file.unlink()
        if learning_file.exists():
            learning_file.unlink()
        print("Agent state reset.")

    if args.mcp:
        # Run MCP server
        from mcp_server import main as mcp_main
        mcp_main()

    elif args.domain:
        # Research specific domain
        from mcp_server import ResearchTools
        tools = ResearchTools()

        print(f"Researching {args.domain}...")
        data = tools.fetch_data(args.domain)

        if "error" in data:
            print(f"Error: {data['error']}")
            return

        for target in data["data"].keys():
            hyp = tools.generate_hypothesis(args.domain, target)
            if "error" in hyp:
                continue

            test = tools.test_hypothesis(hyp, data)
            val = tools.validate_result(test)

            status = "✓" if val["verdict"] == "VALIDATED" else "✗"
            print(f"  {status} {target}: {val['percent_error']:.4f}%")

    else:
        # Run autonomous agent
        from autonomous_agent import AutonomousAgent
        agent = AutonomousAgent()
        agent.run(max_iterations=args.iterations)


if __name__ == "__main__":
    main()
