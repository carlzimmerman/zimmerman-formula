#!/usr/bin/env python3
"""
HeliconLake - Data Source Registry for HermesFlow
==================================================

Named after Mount Helicon, sacred mountain of the Muses where the springs
Hippocrene and Aganippe flowed as sources of inspiration and knowledge.

This lake stores validated data source URLs and metadata so HermesFlow can:
1. Query known sources before falling back to web search
2. Track URL health and mark dead links
3. Build institutional memory of where data lives

Author: Carl Zimmerman
Date: May 5, 2026
Version: 1.0.0
"""

import json
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class SourceEntry:
    """A data source entry in HeliconLake."""
    id: str
    url: str
    description: str
    domains: List[str]
    topics: List[str]
    landing_page: bool = True
    data_urls: List[str] = field(default_factory=list)
    quantities: List[str] = field(default_factory=list)
    format: str = "unknown"
    organization: str = ""
    authority_score: float = 0.5
    last_validated: str = ""
    validation_status: str = "unknown"  # active, dead, unknown
    discovered_by: str = "manual"
    discovery_method: str = "manual"
    notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'SourceEntry':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class HeliconLake:
    """
    Data source registry for HermesFlow discovery.

    Stores URLs, descriptions, and metadata for known data sources
    to accelerate discovery and provide fallback when URLs change.
    """

    def __init__(self, lake_path: Optional[Path] = None):
        """Initialize HeliconLake.

        Args:
            lake_path: Path to HeliconLake directory. Defaults to project root.
        """
        if lake_path is None:
            # Data files are now co-located with this module
            lake_path = Path(__file__).parent

        self.lake_path = lake_path
        self.registry_path = lake_path / "registry.json"
        self.index_path = lake_path / "domain_index.json"
        self.validation_log_path = lake_path / "validation_log.json"

        # Ensure directory exists
        self.lake_path.mkdir(parents=True, exist_ok=True)

        # Load data
        self._load()

    def _load(self):
        """Load registry and index from disk."""
        # Load registry
        if self.registry_path.exists():
            with open(self.registry_path) as f:
                data = json.load(f)
                self.sources = {s['id']: SourceEntry.from_dict(s) for s in data.get('sources', [])}
                self.version = data.get('version', '1.0.0')
        else:
            self.sources = {}
            self.version = '1.0.0'

        # Load domain index
        if self.index_path.exists():
            with open(self.index_path) as f:
                data = json.load(f)
                self.domain_index = data.get('domains', {})
        else:
            self.domain_index = {}

    def _save(self):
        """Save registry and index to disk."""
        # Save registry
        registry_data = {
            'version': self.version,
            'description': 'HeliconLake - Data source registry for HermesFlow discovery',
            'last_updated': datetime.now().isoformat(),
            'sources': [s.to_dict() for s in self.sources.values()]
        }
        with open(self.registry_path, 'w') as f:
            json.dump(registry_data, f, indent=2)

        # Save domain index
        index_data = {
            'version': self.version,
            'description': 'Domain to source ID mappings for HeliconLake',
            'last_updated': datetime.now().isoformat(),
            'domains': self.domain_index
        }
        with open(self.index_path, 'w') as f:
            json.dump(index_data, f, indent=2)

    def _generate_id(self, url: str, domain: str) -> str:
        """Generate a unique ID for a source."""
        # Extract organization from URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        org = parsed.netloc.replace('www.', '').split('.')[0]

        # Create hash of URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:6]

        return f"{org}-{domain}-{url_hash}"

    def find_sources(self, domain: str, topic: str = None) -> List[SourceEntry]:
        """Find sources matching domain and optionally topic.

        Args:
            domain: Domain to search (e.g., 'meteorology', 'seismology')
            topic: Optional topic filter (e.g., 'hurricane', 'earthquake')

        Returns:
            List of matching SourceEntry objects
        """
        results = []

        # Search by domain
        for source in self.sources.values():
            if domain.lower() in [d.lower() for d in source.domains]:
                # If topic specified, check topics
                if topic:
                    topic_lower = topic.lower()
                    if any(topic_lower in t.lower() for t in source.topics):
                        results.append(source)
                else:
                    results.append(source)

        # Sort by authority score (highest first)
        results.sort(key=lambda s: s.authority_score, reverse=True)

        # Filter out dead sources
        results = [s for s in results if s.validation_status != 'dead']

        return results

    def register_source(self, source_data: Dict) -> str:
        """Register a new data source.

        Args:
            source_data: Dictionary with source information.
                Required: url, domains (list)
                Optional: topics, description, format, organization, etc.

        Returns:
            Source ID
        """
        url = source_data.get('url', '')
        domains = source_data.get('domains', [])

        if not url or not domains:
            raise ValueError("url and domains are required")

        # Generate ID if not provided
        source_id = source_data.get('id') or self._generate_id(url, domains[0])

        # Create entry
        entry = SourceEntry(
            id=source_id,
            url=url,
            description=source_data.get('description', ''),
            domains=domains,
            topics=source_data.get('topics', []),
            landing_page=source_data.get('landing_page', True),
            data_urls=source_data.get('data_urls', []),
            quantities=source_data.get('quantities', []),
            format=source_data.get('format', 'unknown'),
            organization=source_data.get('organization', ''),
            authority_score=source_data.get('authority_score', 0.5),
            last_validated=datetime.now().isoformat(),
            validation_status='unknown',
            discovered_by=source_data.get('discovered_by', 'HermesFlow'),
            discovery_method=source_data.get('discovery_method', 'web_search'),
            notes=source_data.get('notes', '')
        )

        # Add to registry
        self.sources[source_id] = entry

        # Update domain index
        for domain in domains:
            if domain not in self.domain_index:
                self.domain_index[domain] = {}

            for topic in entry.topics:
                if topic not in self.domain_index[domain]:
                    self.domain_index[domain][topic] = []
                if source_id not in self.domain_index[domain][topic]:
                    self.domain_index[domain][topic].append(source_id)

        # Save to disk
        self._save()

        return source_id

    def validate_source(self, source_id: str, timeout: int = 10) -> bool:
        """Validate that a source URL is still accessible.

        Args:
            source_id: Source ID to validate
            timeout: Request timeout in seconds

        Returns:
            True if URL is accessible, False otherwise
        """
        if source_id not in self.sources:
            return False

        source = self.sources[source_id]

        try:
            request = urllib.request.Request(
                source.url,
                headers={'User-Agent': 'HermesFlow/1.0 (Scientific Research)'}
            )
            response = urllib.request.urlopen(request, timeout=timeout)
            status_code = response.getcode()

            if status_code == 200:
                source.validation_status = 'active'
                source.last_validated = datetime.now().isoformat()
                self._save()
                self._log_validation(source_id, True, status_code)
                return True
            else:
                self._log_validation(source_id, False, status_code)
                return False

        except urllib.error.HTTPError as e:
            if e.code == 404:
                source.validation_status = 'dead'
                source.last_validated = datetime.now().isoformat()
                self._save()
            self._log_validation(source_id, False, e.code)
            return False

        except Exception as e:
            self._log_validation(source_id, False, str(e))
            return False

    def mark_dead(self, source_id: str):
        """Mark a source as dead (URL no longer works).

        Args:
            source_id: Source ID to mark as dead
        """
        if source_id in self.sources:
            self.sources[source_id].validation_status = 'dead'
            self.sources[source_id].last_validated = datetime.now().isoformat()
            self._save()
            self._log_validation(source_id, False, "marked_dead")

    def _log_validation(self, source_id: str, success: bool, detail: Any):
        """Log a validation attempt."""
        try:
            if self.validation_log_path.exists():
                with open(self.validation_log_path) as f:
                    log_data = json.load(f)
            else:
                log_data = {'version': '1.0.0', 'validations': []}

            log_data['validations'].append({
                'source_id': source_id,
                'timestamp': datetime.now().isoformat(),
                'success': success,
                'detail': str(detail)
            })

            # Keep last 1000 validations
            log_data['validations'] = log_data['validations'][-1000:]

            with open(self.validation_log_path, 'w') as f:
                json.dump(log_data, f, indent=2)

        except Exception:
            pass  # Don't fail on logging errors

    def validate_all(self, max_sources: int = 50) -> Dict[str, bool]:
        """Validate all sources (or up to max_sources).

        Args:
            max_sources: Maximum number of sources to validate

        Returns:
            Dictionary mapping source_id to validation result
        """
        results = {}
        count = 0

        for source_id in list(self.sources.keys()):
            if count >= max_sources:
                break
            results[source_id] = self.validate_source(source_id)
            count += 1

        return results

    def get_statistics(self) -> Dict:
        """Get lake statistics."""
        total = len(self.sources)
        active = sum(1 for s in self.sources.values() if s.validation_status == 'active')
        dead = sum(1 for s in self.sources.values() if s.validation_status == 'dead')
        unknown = sum(1 for s in self.sources.values() if s.validation_status == 'unknown')

        domains = set()
        topics = set()
        for s in self.sources.values():
            domains.update(s.domains)
            topics.update(s.topics)

        return {
            'total_sources': total,
            'active': active,
            'dead': dead,
            'unknown': unknown,
            'domains_covered': len(domains),
            'topics_covered': len(topics),
            'domains': list(domains),
            'last_updated': datetime.now().isoformat()
        }

    def search_web_for_sources(self, domain: str, topic: str) -> List[Dict]:
        """Search the web for new data sources (fallback when lake is empty).

        This uses DuckDuckGo HTML search (no API key required).

        Args:
            domain: Domain to search (e.g., 'meteorology')
            topic: Topic to search (e.g., 'hurricane')

        Returns:
            List of potential source dictionaries
        """
        query = f"{domain} {topic} data download CSV API .gov OR .edu"

        try:
            # Use DuckDuckGo HTML search
            encoded_query = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

            request = urllib.request.Request(
                url,
                headers={'User-Agent': 'HermesFlow/1.0 (Scientific Research)'}
            )
            response = urllib.request.urlopen(request, timeout=15)
            html = response.read().decode('utf-8', errors='ignore')

            # Extract URLs from results
            import re
            results = []

            # Find result links
            link_pattern = r'href="([^"]*)"'
            for match in re.finditer(link_pattern, html):
                href = match.group(1)
                if 'duckduckgo.com/l/' in href:
                    # Extract actual URL from DDG redirect
                    url_match = re.search(r'uddg=([^&]+)', href)
                    if url_match:
                        actual_url = urllib.parse.unquote(url_match.group(1))
                        if any(tld in actual_url for tld in ['.gov', '.edu', '.org']):
                            results.append({
                                'url': actual_url,
                                'domains': [domain],
                                'topics': [topic],
                                'discovery_method': 'web_search',
                                'discovered_by': 'HeliconLake'
                            })

            # Deduplicate
            seen = set()
            unique = []
            for r in results:
                if r['url'] not in seen:
                    seen.add(r['url'])
                    unique.append(r)

            return unique[:10]  # Return top 10

        except Exception as e:
            print(f"Web search failed: {e}")
            return []


# Convenience functions
def get_lake(lake_path: Optional[Path] = None) -> HeliconLake:
    """Get HeliconLake instance."""
    return HeliconLake(lake_path)


def find_sources(domain: str, topic: str = None) -> List[SourceEntry]:
    """Find sources from HeliconLake."""
    lake = get_lake()
    return lake.find_sources(domain, topic)


def register_source(source_data: Dict) -> str:
    """Register a new source in HeliconLake."""
    lake = get_lake()
    return lake.register_source(source_data)


# Test code
if __name__ == "__main__":
    print("HeliconLake - Data Source Registry")
    print("=" * 50)

    lake = HeliconLake()
    stats = lake.get_statistics()

    print(f"\nStatistics:")
    print(f"  Total sources: {stats['total_sources']}")
    print(f"  Active: {stats['active']}")
    print(f"  Dead: {stats['dead']}")
    print(f"  Unknown: {stats['unknown']}")
    print(f"  Domains: {stats['domains_covered']}")

    # Test web search
    print("\nTesting web search for hurricane data...")
    results = lake.search_web_for_sources("meteorology", "hurricane")
    print(f"Found {len(results)} potential sources:")
    for r in results[:5]:
        print(f"  - {r['url'][:60]}...")
