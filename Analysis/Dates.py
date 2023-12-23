from enum import Enum
import datetime as dt
import pandas as pd


class Dates(Enum):
    START_DATE = (dt.datetime.today() - pd.DateOffset(days=365))
    END_DATE = dt.datetime.today()
