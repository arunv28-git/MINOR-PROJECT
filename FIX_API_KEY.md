# Fix: Google Places API Key Setup

## Changes Made

✅ **API is now PRIMARY source** - The system now tries Google Places API first, then falls back to catalog
✅ **Better API key detection** - Added logging to show if API key is loaded
✅ **Improved error messages** - Shows exactly why API calls fail

## Step 1: Check Your .env File

1. Open `backend/.env` file
2. Make sure it has your Google Places API key:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
GOOGLE_PLACES_API_KEY=your-actual-google-places-api-key-here
```

**OR** you can use:

```env
GOOGLE_MAPS_API_KEY=your-actual-google-maps-api-key-here
```

**Important:**
- Remove any quotes around the API key
- No spaces before or after the `=`
- The key should start with `AIza...`

**Example (correct):**
```env
GOOGLE_PLACES_API_KEY=AIzaSyDDXHMBEVEj6zIXZ8azNX4xncuyzrhOyCI
```

**Example (wrong):**
```env
GOOGLE_PLACES_API_KEY="AIzaSyDDXHMBEVEj6zIXZ8azNX4xncuyzrhOyCI"  ❌ (quotes)
GOOGLE_PLACES_API_KEY = AIzaSy...  ❌ (spaces)
GOOGLE_PLACES_API_KEY=  ❌ (empty)
```

## Step 2: Restart Backend Server

**CRITICAL:** After changing `.env` file, you MUST restart the backend server:

1. Stop the server (press `Ctrl+C` in the terminal)
2. Start it again:
   ```powershell
   python run.py
   ```

3. **Check the startup logs** - You should see:
   ```
   [API Info] Google Places API Key loaded: AIzaSyDDXH...yCI
   ```

   If you see this instead:
   ```
   [API Warning] No Google Places API Key found in environment variables!
   ```
   Then your `.env` file is not being read correctly.

## Step 3: Verify API Key is Working

After restarting, test with any destination (e.g., "varkala"). Check the backend console:

**✅ If API key is working:**
```
[API Info] Google Places API Key loaded: AIzaSyDDXH...yCI
[Info] Attempting Google Places API search for attractions near (8.7379, 76.7163)
[Info] ✅ Found 20 attractions from Google Places API: ['Varkala Beach', 'Papanasam Beach', ...]
```

**❌ If API key is invalid:**
```
[API Error] Request Failed: HTTP_400 - API key not valid. Please pass a valid API key.
[Warning] Google Places API search failed: HTTP_400
[Warning] API Error details: API key not valid. Please pass a valid API key.
```

## Step 4: Get a Valid API Key (If Needed)

If you don't have a valid API key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable these APIs:
   - **Places API (New)** ⭐ (Required)
   - **Geocoding API** (for location lookup)
   - **Distance Matrix API** (for travel distance)
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the key
6. Add it to your `.env` file
7. **Restart the backend server**

## Step 5: Test

1. Restart backend: `python run.py`
2. Look for: `[API Info] Google Places API Key loaded: ...`
3. Test with "varkala" or any destination
4. Check console for: `✅ Found X attractions from Google Places API`

## Troubleshooting

### Issue: "No Google Places API Key found"

**Causes:**
- `.env` file doesn't exist
- `.env` file is in wrong location (should be in `backend/` folder)
- API key variable name is wrong
- `.env` file has syntax errors

**Fix:**
1. Check `.env` file exists in `backend/` folder
2. Verify variable name: `GOOGLE_PLACES_API_KEY` (exact spelling)
3. Make sure no quotes around the value
4. Restart server after changes

### Issue: "API key not valid"

**Causes:**
- API key is wrong/expired
- API key doesn't have required APIs enabled
- Billing not enabled on Google Cloud project

**Fix:**
1. Verify API key in Google Cloud Console
2. Enable required APIs (Places API New, Geocoding, Distance Matrix)
3. Enable billing (required for Google Cloud)
4. Check API key restrictions aren't too strict

### Issue: API key works but no results

**Possible causes:**
- API restrictions too strict
- Quota exceeded
- Location coordinates wrong

**Fix:**
- Check API key restrictions in Google Cloud Console
- Verify quota usage
- Check geocoding is working (should see coordinates in logs)

## Current Behavior

**Now the system:**
1. ✅ **Tries Google Places API FIRST** for all destinations
2. ✅ Falls back to catalog only if API fails
3. ✅ Shows clear error messages if API key is missing/invalid
4. ✅ Logs API key status on startup

**This means:**
- Any destination will work if API key is valid
- Real-time data from Google Places
- Catalog is backup only

---

**After fixing your `.env` file and restarting, the API should work!** 🎉




