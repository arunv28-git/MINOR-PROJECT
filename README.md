Smart Trip Planner (Tripster)

A minimal end-to-end starter for a smart trip planner with a Flask backend and a vanilla HTML/Tailwind frontend.

## 📖 Quick Setup Guide

**For detailed step-by-step instructions with troubleshooting, see [SETUP.md](SETUP.md)**

### Quick Start (5 minutes):

1. **Backend Setup:**
   ```powershell
   cd backend
   pip install -r requirements.txt
   # Create .env file with SECRET_KEY and JWT_SECRET_KEY
   python run.py
   ```

2. **Frontend:**
   - Open `frontend/index.html` in your browser
   - OR run: `cd frontend && python -m http.server 8000`

3. **Test Login:**
   - Click "Login" button → Register a new user → Login

**That's it!** The login page works with SQLite (no MongoDB needed).

---

Prerequisites
- Windows 10/11 (PowerShell)
- Python 3.11 or 3.12 (use the embedded venv inside `backend/venv` or your own)
- Chrome/Edge for the frontend

1) Backend Setup

**Prerequisites:**
- Python 3.11 or 3.12
- MongoDB (optional - SQLite is used by default)

**Quick Start (Recommended - SQLite, No Setup Required):**

1. Open PowerShell and navigate to the backend directory:

```powershell
cd backend
# Activate virtual environment (if using one)
# . .\venv\Scripts\Activate.ps1
# OR create a new venv:
# python -m venv venv
# . .\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

2. Create a `.env` file in the `backend` directory (optional, but recommended):

```env
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production
GOOGLE_PLACES_API_KEY=your-google-places-api-key-here
```

3. Run the server:

```powershell
python run.py
```

**That's it!** The application will use SQLite for authentication by default. No MongoDB installation needed!

**Option: Using MongoDB (Optional)**

If you prefer MongoDB over SQLite:

1. Install and start MongoDB:
   - Download MongoDB Community Server from https://www.mongodb.com/try/download/community
   - Install and start MongoDB service (or run `mongod` manually)

2. Add to your `.env` file:

```env
MONGO_URI=mongodb://localhost:27017/tripster
```

3. The app will automatically use MongoDB if `MONGO_URI` is set, otherwise it uses SQLite.

**Note:** Both SQLite and MongoDB support full authentication features. SQLite is simpler to set up (no installation needed) and works great for development and small deployments.

The API will start at `http://127.0.0.1:5000`.

2) Frontend Setup

**Option A: Simple File Opening (Recommended for Development)**

Simply open `frontend/index.html` in your browser (double-click or drag into a tab).

**Option B: Using a Local Server (Recommended for Production-like Testing)**

If you encounter CORS issues or want a more production-like environment:

```powershell
# Using Python's built-in server
cd frontend
python -m http.server 8000
# Then open http://localhost:8000 in your browser

# OR using Node.js http-server (if installed)
# npx http-server -p 8000
```

3) Using the Application

**Registration and Login:**
1. Navigate to the login page (click "Login" button in the header)
2. Click the "Register" tab to create a new account
3. Fill in username, email, and password (minimum 6 characters)
4. After registration, switch to the "Login" tab and sign in
5. Once logged in, you'll see your username in the header

**Planning a Trip:**
1. On the home page, fill in the trip details:
   - Current location (optional)
   - Destination
   - Number of days
   - Budget (in INR)
   - Number of people
   - Dietary preferences
2. Click "Browse Trip" to generate your itinerary
3. If you're logged in, your itinerary will be saved to your account
4. If you're not logged in, you can still use the public endpoint

**Logout:**
- Click the "Logout" button in the header to sign out

4) Project Structure

**Backend:**
- `backend/run.py`: Main entry point for the Flask application
- `backend/app/__init__.py`: Flask app factory with MongoDB, JWT, and CORS setup
- `backend/app/routes.py`: API routes for authentication and itinerary generation
- `backend/app/models.py`: Database models and indexes
- `backend/app/services.py`: Business logic for itinerary generation
- `backend/app.py`: Legacy standalone Flask app (deprecated, use `run.py` instead)
- `backend/requirements.txt`: Python dependencies

