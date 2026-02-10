from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class User:
    name: str
    weight: float
    height: float
    sex: str
    age: int
    _id: Optional[str] = None

    def to_dict(self):
        d = asdict(self)
        if d['_id'] is None:
            del d['_id']
        return d

    @staticmethod
    def from_dict(data: dict):
        return User(
            name=data.get('name'),
            weight=data.get('weight'),
            height=data.get('height'),
            sex=data.get('sex'),
            age=data.get('age'),
            _id=str(data.get('_id')) if data.get('_id') else None
        )
