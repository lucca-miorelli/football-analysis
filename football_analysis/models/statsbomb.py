from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Team(BaseModel):
    id: int
    name: str


class Player(BaseModel):
    id: int
    name: str


class Position(BaseModel):
    id: int
    name: str


class LineupPlayer(BaseModel):
    player: Player
    position: Position
    jersey_number: int


class Tactics(BaseModel):
    formation: int
    lineup: List[LineupPlayer]


class EventType(BaseModel):
    id: int
    name: str


class Outcome(BaseModel):
    id: int
    name: str


class Technique(BaseModel):
    id: int
    name: str


class BodyPart(BaseModel):
    id: int
    name: str


class Card(BaseModel):
    id: int
    name: str


class FiftyFifty(BaseModel):
    event_id: int = Literal[33]
    outcome: Optional[Outcome] = None  # e.g., {108: "Won", 109: "Lost"}


class BadBehaviour(BaseModel):
    event_id: int = Literal[24]
    card: Optional[Card] = None  # e.g., {65: "Yellow", 67: "Red"}


class BallReceipt(BaseModel):
    event_id: int = Literal[42]
    outcome: Optional[Outcome] = None


class BallRecovery(BaseModel):
    event_id: int = Literal[2,]
    offensive: Optional[bool] = None
    recovery_failure: Optional[bool] = None


class Block(BaseModel):
    event_id: int = Literal[6,]
    counterpress: Optional[bool] = None
    deflection: Optional[bool] = None
    offensive: Optional[bool] = None
    save_block: Optional[bool] = None


class Carry(BaseModel):
    event_id: int = Literal[43]
    end_location: Optional[List[float]]


class Clearance(BaseModel):
    event_id: int = Literal[9,]
    aerial_won: Optional[bool] = None
    body_part: Optional[BodyPart] = (
        None  # e.g., {40: "Right Foot", 38: "Left Foot", etc.}
    )


class Dispossessed(BaseModel):
    event_id: int = Literal[3,]


class Dribble(BaseModel):
    event_id: int = Literal[14]
    outcome: Optional[Outcome] = None  # e.g., {106: "Complete", 107: "Incomplete"}
    nutmeg: Optional[bool] = None
    overrun: Optional[bool] = None
    no_touch: Optional[bool] = None


class DribbledPast(BaseModel):
    event_id: int = Literal[39]
    counterpress: Optional[bool]


class Duel(BaseModel):
    event_id: int = Literal[4,]
    counterpress: Optional[bool] = None
    type: Optional[EventType] = None  # e.g., {10: "Aerial Lost", 11: "Tackle", etc.}


class Error(BaseModel):
    event_id: int = Literal[37]


class FoulCommitted(BaseModel):
    event_id: int = Literal[22]
    advantage: Optional[bool] = None
    counterpress: Optional[bool] = None
    offensive: Optional[bool] = None
    penalty: Optional[bool] = None
    card: Optional[Card] = None  # e.g., {65: "Yellow", 67: "Red"}
    type: Optional[EventType] = None  # e.g., {24: "Handball", 23: "Foul Out", etc.}


class FoulWon(BaseModel):
    event_id: int = Literal[21]
    advantage: Optional[bool] = None
    defensive: Optional[bool] = None
    penalty: Optional[bool] = None


class GoalKeeper(BaseModel):
    event_id: int = Literal[23]
    position: Optional[Position] = None  # e.g., {42: "Moving", 44: "Set", etc.}
    technique: Optional[Technique] = None  # e.g., {45: "Diving", 46: "Standing", etc.}
    body_part: Optional[BodyPart] = (
        None  # e.g., {40: "Right Foot", 38: "Left Foot", etc.}
    )
    type: Optional[EventType] = None
    outcome: Optional[Outcome] = None


class HalfEnd(BaseModel):
    event_id: int = Literal[34]
    early_video_end: Optional[bool]
    match_suspend: Optional[bool]


class HalfStart(BaseModel):
    event_id: int = Literal[18]
    late_video_start: Optional[bool]


class InjuryStoppage(BaseModel):
    event_id: int = Literal[40]
    in_chain: Optional[bool]


class Interception(BaseModel):
    event_id: int = Literal[10]
    outcome: Optional[Outcome] = None  # e.g., {4: "Won", 1: "Lost"}


class Miscontrol(BaseModel):
    event_id: int = Literal[38]
    aerial_won: Optional[bool]


class Offside(BaseModel):
    event_id: int = Literal[8,]


class OwnGoalAgainst(BaseModel):
    event_id: int = Literal[20]


class OwnGoalFor(BaseModel):
    event_id: int = Literal[25]


