# Google Places API Key Setup Guide

## Problem
When testing destinations not in the catalog (like "varkala"), you see:
```
[API Error] Request Failed: HTTP_400 - API key not valid. Please pass a valid API key.
```

## Solution Options

### Option 1: Add Destinations to Catalog (Recommended - No API Key Needed)

**Best solution**: Add popular destinations to `backend/static_catalog.json`. This works immediately without any API key.

**Example - Adding Varkala** (already added):
```json
"Varkala": {
  "center": { "lat": 8.7379, "lng": 76.7163 },
  "attractions": [
    "Varkala Beach",
    "Papanasam Beach",
    "Janardanaswamy Temple"
  ],
  "restaurants": [
    { "name": "Cafe del Mar, Varkala" }
  ],
  "stays": [
    { "name": "Zostel Varkala (budget)", "budgetTier": "low" }
  ]
}
```

**To add more destinations:**
1. Open `backend/static_catalog.json`
2. Add a new entry with the destination name as the key
3. Include center coordinates (lat/lng) - you can find these on Google Maps
4. List attractions, restaurants, and stays
5. Save the file
6. Restart the backend server

---

### Option 2: Get a Valid Google Places API Key

If you want to use the Google Places API for destinations not in the catalog:

#### Step 1: Get API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Places API (New)**
   - **Geocoding API**
   - **Distance Matrix API**
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy your API key

#### Step 2: Restrict API Key (Recommended for Security)

1. Click on your API key to edit it
2. Under "API restrictions", select "Restrict key"
3. Choose only the APIs you need:
   - Places API (New)
   - Geocoding API
   - Distance Matrix API
4. Under "Application restrictions", you can restrict by IP or HTTP referrer
5. Save

#### Step 3: Add to .env File

1. Open `backend/.env` file
2. Add or update:
   ```env
   GOOGLE_PLACES_API_KEY=your-actual-api-key-here
   ```
3. Save the file
4. **Restart the backend server**

#### Step 4: Verify

Test with a destination not in the catalog. You should see:
```
[Info] Found X attractions from API: ['Place Name 1', 'Place Name 2', ...]
```

Instead of:
```
[API Error] Request Failed: HTTP_400 - API key not valid
```

---

## Current Catalog Destinations

These work **without** an API key:
- ✅ **Goa** - 5 attractions
- ✅ **Kerala** - 5 attractions  
- ✅ **Karnataka** - 5 attractions
- ✅ **Varkala** - 6 attractions (just added!)

---

## Cost Considerations

**Google Places API Pricing** (as of 2024):
- **Places API (New)**: $17 per 1,000 requests
- **Geocoding API**: $5 per 1,000 requests
- **Distance Matrix API**: $5 per 1,000 requests

**Free Tier**: 
- $200 free credit per month (new users)
- Enough for ~11,000 Places API requests/month

**Recommendation**: 
- For development/testing: Use the catalog (free, unlimited)
- For production: Get an API key and set usage limits

---

## Troubleshooting

### Issue: "API key not valid" error

**Solutions**:
1. Check `.env` file has `GOOGLE_PLACES_API_KEY=your-key`
2. Make sure there are no extra spaces or quotes
3. Restart the backend server after changing `.env`
4. Verify the API key is active in Google Cloud Console
5. Check that required APIs are enabled

### Issue: API key works but no results

**Possible causes**:
- API key restrictions are too strict
- Billing not enabled (required for Google Cloud)
- API quota exceeded

**Solutions**:
- Check API key restrictions in Google Cloud Console
- Enable billing for your project
- Check quota usage in Google Cloud Console

---

## Quick Fix for Now

**For immediate use without API key:**
1. Use destinations in the catalog: Goa, Kerala, Karnataka, Varkala
2. Or add more destinations to `static_catalog.json` (see Option 1 above)

**Varkala is now in the catalog!** Try testing with "varkala" again - it should work now! 🎉











