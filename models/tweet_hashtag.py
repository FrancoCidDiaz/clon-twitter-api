from sqlalchemy import Table, Column, Integer, UniqueConstraint, ForeignKey
from config.db import meta, engine
from datetime import datetime


tweet_hashtags = Table(
    "tweet_hashtags", meta,
    Column("tweet_id", Integer, ForeignKey("tweets.id"), nullable=False),  # Clave foránea a tweets
    Column("hashtag_id", Integer, ForeignKey("hashtags.id"), nullable=False),  # Clave foránea a hashtags
    UniqueConstraint("tweet_id", "hashtag_id", name="uq_tweet_hashtag")  # Asegúrate de que la relación sea única
)


meta.create_all(engine)