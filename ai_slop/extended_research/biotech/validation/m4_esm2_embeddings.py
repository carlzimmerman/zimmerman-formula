#!/usr/bin/env python3
"""
M4 ESM-2 Embedding Analysis
===========================

Uses ESM-2 protein language model to generate embeddings for all peptides.
These embeddings can be used for:
1. Clustering similar peptides
2. Predicting binding affinity (with training data)
3. Finding structural similarities
4. Novelty detection

ESM-2 is lighter than ESMFold and doesn't require openfold.

LICENSE: AGPL-3.0-or-later
AUTHOR: Carl Zimmerman & Claude Opus 4.5
DATE: April 2026
"""

import torch
import esm
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import hashlib


# Check device
if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")


@dataclass
class PeptideEmbedding:
    """ESM-2 embedding for a peptide."""
    peptide_id: str
    sequence: str
    length: int
    embedding_dim: int
    mean_embedding: List[float]  # Mean-pooled embedding
    cluster_id: Optional[int]
    nearest_neighbors: List[str]
    novelty_score: float  # Distance from nearest cluster center
    sha256: str


def load_esm2_model(model_name: str = "esm2_t33_650M_UR50D"):
    """Load ESM-2 model."""
    print(f"Loading ESM-2 model: {model_name}")
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    model = model.eval()

    # Try to move to GPU
    try:
        model = model.to(DEVICE)
        print(f"Model loaded on {DEVICE}")
    except Exception as e:
        print(f"Falling back to CPU: {e}")
        model = model.to("cpu")

    batch_converter = alphabet.get_batch_converter()
    return model, batch_converter, alphabet


def get_embeddings(model, batch_converter, sequences: List[Tuple[str, str]],
                   layer: int = 33) -> Dict[str, np.ndarray]:
    """Get ESM-2 embeddings for sequences."""
    embeddings = {}

    # Process in batches
    batch_size = 8
    for i in range(0, len(sequences), batch_size):
        batch = sequences[i:i+batch_size]

        batch_labels, batch_strs, batch_tokens = batch_converter(batch)
        batch_tokens = batch_tokens.to(next(model.parameters()).device)

        with torch.no_grad():
            results = model(batch_tokens, repr_layers=[layer], return_contacts=False)

        token_representations = results["representations"][layer]

        # Mean pool over sequence length (excluding special tokens)
        for j, (label, seq) in enumerate(batch):
            # Get embeddings for actual sequence (not special tokens)
            seq_len = len(seq)
            seq_repr = token_representations[j, 1:seq_len+1].mean(0)
            embeddings[label] = seq_repr.cpu().numpy()

    return embeddings


def cluster_embeddings(embeddings: Dict[str, np.ndarray], n_clusters: int = 10) -> Dict[str, int]:
    """Cluster peptides by embedding similarity."""
    labels = list(embeddings.keys())
    X = np.array([embeddings[l] for l in labels])

    # PCA for dimensionality reduction
    pca = PCA(n_components=min(50, X.shape[0], X.shape[1]))
    X_pca = pca.fit_transform(X)

    # K-means clustering
    n_clusters = min(n_clusters, len(labels))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_pca)

    return {label: int(cl) for label, cl in zip(labels, cluster_labels)}, kmeans, X_pca


def find_nearest_neighbors(embeddings: Dict[str, np.ndarray], k: int = 5) -> Dict[str, List[str]]:
    """Find k nearest neighbors for each peptide."""
    labels = list(embeddings.keys())
    X = np.array([embeddings[l] for l in labels])

    # Cosine similarity matrix
    sim_matrix = cosine_similarity(X)

    neighbors = {}
    for i, label in enumerate(labels):
        # Get indices of top k+1 similar (excluding self)
        sim_scores = sim_matrix[i]
        top_indices = np.argsort(sim_scores)[::-1][1:k+1]
        neighbors[label] = [labels[j] for j in top_indices]

    return neighbors


def calculate_novelty_scores(embeddings: Dict[str, np.ndarray],
                             cluster_labels: Dict[str, int],
                             kmeans, X_pca) -> Dict[str, float]:
    """Calculate novelty score (distance from cluster center)."""
    labels = list(embeddings.keys())

    novelty = {}
    for i, label in enumerate(labels):
        cluster = cluster_labels[label]
        center = kmeans.cluster_centers_[cluster]
        dist = np.linalg.norm(X_pca[i] - center)
        novelty[label] = float(dist)

    # Normalize to 0-1
    max_dist = max(novelty.values())
    if max_dist > 0:
        novelty = {k: v/max_dist for k, v in novelty.items()}

    return novelty


