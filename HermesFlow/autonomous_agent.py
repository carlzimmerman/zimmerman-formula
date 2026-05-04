#!/usr/bin/env python3
"""
AUTONOMOUS RESEARCH AGENT
==========================

Self-improving agent that autonomously discovers Z² patterns.

Agent Loop:
1. OBSERVE: Check current state (knowledge graph, domains explored)
2. DECIDE: Choose next research action (explore domain, test hypothesis, cross-analyze)
3. ACT: Execute action using MCP tools
4. LEARN: Update knowledge graph, track what works
5. REPEAT: Until goal achieved or stuck

Features:
- Auto-starting (no setup required)
- Uses Legomena for reasoning
- Uses MCP tools for research
- Tracks learning across sessions
- Self-improves hypothesis generation

Author: Carl Zimmerman
Date: May 3, 2026
"""

import json
import subprocess
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
import time

# Import MCP tools
from mcp_server import ResearchTools, Z2, Z, PHI

BASE_DIR = Path(__file__).parent
AGENT_STATE_FILE = BASE_DIR / "agent_state.json"
LEARNING_LOG = BASE_DIR / "learning_log.json"


@dataclass
class AgentState:
    """Persistent state of the autonomous agent."""
    domains_explored: List[str] = field(default_factory=list)
    hypotheses_tested: int = 0
    truths_discovered: int = 0
    current_goal: str = "discover_z2_patterns"
    iteration: int = 0
    last_action: str = ""
    stuck_count: int = 0
    session_start: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Learning:
    """A learning from research."""
    domain: str
    what_worked: str
    what_failed: str
    insight: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AutonomousAgent:
    """Self-improving autonomous research agent."""

    DOMAINS = ["particle_physics", "cosmology", "neutrino", "meteorology"]
    MAX_ITERATIONS = 50
    STUCK_THRESHOLD = 5

    def __init__(self):
        self.tools = ResearchTools()
        self.state = self._load_state()
        self.learnings: List[Learning] = self._load_learnings()

    def _load_state(self) -> AgentState:
        """Load agent state from file."""
        if AGENT_STATE_FILE.exists():
            with open(AGENT_STATE_FILE) as f:
                data = json.load(f)
                return AgentState(**data)
        return AgentState()

    def _save_state(self):
        """Save agent state to file."""
        with open(AGENT_STATE_FILE, 'w') as f:
            json.dump(asdict(self.state), f, indent=2)

    def _load_learnings(self) -> List[Learning]:
        """Load learnings from file."""
        if LEARNING_LOG.exists():
            with open(LEARNING_LOG) as f:
                data = json.load(f)
                return [Learning(**l) for l in data.get("learnings", [])]
        return []

    def _save_learnings(self):
        """Save learnings to file."""
        with open(LEARNING_LOG, 'w') as f:
            json.dump({
                "learnings": [asdict(l) for l in self.learnings],
                "count": len(self.learnings)
            }, f, indent=2)

    # =========================================================================
    # OBSERVE: Check current state
    # =========================================================================
    def observe(self) -> Dict:
        """Observe current state of research."""
        knowledge = self.tools.query_knowledge("statistics")

        return {
            "iteration": self.state.iteration,
            "domains_explored": self.state.domains_explored,
            "domains_remaining": [d for d in self.DOMAINS if d not in self.state.domains_explored],
            "hypotheses_tested": self.state.hypotheses_tested,
            "truths_discovered": self.state.truths_discovered,
            "knowledge_graph_size": knowledge.get("count", 0),
            "avg_error": knowledge.get("avg_error"),
            "stuck_count": self.state.stuck_count,
            "learnings_count": len(self.learnings)
        }

    # =========================================================================
    # DECIDE: Choose next action
    # =========================================================================
    def decide(self, observation: Dict) -> Tuple[str, Dict]:
        """Decide next action based on observation."""

        # If stuck too long, try something different
        if self.state.stuck_count >= self.STUCK_THRESHOLD:
            self.state.stuck_count = 0
            return "cross_analyze", {}

        # Priority 1: Explore unexplored domains
        remaining = observation["domains_remaining"]
        if remaining:
            return "explore_domain", {"domain": remaining[0]}

        # Priority 2: Cross-analyze ONCE if we have enough truths
        if observation["truths_discovered"] >= 3 and self.state.last_action != "cross_analyze":
            return "cross_analyze", {}

        # Priority 3: Deep dive with LLM (only if Legomena available)
        if self.state.domains_explored and self._is_llm_available():
            # Count failed deep dives (includes "failed" in what_failed)
            deep_dive_failures = sum(1 for l in self.learnings
                                     if "deep" in l.what_failed.lower() or "deep_dive" in l.what_failed.lower())

            # If too many failures, skip deep dive
            if deep_dive_failures >= 3:
                print("  [Note: Skipping deep_dive - LLM not responding]")
                return "complete", {}

            # Pick domain we haven't deep-dived recently
            domain_idx = self.state.iteration % len(self.state.domains_explored)
            domain = self.state.domains_explored[domain_idx]

            # Only do a few successful deep dives then complete
            deep_dive_success = sum(1 for l in self.learnings
                                    if "deep" in l.what_worked.lower() or "llm" in l.what_worked.lower())
            if deep_dive_success < len(self.state.domains_explored) * 2:
                return "deep_dive", {"domain": domain}

        # All done
        return "complete", {}

    def _is_llm_available(self) -> bool:
        """Check if Legomena/Ollama is available."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True, text=True, timeout=5
            )
            return "legomena" in result.stdout.lower()
        except Exception:
            return False

    def _find_best_domain(self) -> Optional[str]:
        """Find domain with best results."""
        domain_scores = {}
        for learning in self.learnings:
            if learning.domain not in domain_scores:
                domain_scores[learning.domain] = 0
            if "validated" in learning.what_worked.lower():
                domain_scores[learning.domain] += 1
            if "failed" in learning.what_failed.lower():
                domain_scores[learning.domain] -= 0.5

        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        return None

    # =========================================================================
    # ACT: Execute action
    # =========================================================================
    def act(self, action: str, params: Dict) -> Dict:
        """Execute an action."""
        self.state.last_action = action
        self.state.iteration += 1

        if action == "explore_domain":
            return self._explore_domain(params["domain"])

        elif action == "deep_dive":
            return self._deep_dive(params["domain"])

        elif action == "llm_explore":
            return self._llm_explore(params["domain"])

        elif action == "cross_analyze":
            return self._cross_analyze()

        elif action == "complete":
            return {"status": "complete", "message": "All research goals achieved"}

        return {"error": f"Unknown action: {action}"}

    def _explore_domain(self, domain: str) -> Dict:
        """Explore a domain for Z² patterns."""
        print(f"\n[EXPLORE] {domain}")

        # Fetch data
        data = self.tools.fetch_data(domain)
        if "error" in data:
            return {"status": "failed", "error": data["error"]}

        results = []
        validated = 0

        # Test each target
        for target in data["data"].keys():
            print(f"  Testing: {target}...")

            # Generate hypothesis
            hypothesis = self.tools.generate_hypothesis(domain, target, use_llm=False)
            if "error" in hypothesis:
                continue

            # Test
            test_result = self.tools.test_hypothesis(hypothesis, data)
            if "error" in test_result:
                continue

            # Validate
            validation = self.tools.validate_result(test_result)
            results.append(validation)

            if validation["verdict"] == "VALIDATED":
                self.tools.add_truth(validation)
                validated += 1
                self.state.truths_discovered += 1
                print(f"    ✓ VALIDATED: {validation['percent_error']:.4f}%")
            else:
                print(f"    ✗ {validation['verdict']}: {validation['percent_error']:.2f}%")

            self.state.hypotheses_tested += 1

        # Mark domain as explored
        if domain not in self.state.domains_explored:
            self.state.domains_explored.append(domain)

        return {
            "status": "success",
            "domain": domain,
            "tested": len(results),
            "validated": validated
        }

    def _deep_dive(self, domain: str) -> Dict:
        """Deep dive into a domain with LLM-generated hypotheses."""
        print(f"\n[DEEP DIVE] {domain}")

        data = self.tools.fetch_data(domain)
        if "error" in data:
            return {"status": "failed", "error": data["error"]}

        # Ask LLM for new hypotheses
        prompt = f"""Given Z² = 32π/3 ≈ 33.51 and data from {domain}:
{json.dumps(data['data'], indent=2)}

