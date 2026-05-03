#!/usr/bin/env python3
"""
TruthFlow Fetcher - arXiv and NASA ADS Integration
===================================================
Fetches relevant papers for Z² validation.

Author: Carl Zimmerman
Date: May 2, 2026
"""

import requests
import feedparser
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
import time
import urllib.parse

# ============================================================================
# CONFIGURATION
# ============================================================================

ARXIV_API = "http://export.arxiv.org/api/query"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "fetched_papers")

# Search categories relevant to Z²
CATEGORIES = [
    "hep-th",    # High Energy Physics - Theory
    "hep-ph",    # High Energy Physics - Phenomenology
    "gr-qc",     # General Relativity and Quantum Cosmology
    "astro-ph.CO",  # Cosmology and Nongalactic Astrophysics
    "astro-ph.GA",  # Astrophysics of Galaxies (MOND)
]

# Keywords for Z² validation targets
KEYWORDS = {
    "cosmology": [
        "dark energy", "cosmological constant", "Hubble tension",
        "Omega_Lambda", "dark matter", "MOND", "modified gravity"
    ],
    "particle_physics": [
        "fine structure constant", "weak mixing angle", "Weinberg angle",
        "electroweak", "Higgs mass", "hierarchy problem", "naturalness"
    ],
    "quantum_gravity": [
        "spectral dimension", "dimensional reduction", "holographic",
        "Bekenstein bound", "tensor-to-scalar ratio", "primordial gravitational"
    ],
    "measurements": [
        "precision measurement", "CODATA", "PDG", "Planck 2018",
        "galaxy rotation", "SPARC", "MOND fit"
    ]
}


@dataclass
class Paper:
    """Represents an arXiv paper."""
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    categories: List[str]
    published: str
    updated: str
    pdf_url: str
    relevance_keywords: List[str]


# ============================================================================
# FETCHING FUNCTIONS
# ============================================================================

def search_arxiv(query: str, max_results: int = 50,
                 start: int = 0, sort_by: str = "relevance") -> List[Paper]:
    """
    Search arXiv for papers matching query.

    Args:
        query: Search query (can use AND, OR, NOT)
        max_results: Maximum papers to return
        start: Start index for pagination
        sort_by: 'relevance', 'lastUpdatedDate', or 'submittedDate'

    Returns: List of Paper objects
    """
    # Build URL manually with proper encoding
    encoded_query = urllib.parse.quote(query)
    url = f"{ARXIV_API}?search_query={encoded_query}&start={start}&max_results={max_results}&sortBy={sort_by}&sortOrder=descending"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Error fetching from arXiv: {e}")
        return []

    feed = feedparser.parse(response.content)

    # Debug: check if we got results
    if not feed.entries:
        print(f"  No entries found. Feed status: {feed.get('status', 'unknown')}")

    papers = []
    for entry in feed.entries:
        # Extract arXiv ID
        arxiv_id = entry.id.split("/abs/")[-1]

        # Find which keywords matched
        text = (entry.title + " " + entry.summary).lower()
        matched_keywords = []
        for category, kws in KEYWORDS.items():
            for kw in kws:
                if kw.lower() in text:
                    matched_keywords.append(kw)

        paper = Paper(
            arxiv_id=arxiv_id,
            title=entry.title.replace("\n", " "),
            authors=[a.name for a in entry.authors],
            abstract=entry.summary.replace("\n", " "),
            categories=[t.term for t in entry.tags],
            published=entry.published,
            updated=entry.updated,
            pdf_url=entry.id.replace("/abs/", "/pdf/") + ".pdf",
            relevance_keywords=matched_keywords
        )
        papers.append(paper)

    return papers


def search_for_z2_validation() -> dict:
    """
    Run all searches relevant to Z² validation.

    Returns: Dict mapping category to list of papers
    """
    results = {}

    # Search for each topic
    # Simplified queries for better arXiv API compatibility
    queries = [
        ("dark_energy", 'cat:astro-ph.CO AND abs:dark+energy'),
        ("mond", 'abs:MOND OR abs:modified+Newtonian'),
        ("fine_structure", 'abs:fine+structure+constant'),
        ("weak_mixing", 'abs:weak+mixing+angle OR abs:Weinberg+angle'),
        ("hierarchy", 'abs:hierarchy+problem'),
        ("spectral_dimension", 'abs:spectral+dimension'),
        ("tensor_scalar", 'abs:tensor+scalar+ratio'),
        ("holographic", 'cat:hep-th AND abs:holographic'),
    ]

    for name, query in queries:
        print(f"Searching for: {name}...")
        papers = search_arxiv(query, max_results=20)
        results[name] = papers
        time.sleep(3)  # Be nice to arXiv

    return results


def save_results(results: dict, output_dir: str = OUTPUT_DIR):
    """Save fetched papers to JSON files."""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for category, papers in results.items():
        filename = f"{category}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)

        data = {
            "category": category,
            "timestamp": timestamp,
            "count": len(papers),
            "papers": [asdict(p) for p in papers]
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Saved {len(papers)} papers to {filename}")


# ============================================================================
# SPECIFIC FETCHERS FOR Z² PREDICTIONS
# ============================================================================

def fetch_omega_lambda_measurements() -> List[Paper]:
    """Fetch latest Ω_Λ measurements for Z² = 13/19 validation."""
    query = 'all:"Omega_Lambda" OR (all:"dark energy" AND all:"Planck")'
    return search_arxiv(query, max_results=30, sort_by="submittedDate")


def fetch_alpha_measurements() -> List[Paper]:
    """Fetch α measurements for Z² = 4Z²+3 validation."""
    query = 'all:"fine structure constant" AND (all:measurement OR all:precision)'
    return search_arxiv(query, max_results=30, sort_by="submittedDate")


def fetch_mond_data() -> List[Paper]:
    """Fetch MOND/galaxy rotation data for μ(x) = x/(1+x) validation."""
    query = 'all:MOND OR all:"SPARC" OR (all:"rotation curve" AND all:galaxy)'
    return search_arxiv(query, max_results=30, sort_by="submittedDate")


def fetch_tensor_scalar_predictions() -> List[Paper]:
    """Fetch r predictions for Z² = 0.015 validation (future test)."""
    query = 'all:"tensor-to-scalar ratio" AND (all:prediction OR all:LiteBIRD OR all:CMB)'
    return search_arxiv(query, max_results=30, sort_by="submittedDate")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("TRUTHFLOW FETCHER - arXiv Search")
    print("=" * 60)
    print()

    # Run comprehensive search
    results = search_for_z2_validation()

    # Save results
    save_results(results)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total = sum(len(papers) for papers in results.values())
    print(f"Total papers fetched: {total}")
    for category, papers in results.items():
        print(f"  {category}: {len(papers)} papers")

    print("\nPapers saved to: TruthFlow/fetched_papers/")
    print("Next step: Run 02_parser to extract empirical data")
