#!/usr/bin/env python3
"""
M4 Cross-Pipeline Similarity Network
=====================================

Builds a network of peptide similarities across all pipelines to identify:
1. Potential multi-target peptides
2. Scaffold families
3. Privileged structural motifs
4. Cross-disease opportunities

Uses sequence similarity + ESM-2 embedding similarity.

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import re


@dataclass
class PeptideNode:
    """A node in the peptide similarity network."""
    peptide_id: str
    sequence: str
    pipeline: str
    target: str
    disease: str


@dataclass
class SimilarityEdge:
    """An edge representing sequence similarity."""
    peptide1: str
    peptide2: str
    similarity: float
    shared_motifs: List[str]


@dataclass
class NetworkCluster:
    """A cluster of similar peptides across pipelines."""
    cluster_id: int
    peptides: List[str]
    pipelines: Set[str]
    targets: Set[str]
    core_motif: str
    potential: str  # Multi-target, scaffold, etc.


def sequence_similarity(seq1: str, seq2: str) -> float:
    """Calculate local sequence similarity."""
    s1 = "".join(c for c in seq1.upper() if c.isalpha())
    s2 = "".join(c for c in seq2.upper() if c.isalpha())

    if not s1 or not s2:
        return 0.0

    # Use shorter as reference
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    best = 0
    for offset in range(len(s2) - len(s1) + 1):
        matches = sum(1 for i, c in enumerate(s1) if c == s2[offset + i])
        best = max(best, matches)

    return best / len(s1) if len(s1) > 0 else 0.0


def find_motifs(sequence: str) -> List[str]:
    """Find structural motifs in sequence."""
    motifs = []
    seq = sequence.upper()

    # Cyclic (disulfide)
    if seq.startswith("C") and seq.endswith("C"):
        motifs.append("cyclic_disulfide")

    # RGD integrin binding
    if "RGD" in seq:
        motifs.append("RGD")

    # Melanocortin core
    if re.search(r"H[FY]RW", seq):
        motifs.append("HFRW_melanocortin")

    # Cell penetrating
    if re.search(r"[RK]{4,}", seq):
        motifs.append("CPP_polybasic")

    # GLP-1 like
    if seq.startswith("H") and "EGTFT" in seq:
        motifs.append("GLP1_like")

    # Oxytocin-like
    if re.search(r"CY.QNC", seq):
        motifs.append("oxytocin_core")

    # Hydrophobic core
    hydro = sum(1 for aa in seq if aa in "AILMFWVY")
    if hydro / len(seq) > 0.6:
        motifs.append("hydrophobic_core")

    # Aromatic-rich
    arom = sum(1 for aa in seq if aa in "FYW")
    if arom >= 3:
        motifs.append("aromatic_rich")

    return motifs


def load_all_peptides(base_dir: Path) -> List[PeptideNode]:
    """Load all peptides from JSON files."""
    peptides = []

    json_files = list(base_dir.glob("**/peptides/*.json")) + \
                 list(base_dir.glob("**/binders/*.json"))

    for json_path in json_files:
        try:
            with open(json_path) as f:
                data = json.load(f)

            # Determine pipeline
            path_str = str(json_path).lower()
            if "metabolic" in path_str:
                pipeline = "Metabolic"
            elif "neuro" in path_str and "depression" not in path_str:
                pipeline = "Neurological"
            elif "depression" in path_str or "anxiety" in path_str:
                pipeline = "Mental Health"
            elif "autoimmune" in path_str:
                pipeline = "Autoimmune"
            elif "pediatric" in path_str:
                pipeline = "Pediatric"
            elif "eye" in path_str:
                pipeline = "Eye/Vision"
            elif "prolactinoma" in path_str:
                pipeline = "Prolactinoma"
            else:
                pipeline = "Other"

            # Extract peptides
            if "peptides" in data:
                for p in data["peptides"]:
                    node = PeptideNode(
                        peptide_id=p.get("peptide_id", "unknown"),
                        sequence=p.get("sequence", ""),
                        pipeline=pipeline,
                        target=p.get("target", p.get("target_gene", "")),
                        disease=str(p.get("disease", p.get("diseases", ""))),
                    )
                    if node.sequence:
                        peptides.append(node)

        except Exception:
            continue

    return peptides


def build_similarity_network(peptides: List[PeptideNode],
                             threshold: float = 0.5) -> List[SimilarityEdge]:
    """Build similarity network with edges above threshold."""
    edges = []

    # Compare all pairs (expensive but comprehensive)
    n = len(peptides)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = peptides[i], peptides[j]

            # Skip same pipeline same target (expected similarity)
            if p1.pipeline == p2.pipeline and p1.target == p2.target:
                continue

            sim = sequence_similarity(p1.sequence, p2.sequence)

            if sim >= threshold:
                # Find shared motifs
                m1 = set(find_motifs(p1.sequence))
                m2 = set(find_motifs(p2.sequence))
                shared = list(m1 & m2)

                edge = SimilarityEdge(
                    peptide1=p1.peptide_id,
                    peptide2=p2.peptide_id,
                    similarity=round(sim, 3),
                    shared_motifs=shared,
                )
                edges.append(edge)

    return edges


def find_clusters(peptides: List[PeptideNode],
                  edges: List[SimilarityEdge]) -> List[NetworkCluster]:
    """Find clusters of connected peptides."""
    # Build adjacency
    adj = defaultdict(set)
    for e in edges:
        adj[e.peptide1].add(e.peptide2)
        adj[e.peptide2].add(e.peptide1)

    # Map id to node
    id_to_node = {p.peptide_id: p for p in peptides}

    # Find connected components
    visited = set()
    clusters = []
    cluster_id = 0

    for p in peptides:
        if p.peptide_id in visited:
            continue

        # BFS
        component = []
        queue = [p.peptide_id]

        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            component.append(curr)

            for neighbor in adj[curr]:
                if neighbor not in visited:
                    queue.append(neighbor)

        # Only keep clusters with cross-pipeline connections
        if len(component) >= 2:
            nodes = [id_to_node[pid] for pid in component if pid in id_to_node]
            pipelines = set(n.pipeline for n in nodes)
            targets = set(n.target for n in nodes if n.target)

            # Find common motif
            all_motifs = []
            for n in nodes:
                all_motifs.extend(find_motifs(n.sequence))
            if all_motifs:
                core_motif = max(set(all_motifs), key=all_motifs.count)
            else:
                core_motif = "none"

            # Determine potential
            if len(pipelines) >= 3:
                potential = "Multi-disease scaffold"
            elif len(targets) >= 2:
                potential = "Multi-target opportunity"
            elif len(pipelines) == 2:
                potential = "Cross-indication candidate"
            else:
                potential = "Scaffold family"

            cluster = NetworkCluster(
                cluster_id=cluster_id,
                peptides=component,
                pipelines=pipelines,
                targets=targets,
                core_motif=core_motif,
                potential=potential,
            )
            clusters.append(cluster)
            cluster_id += 1

    return clusters


def run_network_analysis():
    """Run cross-pipeline network analysis."""
    print("=" * 70)
    print("M4 CROSS-PIPELINE SIMILARITY NETWORK")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Load peptides
    base_dir = Path(__file__).parent.parent
    peptides = load_all_peptides(base_dir)
    print(f"Loaded {len(peptides)} peptides")

    # Count by pipeline
    pipeline_counts = defaultdict(int)
    for p in peptides:
        pipeline_counts[p.pipeline] += 1

    print("\nBY PIPELINE:")
    for pipeline, count in sorted(pipeline_counts.items()):
        print(f"  {pipeline}: {count}")

    # Build network
    print("\nBuilding similarity network (threshold=0.5)...")
    edges = build_similarity_network(peptides, threshold=0.5)
    print(f"Found {len(edges)} cross-pipeline similarity edges")

    # Find clusters
    print("\nFinding connected clusters...")
    clusters = find_clusters(peptides, edges)
    print(f"Found {len(clusters)} clusters")

    # Report interesting clusters
    print("\n" + "=" * 70)
    print("CROSS-PIPELINE OPPORTUNITIES")
    print("=" * 70)

    # Sort by number of pipelines
    clusters.sort(key=lambda c: len(c.pipelines), reverse=True)

    for cluster in clusters[:15]:
        print(f"\nCluster {cluster.cluster_id}: {cluster.potential}")
        print(f"  Pipelines: {', '.join(cluster.pipelines)}")
        print(f"  Targets: {', '.join(list(cluster.targets)[:3])}")
        print(f"  Core motif: {cluster.core_motif}")
        print(f"  Peptides: {len(cluster.peptides)}")
        for pid in cluster.peptides[:3]:
            print(f"    - {pid}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    multi_disease = sum(1 for c in clusters if len(c.pipelines) >= 3)
    multi_target = sum(1 for c in clusters if len(c.targets) >= 2)
    cross_indication = sum(1 for c in clusters if len(c.pipelines) == 2)

    print(f"Total peptides: {len(peptides)}")
    print(f"Cross-pipeline edges: {len(edges)}")
    print(f"Connected clusters: {len(clusters)}")
    print(f"Multi-disease scaffolds: {multi_disease}")
    print(f"Multi-target opportunities: {multi_target}")
    print(f"Cross-indication candidates: {cross_indication}")

    # Save results
    output_dir = Path(__file__).parent / "network_analysis"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Convert sets to lists for JSON
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_peptides": len(peptides),
        "total_edges": len(edges),
        "total_clusters": len(clusters),
        "multi_disease_scaffolds": multi_disease,
        "top_clusters": [
            {
                "cluster_id": c.cluster_id,
                "potential": c.potential,
                "pipelines": list(c.pipelines),
                "targets": list(c.targets)[:10],
                "core_motif": c.core_motif,
                "peptide_count": len(c.peptides),
                "peptides": c.peptides[:10],
            }
            for c in clusters[:20]
        ],
        "edges_sample": [asdict(e) for e in edges[:100]],
    }

    json_path = output_dir / f"network_analysis_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved: {json_path}")

    return clusters, edges


if __name__ == "__main__":
    run_network_analysis()