def load_sequences_from_fastas(base_dir: Path) -> List[Tuple[str, str]]:
    """Load all peptide sequences from FASTA files."""
    sequences = []

    fasta_files = list(base_dir.glob("**/*.fasta"))

    for fasta_path in fasta_files:
        if "peptide" in fasta_path.name.lower() or "binder" in fasta_path.name.lower():
            current_id = None
            current_seq = []

            with open(fasta_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(">"):
                        if current_id and current_seq:
                            seq = "".join(current_seq)
                            if len(seq) <= 100:  # ESM-2 works best on shorter sequences
                                sequences.append((current_id, seq))
                        current_id = line[1:].split("|")[0]
                        current_seq = []
                    else:
                        current_seq.append(line)

                if current_id and current_seq:
                    seq = "".join(current_seq)
                    if len(seq) <= 100:
                        sequences.append((current_id, seq))

    return sequences


def run_esm2_analysis():
    """Run ESM-2 embedding analysis on all peptides."""
    print("=" * 70)
    print("M4 ESM-2 EMBEDDING ANALYSIS")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Device: {DEVICE}")
    print()

    # Load sequences
    base_dir = Path(__file__).parent.parent
    sequences = load_sequences_from_fastas(base_dir)
    print(f"Loaded {len(sequences)} peptide sequences")

    if not sequences:
        print("No sequences found!")
        return None

    # Limit for initial analysis
    max_sequences = 200
    if len(sequences) > max_sequences:
        print(f"Limiting to first {max_sequences} sequences for analysis")
        sequences = sequences[:max_sequences]

    # Load model
    model, batch_converter, alphabet = load_esm2_model()

    # Get embeddings
    print("\nGenerating embeddings...")
    embeddings = get_embeddings(model, batch_converter, sequences)
    print(f"Generated {len(embeddings)} embeddings")

    # Get embedding dimension
    embed_dim = list(embeddings.values())[0].shape[0]
    print(f"Embedding dimension: {embed_dim}")

    # Cluster
    print("\nClustering peptides...")
    n_clusters = min(15, len(embeddings) // 5)
    cluster_labels, kmeans, X_pca = cluster_embeddings(embeddings, n_clusters)

    # Count per cluster
    cluster_counts = {}
    for cl in cluster_labels.values():
        cluster_counts[cl] = cluster_counts.get(cl, 0) + 1
    print(f"Clusters: {len(set(cluster_labels.values()))}")
    for cl, count in sorted(cluster_counts.items()):
        print(f"  Cluster {cl}: {count} peptides")

    # Find neighbors
    print("\nFinding nearest neighbors...")
    neighbors = find_nearest_neighbors(embeddings, k=3)

    # Calculate novelty
    print("\nCalculating novelty scores...")
    novelty_scores = calculate_novelty_scores(embeddings, cluster_labels, kmeans, X_pca)

    # Create results
    results = []
    for pep_id, seq in sequences:
        if pep_id in embeddings:
            result = PeptideEmbedding(
                peptide_id=pep_id,
                sequence=seq,
                length=len(seq),
                embedding_dim=embed_dim,
                mean_embedding=embeddings[pep_id][:10].tolist(),  # First 10 dims
                cluster_id=cluster_labels.get(pep_id),
                nearest_neighbors=neighbors.get(pep_id, []),
                novelty_score=round(novelty_scores.get(pep_id, 0), 4),
                sha256=hashlib.sha256(seq.encode()).hexdigest()[:16],
            )
            results.append(result)

    # Find most novel peptides
    print("\nMOST NOVEL PEPTIDES (highest novelty scores):")
    sorted_by_novelty = sorted(results, key=lambda x: x.novelty_score, reverse=True)
    for r in sorted_by_novelty[:10]:
        print(f"  {r.peptide_id}: {r.sequence[:20]}... novelty={r.novelty_score:.3f}")

    # Save results
    output_dir = Path(__file__).parent / "esm2_analysis"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output = {
        "timestamp": datetime.now().isoformat(),
        "device": str(DEVICE),
        "total_peptides": len(results),
        "embedding_dim": embed_dim,
        "n_clusters": len(set(cluster_labels.values())),
        "cluster_distribution": cluster_counts,
        "most_novel": [asdict(r) for r in sorted_by_novelty[:20]],
        "all_results": [
            {
                "peptide_id": r.peptide_id,
                "sequence": r.sequence,
                "cluster_id": r.cluster_id,
                "novelty_score": r.novelty_score,
                "nearest_neighbors": r.nearest_neighbors,
            }
            for r in results
        ],
    }

    json_path = output_dir / f"esm2_embeddings_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved: {json_path}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total peptides analyzed: {len(results)}")
    print(f"Clusters identified: {len(set(cluster_labels.values()))}")
    print(f"Average novelty score: {np.mean(list(novelty_scores.values())):.3f}")
    print(f"Most novel peptide: {sorted_by_novelty[0].peptide_id} ({sorted_by_novelty[0].novelty_score:.3f})")

    return results


if __name__ == "__main__":
    run_esm2_analysis()
