# Debug Guide: Place Names Not Loading

## Quick Diagnostic Steps

### 1. Check Backend Console Output

When you generate an itinerary, look for these log messages in your backend terminal:

**Expected logs for a working destination (e.g., "Goa"):**
```
[Debug] Looking up destination: 'Goa'
[Debug] Catalog lookup result: True
[Debug] Found catalog entry for Goa
Catalog center for Goa: (15.2993, 74.1240)
[Info] Found catalog data for Goa
[Info] Found 5 attractions from catalog: ['Baga Beach', 'Calangute Beach', 'Basilica of Bom Jesus (Old Goa)']
[Info] Mapped 5 attractions for ML processing: ['Baga Beach', 'Calangute Beach', 'Basilica of Bom Jesus (Old Goa)']
[Info] Created 3 clusters from 5 attractions
[Info] Selected 5 activities across 3 days
  Day 1: ['Baga Beach', 'Calangute Beach']
  Day 2: ['Basilica of Bom Jesus (Old Goa)']
  Day 3: ['Dudhsagar Falls', 'Fort Aguada']
```

**If you see this instead:**
```
[Debug] Looking up destination: 'YourDestination'
[Debug] Catalog lookup result: False
[Debug] No catalog entry found for 'YourDestination'
[Warning] No attractions found from catalog or API. Itinerary will have generic activities.
[Warning] No attractions available for YourDestination. Creating fallback activities.
```

This means the destination is not in the catalog.

### 2. Test with Known Catalog Destinations

Try these destinations (they should work):
- **Goa** - Should show: Baga Beach, Calangute Beach, Basilica of Bom Jesus, Dudhsagar Falls, Fort Aguada
- **Kerala** - Should show: Alleppey Backwaters, Munnar Tea Gardens, Fort Kochi, Wayanad Wildlife, Kovalam Beach
- **Karnataka** - Should show: Mysore Palace, Hampi Ruins, Coorg Plantations, Gokarna Beaches, Bengaluru City Highlights

### 3. Check Catalog File

Verify the catalog file exists and has data:
- File: `backend/static_catalog.json`
- Should contain entries for Goa, Kerala, and Karnataka

### 4. Common Issues and Solutions

#### Issue: "Explore local area near hotel" appears

**Cause**: No attractions found or selected

**Solutions**:
1. **Check destination name**: Make sure you're using exact names like "Goa", "Kerala", or "Karnataka" (case doesn't matter)
2. **Check backend logs**: Look for `[Debug] Catalog lookup result: False`
3. **Try a catalog destination**: Test with "Goa" first to verify the system works

#### Issue: Catalog lookup returns False

**Possible causes**:
- Destination name doesn't match catalog keys
- Catalog file not loading properly
- Typo in destination name

**Solution**: 
- Use exact destination names: "Goa", "Kerala", "Karnataka"
- Check backend console for catalog loading errors

#### Issue: Attractions found but not showing

**Check logs for**:
- `[Info] Mapped X attractions for ML processing`
- `[Info] Selected X activities across Y days`

If you see "Mapped" but "Selected 0", the ML selection might be filtering them out.

### 5. Manual Test

Run this Python code to test catalog loading:

```python
import sys
sys.path.append('backend')
from data import get_catalog_for_destination, get_catalog_attractions

# Test catalog lookup
dest = "Goa"
cat = get_catalog_for_destination(dest)
print(f"Catalog for {dest}: {cat is not None}")

if cat:
    attractions = get_catalog_attractions(dest, 15.2993, 74.1240)
    print(f"Attractions: {[a['name'] for a in attractions]}")
```

### 6. What to Report

If place names still don't load, please provide:
1. The destination you're testing with
2. The backend console output (copy the relevant logs)
3. Whether you see "Catalog lookup result: True" or "False"

---

## Recent Fixes Applied

1. ✅ Added fallback activities when no attractions found (shows "Explore {destination}" instead of generic names)
2. ✅ Enhanced debugging logs to track catalog lookup
3. ✅ Improved destination name matching (case-insensitive, partial matching)
4. ✅ Added validation to ensure names are preserved through ML pipeline

---

**Next Steps**: 
- Restart your backend server
- Test with "Goa" destination
- Check the console logs
- Report what you see











