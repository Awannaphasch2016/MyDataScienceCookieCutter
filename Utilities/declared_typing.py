import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from typing_extensions import TypedDict

PerDayAverage = Dict[str, float]
SavedData = Dict[str, Dict[str, List]]
RunningConditions = Dict[str, str]

class RunningCondition(TypedDict):
    cralwer_option: str
    collection_name: str
    respond_type: str
    search_type: str

Url = str
Json = Dict


class SubredditCollection(TypedDict):
    collection: List[str]
    name: str

class RunningConstraints(TypedDict):
    aggs: str
    frequency: str
    after: int
    before: Optional[int]
    size: int
    metadata: str
    sort: str
    fields: str

class RedditCralwerCondition(TypedDict):
    subreddit_collection_class: SubredditCollection
    initial_day_interval: int
    request_timestamp: str
    respond_type: str
    search_type: str
