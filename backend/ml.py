from typing import List, Dict, Tuple
import math

try:
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except Exception:
    # Fallback stub if sklearn isn't available; clusters everything into one group
    KMeans = None
    SKLEARN_AVAILABLE = False


# Minimal sample attractions data structure (could be loaded from CSV/API)
SAMPLE_ATTRACTIONS: List[Dict] = [
    {"name": "City Museum", "lat": 28.6139, "lng": 77.2090, "est_fee": 150, "duration_hours": 2.0, "category": "museum"},
    {"name": "Heritage Fort", "lat": 28.6562, "lng": 77.2410, "est_fee": 250, "duration_hours": 2.5, "category": "heritage"},
    {"name": "Central Park", "lat": 28.6270, "lng": 77.2150, "est_fee": 0,   "duration_hours": 1.5, "category": "park"},
    {"name": "Riverfront Walk", "lat": 28.6000, "lng": 77.2000, "est_fee": 0,   "duration_hours": 1.0, "category": "walk"},
    {"name": "Art Gallery", "lat": 28.6200, "lng": 77.2300, "est_fee": 100, "duration_hours": 1.5, "category": "art"},
    {"name": "Science Center", "lat": 28.5900, "lng": 77.1700, "est_fee": 200, "duration_hours": 2.0, "category": "science"},
]


PLACEHOLDER_ACTIVITY_POOL: List[Dict] = [
    {
        "name": "Morning heritage walk & photo stops",
        "duration_hours": 1.5,
        "est_fee": 0.0,
        "category": "sightseeing",
    },
    {
        "name": "Local market stroll for souvenirs",
        "duration_hours": 1.0,
        "est_fee": 0.0,
        "category": "shopping",
    },
    {
        "name": "Sunset viewpoint and café break",
        "duration_hours": 1.5,
        "est_fee": 200.0,
        "category": "relaxation",
    },
    {
        "name": "Evening promenade & street food tasting",
        "duration_hours": 1.5,
        "est_fee": 150.0,
        "category": "food",
    },
]


def cluster_attractions_by_location(num_days: int, attractions: List[Dict] | None = None) -> List[List[Dict]]:
    # Handle empty or None attractions
    if attractions is None or (isinstance(attractions, list) and len(attractions) == 0):
        # Return empty clusters - caller should handle this
        return [[] for _ in range(num_days)]
    
    data = attractions
    
    # Ensure k is valid
    k = min(num_days, len(data))
    
    if k <= 1 or not SKLEARN_AVAILABLE:
        # simple chunking fallback - distribute evenly across days
        if not data:
            return [[] for _ in range(num_days)]
        # If only 1 day or 1 attraction, put all in first day
        if k == 1:
            result = [data] + [[] for _ in range(num_days - 1)]
            return result[:num_days]
        return [data] if data else [[] for _ in range(num_days)]

    X = [[a["lat"], a["lng"]] for a in data]
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = kmeans.fit_predict(X)

    clusters: List[List[Dict]] = [[] for _ in range(k)]
    for a, label in zip(data, labels):
        clusters[label].append(a)
    
    # Ensure non-empty per day by merging empties if necessary
    non_empty = [c for c in clusters if c]
    return non_empty if non_empty else [data]


