"""
HELICONLAKE - Data Source Registry
==================================

Named after Mount Helicon, sacred mountain of the Muses where the springs
Hippocrene and Aganippe flowed as sources of inspiration and knowledge.

This lake stores validated data source URLs and metadata so HermesFlow can:
1. Query known sources before falling back to web search
2. Track URL health and mark dead links
3. Build institutional memory of where data lives

Usage:
    from OlympusFlow.lakes.helicon import HeliconLake, SourceEntry

    lake = HeliconLake()
    sources = lake.find_sources("cosmology", "dark energy")
    lake.register_source({...})
"""

from .lake import HeliconLake, SourceEntry

__version__ = "3.0.0"
__all__ = ["HeliconLake", "SourceEntry"]
