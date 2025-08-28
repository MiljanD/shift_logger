
from reporting.exporter import Exporter
from datetime import datetime
import pandas as pd


def convert_to_df(exported_data):
    columns = ["log_id", "card_id", "name", "check_in", "check_out"]
    df = pd.DataFrame(exported_data, columns=columns)

    df["duration"] = pd.to_datetime(df["check_out"]) - pd.to_datetime(df["check_in"])
    df["hours"] = round(df["duration"].dt.total_seconds() / 3600, 2)
    df["time +/-"] = round(df["hours"] - 8, 2)

    return df


def convert_cell_value_to_str(value):
    if pd.isna(value):
        return "-"
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return str(value)
