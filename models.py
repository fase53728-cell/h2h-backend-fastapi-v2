from pydantic import BaseModel
from typing import List, Dict, Optional

class League(BaseModel):
    league_id: str
    name: str

class Team(BaseModel):
    team_id: str
    name: str

class TeamStats(BaseModel):
    team_id: str
    name: str
    raw_columns: Dict[str, float] = {}
    win_prob: Optional[float] = None
    draw_prob: Optional[float] = None
    loss_prob: Optional[float] = None
    avg_goals_for: Optional[float] = None
    avg_goals_against: Optional[float] = None
    over_15_prob: Optional[float] = None
    over_25_prob: Optional[float] = None
    btts_prob: Optional[float] = None

class H2HPrediction(BaseModel):
    best_bet: str
    comment: str

class H2HAnalysis(BaseModel):
    league_id: str
    home: TeamStats
    away: TeamStats
    prediction: H2HPrediction
