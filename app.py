"""
Life RPG — ერთფაილიანი აპლიკაცია (engine + Google Sheets + UI).
გაშვება: streamlit run app.py
"""
from __future__ import annotations

import json
import math
import os
from datetime import date, timedelta

import pandas as pd
import streamlit as st

# =====================================================================
# 1. ENGINE — ლეველები, EXP, კოეფიციენტები
# =====================================================================
BASE_EXP = 100               # EXP 1 -> 2 ლეველისთვის
STEP_EXP = 50                # ყოველ შემდეგ ლეველზე +50
STREAK_BONUS_PER_DAY = 0.02  # +2% ყოველ ზედიზედ დღეზე
STREAK_BONUS_CAP = 0.60      # მაქსიმუმ +60%
PENALTY_RATIO = 0.5          # ჯარიმა = ბაზური EXP-ის 50%
ACTIVITY_EXP_PER_30MIN = 20  # აქტივობა: 30 წუთი = 20 EXP (სირთულეზე მრავლდება)
DIFFICULTY = {"მარტივი": 1.0, "საშუალო": 1.5, "რთული": 2.0, "ეპიკური": 3.0}


def to_int(x: float) -> int:
    return int(math.floor(x + 0.5))


def num(x, default=0) -> int:
    try:
        return int(float(str(x).replace(",", ".").strip()))
    except (ValueError, TypeError):
        return default


def exp_for_level_up(level: int) -> int:
    return BASE_EXP + STEP_EXP * (level - 1)


def total_exp_to_reach(level: int) -> int:
    n = level - 1
    return BASE_EXP * n + STEP_EXP * n * (n - 1) // 2


def level_from_exp(total_exp: int) -> int:
    total_exp = max(0, total_exp)
    level = 1
    # სწრაფი მიახლოება, შემდეგ ზუსტი კორექცია
    a, b = STEP_EXP / 2, BASE_EXP - STEP_EXP / 2
    level = max(1, int((-b + math.sqrt(b * b + 4 * a * total_exp)) / (2 * a)) + 1)
    while total_exp_to_reach(level + 1) <= total_exp:
        level += 1
    while level > 1 and total_exp_to_reach(level) > total_exp:
        level -= 1
    return level


def get_progress(total_exp: int, peak_level: int = 1) -> dict:
    """ლეველი არასდროს ეცემა: გამოიყენება ისტორიული მაქსიმუმი."""
    total_exp = max(0, int(total_exp))
    level = max(level_from_exp(total_exp), int(peak_level), 1)
    needed = exp_for_level_up(level)
    in_level = min(max(0, total_exp - total_exp_to_reach(level)), needed)
    return {
        "level": level, "total": total_exp, "in_level": in_level,
        "needed": needed, "remaining": needed - in_level,
        "ratio": in_level / needed,
    }


def streak_multiplier(streak: int) -> float:
    return 1.0 + min(max(streak, 0) * STREAK_BONUS_PER_DAY, STREAK_BONUS_CAP)


def exp_reward(base: float, difficulty: str, streak: int = 0) -> int:
    return to_int(base * DIFFICULTY.get(difficulty, 1.0) * streak_multiplier(streak))


def exp_penalty(base: float, difficulty: str) -> int:
    return to_int(base * DIFFICULTY.get(difficulty, 1.0) * PENALTY_RATIO)


def activity_exp(minutes: int, difficulty: str) -> int:
    return to_int(minutes / 30 * ACTIVITY_EXP_PER_30MIN * DIFFICULTY.get(difficulty, 1.0))


def replay_ledger(ledger: list[tuple[str, int]]) -> tuple[int, int]:
    """(თარიღი, ცვლილება) სიიდან აბრუნებს (საბოლოო EXP, მიღწეული მაქსიმალური ლეველი)."""
    total, peak = 0, 1
    for _, delta in sorted(ledger, key=lambda t: t[0]):
        total = max(0, total + delta)
        peak = max(peak, level_from_exp(total))
    return total, peak


