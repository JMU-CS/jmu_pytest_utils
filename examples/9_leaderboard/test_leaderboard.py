"""Example of using leaderboard functionality in tests."""

from jmu_pytest_utils.decorators import weight
import time


@weight(10)
def test_multiple_metrics():
    """Example of setting multiple leaderboard entries."""
    # Simulate some work
    time.sleep(0.1)
    
    # Add various metrics to the leaderboard
    test_multiple_metrics.leaderboard = [
        {"name": "Advanced Score", "value": 950},
        {"name": "Response Time", "value": 125, "order": "asc"},
        {"name": "Rating", "value": "★★★★☆"}
    ]

