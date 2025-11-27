# Tripster Project - File Explanation Guide

## Overview
**Tripster** is a smart travel planning web application that helps users create personalized trip itineraries based on their destination, budget, number of days, and preferences.

---

## 🎨 FRONTEND FILES (What Users See)

### HTML Pages

#### `index.html` - **Homepage**
- **What it does**: The main landing page where users start planning their trip
- **Key features**:
  - Hero section with a search form
  - Users enter: current location, destination, days, budget, number of people, dietary preferences
  - Shows popular destinations and services
  - Displays the generated trip plan after submission

#### `login.html` - **Login/Registration Page**
- **What it does**: Handles user authentication (login and signup)
- **Key features**:
  - Two tabs: Login and Register
  - Users can create accounts or sign in
  - Password visibility toggle
  - Validates email format and password matching

#### `plan.html` - **Trip Plan Display Page**
- **What it does**: Shows the detailed itinerary after it's generated
- **Key features**:
  - Displays day-by-day activities with times
  - Shows hotel suggestions with prices
  - Lists restaurant recommendations
  - Budget breakdown visualization
  - Allows users to add custom places to their plan
  - Shows travel distance and cost information

#### `places.html` - **Places Discovery Page**
- **What it does**: Helps users discover and explore popular destinations
- **Key features**:
  - Search bar to find destinations
  - Featured trip cards (Gokarna, Varkala, Meghalaya)
  - Popular activity categories
  - Quick links to plan trips for featured destinations

#### `about.html` & `services.html` - **Information Pages**
- **What they do**: Provide information about the company and services offered

---

### JavaScript Files

#### `assets/app.js` - **Main Application Logic**
- **What it does**: Handles the trip planning form submission and displays results
- **Key functions**:
  - Collects form data (destination, budget, days, etc.)
  - Sends request to backend API
  - Shows loading spinner while generating plan
  - Handles errors (server not running, budget too low, etc.)
  - Redirects to plan page after successful generation
  - Pre-fills form from URL parameters

#### `assets/auth.js` - **Authentication Logic**
- **What it does**: Manages user login, registration, and session
- **Key functions**:
  - Handles login form submission
  - Handles registration form submission
  - Stores authentication token in browser storage
  - Provides utility functions for checking if user is logged in
  - Handles logout functionality
  - Password visibility toggles

---

### CSS Files (Styling)
- `base.css` - Common styles used across all pages
- `home.css` - Styles for the homepage
- `auth.css` - Styles for login/registration page
- `plan.css` - Styles for the trip plan display
- `places.css` - Styles for the places page
- `services.css` - Styles for services page
- `about.css` - Styles for about page

---

## ⚙️ BACKEND FILES (Server-Side Logic)

### Main Application Files

#### `app.py` - **Legacy Main Application** (Old version)
- **What it does**: Original Flask app that handles trip planning
- **Note**: This is the older version. The new version uses the `app/` folder structure

#### `run.py` - **Application Starter**
- **What it does**: The entry point to start the Flask server
- **Simple explanation**: When you run `python run.py`, it starts the web server on port 5000

#### `app/__init__.py` - **Application Factory**
- **What it does**: Creates and configures the Flask application
- **Key responsibilities**:
  - Sets up database connections (MongoDB or SQLite)
  - Configures authentication (JWT tokens)
  - Registers all API routes
  - Sets up CORS (allows frontend to communicate with backend)
  - Initializes password hashing and security features

---

### API & Route Files

#### `app/routes.py` - **API Endpoints**
- **What it does**: Defines all the API routes (URLs) that the frontend can call
- **Key endpoints**:
  - `/api/auth/signup` - Register new users
  - `/api/auth/signin` - Login users
  - `/api/itinerary/generate` - Generate trip plan (requires login)
  - `/api/itinerary/generate-public` - Generate trip plan (no login needed)
  - `/plan-trip` - Legacy endpoint for backward compatibility
  - `/itinerary/<id>` - Get saved itinerary by ID

---

### Service & Business Logic

#### `app/services.py` - **Trip Planning Service**
- **What it does**: The "brain" of the trip planning system
- **Key responsibilities**:
  - Takes user input (destination, budget, days, etc.)
  - Calls Google Maps API to find attractions, hotels, restaurants
  - Uses machine learning to cluster attractions by location
  - Distributes activities across days
  - Calculates travel costs and distances
  - Generates the complete itinerary structure
  - Returns a JSON response with the full plan

#### `apis.py` - **External API Integration**
- **What it does**: Communicates with Google Maps/Places APIs
- **Key functions**:
  - `google_geocode_place()` - Converts place names to coordinates (lat/lng)
  - `find_attractions_api()` - Finds tourist attractions near a location
  - `google_hotels_search()` - Searches for hotels
  - `find_restaurants_in_budget_api()` - Finds restaurants within budget
  - `google_distance_matrix()` - Calculates travel distance and time between locations