def current_streak(done_dates: set[str], today: date) -> int:
    """ზედიზედ დღეები, როცა ≥1 დავალება შესრულდა (დღევანდელი ჯერ არ აკლდება სტრიკს)."""
    d = today if today.isoformat() in done_dates else today - timedelta(days=1)
    n = 0
    while d.isoformat() in done_dates:
        n += 1
        d -= timedelta(days=1)
    return n


# =====================================================================
# 2. GOOGLE SHEETS — სინქრონიზაცია და ფორმატირება
# =====================================================================
SHEET_NAME = "levels example"
TAB_TASKS, TAB_ACTS, TAB_GOALS = "ყოველდღიური დავალებები", "აქტივობები", "მიზნები"
HEADERS = {
    TAB_TASKS: ["თარიღი", "დავალება", "სირთულე", "ბაზური EXP", "სტატუსი", "EXP ცვლილება"],
    TAB_ACTS: ["თარიღი", "აქტივობა", "კატეგორია", "წუთები", "სირთულე", "EXP"],
    TAB_GOALS: ["მიზანი", "ვადა", "სირთულე", "ბაზური EXP", "სტატუსი", "დასრულების თარიღი", "მიღებული EXP"],
}
GREEN, RED, YELLOW = (0.72, 0.88, 0.72), (0.96, 0.73, 0.73), (1.0, 0.95, 0.70)
STATUS_COL = {TAB_TASKS: "E", TAB_GOALS: "E"}
STATUS_COLORS = {
    TAB_TASKS: [("შესრულდა", GREEN), ("ვერ შესრულდა", RED), ("მოლოდინში", YELLOW)],
    TAB_GOALS: [("შესრულებული", GREEN), ("აქტიური", YELLOW)],
}


class SheetsError(Exception):
    pass


@st.cache_resource(show_spinner="Google Sheets-თან კავშირი...")
def get_spreadsheet():
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" in st.secrets:          # Streamlit Cloud
            info = dict(st.secrets["gcp_service_account"])
        elif os.path.exists("credentials.json"):          # ლოკალურად
            with open("credentials.json", encoding="utf-8") as f:
                info = json.load(f)
        else:
            raise SheetsError(
                "ვერ მოიძებნა სერვის-ექაუნთის გასაღები: ლოკალურად დადე credentials.json, "
                "ღრუბელში კი Secrets-ში [gcp_service_account] ბლოკი.")
        client = gspread.authorize(Credentials.from_service_account_info(info, scopes=scopes))
        name = st.secrets.get("sheet_name", SHEET_NAME) if "sheet_name" in st.secrets else SHEET_NAME
        sh = client.open(name)
        _ensure_tabs(sh)
        return sh
    except SheetsError:
        raise
    except Exception as e:  # noqa: BLE001
        raise SheetsError(f"{type(e).__name__}: {e}") from e


def _ensure_tabs(sh) -> None:
    """ქმნის ტაბებს/სათაურებს, თუ არ არსებობს, და ერთხელ აფორმატებს."""
    import gspread

    existing = {w.title: w for w in sh.worksheets()}
    for tab, headers in HEADERS.items():
        ws = existing.get(tab) or sh.add_worksheet(tab, rows=1000, cols=len(headers))
        if ws.row_values(1)[: len(headers)] != headers:
            ws.update(range_name="A1", values=[headers])
        try:
            _format(ws, tab, len(headers))
        except Exception:  # ფორმატირება კრიტიკული არ არის
            pass


def _format(ws, tab: str, ncols: int) -> None:
    from gspread.utils import rowcol_to_a1
    from gspread_formatting import (BooleanCondition, BooleanRule, CellFormat, Color,
                                    ConditionalFormatRule, GridRange, TextFormat,
                                    format_cell_range, get_conditional_format_rules)

    last = rowcol_to_a1(1, ncols)
    format_cell_range(ws, f"A1:{last}", CellFormat(
        backgroundColor=Color(0.17, 0.2, 0.32),
        textFormat=TextFormat(bold=True, foregroundColor=Color(1, 1, 1))))
    ws.freeze(rows=1)
    if tab in STATUS_COL:
        col = STATUS_COL[tab]
        rules = get_conditional_format_rules(ws)
        rules.clear()
        for text, rgb in STATUS_COLORS[tab]:
            rules.append(ConditionalFormatRule(
                ranges=[GridRange.from_a1_range(f"{col}2:{col}1000", ws)],
                booleanRule=BooleanRule(
                    condition=BooleanCondition("TEXT_EQ", [text]),
                    format=CellFormat(backgroundColor=Color(*rgb)))))
        rules.save()


