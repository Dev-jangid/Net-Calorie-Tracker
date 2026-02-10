from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Activity:
    activity_name: str
    specific_motion: str
    met_value: float
    _id: Optional[str] = None

    def to_dict(self):
        d = asdict(self)
        if d['_id'] is None:
            del d['_id']
        return d

    @staticmethod
    def from_dict(data: dict):
        return Activity(
            activity_name=data.get('ACTIVITY') or data.get('activity_name') or data.get('Activity Name'),
            specific_motion=data.get('SPECIFIC MOTION') or data.get('specific_motion') or data.get('Specific Motion') or "",
            met_value=float(data.get('METs') or data.get('met_value') or data.get('MET Value') or 0),
            _id=str(data.get('_id')) if data.get('_id') else None
        )
