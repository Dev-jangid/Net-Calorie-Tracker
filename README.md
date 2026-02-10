<<<<<<< HEAD
# Net-Calorie-Tracker
=======
# Net Calorie Tracker

A comprehensive calorie and activity tracking application built with **Python**, **Streamlit**, and **MongoDB**. This tool helps users track their daily energy balance by calculating BMR, logging food intake, and monitoring exercise burn using standard MET values.

## Features

- **Multi-User Management**: Create and manage multiple user profiles with custom age, weight, height, and gender for accurate BMR calculation.
- **Dynamic Energy Balance**: Real-time dashboard showing `Food IN - (BMR + Exercise OUT) = Net Calories`.
- **Categorized Selection**: High-performance cascading dropdowns (Food Group -> Food Name) for intuitive logging.
- **Dual-Mode Workflow (Direct Search)**: Bypass categories by searching directly in the "Food Name" or "Specific Motion" lists for a global database search.
- **Manual Entry Support**: Log custom food or activities with full macro/MET control.
- **Macro-nutrient Tracking**: Detailed breakdown of Protein, Fat, and Carbohydrates for every food item.
- **Persistent History**: Saves daily logs to MongoDB, allowing users to track progress over time.
- **Excel-Style Reports**: Full-width horizontal log tables for easy reading of nutritional data and exercise specifics.

---

## System Architecture

The application follows a modular **Service-Model-UI** architecture to ensure separation of concerns and maintainability.

### 1. Presentation Layer (Streamlit)

- **`app.py`**: The entry point. Manages session state, page navigation (via sidebar), and reactive UI rendering.
- **Views**:
  - **User Management**: Profile creation and deletion.
  - **Calories Tracker**: Core dashboard with merged Search/Manual logging forms.

### 2. Service Layer (Business Logic)

- **`services/user_service.py`**: Handles User CRUD and MongoDB persistence.
- **`services/calorie_service.py`**: Manages `DailyLog` objects, computes calorie totals, and interacts with datasets.
- **`services/bmr_service.py`**: Implements the **Harris-Benedict Equation** for BMR tracking.

### 3. Data Layer (Models & Persistence)

- **`models/`**: Strictly typed dataclasses for `User`, `Food`, `Activity`, and `DailyLog`.
- **`db/mongo.py`**: Singleton-pattern database connection utility.

---

## Project Structure

```
.
├── app.py                # Main Streamlit application
├── db/                   # Database connection layer
├── models/               # Data classes (User, Food, Activity, Log)
├── services/             # Business logic & Calculations
├── scripts/              # Data loading & setup utilities
├── data/                 # Source Excel files
└── utils/                # Date and helper utilities
```

## Data Models

### User Model

Stored in `users` collection.

- `name`, `weight` (kg), `height` (cm), `sex` (Male/Female), `age`.

### Food Model

Stored in `food_items` collection.

- `food_name`, `calories_per_serving`, `protein`, `fat`, `carbs`, `food_group`.

### Daily Log Model

Stored in `daily_logs` collection. Keys: `user_id` + `date`.

- `bmr_at_time`: Snapshot of user's BMR at log creation.
- `foods` / `activities`: Lists of specific entries with portions/durations.

---

## Core Logic & Formulas

### 1. BMR (Basal Metabolic Rate)

Calculated using the **Harris-Benedict Equation**:

- **Men**: $66.4730 + (13.7516 \times \text{weight in kg}) + (5.0033 \times \text{height in cm}) - (6.7550 \times \text{age in years})$
- **Women**: $655.0955 + (9.5634 \times \text{weight in kg}) + (1.8496 \times \text{height in cm}) - (4.6756 \times \text{age in years})$

### 2. Activity Burn (MET Calculation)

Calculated using the **Metabolic Equivalent of Task (MET)**:

$$
\text{Calories Burnt} = \text{MET} \times \text{Weight (kg)} \times \text{Duration (hours)}
$$

### 3. Net Calorie Computation

$$
\text{Net} = \text{Total Intake} - (\text{BMR} + \text{Exercise Burn})
$$

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- MongoDB instance (Local or Atlas)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=calorie_tracker
```

### 3. Load the Database

Run the injection scripts to load food and activity data:

```bash
python scripts/load_food.py
python scripts/load_activities.py
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## Selection Logic (Functional Spec)

The application implements a **Dual-Mode selection system** for both food and activities, ensuring both precision and speed.

### Food Intake Logic

- **Food Group = NULL** (`-- Select Category --`): **Food Name** dropdown acts as a **Global Search**, displaying all items in the database.
- **Food Group = SELECTED**: **Food Name** dropdown displays only the items **Filtered by Group**.

### Activity Selection Logic

- **Activity List = NULL** (`-- Select Activity --`): **Motion List** acts as a **Global Search**.
- **Activity List = SELECTED**: **Motion List** is **Filtered by Activity**.

> Selecting an item directly without picking a category will automatically resolve the correct category and its metadata (Calories/MET) from the database.

---

## Search & Performance

- **Optimized Search**: To handle 14,000+ records, datasets are filtered using optimized list comprehensions in memory.
- **Display Limits**: Results are capped (1,000 for Foods, 200 for Activities) to maintain a lag-free Streamlit experience.

---

*Generated by Antigravity AI - Project Documentation*
>>>>>>> 1e7f751 (Initial commit - Final version of Net Calorie Tracker)
