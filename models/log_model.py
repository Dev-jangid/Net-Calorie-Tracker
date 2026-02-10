from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class FoodEntry:
    food_id: str
    food_name: str
    portion: float # Multiple of serving size
    calories: float
    meal_type: str # Breakfast, Lunch, Dinner, Snack
    fat: float = 0.0
    protein: float = 0.0
    carbs: float = 0.0
    excel_id: Optional[int] = None
    food_group: Optional[str] = None
    serving_desc: Optional[str] = None

@dataclass
class ActivityEntry:
    activity_id: str
    activity_name: str
    duration_minutes: float
    calories_burnt: float
    specific_motion: str = ""

@dataclass
class DailyLog:
    user_id: str
    date: str # ISO format YYYY-MM-DD
    foods: List[FoodEntry] = field(default_factory=list)
    activities: List[ActivityEntry] = field(default_factory=list)
    bmr_at_time: float = 0.0
    net_calories: float = 0.0
    _id: Optional[str] = None

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "date": self.date,
            "foods": [vars(f) for f in self.foods],
            "activities": [vars(a) for a in self.activities],
            "bmr_at_time": self.bmr_at_time,
            "net_calories": self.net_calories
        }

    @staticmethod
    def from_dict(data: dict):
        foods = [FoodEntry(**f) for f in data.get('foods', [])]
        activities = [ActivityEntry(**a) for a in data.get('activities', [])]
        return DailyLog(
            user_id=str(data.get('user_id')),
            date=data.get('date'),
            foods=foods,
            activities=activities,
            bmr_at_time=data.get('bmr_at_time', 0.0),
            net_calories=data.get('net_calories', 0.0),
            _id=str(data.get('_id')) if data.get('_id') else None
        )
