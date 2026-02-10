from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Food:
    food_name: str
    serving_size: str
    calories_per_serving: float
    excel_id: Optional[int] = None
    food_group: Optional[str] = None
    fat: float = 0.0
    protein: float = 0.0
    carbs: float = 0.0
    _id: Optional[str] = None

    def to_dict(self):
        d = asdict(self)
        if d['_id'] is None:
            del d['_id']
        return d

    @staticmethod
    def from_dict(data: dict):
        return Food(
            food_name=data.get('name') or data.get('food_name') or data.get('Food Name'),
            serving_size=data.get('Serving Description 1') or data.get('serving_size') or data.get('Serving Size') or "1 serving",
            calories_per_serving=float(data.get('Calories') or data.get('calories_per_serving') or data.get('Calories per Serving Size') or 0),
            excel_id=data.get('ID'),
            food_group=data.get('Food Group'),
            fat=float(data.get('Fat (g)') or 0.0),
            protein=float(data.get('Protein (g)') or 0.0),
            carbs=float(data.get('Carbohydrate (g)') or 0.0),
            _id=str(data.get('_id')) if data.get('_id') else None
        )