class Pass(BaseModel):
    # event_id: int = Field(..., alias='id')
    recipient: Optional[Player] = None
    length: Optional[float] = None
    angle: Optional[float] = None
    height: Optional[Dict[str, Any]] = (
        None  # Expecting a dictionary but without strict typing for now
    )
    end_location: Optional[List[float]] = None
    assisted_shot_id: Optional[UUID] = None
    backheel: Optional[bool] = None
    deflected: Optional[bool] = None
    miscommunication: Optional[bool] = None
    cross: Optional[bool] = None
    cut_back: Optional[bool] = None
    switch: Optional[bool] = None
    shot_assist: Optional[bool] = None
    goal_assist: Optional[bool] = None
    body_part: Optional[BodyPart] = None
    type: Optional[EventType] = None
    outcome: Optional[Outcome] = None
    technique: Optional[Technique] = None

    class Config:
        allow_population_by_field_name = True


class PlayerOff(BaseModel):
    event_id: int = Literal[27]
    permanent: Optional[bool]


class PlayerOn(BaseModel):
    event_id: int = Literal[26]


class Pressure(BaseModel):
    event_id: int = Literal[17]
    counterpress: Optional[bool]


class RefereeBallDrop(BaseModel):
    event_id: int = Literal[41]


class Shield(BaseModel):
    event_id: int = Literal[28]


class Shot(BaseModel):
    event_id: int = Literal[16]
    key_pass_id: Optional[UUID] = None
    end_location: Optional[List[float]] = None
    aerial_won: Optional[bool] = None
    follows_dribble: Optional[bool] = None
    first_time: Optional[bool] = None
    freeze_frame: Optional[List[Dict[str, Any]]] = None
    open_goal: Optional[bool] = None
    statsbomb_xg: Optional[float] = None
    deflected: Optional[bool] = None
    technique: Optional[Technique] = (
        None  # e.g., {89: "Backheel", 94: "Overhead Kick", etc.}
    )
    body_part: Optional[BodyPart] = (
        None  # e.g., {40: "Right Foot", 38: "Left Foot", etc.}
    )
    type: Optional[EventType] = None  # e.g., {61: "Corner", 88: "Penalty", etc.}
    outcome: Optional[Outcome] = None  # e.g., {100: "Saved", 98: "Off T", etc.}


class StartingXI(BaseModel):
    event_id: int = Literal[35]
    tactics: Optional[Tactics]


class Substitution(BaseModel):
    event_id: int = Literal[19]
    replacement: Player
    outcome: Optional[Outcome] = None  # e.g., {103: "Tactical", 102: "Injury", etc.}


class TacticalShift(BaseModel):
    event_id: int = Literal[36]
    tactics: Tactics


class StatsBombEvent(BaseModel):
    id: UUID
    index: int
    period: int
    timestamp: str
    minute: int
    second: int
    type: EventType
    possession: int
    possession_team: Team
    play_pattern: dict
    team: Team
    duration: Optional[float] = None
    under_pressure: Optional[bool] = None
    off_camera: Optional[bool] = None
    out: Optional[bool] = None
    related_events: Optional[List[UUID]] = None
    location: Optional[List[float]] = None
    tactics: Optional[Tactics] = None
    pass_: Optional[Pass] = Field(None, alias="pass")
    shot: Optional[Shot] = None
    carry: Optional[Carry] = None
    pressure: Optional[Pressure] = None
    block: Optional[Block] = None
    duel: Optional[Duel] = None
    interception: Optional[Interception] = None
    clearance: Optional[Clearance] = None
    bad_behaviour: Optional[BadBehaviour] = None
    foul_committed: Optional[FoulCommitted] = None
    foul_won: Optional[FoulWon] = None
    dribble: Optional[Dribble] = None
    fifty_fifty: Optional[FiftyFifty] = Field(None, alias="50_50")
    injury_stoppage: Optional[InjuryStoppage] = None
    substitution: Optional[Substitution] = None
    goalkeeper: Optional[GoalKeeper] = None
    half_start: Optional[HalfStart] = None
    half_end: Optional[HalfEnd] = None
    player_off: Optional[PlayerOff] = None
    player_on: Optional[PlayerOn] = None
    shield: Optional[Shield] = None
    ball_recovery: Optional[BallRecovery] = None
    ball_receipt: Optional[BallReceipt] = None
    own_goal_against: Optional[OwnGoalAgainst] = None
    own_goal_for: Optional[OwnGoalFor] = None
    tactical_shift: Optional[TacticalShift] = None
    error: Optional[Error] = None
    dribbled_past: Optional[DribbledPast] = None
    miscontrol: Optional[Miscontrol] = None
    offside: Optional[Offside] = None
    referee_ball_drop: Optional[RefereeBallDrop] = None


class EventData(BaseModel):
    events: List[StatsBombEvent]