**Frontend:**
- `frontend/index.html`: Main landing page with trip planning form
- `frontend/login.html`: Login and registration page
- `frontend/assets/app.js`: Main application JavaScript (trip planning logic)
- `frontend/assets/auth.js`: Authentication JavaScript (login, register, token management)
- `frontend/assets/styles.css`: Custom CSS styles

Notes
- The API key is read from the environment variable `GOOGLE_PLACES_API_KEY`.
- Next steps: add real data collection (Google Maps, TripAdvisor, Zomato), ML models (KMeans, ranking, knapsack), and persistence (MySQL/MongoDB).

ML features
- Basic KMeans clustering (via `backend/ml.py`) groups attractions by location across days.
- Greedy selector keeps daily attraction fees and time under caps.
- Mock hotels/restaurants live in `backend/data.py`. Replace with API/CSV data to go live.

Project synopsis (expanded)

Objectives
- Collect and unify travel data (attractions, hotels, restaurants, transport) for Indian destinations
- Clean and impute missing values; normalize ratings/cost/time
- Use ML to cluster attractions by geography/time and optimize day-wise plans within a user budget
- Provide a simple web UI and REST API; no bookings, only budget-fit suggestions and guidance

Problem statement
Travelers struggle to convert large lists of attractions into realistic day-wise plans that fit budget, time and preferences. Existing sites list places but rarely provide optimized itineraries with cost visibility. This system generates structured, budget-aware plans with a clear minimum-budget disclaimer.

High-level architecture
- Frontend: static `index.html` + Tailwind + `assets/app.js`
- Backend API: Flask (`app.py`), CORS enabled
- Data layer: mock datasets in `data.py` (replaceable by CSV/API)
- ML layer: `ml.py` (KMeans clustering + greedy budget/time selection)
- Optional external APIs: Google Maps/Places, TripAdvisor, Zomato/Swiggy, Booking providers (future)

Data sources (current and planned)
- Current: curated mock data for hotels/restaurants; sample attractions in `ml.py`
- Planned APIs: `Google Places`, `TripAdvisor`, `Zomato`, `OpenStreetMap` routing (for distance/time)
- Planned CSVs: city-wise attractions with lat/lng, expected fees, durations, seasonal notes

Preprocessing & imputation
- Normalize costs to INR; standardize durations to hours
- Missing fees/durations: median per category/city; optional linear regression with city and category features
- Deduplicate records by name+geo radius, unify rating scales to 1–5

ML components
- Clustering: KMeans groups attractions by proximity into N day-buckets
- Selection: greedy fit under per-day time (default 6h) and per-day activity-fee budget
- Roadmap: preference-aware ranking (weighted scores), knapsack optimizer for activities/food, city-aware priors

Budget model
- Split of total budget: 40% stay, 25% food, 20% activities, 15% transport (tunable)
- Minimum budget estimator: cheapest hotel × nights + two cheapest meals/day × people + daily transport and activity buffers
- Disclaimer: estimates only; vary by season, availability, and choices

API design
- `GET /` → service info
- `GET /health` → `{ status: ok }`
- `POST /api/auth/signup` → Register new user (body: `{ username, email, password }`)
- `POST /api/auth/signin` → Login user (body: `{ username, password }`) → returns JWT token
- `POST /plan-trip` → Public endpoint (no auth required) → body: `{ destination, days, budget, people, travelerType }`
- `POST /api/itinerary/generate` → Authenticated endpoint (requires JWT token in Authorization header)
  - Response: title, `budget_summary`, `minimum_budget`, `hotel`, `daily_plan[]` (activities + restaurants), `activities_fee_estimated`

Frontend UX
- Hero form (destination, days, INR budget)
- Result cards: minimum budget banner, budget breakdown, suggested stay, day-wise activities and restaurants, cost hints

