import streamlit as st
from datetime import date
from engine import (
    ACTIVITY_MULTIPLIERS,
    DAILY_TASKS_EXP,
    PlayerProgress,
    exp_needed_for_level,
    total_exp_for_level,
)
from sheets_sync import SheetsManager

st.set_page_config(page_title="Life RPG Tracker", page_icon="⚡", layout="centered")

# ლოკალური მდგომარეობის ინიციალიზაცია
if "player" not in st.session_state:
    st.session_state.player = PlayerProgress()

if "sheets" not in st.session_state:
    st.session_state.sheets = None
    st.session_state.sheets_error = None
    try:
        st.session_state.sheets = SheetsManager()
    except Exception as e:
        st.session_state.sheets_error = str(e)

player: PlayerProgress = st.session_state.player
sheets: SheetsManager | None = st.session_state.sheets

# --- ზედა ბლოკი: ლეველი და EXP ---
st.title("⚡ Life RPG Tracker")

next_lvl_total = total_exp_for_level(player.level + 1)
prev_lvl_total = total_exp_for_level(player.level)
needed_for_next = max(1, next_lvl_total - prev_lvl_total)
current_in_lvl = max(0, player.exp - prev_lvl_total)
progress_ratio = min(1.0, max(0.0, current_in_lvl / needed_for_next))

col1, col2, col3 = st.columns(3)
col1.metric("ლეველი", player.level)
col2.metric("ჯამური EXP", f"{player.exp:+d}")
col3.metric("შემდეგ ლეველამდე", f"{max(0, next_lvl_total - player.exp)} EXP")

st.progress(progress_ratio)

if st.session_state.sheets_error:
    st.warning(f"Google Sheets-თან კავშირი ვერ მოხერხდა (იმუშავებს მხოლოდ ლოკალური ლოგიკა): {st.session_state.sheets_error}")
else:
    st.success("Google Sheets დაკავშირებულია (`levels example`)")

st.divider()

# --- ტაბები 3 კატეგორიისთვის ---
tab_daily, tab_activity, tab_goal, tab_stats = st.tabs([
    "📅 ყოველდღიური",
    "🏃 აქტივობები",
    "🎯 მიზნები",
    "📊 რეიტინგი და ლოგი",
])

# 1. ყოველდღიური დავალებები
with tab_daily:
    st.subheader("ყოველდღიური დავალებები")
    selected_date = st.date_input("თარიღი", value=date.today(), key="daily_date")
    date_str = selected_date.strftime("%d/%m/%Y")

    # ცხრილის სვეტების შესაბამისი სახელები
    ui_to_engine_task = {
        "ძილი": "ძილი",
        "ჭამა 1": "ჭამა 1",
        "ჭამა 2": "ჭამა 2",
        "კბილები": "კბილების ორჯერ გამოხეხვა",
        "მეცადინეობა": "მეცადინეობა",
        "სუფთა ჰაერი": "სუფთა ჰაერზე ყოფნა",
    }

    for sheet_task_name, engine_task_name in ui_to_engine_task.items():
        pts = DAILY_TASKS_EXP[engine_task_name]
        c1, c2, c3 = st.columns([4, 1.5, 1.5])
        c1.write(f"**{sheet_task_name}** (`+{pts}` / `-{pts} EXP`)")

        if c2.button("✅ შესრულდა", key=f"ok_{sheet_task_name}"):
            delta = player.log_daily_task(engine_task_name, completed=True)
            if sheets:
                sheets.record_daily_task(sheet_task_name, completed=True, date_str=date_str)
            st.toast(f"{sheet_task_name}: {delta:+d} EXP")
            st.rerun()

        if c3.button("❌ არა", key=f"no_{sheet_task_name}"):
            delta = player.log_daily_task(engine_task_name, completed=False)
            if sheets:
                sheets.record_daily_task(sheet_task_name, completed=False, date_str=date_str)
            st.toast(f"{sheet_task_name}: {delta:+d} EXP")
            st.rerun()

