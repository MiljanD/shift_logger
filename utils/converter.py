import pandas as pd
from reporting.exporter import Exporter

def convert_to_df(exported_data):
    columns = ["log_id", "card_id", "name", "check_in", "check_out"]
    df = pd.DataFrame(exported_data, columns=columns)

    df["duration"] = pd.to_datetime(df["check_out"]) - pd.to_datetime(df["check_in"])
    df["hours"] = df["duration"].dt.total_seconds() / 3600

    return df


if __name__ == "__main__":
    logs = Exporter()
    exp_data = logs.export_monthly_logs(year=2025, month=9)
    df1 = convert_to_df(exp_data)
    print(df1)