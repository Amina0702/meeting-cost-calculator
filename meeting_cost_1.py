"""
Meeting Cost Calculator
Because some meetings really should have been an email.
Built by Amina Farooq
"""

import streamlit as st

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Meeting Cost Calculator",
    layout="centered"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .big-cost {
        font-size: 52px;
        font-weight: 800;
        text-align: center;
        padding: 20px;
    }
    .verdict-box {
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        margin: 10px 0;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 13px;
        font-weight: 700;
        color: #1a3a5c;
        letter-spacing: 1px;
        margin-top: 20px;
        margin-bottom: 8px;
        border-bottom: 2px solid #dde4ed;
        padding-bottom: 4px;
    }
    .alt-item {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 4px 0;
        font-size: 14px;
    }
    .recurring-row {
        background: white;
        border-radius: 6px;
        padding: 10px 16px;
        margin: 4px 0;
        display: flex;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .share-box {
        background: #f0f4f8;
        border: 1px solid #dde4ed;
        border-radius: 8px;
        padding: 16px;
        font-size: 14px;
        line-height: 1.6;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 12px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CURRENCIES
# ─────────────────────────────────────────────
CURRENCIES = {
    "USD $" : (1.0,    "$"),
    "INR ₹" : (83.0,   "₹"),
    "GBP £" : (0.79,   "£"),
    "EUR €" : (0.92,   "€"),
    "AED د" : (3.67,   "AED"),
}

# ─────────────────────────────────────────────
# VERDICT
# ─────────────────────────────────────────────
def get_verdict(cost_usd):
    if cost_usd < 20:
        return ("REASONABLE", "#2e7d32",
                "#e8f5e9",
                "This meeting was worth the time.")
    elif cost_usd < 50:
        return ("MODERATE", "#f57c00",
                "#fff3e0",
                "Consider shortening next time.")
    elif cost_usd < 100:
        return ("EXPENSIVE", "#c62828",
                "#ffebee",
                "This could have been an email.")
    elif cost_usd < 200:
        return ("VERY EXPENSIVE", "#c62828",
                "#ffebee",
                "Seriously reconsider this meeting.")
                
    else:
        return ("EXTREMELY EXPENSIVE", "#b71c1c",
                "#ffcdd2",
                "This meeting cost more than a flight ticket!")

# ─────────────────────────────────────────────
# ALTERNATIVES
# ─────────────────────────────────────────────
def get_alternatives(cost_usd, symbol, fx):
    alts = []
    c = cost_usd * fx  # local currency amount
    
    if c > 500:
        alts.append(
            "A detailed email to all attendees")
    if c > 1000:
        alts.append(
            "A shared document with comments")
    if c > 2000:
        alts.append(
            f"Team chai and snacks for everyone")
    if c > 5000:
        alts.append(
            "Team lunch for everyone")
    if c > 8000:
        alts.append(
            "A domestic flight ticket")
    if c > 15000:
        alts.append(
            "A weekend hotel stay")
    if c > 25000:
        alts.append(
            "A brand new smartphone")
    if c > 50000:
        alts.append(
            "A MacBook Air")
    return alts


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style='background:#1a3a5c; padding:28px 32px;
border-radius:12px; margin-bottom:24px;'>
<h1 style='color:white; margin:0; font-size:28px;'>
 Meeting Cost Calculator</h1>
<p style='color:#8aafd4; margin:6px 0 0 0; font-size:14px;'>
Because some meetings really should have been an email.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MEETING DETAILS
# ─────────────────────────────────────────────
st.markdown(
    "<div class='section-header'>MEETING DETAILS</div>",
    unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    duration = st.number_input(
        "Duration (minutes)",
        min_value=5,
        max_value=480,
        value=60,
        step=5)
with col2:
    currency = st.selectbox(
        "Currency",
        list(CURRENCIES.keys()))

fx_rate, symbol = CURRENCIES[currency]

# ─────────────────────────────────────────────
# ATTENDEES
# ─────────────────────────────────────────────
st.markdown(
    "<div class='section-header'>ATTENDEES</div>",
    unsafe_allow_html=True)

st.caption(
    "Enter each attendee's role and annual salary (your best estimate). "
    "Name is optional.")

ROLES = [
    "Intern",
    "Analyst",
    "Senior Analyst",
    "Consultant",
    "Senior Consultant",
    "Manager",
    "Senior Manager",
    "Director",
    "VP",
    "C-Suite",
]

# Dynamic attendees using session state
if "num_attendees" not in st.session_state:
    st.session_state.num_attendees = 3

col_add, col_remove = st.columns([1, 1])
with col_add:
    if st.button("+ Add Attendee"):
        st.session_state.num_attendees += 1
with col_remove:
    if st.button("- Remove Last") and \
            st.session_state.num_attendees > 1:
        st.session_state.num_attendees -= 1

attendee_data = []
for i in range(st.session_state.num_attendees):
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        name = st.text_input(
            f"Name {i+1}",
            value=f"Person {i+1}",
            key=f"name_{i}")
    with c2:
        role = st.selectbox(
            f"Role {i+1}",
            ROLES,
            index=min(i + 3, len(ROLES) - 1),
            key=f"role_{i}")
    with c3:
        salary = st.number_input(
            f"Estimated Annual Salary {i+1} ({symbol})",
            min_value=0,
            max_value=10000000,
            value=int(60000 * fx_rate),
            step=int(1000 * fx_rate),
            key=f"salary_{i}")
    attendee_data.append({
        "name"  : name,
        "role"  : role,
        "salary": salary / fx_rate
    })

# ─────────────────────────────────────────────
# CALCULATE BUTTON
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
calculate = st.button(
    "Calculate Meeting Cost",
    type="primary",
    use_container_width=True)

# ─────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────
if calculate:
    total_cost_usd = 0
    costs          = []

    for a in attendee_data:
        hourly       = a["salary"] / 52 / 40
        meeting_cost = hourly * (duration / 60)
        total_cost_usd += meeting_cost
        costs.append({
            "name" : a["name"],
            "role" : a["role"],
            "cost" : meeting_cost
        })

    total_display   = total_cost_usd * fx_rate
    per_min_display = (
        total_cost_usd / duration) * fx_rate
    avg_per_person  = (
        total_display / len(attendee_data))

    verdict, color, bg_color, message = \
        get_verdict(total_cost_usd)
    alternatives = get_alternatives(
        total_cost_usd, symbol, fx_rate)

    st.divider()

    # ── Big cost display
    st.markdown(
        f"<div class='big-cost' "
        f"style='color:{color};'>"
        f"{symbol}{total_display:,.2f}</div>",
        unsafe_allow_html=True)

    # ── 3 metric cards
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(
            "Cost Per Minute",
            f"{symbol}{per_min_display:,.2f}")
    with m2:
        st.metric(
            "Avg Per Person",
            f"{symbol}{avg_per_person:,.2f}")
    with m3:
        st.metric(
            "Total Attendees",
            len(attendee_data))

    # ── Verdict
    st.markdown(
        f"<div class='verdict-box' "
        f"style='background:{bg_color}; "
        f"color:{color};'>"
        f"{verdict} — {message}</div>",
        unsafe_allow_html=True)

    # ── Per person breakdown
    st.markdown(
        "<div class='section-header'>"
        "COST PER PERSON</div>",
        unsafe_allow_html=True)

    for a in costs:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write(
                f"**{a['name']}** "
                f"({a['role']})")
        with c2:
            st.write(
                f"**{symbol}"
                f"{a['cost'] * fx_rate:,.2f}**")

    # ── Alternatives
    if alternatives:
        st.markdown(
            "<div class='section-header'>"
            "THIS MEETING COST THE SAME AS..."
            "</div>",
            unsafe_allow_html=True)
        for alt in alternatives:
            st.markdown(
                f"<div class='alt-item'>"
                f"-> {alt}</div>",
                unsafe_allow_html=True)

    # ── Recurring projection
    st.markdown(
        "<div class='section-header'>"
        "IF THIS IS A RECURRING MEETING..."
        "</div>",
        unsafe_allow_html=True)

    rec_data = {
        "Frequency"  : [],
        "Per Month"  : [],
        "Per Year"   : [],
    }
    for freq, multiplier in [
        ("Daily (5x/week)", 20),
        ("Weekly",          4),
        ("Bi-weekly",       2),
        ("Monthly",         1),
    ]:
        monthly = total_display * multiplier
        annual  = monthly * 12
        rec_data["Frequency"].append(freq)
        rec_data["Per Month"].append(
            f"{symbol}{monthly:,.0f}")
        rec_data["Per Year"].append(
            f"{symbol}{annual:,.0f}")

    import pandas as pd
    st.dataframe(
        pd.DataFrame(rec_data),
        hide_index=True,
        use_container_width=True)

    # ── LinkedIn share text
    st.markdown(
        "<div class='section-header'>"
        "SHARE ON LINKEDIN</div>",
        unsafe_allow_html=True)

    share_text = (
        f"I just calculated the cost of our meeting "
        f"— {symbol}{total_display:,.0f} for "
        f"{int(duration)} minutes with "
        f"{len(attendee_data)} people!\n\n"
        f"That is {symbol}{per_min_display:,.2f} "
        f"per minute.\n\n"
        f"Verdict: {verdict}\n\n"
        f"{message}\n\n"
        f"Calculate yours for free !\n"
        f"[link :https://meeting-cost-calculator-xush2a5ehvx8cek2mtwey4.streamlit.app/]\n\n"
        f"#productivity #meetings #leadership "
        f"#worksmarter #management")



    st.code(share_text, language=None)
    st.caption(
        "Copy the text above and paste "
        "on LinkedIn!")

    # ── Footer
    st.markdown(
        "<div class='footer'>"
        "Built with Python & Streamlit by "
        "Amina Farooq | "
        "Free to use and share"
        "</div>",
        unsafe_allow_html=True)

