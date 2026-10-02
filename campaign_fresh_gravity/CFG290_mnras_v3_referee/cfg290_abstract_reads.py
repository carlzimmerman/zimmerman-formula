#!/usr/bin/env python3
"""cfg290_abstract_reads.py -- CFG290 referee: print the arXiv abstracts (API, Atom; arXiv metadata is CC0; printed to stdout, kept as the .out) of the papers whose content
the manuscript characterises, so each characterisation can be compared with the authors' own words.  Abstract-level only."""
import urllib.request, xml.etree.ElementTree as ET, time
IDS = {"Milgrom1999": "astro-ph/9805346", "Milgrom2020": "2001.09729", "Limbach2008": "0809.2790", "OppenheimRusso2024": "2402.19459",
       "HertzbergLoeb2024": "2404.13037", "Mayer2023": "2206.04333", "Jeanneau2026": "2603.28856", "Ciocan2026": "2604.22613",
       "Varasteanu2026": "2608.03576", "Milgrom2017": "1703.06110", "Ubler2017": "1703.04321", "Desmond2023": "2303.11314",
       "Hirtenstein2019": "1811.11768", "NestorShachar2023": "2209.12199", "Puglisi2023": "2305.04382", "Varasteanu2025": "2504.20857"}
ns = {"a": "http://www.w3.org/2005/Atom"}
for k, aid in IDS.items():
    x = ET.fromstring(urllib.request.urlopen(urllib.request.Request("http://export.arxiv.org/api/query?id_list=" + aid,
                      headers={"User-Agent": "cfg290-referee"}), timeout=30).read())
    e = x.find("a:entry", ns)
    print(f"=== {k} ({aid}) v-latest: {e.findtext('a:id', '', ns)}\n  {' '.join(e.findtext('a:title', '', ns).split())}\n  {' '.join(e.findtext('a:summary', '', ns).split())}\n", flush=True)
    time.sleep(3)