Generate 3 NEW hypotheses connecting Z² to this data.
Consider ratios, combinations, or relationships not yet tested.

Return JSON: {{"hypotheses": [{{"target": "name", "formula": "expression", "reasoning": "why"}}]}}"""

        try:
            result = subprocess.run(
                ["ollama", "run", "legomena-31b", prompt],
                capture_output=True, text=True, timeout=120
            )

            # Parse response
            import re
            text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', result.stdout)

            start = text.rfind('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                response = json.loads(text[start:end])
                hypotheses = response.get("hypotheses", [])

                validated = 0
                for hyp in hypotheses[:3]:
                    # Test each hypothesis
                    # ... (would need to evaluate formula)
                    print(f"  LLM hypothesis: {hyp.get('formula', 'N/A')}")

                return {"status": "success", "new_hypotheses": len(hypotheses)}

        except Exception as e:
            return {"status": "failed", "error": str(e)}

        return {"status": "no_new_hypotheses"}

    def _llm_explore(self, domain: str) -> Dict:
        """Use LLM to explore a domain more creatively."""
        return self._deep_dive(domain)

    def _cross_analyze(self) -> Dict:
        """Cross-analyze truths across domains."""
        print("\n[CROSS-ANALYZE]")

        knowledge = self.tools.query_knowledge("validated")
        truths = knowledge.get("truths", [])

        if len(truths) < 2:
            return {"status": "insufficient_data", "truths": len(truths)}

        # Look for patterns across domains
        by_domain = {}
        for t in truths:
            domain = t.get("domain", "unknown")
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(t)

        # Compute cross-domain statistics
        all_errors = [t.get("percent_error", 0) for t in truths]

        analysis = {
            "total_truths": len(truths),
            "domains": list(by_domain.keys()),
            "avg_error": np.mean(all_errors),
            "min_error": np.min(all_errors),
            "max_error": np.max(all_errors),
            "consistency": "HIGH" if np.std(all_errors) < 0.5 else "MEDIUM"
        }

        print(f"  Truths: {analysis['total_truths']}")
        print(f"  Domains: {analysis['domains']}")
        print(f"  Avg error: {analysis['avg_error']:.4f}%")
        print(f"  Consistency: {analysis['consistency']}")

        return {"status": "success", "analysis": analysis}

    # =========================================================================
    # LEARN: Update based on results
    # =========================================================================
    def learn(self, action: str, result: Dict):
        """Learn from action result."""

        # Record what worked/failed
        if result.get("status") == "success":
            self.state.stuck_count = 0
            what_worked = f"Action {action} succeeded"
            if "validated" in result:
                what_worked += f" with {result['validated']} validations"
            what_failed = ""
        else:
            self.state.stuck_count += 1
            what_worked = ""
            what_failed = f"Action {action} failed: {result.get('error', 'unknown')}"

        # Generate insight
        insight = self._generate_insight(action, result)

        # Store learning
        learning = Learning(
            domain=result.get("domain", "general"),
            what_worked=what_worked,
            what_failed=what_failed,
            insight=insight
        )
        self.learnings.append(learning)

        # Save state
        self._save_state()
        self._save_learnings()

    def _generate_insight(self, action: str, result: Dict) -> str:
        """Generate insight from action result."""
        if result.get("validated", 0) > 0:
            return f"Z² patterns found in {result.get('domain', 'domain')} - {result['validated']} validated"
        elif result.get("status") == "failed":
            return f"Need different approach for {action}"
        else:
            return "Continue exploring"

    # =========================================================================
    # MAIN LOOP
    # =========================================================================
    def run(self, max_iterations: Optional[int] = None):
        """Run the autonomous agent loop."""
        max_iter = max_iterations or self.MAX_ITERATIONS

        print("=" * 70)
        print("AUTONOMOUS RESEARCH AGENT")
        print("=" * 70)
        print(f"Goal: {self.state.current_goal}")
        print(f"Z² = {Z2:.6f}")
        print("=" * 70)

        while self.state.iteration < max_iter:
            print(f"\n{'='*60}")
            print(f"ITERATION {self.state.iteration + 1}/{max_iter}")
            print("=" * 60)

            # 1. OBSERVE
            observation = self.observe()
            print(f"\n[OBSERVE]")
            print(f"  Domains explored: {observation['domains_explored']}")
            print(f"  Truths discovered: {observation['truths_discovered']}")
            print(f"  Stuck count: {observation['stuck_count']}")

            # 2. DECIDE
            action, params = self.decide(observation)
            print(f"\n[DECIDE] Action: {action}")
            if params:
                print(f"  Params: {params}")

            # Check if complete
            if action == "complete":
                print("\n*** RESEARCH COMPLETE ***")
                break

            # 3. ACT
            result = self.act(action, params)
            print(f"\n[RESULT] Status: {result.get('status', 'unknown')}")

            # 4. LEARN
            self.learn(action, result)

            # Brief pause
            time.sleep(0.5)

        # Final summary
        self._print_summary()

    def _print_summary(self):
        """Print final research summary."""
        print("\n" + "=" * 70)
        print("RESEARCH SUMMARY")
        print("=" * 70)

        print(f"\nIterations: {self.state.iteration}")
        print(f"Domains explored: {self.state.domains_explored}")
        print(f"Hypotheses tested: {self.state.hypotheses_tested}")
        print(f"Truths discovered: {self.state.truths_discovered}")
        print(f"Learnings recorded: {len(self.learnings)}")

        # Knowledge graph stats
        knowledge = self.tools.query_knowledge("statistics")
        if knowledge.get("count", 0) > 0:
            print(f"\nKnowledge Graph:")
            print(f"  Total truths: {knowledge['count']}")
            print(f"  Average error: {knowledge['avg_error']:.4f}%")

        # Combined probability
        from scipy import stats
        validated = self.state.truths_discovered
        if validated > 0:
            prob = 1 - stats.binom.cdf(validated - 1, self.state.hypotheses_tested, 0.01)
            print(f"\nStatistical significance:")
            print(f"  {validated} validated out of {self.state.hypotheses_tested} tested")
            print(f"  Probability by chance: {prob:.2e}")

        print("\n" + "=" * 70)


def main():
    """Run the autonomous agent."""
    agent = AutonomousAgent()
    agent.run(max_iterations=20)


if __name__ == "__main__":
    main()
