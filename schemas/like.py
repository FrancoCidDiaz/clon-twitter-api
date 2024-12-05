from pydantic import BaseModel

class Like(BaseModel):
    user_id: int
    tweet_id: int
