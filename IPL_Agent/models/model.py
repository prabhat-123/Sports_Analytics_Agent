from typing import Optional
from pydantic import BaseModel

class IPL_MatchInfoCSV(BaseModel):
    id: int 
    season: str 
    city: Optional[str] = None 
    date: str 
    team1: str 
    team2: str 
    toss_winner: str 
    toss_decision: str 
    result: str 
    dl_applied: int 
    winner: Optional[str]= None 
    win_by_runs: int
    win_by_wickets: int
    player_of_match: Optional[str] = None 
    venue: str 
    umpire1: str 
    umpire2: str 
    umpire3: Optional[str] = None 

class IPL_MatchDataCSV(BaseModel):
    match_id: int 
    season: str 
    start_date: str 
    venue: str 
    innings: int 
    ball: float 
    batting_team: str 
    bowling_team: str 
    striker: str 
    non_striker: str 
    bowler: str 
    runs_off_bat: int 
    extras: int 
    wides: Optional[float] = None
    noballs: Optional[float] = None
    byes: Optional[float] = None
    legbyes: Optional[float] = None
    penalty: Optional[float] = None
    wicket_type: Optional[str] = None
    player_dismissed: Optional[str] = None
    other_wicket_type: Optional[float] = None
    other_player_dismissed: Optional[float] = None