@st.cache_data(ttl=30, show_spinner=False)
def read_tab(tab: str) -> list[dict]:
    try:
        return get_spreadsheet().worksheet(tab).get_all_records()
    except SheetsError:
        raise
    except Exception as e:  # noqa: BLE001
        raise SheetsError(f"ვერ წავიკითხე „{tab}“: {e}") from e


def append_row(tab: str, row: list) -> None:
    try:
        get_spreadsheet().worksheet(tab).append_row(row, value_input_option="USER_ENTERED")
        read_tab.clear()
    except Exception as e:  # noqa: BLE001
        raise SheetsError(f"ჩაწერა ვერ მოხერხდა „{tab}“: {e}") from e


def update_cells(tab: str, row_idx: int, first_col: str, values: list) -> None:
    """row_idx — Sheets-ის რეალური სტრიქონის ნომერი (სათაური = 1)."""
    try:
        ws = get_spreadsheet().worksheet(tab)
        end_col = chr(ord(first_col) + len(values) - 1)
        ws.update(range_name=f"{first_col}{row_idx}:{end_col}{row_idx}", values=[values])
        read_tab.clear()
    except Exception as e:  # noqa: BLE001
        raise SheetsError(f"განახლება ვერ მოხერხდა „{tab}“: {e}") from e