def select_daily_attractions(
    clusters: List[List[Dict]],
    activities_budget_total: float,
    num_days: int,
    max_hours_per_day: float = 6.0,
) -> Tuple[List[List[Dict]], float]:
    """0/1 knapsack by fee (cost) with a time guard; falls back to greedy if needed."""
    
    # Flatten all clusters to get all attractions
    all_attractions = []
    for cluster in clusters:
        all_attractions.extend(cluster)
    
    # If we have fewer clusters than days, redistribute all attractions evenly across all days
    # This ensures every day gets some activities
    if len(clusters) < num_days:
        # Redistribute evenly across num_days using round-robin
        clusters = [[] for _ in range(num_days)]
        for i, attraction in enumerate(all_attractions):
            clusters[i % num_days].append(attraction)
    else:
        # Ensure we have exactly num_days clusters (pad with empty lists if needed)
        while len(clusters) < num_days:
            clusters.append([])
        # Trim to exactly num_days if we somehow have more
        clusters = clusters[:num_days]
    
    per_day_budget = activities_budget_total / num_days

    all_days: List[List[Dict]] = []
    total_fees = 0.0
    placeholder_cursor = 0
    
    for day_cluster in clusters:
        items = day_cluster
        B = int(max(0, per_day_budget))
        n = len(items)
        
        if n == 0 or B <= 0:
            day_picks = []
            # Fill day with placeholders to meet minimum count
            while len(day_picks) < 3:
                placeholder = PLACEHOLDER_ACTIVITY_POOL[placeholder_cursor % len(PLACEHOLDER_ACTIVITY_POOL)].copy()
                placeholder_cursor += 1
                day_picks.append(placeholder)
            day_picks = day_picks[:4]
            all_days.append(day_picks)
            total_fees += sum(float(a.get("est_fee", 0) or 0) for a in day_picks)
            continue
            
        # value and weight arrays
        values = [1.0 / max(0.5, float(it.get("duration_hours", 1.0))) for it in items]
        costs = [int(max(0, float(it.get("est_fee", 0)))) for it in items]
        durations = [float(it.get("duration_hours", 1.0)) for it in items]

        dp = [[0.0] * (B + 1) for _ in range(n + 1)]
        keep = [[False] * (B + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            v = values[i - 1]
            w = costs[i - 1]
            for b in range(B + 1):
                dp[i][b] = dp[i - 1][b]
                if w <= b and dp[i - 1][b - w] + v > dp[i][b]:
                    dp[i][b] = dp[i - 1][b - w] + v
                    keep[i][b] = True

        # backtrack to get selected indices
        b = B
        chosen_idx = []
        for i in range(n, 0, -1):
            if keep[i][b]:
                chosen_idx.append(i - 1)
                b -= costs[i - 1]
        chosen_idx.reverse()

        # Prune if time exceeds daily cap by dropping longest first
        day_picks = [items[i] for i in chosen_idx]
        hours_sum = sum(durations[i] for i in chosen_idx)
        fee_sum = sum(costs[i] for i in chosen_idx)
        
        if hours_sum > max_hours_per_day:
            day_picks.sort(key=lambda x: x.get("duration_hours", 1.0), reverse=True)
            while day_picks and hours_sum > max_hours_per_day:
                removed = day_picks.pop(0)
                hours_sum -= float(removed.get("duration_hours", 1.0))
                fee_sum -= int(max(0, float(removed.get("est_fee", 0))))
        
        # Fallback: if knapsack failed or budget was 0, use greedy
        if not day_picks:
            candidates = sorted(items, key=lambda x: (x.get("est_fee", 0), x.get("duration_hours", 1.0)))
            day_picks = []
            fee_sum = 0.0
            hours_sum = 0.0
            for a in candidates:
                fee = float(a.get("est_fee", 0) or 0)
                dur = float(a.get("duration_hours", 1.0) or 1.0)
                if fee_sum + fee <= per_day_budget and hours_sum + dur <= max_hours_per_day:
                    day_picks.append(a)
                    fee_sum += fee
                    hours_sum += dur

        # Top up selections to guarantee at least three attractions per day.
        chosen_set = set(chosen_idx)
        remaining_candidates = [
            items[i] for i in range(n) if i not in chosen_set and items[i] not in day_picks
        ]
        remaining_candidates.sort(key=lambda x: (x.get("est_fee", 0), x.get("duration_hours", 1.0)))

        for candidate in remaining_candidates:
            if len(day_picks) >= 4:
                break
            fee = float(candidate.get("est_fee", 0) or 0)
            dur = float(candidate.get("duration_hours", 1.0) or 1.0)

            if len(day_picks) < 3:
                day_picks.append(candidate)
                fee_sum += fee
                hours_sum += dur
            else:
                if hours_sum + dur <= max_hours_per_day * 1.15 and fee_sum + fee <= per_day_budget * 1.25:
                    day_picks.append(candidate)
                    fee_sum += fee
                    hours_sum += dur

        # Fill with placeholders if we still have fewer than three activities.
        while len(day_picks) < 3:
            placeholder = PLACEHOLDER_ACTIVITY_POOL[placeholder_cursor % len(PLACEHOLDER_ACTIVITY_POOL)].copy()
            placeholder_cursor += 1
            day_picks.append(placeholder)

        # Cap the day at four activities and recalculate aggregates for consistency.
        if len(day_picks) > 4:
            day_picks = day_picks[:4]
        fee_sum = sum(float(a.get("est_fee", 0) or 0) for a in day_picks)
        hours_sum = sum(float(a.get("duration_hours", 1.0) or 1.0) for a in day_picks)
                    
        all_days.append(day_picks)
        total_fees += fee_sum
        
    return all_days, total_fees