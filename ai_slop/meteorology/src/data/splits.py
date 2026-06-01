"""
Data Splits for Weather Prediction

Following WeatherBench 2 standard splits for reproducibility and fair comparison.
"""

from datetime import datetime
from typing import Dict, Tuple

# WeatherBench 2 Standard Splits
# ==============================
# These are the canonical splits used by GraphCast, Pangu-Weather, etc.
# Using the same splits enables direct comparison with published results.

WEATHERBENCH_SPLITS = {
    'train': ('1979-01-01', '2017-12-31'),      # 39 years
    'validation': ('2018-01-01', '2019-12-31'),  # 2 years
    'test': ('2020-01-01', '2021-12-31'),        # 2 years
}

# Extended test set (for more recent evaluation)
EXTENDED_SPLITS = {
    'train': ('1979-01-01', '2018-12-31'),
    'validation': ('2019-01-01', '2020-12-31'),
    'test': ('2021-01-01', '2023-12-31'),
}

# Fast development splits (for debugging)
FAST_DEV_SPLITS = {
    'train': ('2015-01-01', '2017-12-31'),       # 3 years
    'validation': ('2018-01-01', '2018-12-31'),  # 1 year
    'test': ('2019-01-01', '2019-12-31'),        # 1 year
}

# Tiny splits (for unit tests)
TINY_SPLITS = {
    'train': ('2017-01-01', '2017-03-31'),
    'validation': ('2017-04-01', '2017-04-30'),
    'test': ('2017-05-01', '2017-05-31'),
}


def get_train_val_test_splits(
    split_config: str = 'weatherbench'
) -> Dict[str, Tuple[datetime, datetime]]:
    """
    Get datetime ranges for train/val/test splits.

    Args:
        split_config: One of 'weatherbench', 'extended', 'fast_dev', 'tiny'

    Returns:
        Dictionary mapping split names to (start, end) datetime tuples
    """
    configs = {
        'weatherbench': WEATHERBENCH_SPLITS,
        'extended': EXTENDED_SPLITS,
        'fast_dev': FAST_DEV_SPLITS,
        'tiny': TINY_SPLITS,
    }

    if split_config not in configs:
        raise ValueError(f"Unknown split config: {split_config}. Choose from: {list(configs.keys())}")

    splits = configs[split_config]

    return {
        name: (
            datetime.fromisoformat(start),
            datetime.fromisoformat(end)
        )
        for name, (start, end) in splits.items()
    }


def get_split_info(split_config: str = 'weatherbench') -> str:
    """Return human-readable description of splits."""
    splits = get_train_val_test_splits(split_config)

    lines = [f"Data splits ({split_config}):", "-" * 40]
    for name, (start, end) in splits.items():
        duration = (end - start).days / 365.25
        lines.append(f"  {name:12s}: {start.date()} to {end.date()} ({duration:.1f} years)")

    return "\n".join(lines)