Non-functional requirements
- Uses SQLite by default for authentication (no setup required)
- Optional MongoDB support (automatically used if MONGO_URI is configured)
- CORS enabled for static file usage
- JWT-based authentication for protected endpoints
- Extensible: drop-in CSV/API fetchers; replace mock with real data sources
- User authentication and session management (works with both SQLite and MongoDB)

Testing & evaluation
- Unit: budget allocator, minimum-budget estimator, ML clustering selectors
- Scenario tests: budgets below/close to/above minimum; 1–7 day itineraries
- Metrics (initial): activity coverage per day, budget adherence (% over/under), average attraction rating

Risks & mitigations
- Data quality gaps → fallbacks, imputation, city-specific baselines
- API rate limits → local caching, scheduled harvests
- Route realism → integrate travel-time estimates (OSRM/Google Directions) in future

Roadmap (suggested)
1. City-aware datasets and priors (e.g., New Delhi, Goa, Bengaluru)
2. Preference filters (veg-only, cultural, adventure), and time windows
3. Knapsack-based optimizer for activities/food; add travel-time penalty
4. Persist itineraries (SQLite/MySQL) and simple share link
5. Real data integration (Places/TripAdvisor/Zomato) with caching layer

Synopsis alignment

PROJECT TITLE: SMART TRIP PLANNER

OBJECTIVE
- Design and develop a trip planning system that uses AI/ML to collect, clean, link travel data (popular places, hotels, restaurants) and automatically generate personalized itineraries within a user-defined budget.

PROBLEM STATEMENT
- Travelers struggle to balance budget, time, and preferences. Platforms list attractions but do not optimize costs or create structured day-wise plans. An intelligent system should integrate multiple data sources and apply ML models to suggest optimized itineraries.

PROPOSED SYSTEM
- User Interaction: input destination, days, budget, preferences (login planned as future work).
- Data Collection: fetch from APIs/datasets (attractions, hotels, restaurants, transport).
- AI/ML Processing: clean and impute missing data (entry fees, hotel prices); cluster and select.
- Itinerary Generation: customized, day‑wise plan within budget, with minimum‑budget guidance.

METHODOLOGY
- Data Collection: Google Maps/Places, TripAdvisor, Zomato; CSVs for attractions/hotels/restaurants.
- Preprocessing: handle missing values (median/regression), normalize ratings/costs/time.
- Models: KMeans for clustering, ranking/recommendation for picks, greedy/knapsack for budget.
- Generation: assign attractions/hotels/restaurants per day; optimize order/route (future routing).

APPLICATIONS
- Individual travelers planning on limited budgets
- Travel agencies offering automated plans
- Students/young travelers seeking affordable vacations

TOOLS AND TECHNOLOGIES
- Programming Languages: Python (backend), JavaScript (frontend)
- Libraries: Pandas, NumPy, Scikit‑learn (ML models)
- Frameworks: Flask (current), React/Angular (future UI options)
- Database: MySQL / MongoDB (planned; current version is stateless)
- APIs: Google Maps/Places, TripAdvisor, Booking.com, Zomato (planned integrations)

TEAM
- 4NI23CS028 ARUN V — 2023cs_arunv_a@nie.ac.in 
- 4NI23CS052 DHRUPAD S — 2023cs_dhrupadsuresha_a@nie.ac.in
- 4NI23CS044 CHINMAYA PUTTASWAMY — 2023cs_chinmayaputtaswamy_a@nie.ac.in 
- 4NI23CS047 DEEKSHITH KUMAR K — 2023cs_deekshithkumark_a@nie.ac.in

Current status vs. planned
- **Implemented:** Flask API, INR budget logic, minimum‑budget estimator, hotel/restaurant budget picks, ML clustering selector for attractions, frontend form/UI, **user authentication (login/register), JWT token management, SQLite-based authentication (default), optional MongoDB support, protected API endpoints.**
- **Planned:** Real API integrations (Places/TripAdvisor/Zomato/Booking), enhanced preference filters, routing/time windows, knapsack optimizer, shareable itineraries, user profile management, saved itineraries per user.

