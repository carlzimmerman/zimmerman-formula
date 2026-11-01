#!/usr/bin/env python3
"""Serialization-only wrapper retaining every failed static solve diagnostic."""
import json
import math
import resource
import sys
import static_response as experiment


class ExplicitNonfiniteJSON:
    @staticmethod
    def dumps(value, **kwargs):
        nonfinite = {}

        def clean(item, path):
            if isinstance(item, dict):
                return {key: clean(val, path + "." + str(key)) for key, val in item.items()}
            if isinstance(item, (list, tuple)):
                return [clean(val, path + "[" + str(index) + "]") for index, val in enumerate(item)]
            if isinstance(item, float) and not math.isfinite(item):
                nonfinite[path] = repr(item)
                return None
            return item

        result = clean(value, "$")
        if isinstance(result, dict) and result.get("claim_id") == "FR01_STATIC":
            result["nonfinite_diagnostics_replaced_by_null"] = nonfinite
            result["peak_rss_bytes_macos"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            result["serialization_amendment"] = "STATIC_AMENDMENT_A1.md"
        return json.dumps(result, **kwargs)


if __name__ == "__main__":
    experiment.json = ExplicitNonfiniteJSON
    sys.exit(experiment.main())
