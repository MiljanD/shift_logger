
from datetime import datetime
from fpdf import FPDF
from numpy.ma.extras import average
from utils.converter import convert_to_df, convert_cell_value_to_str
from utils.time_utils import convert_datetime_to_date
from reporting.exporter import Exporter
from pathlib import Path


class ReportGenerator(FPDF):
    def __init__(self):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.export = Exporter()


    def generate_daily_pdf_report(self, current_date):
        self.add_page()
        raw_data = self.export.export_logs_by_day(date=current_date)
        df_formed_data = convert_to_df(raw_data)
        columns = df_formed_data.columns

        self.generate_daily_log_table(columns, df_formed_data)

        folder_path = Path(__name__).parent
        self.output(f"{folder_path}/daily_reports/{current_date.date()}.pdf")



    def generate_daily_log_table(self, columns, extracted_df):
        for column in columns:
            if "_" in column:
                column_title = column.replace("_", " ").title()
            else:
                column_title = column.title()

            self.set_font(family="Times", size=12, style="B")
            self.set_text_color(80, 80, 80)
            if column == columns[-1]:
                self.cell(w=30, h=8, txt=column_title, border=1, ln=1)
            elif column == "check_in" or column == "check_out":
                self.cell(w=35, h=8, txt=column_title, border=1)
            else:
                self.cell(w=30, h=8, txt=column_title, border=1)

        for index, row in extracted_df.iterrows():
            for idx in range(len(columns)):
                cell_value = convert_cell_value_to_str(row[columns[idx]])
                self.set_font(family="Times", size=10)
                self.set_text_color(80, 80, 80)
                if columns[idx] == "time +/-":
                    self.cell(w=30, h=8, txt=cell_value, border=1, ln=1)
                elif columns[idx] == "check_in" or columns[idx] == "check_out":
                    self.cell(w=35, h=8, txt=cell_value, border=1)
                else:
                    self.cell(w=30, h=8, txt=cell_value, border=1)


    def generate_weekly_report(self, year, week):
        self.add_page()

        raw_data = self.export.export_weekly_logs(year=year, week=week)
        df_weekly_data = convert_to_df(raw_data)
        worker_based_df = self.generate_pivot_df(df_weekly_data)
        columns = worker_based_df.columns

        self.generate_multi_day_log_table(columns, worker_based_df)

        folder_path = Path(__name__).parent
        self.output(f"{folder_path}/weekly_reports/calendar_week_{week}.pdf")


    def generate_monthly_report(self, year, month):
        self.add_page()

        raw_data = self.export.export_monthly_logs()
        df_monthly_data = convert_to_df(raw_data)
        worker_based_df = self.generate_pivot_df(df_monthly_data)
        columns = worker_based_df.columns

        self.generate_multi_day_log_table(columns, worker_based_df)

        folder_path = Path(__name__).parent
        self.output(f"{folder_path}/monthly_reports/{month}_{year}.pdf")



    def generate_multi_day_log_table(self, columns, extracted_df):
        for column in columns:
            if "_" in column:
                column_title = column.replace("_", " ").title()
            else:
                column_title = column.title()

            self.set_font(family="Times", size=12, style="B")
            self.set_text_color(80, 80, 80)
            if column == columns[-1]:
                self.cell(w=45, h=8, txt=column_title, border=1, ln=1)
            else:
                self.cell(w=30, h=8, txt=column_title, border=1)

        for index, row in extracted_df.iterrows():
            for idx in range(len(columns)):
                cell_value = convert_cell_value_to_str(row[columns[idx]])
                self.set_font(family="Times", size=10)
                self.set_text_color(80, 80, 80)
                if columns[idx] == "avg worked hours":
                    self.cell(w=45, h=8, txt=cell_value, border=1, ln=1)
                else:
                    self.cell(w=30, h=8, txt=cell_value, border=1)




    def generate_pivot_df(self, extracted_df):
        dates = {convert_datetime_to_date(date) for date in extracted_df["check_in"]}
        print(dates)
        pivot_df = extracted_df.groupby("name").agg({
            "hours": "sum",
            "time +/-": "sum"
        }).reset_index()
        pivot_df["hours"] = round(pivot_df["hours"], 2)
        pivot_df["time +/-"] = round(pivot_df["time +/-"], 2)
        pivot_df["worked days"] = round(pivot_df["hours"] / 8, 0)
        pivot_df["avg worked hours"] = round(pivot_df["hours"] / len(dates), 2)

        return pivot_df

