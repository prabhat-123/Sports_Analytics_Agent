from sqlmodel import Field, SQLModel
from db.db_access import PostgresDB


class IPL_MatchInfo(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    season: str = Field(nullable = False)
    city: str = Field(nullable = True)
    date: str = Field(nullable = False)
    team1: str = Field(nullable = False)
    team2: str = Field(nullable = False)
    toss_winner: str = Field(nullable = False)
    toss_decision: str = Field(nullable = False)
    result: str = Field(nullable = False)
    dl_applied: int = Field(nullable = False)
    winner: str = Field(nullable = True)
    win_by_runs: int = Field(nullable = False)
    win_by_wickets: int = Field(nullable = False)
    player_of_match: str = Field(nullable = True)
    venue: str = Field(nullable = False)
    umpire1: str = Field(nullable = False)
    umpire2: str = Field(nullable = False)
    umpire3: str = Field(nullable = True)

class IPL_MatchData(SQLModel, table = True):
    pk: int = Field(nullable = False, primary_key=True)

    match_id: int = Field(nullable = False)
    season: str = Field(nullable = False)
    start_date: str = Field(nullable = False)
    venue: str = Field(nullable = False)
    innings: int = Field(nullable = False)
    ball: float = Field(nullable = False)
    batting_team: str = Field(nullable = False)
    bowling_team: str = Field(nullable = False)
    striker: str = Field(nullable = False)
    non_striker: str = Field(nullable = False)
    bowler: str = Field(nullable = False)
    runs_off_bat: int = Field(nullable = False)
    extras: int = Field(nullable = False)
    wides: float = Field(nullable = True)
    noballs: float = Field(nullable = True)
    byes: float = Field(nullable = True)
    legbyes: float = Field(nullable = True)
    penalty: float = Field(nullable = True)
    wicket_type: str = Field(nullable = True)
    player_dismissed: str = Field(nullable = True)
    other_wicket_type: float = Field(nullable = True)
    other_player_dismissed: float = Field(nullable = True)


def create_db_and_tables():
    db_obj = PostgresDB()
    engine = db_obj.connect_to_db()
    SQLModel.metadata.create_all(engine)
    for table_name, table in SQLModel.metadata.tables.items():
        columns = ', '.join(str(column.compile(dialect=engine.dialect)) for column in table.c)
        print(f"Create TABLE {table_name} ({columns})")