# 2. აქტივობები
with tab_activity:
    st.subheader("აქტივობის ჩაწერა")
    act_date = st.date_input("თარიღი", value=date.today(), key="act_date").strftime("%d/%m/%Y")
    act_name = st.text_input("მოქმედების სახელი (მაგ: ვარჯიში, კითხვა, სირბილი)")
    act_category = st.selectbox("კატეგორია", list(ACTIVITY_MULTIPLIERS.keys()))
    st.caption(f"კატეგორიის კოეფიციენტი: **×{ACTIVITY_MULTIPLIERS[act_category]}** -> შედეგი იქნება **`{5 * ACTIVITY_MULTIPLIERS[act_category]:+d}`** ან **`{-5 * ACTIVITY_MULTIPLIERS[act_category]:+d} EXP`**")

    b1, b2 = st.columns(2)
    if b1.button("✅ შესრულდა ბოლომდე", use_container_width=True):
        label = act_name.strip() or act_category
        delta = player.log_activity(act_category, completed=True)
        if sheets:
            sheets.record_activity(label, act_category, completed=True, date_str=act_date)
        st.success(f"ჩაიწერა: {label} ({delta:+d} EXP)")
        st.rerun()

    if b2.button("❌ დაწყებული / არ დასრულდა", use_container_width=True):
        label = act_name.strip() or act_category
        delta = player.log_activity(act_category, completed=False)
        if sheets:
            sheets.record_activity(label, act_category, completed=False, date_str=act_date)
        st.error(f"ჩაიწერა: {label} ({delta:+d} EXP)")
        st.rerun()

# 3. მიზნები
with tab_goal:
    st.subheader("ახალი მიზნის დამატება")
    goal_name = st.text_input("მიზნის დასახელება")
    g_col1, g_col2 = st.columns(2)
    deadline = g_col1.date_input("დედლაინი", key="goal_deadline").strftime("%d/%m/%Y")
    difficulty = g_col2.number_input("სირთულე / კოეფიციენტი", min_value=1, max_value=100, value=10, step=1)

    if st.button("➕ მიზნის დამატება ცხრილში"):
        if goal_name.strip():
            if sheets:
                sheets.add_goal(goal_name.strip(), deadline=deadline, difficulty=int(difficulty))
            st.success(f"მიზანი დაემატა: {goal_name.strip()}")
        else:
            st.warning("ჯერ ჩაწერე მიზნის სახელი.")

    st.divider()
    st.subheader("მიზნის შედეგის დაფიქსირება")
    target_goal = st.text_input("მიზნის ზუსტი სახელი (როგორც ცხრილშია)")
    target_mult = st.number_input("მიზნის კოეფიციენტი EXP-ის გამოსათვლელად", min_value=1, max_value=100, value=int(difficulty), step=1, key="goal_mult_eval")

    g_b1, g_b2 = st.columns(2)
    if g_b1.button("🏆 მიზანი შესრულდა", use_container_width=True):
        if target_goal.strip():
            delta = player.log_goal(target_goal.strip(), multiplier=int(target_mult), completed=True)
            if sheets:
                sheets.complete_goal(target_goal.strip(), completed=True)
            st.success(f"მიზანი შესრულდა! {delta:+d} EXP")
            st.rerun()

    if g_b2.button("💥 მიზანი ჩავარდა", use_container_width=True):
        if target_goal.strip():
            delta = player.log_goal(target_goal.strip(), multiplier=int(target_mult), completed=False)
            if sheets:
                sheets.complete_goal(target_goal.strip(), completed=False)
            st.error(f"მიზანი ჩავარდა! {delta:+d} EXP")
            st.rerun()

# 4. დაყოფილი რეიტინგი და ისტორია
with tab_stats:
    st.subheader("დაყოფილი რეიტინგი (EXP კატეგორიების მიხედვით)")
    for cat, pts in player.category_exp.items():
        st.write(f"- **{cat}:** `{pts:+d} EXP`")

    st.divider()
    st.subheader("ბოლო მოქმედებების ლოგი")
    if player.history:
        for item in reversed(player.history):
            st.text(item)
    else:
        st.info("ჯერ ქმედებები არ ჩაწერილა ამ სესიაში.")