# =====================================================================
# 3. UI
# =====================================================================
st.set_page_config(page_title="Life RPG", page_icon="⚔️", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
.block-container {padding: 1rem 1rem 4rem; max-width: 1100px;}
.stButton > button, .stFormSubmitButton > button {
    width: 100%; min-height: 3rem; font-size: 1.05rem; border-radius: 12px;}
.card {background: rgba(128,128,160,.12); border: 1px solid rgba(128,128,160,.25);
    border-radius: 16px; padding: 1rem 1.2rem; margin-bottom: .8rem;}
.lvl {font-size: 2.6rem; font-weight: 800; line-height: 1;}
.sub {opacity: .7; font-size: .9rem;}
.bar {height: 16px; border-radius: 10px; background: rgba(128,128,160,.25); overflow: hidden;}
.bar > div {height: 100%; background: linear-gradient(90deg,#6a5cff,#00c2a8);}
.task {display:flex; justify-content:space-between; gap:.5rem; padding:.2rem 0;}
@media (max-width: 640px) {
  .block-container {padding: .6rem .6rem 4rem;}
  .lvl {font-size: 2.1rem;}
}
</style>
""", unsafe_allow_html=True)


def load_all():
    return read_tab(TAB_TASKS), read_tab(TAB_ACTS), read_tab(TAB_GOALS)


def build_ledger(tasks, acts, goals):
    ledger = []
    for r in tasks:
        if r.get("სტატუსი") in ("შესრულდა", "ვერ შესრულდა"):
            ledger.append((str(r.get("თარიღი", "")), num(r.get("EXP ცვლილება"))))
    for r in acts:
        ledger.append((str(r.get("თარიღი", "")), num(r.get("EXP"))))
    for r in goals:
        if r.get("სტატუსი") == "შესრულებული":
            ledger.append((str(r.get("დასრულების თარიღი", "")), num(r.get("მიღებული EXP"))))
    return ledger


st.title("⚔️ Life RPG")

try:
    tasks, acts, goals = load_all()
except SheetsError as e:
    st.error(f"Google Sheets-თან კავშირი ვერ დამყარდა.\n\n**მიზეზი:** {e}")
    st.info("შეამოწმე: 1) გასაღები (credentials.json / Secrets); 2) ცხრილი სახელად "
            f"„{SHEET_NAME}“ გაზიარებულია სერვის-ექაუნთის ელფოსტაზე (Editor); "
            "3) ჩართულია Google Sheets API და Drive API.")
    if st.button("🔄 თავიდან ცდა"):
        get_spreadsheet.clear()
        read_tab.clear()
        st.rerun()
    st.stop()

today = date.today()
today_s = today.isoformat()
total, peak = replay_ledger(build_ledger(tasks, acts, goals))
prog = get_progress(total, peak)
done_dates = {str(r.get("თარიღი")) for r in tasks if r.get("სტატუსი") == "შესრულდა"}
streak = current_streak(done_dates, today)

# ---- მთავარი ბარათი ----
st.markdown(f"""
<div class="card">
  <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:1rem; flex-wrap:wrap;">
    <div><div class="sub">ლეველი</div><div class="lvl">{prog['level']}</div></div>
    <div style="text-align:right"><div class="sub">სულ EXP</div>
      <div style="font-size:1.6rem;font-weight:700">{prog['total']:,}</div></div>
    <div style="text-align:right"><div class="sub">სტრიკი 🔥</div>
      <div style="font-size:1.6rem;font-weight:700">{streak} დღე</div></div>
  </div>
  <div class="bar" style="margin:.8rem 0 .3rem"><div style="width:{prog['ratio']*100:.1f}%"></div></div>
  <div class="sub">{prog['in_level']} / {prog['needed']} EXP · შემდეგ ლეველამდე დარჩა
     <b>{prog['remaining']}</b> · სტრიკის ბონუსი ×{streak_multiplier(streak):.2f}</div>
</div>
""", unsafe_allow_html=True)

tab_today, tab_acts, tab_goals, tab_stats = st.tabs(
    ["📋 დღეს", "🏃 აქტივობები", "🎯 მიზნები", "📊 სტატისტიკა"])


def safe(fn, *a, **kw):
    try:
        fn(*a, **kw)
        st.rerun()
    except SheetsError as e:
        st.error(str(e))


# ---- დღეს ----
with tab_today:
    with st.form("add_task", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 1.3, 1])
        title = c1.text_input("ახალი დავალება", placeholder="მაგ. 30 წთ იტალიური")
        diff = c2.selectbox("სირთულე", list(DIFFICULTY))
        base = c3.number_input("ბაზური EXP", 1, 1000, 20, step=5)
        if st.form_submit_button("➕ დამატება") and title.strip():
            safe(append_row, TAB_TASKS, [today_s, title.strip(), diff, int(base), "მოლოდინში", 0])

    pending = [(i + 2, r) for i, r in enumerate(tasks) if r.get("სტატუსი") == "მოლოდინში"]
    st.subheader(f"მოლოდინში ({len(pending)})")
    if not pending:
        st.caption("ყველაფერი დახურულია 🎉")
    for row_idx, r in pending:
        b = num(r.get("ბაზური EXP"), 10)
        d = str(r.get("სირთულე", "მარტივი"))
        gain, loss = exp_reward(b, d, streak), exp_penalty(b, d)
        st.markdown(f"<div class='card'><b>{r.get('დავალება')}</b>"
                    f"<div class='sub'>{r.get('თარიღი')} · {d} · +{gain} / −{loss} EXP</div></div>",
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button(f"✅ +{gain}", key=f"ok{row_idx}"):
            safe(update_cells, TAB_TASKS, row_idx, "E", ["შესრულდა", gain])
        if c2.button(f"❌ −{loss}", key=f"no{row_idx}"):
            safe(update_cells, TAB_TASKS, row_idx, "E", ["ვერ შესრულდა", -loss])

    closed_today = [r for r in tasks if str(r.get("თარიღი")) == today_s
                    and r.get("სტატუსი") in ("შესრულდა", "ვერ შესრულდა")]
    if closed_today:
        st.subheader("დღეს დახურული")
        for r in closed_today:
            icon = "✅" if r["სტატუსი"] == "შესრულდა" else "❌"
            st.write(f"{icon} {r['დავალება']} · **{num(r.get('EXP ცვლილება')):+d}** EXP")

# ---- აქტივობები ----
with tab_acts:
    with st.form("add_act", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("აქტივობა", placeholder="მაგ. ცურვა")
        cat = c2.selectbox("კატეგორია", ["სპორტი", "სწავლა", "პროგრამირება", "წიგნი", "სხვა"])
        c3, c4 = st.columns(2)
        mins = c3.number_input("წუთები", 5, 600, 30, step=5)
        diff = c4.selectbox("სირთულე", list(DIFFICULTY), key="act_diff")
        pts = activity_exp(int(mins), diff)
        st.caption(f"მიიღებ: **+{pts} EXP**")
        if st.form_submit_button("➕ ჩაწერა") and name.strip():
            safe(append_row, TAB_ACTS, [today_s, name.strip(), cat, int(mins), diff, pts])
    if acts:
        st.dataframe(pd.DataFrame(acts).iloc[::-1].head(30), use_container_width=True, hide_index=True)

# ---- მიზნები ----
with tab_goals:
    with st.form("add_goal", clear_on_submit=True):
        goal = st.text_input("ახალი მიზანი", placeholder="მაგ. IELTS/CILS C2 ჩაბარება")
        c1, c2, c3 = st.columns(3)
        due = c1.date_input("ვადა", today + timedelta(days=30))
        diff = c2.selectbox("სირთულე", list(DIFFICULTY), index=2, key="goal_diff")
        base = c3.number_input("ბაზური EXP", 10, 10000, 200, step=10)
        if st.form_submit_button("➕ მიზნის დამატება") and goal.strip():
            safe(append_row, TAB_GOALS, [goal.strip(), due.isoformat(), diff, int(base), "აქტიური", "", 0])

    active = [(i + 2, r) for i, r in enumerate(goals) if r.get("სტატუსი") == "აქტიური"]
    st.subheader(f"აქტიური ({len(active)})")
    for row_idx, r in active:
        d = str(r.get("სირთულე", "მარტივი"))
        gain = exp_reward(num(r.get("ბაზური EXP"), 100), d, 0)
        left = (date.fromisoformat(str(r["ვადა"])) - today).days if r.get("ვადა") else None
        left_txt = "" if left is None else (f" · დარჩა {left} დღე" if left >= 0 else f" · ვადა გავიდა {-left} დღით")
        st.markdown(f"<div class='card'><b>{r.get('მიზანი')}</b>"
                    f"<div class='sub'>{d}{left_txt} · +{gain} EXP</div></div>", unsafe_allow_html=True)
        if st.button(f"🏆 დასრულება (+{gain})", key=f"g{row_idx}"):
            safe(update_cells, TAB_GOALS, row_idx, "E", ["შესრულებული", today_s, gain])
    finished = [r for r in goals if r.get("სტატუსი") == "შესრულებული"]
    if finished:
        st.subheader(f"შესრულებული ({len(finished)})")
        for r in finished:
            st.write(f"🏆 {r['მიზანი']} · {r.get('დასრულების თარიღი')} · +{num(r.get('მიღებული EXP'))} EXP")

# ---- სტატისტიკა ----
with tab_stats:
    per_day: dict[str, int] = {}
    for d_s, delta in build_ledger(tasks, acts, goals):
        if d_s:
            per_day[d_s] = per_day.get(d_s, 0) + delta
    days = [(today - timedelta(days=i)).isoformat() for i in range(13, -1, -1)]
    df = pd.DataFrame({"EXP": [per_day.get(d, 0) for d in days]}, index=days)
    st.subheader("EXP ბოლო 14 დღეში")
    st.bar_chart(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("მაქს. ლეველი", prog["level"])
    c2.metric("შესრულებული დავალებები", sum(r.get("სტატუსი") == "შესრულდა" for r in tasks))
    c3.metric("შესრულებული მიზნები", len(finished))
    if st.button("🔄 განახლება Sheets-იდან"):
        read_tab.clear()
        st.rerun()