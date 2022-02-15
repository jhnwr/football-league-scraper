from typing import Optional

from sqlmodel import Field, SQLModel


class Team(SQLModel, table=True):
    team_name: Optional[str] = Field(default=None, primary_key=True)
    league_name: str = Field()
    position: int = Field()
    played: int = Field()
    won: int = Field()
    drawn: int = Field()
    lost: int = Field()
    goals_for: int = Field()
    goals_against: int = Field()
    goal_difference: int = Field()
    points: int = Field()