#### `ml.py` - **Machine Learning Logic**
- **What it does**: Uses AI to organize attractions intelligently
- **Key functions**:
  - `cluster_attractions_by_location()` - Groups nearby attractions together using K-Means clustering
  - `select_daily_attractions()` - Selects which attractions to visit each day based on budget and time
  - Uses "knapsack algorithm" to maximize value within budget constraints

#### `data.py` - **Local Data & Fallbacks**
- **What it does**: Provides backup data when APIs fail or for specific destinations
- **Key features**:
  - Mock hotels and restaurants data
  - Static catalog of destinations (from `static_catalog.json`)
  - Functions to estimate minimum budget
  - Fallback hotel/restaurant selection when APIs don't work
  - Budget calculation helpers

---

### Database Files

#### `app/db.py` - **SQLite Database Helper**
- **What it does**: Manages user data in SQLite database
- **Key functions**:
  - `init_user_db()` - Creates users table if it doesn't exist
  - `create_user()` - Adds new user to database
  - `get_user_by_username()` - Finds user by username
  - `get_user_by_id()` - Finds user by ID
  - `check_username_exists()` - Checks if username is taken
  - `check_email_exists()` - Checks if email is already registered

#### `app/models.py` - **MongoDB Models** (Optional)
- **What it does**: Sets up MongoDB database indexes (if MongoDB is configured)
- **Note**: The app works with SQLite by default, MongoDB is optional

#### `tripster.db` - **SQLite Database File**
- **What it is**: The actual database file storing user accounts and saved itineraries
- **Note**: This is a binary file created automatically

---

### Configuration Files

#### `requirements.txt` - **Python Dependencies**
- **What it does**: Lists all Python packages needed to run the backend
- **Key packages**: Flask, Flask-CORS, scikit-learn, requests, etc.

#### `static_catalog.json` - **Destination Catalog**
- **What it is**: A JSON file containing pre-defined data for popular destinations
- **Contains**: Attractions, hotels, restaurants for specific places like Goa, Delhi, etc.

#### `.env` - **Environment Variables** (Not in repo, but needed)
- **What it does**: Stores sensitive configuration like API keys
- **Contains**: Google Maps API key, database connection strings, secret keys

---

## 🔄 HOW IT ALL WORKS TOGETHER

### User Journey:

1. **User visits homepage** (`index.html`)
   - Sees the search form

2. **User fills form and submits**
   - `app.js` collects the data
   - Sends POST request to `/plan-trip` or `/api/itinerary/generate`

3. **Backend receives request** (`app/routes.py`)
   - Routes to `app/services.py`

4. **Service generates itinerary** (`app/services.py`)
   - Calls `apis.py` to get attractions, hotels, restaurants from Google
   - Calls `ml.py` to intelligently organize attractions
   - Uses `data.py` for fallback data if APIs fail
   - Calculates budgets and travel costs

5. **Response sent back to frontend**
   - `app.js` receives the itinerary JSON
   - Redirects to `plan.html`

6. **Plan displayed** (`plan.html`)
   - Shows day-by-day activities
   - Displays hotel and restaurant suggestions
   - Shows budget breakdown

### Authentication Flow:

1. **User registers** (`login.html` → `auth.js`)
   - Sends to `/api/auth/signup`
   - `app/routes.py` handles it
   - `app/db.py` saves user to database
   - Password is hashed using bcrypt

2. **User logs in**
   - Sends to `/api/auth/signin`
   - Backend verifies password
   - Returns JWT token
   - Frontend stores token in localStorage

3. **User generates plan**
   - Token sent with request
   - Backend verifies token
   - Plan is generated and saved

---

## 📊 KEY TECHNOLOGIES

- **Frontend**: HTML, CSS, JavaScript (Vanilla JS, no frameworks)
- **Backend**: Python, Flask (web framework)
- **Database**: SQLite (default), MongoDB (optional)
- **APIs**: Google Maps/Places API
- **ML**: scikit-learn (for clustering attractions)
- **Authentication**: JWT (JSON Web Tokens), bcrypt (password hashing)

---

## 🎯 MAIN FEATURES

1. **Smart Itinerary Generation**: Uses ML to organize attractions by location
2. **Budget-Aware Planning**: Suggests hotels/restaurants within budget
3. **Travel Cost Calculation**: Estimates travel distance and costs
4. **User Authentication**: Login/signup system
5. **Fallback Data**: Works even if external APIs fail
6. **Custom Place Addition**: Users can add their own places to the plan

---

## 💡 SIMPLE ANALOGIES

- **`app/services.py`** = The travel agent who plans your trip
- **`apis.py`** = The phone book to find hotels and restaurants
- **`ml.py`** = The smart assistant that groups nearby places together
- **`app/routes.py`** = The receptionist who directs requests to the right department
- **`app/db.py`** = The filing cabinet storing user information
- **`app.js`** = The front desk that talks to customers and coordinates everything

---

This should help you explain the project clearly in your presentation! 🚀


