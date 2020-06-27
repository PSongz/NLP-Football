CONNECTION_STRING = "sqlite:///tweets.db"
CSV_NAME = "EPL_tweets.csv"
TABLE_NAME = "EPL"

try:
    from private import *
except Exception:
    pass