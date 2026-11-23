from datetime import datetime
import gspread
from gspread_formatting import CellFormat, Color, format_cell_range
import streamlit as st
from engine import ACTIVITY_MULTIPLIERS, DAILY_TASKS_EXP

SPREADSHEET_NAME = "levels example"
CREDENTIALS_FILE = "credentials.json"

# ფერების კოდები (RGB 0-დან 1-მდე)
GREEN_FILL = CellFormat(backgroundColor=Color(0.20, 0.66, 0.33))  # შესრულებული
RED_FILL = CellFormat(backgroundColor=Color(0.92, 0.26, 0.21))    # შეუსრულებელი

DAILY_COLUMN_MAP = {
    "ძილი": 2,
    "ჭამა 1": 3,
    "ჭამა 2": 4,
    "კბილები": 5,
    "მეცადინეობა": 6,
    "სუფთა ჰაერი": 7,
}


class SheetsManager:
    def __init__(self) -> None:
        # თუ აპლიკაცია ღრუბელშია (Streamlit Cloud), იყენებს st.secrets-ს,
        # ხოლო თუ კომპიუტერზეა გაშვებული — ლოკალურ credentials.json ფაილს.
        try:
            has_secrets = "gcp_service_account" in st.secrets
        except Exception:
            has_secrets = False

        if has_secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            self.client = gspread.service_account_from_dict(creds_dict)
        else:
            self.client = gspread.service_account(filename=CREDENTIALS_FILE)

        self.sheet = self.client.open(SPREADSHEET_NAME)
        self.daily_ws = self.sheet.worksheet("ყოველდღიური დავალებები")
        self.activities_ws = self.sheet.worksheet("აქტივობები")
        self.goals_ws = self.sheet.worksheet("მიზნები")

    def _today_str(self) -> str:
        return datetime.now().strftime("%d/%m/%Y")

    def _get_or_create_date_row(self, worksheet: gspread.Worksheet, date_str: str, is_daily: bool = False) -> int:
        """პოულობს თარიღის რიგს ან ქმნის ახალს ცხრილის ბოლოში."""
        dates = worksheet.col_values(1)
        if date_str in dates:
            return dates.index(date_str) + 1

        new_row_idx = len(dates) + 1
        if is_daily:
            row_data = [
                date_str, "", "", "", "", "", "",
                f'=COUNTIF(B{new_row_idx}:G{new_row_idx}, ">0")&"/6; "&TEXT(COUNTIF(B{new_row_idx}:G{new_row_idx}, ">0")/6, "0%")',
                f'=SUM(B{new_row_idx}:G{new_row_idx})'
            ]
            worksheet.append_row(row_data, value_input_option="USER_ENTERED")
        else:
            worksheet.append_row([date_str], value_input_option="USER_ENTERED")
        return new_row_idx

    def record_daily_task(self, task_name: str, completed: bool, date_str: str | None = None) -> int:
        """წერს ყოველდღიურ დავალებას შესაბამის სვეტში და აფერადებს."""
        target_date = date_str or self._today_str()
        row = self._get_or_create_date_row(self.daily_ws, target_date, is_daily=True)
        col = DAILY_COLUMN_MAP[task_name]

        # სახელების შესაბამისობა engine.py-სთან
        engine_key = {
            "კბილები": "კბილების ორჯერ გამოხეხვა",
            "სუფთა ჰაერი": "სუფთა ჰაერზე ყოფნა",
        }.get(task_name, task_name)

        base_exp = DAILY_TASKS_EXP[engine_key]
        delta = base_exp if completed else -base_exp

        self.daily_ws.update_cell(row, col, delta)
        cell_a1 = gspread.utils.rowcol_to_a1(row, col)
        format_cell_range(self.daily_ws, cell_a1, GREEN_FILL if completed else RED_FILL)
        return delta

    def record_activity(self, activity_name: str, category: str, completed: bool, date_str: str | None = None) -> int:
        """ამატებს აქტივობას დღის რიგში პირველივე თავისუფალ უჯრაში და აფერადებს."""
        target_date = date_str or self._today_str()
        row = self._get_or_create_date_row(self.activities_ws, target_date, is_daily=False)

        row_values = self.activities_ws.row_values(row)
        next_col = len(row_values) + 1 if len(row_values) >= 1 else 2

        raw = 5 if completed else -5
        delta = raw * ACTIVITY_MULTIPLIERS[category]

        self.activities_ws.update_cell(row, next_col, activity_name)
        cell_a1 = gspread.utils.rowcol_to_a1(row, next_col)
        format_cell_range(self.activities_ws, cell_a1, GREEN_FILL if completed else RED_FILL)
        return delta

    def add_goal(self, goal_name: str, deadline: str, difficulty: int, start_date: str | None = None) -> None:
        """ამატებს ახალ მიზანს ცხრილში."""
        start = start_date or self._today_str()
        next_row = len(self.goals_ws.col_values(1)) + 1
        formula = f'=IF(E{next_row}="შესრულებული", 5*D{next_row}, IF(E{next_row}="შეუსრულებელი", -5*D{next_row}, 0))'
        self.goals_ws.append_row([goal_name, start, deadline, difficulty, "აქტიური", formula], value_input_option="USER_ENTERED")

    def complete_goal(self, goal_name: str, completed: bool) -> int:
        """ცვლის მიზნის სტატუსს, აფერადებს და აბრუნებს მიღებულ/დაკლებულ ქულას."""
        cell = self.goals_ws.find(goal_name)
        if not cell:
            raise ValueError(f"მიზანი ვერ მოიძებნა: {goal_name}")
        row = cell.row
        difficulty = int(self.goals_ws.cell(row, 4).value)
        status_text = "შესრულებული" if completed else "შეუსრულებელი"

        self.goals_ws.update_cell(row, 5, status_text)
        cell_a1 = gspread.utils.rowcol_to_a1(row, 5)
        format_cell_range(self.goals_ws, cell_a1, GREEN_FILL if completed else RED_FILL)
        return (5 if completed else -5) * difficulty