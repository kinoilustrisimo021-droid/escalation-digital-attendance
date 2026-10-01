from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st


TEAM_NAME = "Escalation & Digital"
TIMEZONE = ZoneInfo("Asia/Singapore")
DATA_FILE = Path(__file__).with_name("attendance_records.csv")
STATUSES = ("Ontime", "Late", "Halfday", "Absent")
STATUS_ALIASES = {"On time": "Ontime", "Half day": "Halfday"}


st.set_page_config(
    page_title=f"{TEAM_NAME} Attendance",
    page_icon="✓",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def save_attendance(date_value: str, first_name: str, last_name: str, status: str) -> None:
    """Append one attendance entry to a CSV file beside the app."""
    is_new_file = not DATA_FILE.exists()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if is_new_file:
            writer.writerow(
                ["date", "first_name", "last_name", "full_name", "status", "submitted_at"]
            )
        writer.writerow(
            [
                date_value,
                first_name,
                last_name,
                f"{first_name} {last_name}",
                status,
                datetime.now(TIMEZONE).isoformat(timespec="seconds"),
            ]
        )


def load_attendance() -> list[dict[str, str]]:
    """Load valid attendance rows for the monthly summary."""
    if not DATA_FILE.exists():
        return []

    records: list[dict[str, str]] = []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            try:
                datetime.strptime(row.get("date", ""), "%Y-%m-%d")
            except (TypeError, ValueError):
                continue

            normalized_status = STATUS_ALIASES.get(
                row.get("status", ""), row.get("status", "")
            )
            if normalized_status not in STATUSES:
                continue

            row["status"] = normalized_status
            records.append(row)

    return records


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');

        :root {
            --ink: #172137;
            --muted: #6f7890;
            --primary: #5b5bd6;
            --primary-dark: #4747b9;
            --teal: #30bca8;
            --surface: rgba(255, 255, 255, 0.88);
        }

        html, body, [class*="css"] {
            font-family: "DM Sans", sans-serif;
        }

        .stApp {
            color: var(--ink);
            background:
                radial-gradient(circle at 10% 8%, rgba(91, 91, 214, .13), transparent 26%),
                radial-gradient(circle at 92% 88%, rgba(48, 188, 168, .15), transparent 26%),
                linear-gradient(145deg, #f8f9ff 0%, #f1f5fc 52%, #f7fbfa 100%);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: .35;
            background-image:
                linear-gradient(rgba(75, 86, 121, .06) 1px, transparent 1px),
                linear-gradient(90deg, rgba(75, 86, 121, .06) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: linear-gradient(to bottom, black, transparent 80%);
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 760px;
            padding-top: 3.2rem;
            padding-bottom: 3rem;
        }

        .ambient {
            position: fixed;
            border-radius: 999px;
            pointer-events: none;
            filter: blur(2px);
            z-index: 0;
        }

        .orb-one {
            width: 180px;
            height: 180px;
            top: 12%;
            left: -55px;
            background: linear-gradient(135deg, rgba(91, 91, 214, .22), rgba(130, 116, 236, .05));
            animation: float-one 10s ease-in-out infinite;
        }

        .orb-two {
            width: 230px;
            height: 230px;
            right: -90px;
            bottom: 4%;
            background: linear-gradient(135deg, rgba(48, 188, 168, .20), rgba(48, 188, 168, .03));
            animation: float-two 13s ease-in-out infinite;
        }

        .spark {
            width: 13px;
            height: 13px;
            top: 28%;
            right: 10%;
            background: #f4b95f;
            box-shadow: 0 0 22px rgba(244, 185, 95, .65);
            animation: sparkle 5s ease-in-out infinite;
        }

        @keyframes float-one {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            50% { transform: translate(34px, 55px) rotate(12deg); }
        }

        @keyframes float-two {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(-35px, -45px) scale(1.08); }
        }

        @keyframes sparkle {
            0%, 100% { transform: translateY(0) scale(.85); opacity: .45; }
            50% { transform: translateY(-32px) scale(1.18); opacity: 1; }
        }

        .brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: .65rem;
            color: #515b75;
            font-size: .82rem;
            font-weight: 700;
            letter-spacing: .13em;
            text-transform: uppercase;
            margin-bottom: 1.15rem;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 29px;
            height: 29px;
            border-radius: 9px;
            color: white;
            font-size: .9rem;
            background: linear-gradient(135deg, var(--primary), #7975e8);
            box-shadow: 0 7px 18px rgba(91, 91, 214, .22);
        }

        .hero-title {
            margin: 0;
            text-align: center;
            color: var(--ink);
            font-family: "Manrope", sans-serif;
            font-size: clamp(2rem, 7vw, 3.15rem);
            font-weight: 800;
            letter-spacing: -.055em;
            line-height: 1.06;
        }

        .hero-copy {
            max-width: 520px;
            margin: .8rem auto 2rem;
            text-align: center;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.65;
        }

        .form-shell {
            height: 0;
            margin: 0;
        }

        [data-testid="stForm"] {
            position: relative;
            padding: 1.55rem 1.65rem 1.65rem;
            border: 1px solid rgba(255, 255, 255, .9);
            border-radius: 24px;
            background: var(--surface);
            box-shadow:
                0 24px 65px rgba(50, 59, 90, .12),
                inset 0 1px 0 rgba(255, 255, 255, .92);
            backdrop-filter: blur(18px);
        }

        [data-testid="stWidgetLabel"] p {
            color: #3e4962;
            font-size: .88rem;
            font-weight: 700;
            letter-spacing: .01em;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            min-height: 47px;
            border-color: #dfe3ee;
            border-radius: 12px;
            background: rgba(250, 251, 255, .92);
            transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
        }

        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(91, 91, 214, .11);
            transform: translateY(-1px);
        }

        input[aria-label="First name"],
        input[aria-label="Last name"] {
            text-transform: uppercase;
            letter-spacing: .035em;
        }

        [data-testid="stFormSubmitButton"] button {
            width: 100%;
            min-height: 50px;
            margin-top: .75rem;
            border: 0;
            border-radius: 13px;
            color: white;
            font-weight: 700;
            background: linear-gradient(105deg, var(--primary), #6e68df 58%, var(--teal));
            box-shadow: 0 12px 25px rgba(91, 91, 214, .25);
            transition: transform .2s ease, box-shadow .2s ease;
        }

        [data-testid="stFormSubmitButton"] button:hover {
            color: white;
            border: 0;
            transform: translateY(-2px);
            box-shadow: 0 16px 30px rgba(91, 91, 214, .32);
        }

        [data-testid="stAlert"] {
            border-radius: 14px;
            margin-top: 1rem;
        }

        [data-testid="stButton"] button {
            width: 100%;
            min-height: 48px;
            margin-top: .8rem;
            border: 1px solid rgba(91, 91, 214, .2);
            border-radius: 13px;
            color: var(--primary-dark);
            font-weight: 700;
            background: rgba(255, 255, 255, .78);
            box-shadow: 0 9px 25px rgba(50, 59, 90, .07);
            backdrop-filter: blur(12px);
            transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
        }

        [data-testid="stButton"] button:hover {
            color: var(--primary-dark);
            border-color: rgba(91, 91, 214, .48);
            transform: translateY(-2px);
            box-shadow: 0 13px 28px rgba(50, 59, 90, .11);
        }

        .summary-heading {
            margin: 2rem 0 .25rem;
            color: var(--ink);
            font-family: "Manrope", sans-serif;
            font-size: 1.55rem;
            font-weight: 800;
            letter-spacing: -.035em;
        }

        .summary-copy {
            margin: 0 0 1rem;
            color: var(--muted);
            font-size: .9rem;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .75rem;
            margin-top: 1rem;
        }

        .summary-card {
            position: relative;
            overflow: hidden;
            min-height: 118px;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, .9);
            border-radius: 17px;
            background: rgba(255, 255, 255, .86);
            box-shadow: 0 12px 30px rgba(50, 59, 90, .09);
            backdrop-filter: blur(14px);
        }

        .summary-card::after {
            content: "";
            position: absolute;
            width: 52px;
            height: 52px;
            right: -17px;
            bottom: -17px;
            border-radius: 999px;
            background: var(--card-color);
            opacity: .16;
        }

        .summary-dot {
            display: block;
            width: 9px;
            height: 9px;
            margin-bottom: .8rem;
            border-radius: 999px;
            background: var(--card-color);
            box-shadow: 0 0 0 5px color-mix(in srgb, var(--card-color) 14%, transparent);
        }

        .summary-number {
            color: var(--ink);
            font-family: "Manrope", sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1;
        }

        .summary-label {
            margin-top: .4rem;
            color: var(--muted);
            font-size: .78rem;
            font-weight: 700;
        }

        .summary-total {
            margin-top: .9rem;
            padding: .8rem 1rem;
            border: 1px solid rgba(91, 91, 214, .11);
            border-radius: 13px;
            color: #606a82;
            font-size: .84rem;
            text-align: center;
            background: rgba(255, 255, 255, .58);
        }

        .privacy-note {
            margin-top: 1.2rem;
            text-align: center;
            color: #8a92a6;
            font-size: .78rem;
        }

        @media (max-width: 640px) {
            [data-testid="stMainBlockContainer"] { padding: 2rem 1rem; }
            [data-testid="stForm"] { padding: 1.25rem 1.05rem 1.35rem; border-radius: 20px; }
            .hero-copy { margin-bottom: 1.4rem; }
            .summary-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }

        @media (prefers-reduced-motion: reduce) {
            .ambient { animation: none !important; }
        }
    </style>

    <div class="ambient orb-one"></div>
    <div class="ambient orb-two"></div>
    <div class="ambient spark"></div>

    <div class="brand">
        <span class="brand-mark">✓</span>
        <span>Escalation &amp; Digital</span>
    </div>
    <h1 class="hero-title">Team attendance,<br>made simple.</h1>
    <p class="hero-copy">A quick daily check-in to keep our team connected, coordinated, and ready for the day.</p>
    """,
    unsafe_allow_html=True,
)


today = datetime.now(TIMEZONE).date()

with st.form("attendance_form", clear_on_submit=True):
    st.date_input(
        "Date",
        value=today,
        min_value=today,
        max_value=today,
        help="Attendance is recorded for today.",
    )

    first_col, last_col = st.columns(2, gap="medium")
    with first_col:
        first_name = st.text_input("First name", placeholder="FIRST NAME", max_chars=50)
    with last_col:
        last_name = st.text_input("Last name", placeholder="LAST NAME", max_chars=50)

    status = st.selectbox(
        "Attendance status",
        options=STATUSES,
        index=None,
        placeholder="Select your status",
    )

    submitted = st.form_submit_button("Submit attendance  →", use_container_width=True)


if submitted:
    clean_first_name = " ".join(first_name.split()).upper()
    clean_last_name = " ".join(last_name.split()).upper()

    if not clean_first_name or not clean_last_name:
        st.error("Please enter both your first name and last name.", icon="⚠️")
    elif status is None:
        st.error("Please select your attendance status.", icon="⚠️")
    else:
        save_attendance(
            date_value=today.isoformat(),
            first_name=clean_first_name,
            last_name=clean_last_name,
            status=status,
        )
        st.success(
            f"Attendance submitted for {clean_first_name} {clean_last_name} — {status}.",
            icon="✅",
        )
        st.balloons()


if "show_summary" not in st.session_state:
    st.session_state.show_summary = False

summary_button_label = (
    "Hide monthly summary" if st.session_state.show_summary else "View monthly summary"
)
if st.button(summary_button_label, use_container_width=True):
    st.session_state.show_summary = not st.session_state.show_summary


if st.session_state.show_summary:
    attendance_records = load_attendance()
    available_months = sorted(
        {record["date"][:7] for record in attendance_records}, reverse=True
    )
    if not available_months:
        available_months = [today.strftime("%Y-%m")]

    st.markdown(
        """
        <h2 class="summary-heading">Monthly summary</h2>
        <p class="summary-copy">Choose a month to see the team's attendance breakdown.</p>
        """,
        unsafe_allow_html=True,
    )

    selected_month = st.selectbox(
        "Month",
        options=available_months,
        format_func=lambda month: datetime.strptime(month, "%Y-%m").strftime("%B %Y"),
        key="summary_month",
    )

    monthly_records = [
        record for record in attendance_records if record["date"].startswith(selected_month)
    ]
    status_counts = {
        status_name: sum(
            record["status"] == status_name for record in monthly_records
        )
        for status_name in STATUSES
    }

    st.markdown(
        f"""
        <div class="summary-grid">
            <div class="summary-card" style="--card-color: #30bca8;">
                <span class="summary-dot"></span>
                <div class="summary-number">{status_counts["Ontime"]}</div>
                <div class="summary-label">Ontime</div>
            </div>
            <div class="summary-card" style="--card-color: #f4b95f;">
                <span class="summary-dot"></span>
                <div class="summary-number">{status_counts["Late"]}</div>
                <div class="summary-label">Late</div>
            </div>
            <div class="summary-card" style="--card-color: #6e68df;">
                <span class="summary-dot"></span>
                <div class="summary-number">{status_counts["Halfday"]}</div>
                <div class="summary-label">Halfday</div>
            </div>
            <div class="summary-card" style="--card-color: #ef7184;">
                <span class="summary-dot"></span>
                <div class="summary-number">{status_counts["Absent"]}</div>
                <div class="summary-label">Absent</div>
            </div>
        </div>
        <div class="summary-total">
            <strong>{len(monthly_records)}</strong> total attendance
            {"record" if len(monthly_records) == 1 else "records"} for
            {datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not monthly_records:
        st.info("No attendance has been submitted for this month yet.")


st.markdown(
    '<p class="privacy-note">Internal attendance portal · Escalation &amp; Digital</p>',
    unsafe_allow_html=True,
)
