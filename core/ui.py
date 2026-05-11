"""
core/ui.py
VTVault — Alchemist's Terminal Theme + Updated Sidebar
"""

import streamlit as st
from core.config import ROLE_CSS, BADGE_STYLES

# Lazy DB import
def _get_db():
    from database import get_user, claim_daily_bonus, get_user_badges, get_all_achievements, get_equipped, pot_total
    return get_user, claim_daily_bonus, get_user_badges, get_all_achievements, get_equipped, pot_total

def inject_styles():
    """VTVault Alchemist's Terminal Theme"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Comic+Neue:wght@400;700&display=swap');

        .stApp {
            background-color: #12141D !important;
            color: #E0E0E0 !important;
            font-family: 'Courier Prime', monospace;
        }

        h1, h2, h3, .vtvault-header {
            color: #FFB84D !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
        }

        .vtvault-header {
            font-size: 2.8rem;
            text-shadow: 0 0 15px #FFB84D88;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1A1D29;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 8px;
            gap: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #E0E0E0;
            border-radius: 4px;
            padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFB84D !important;
            color: #12141D !important;
            font-weight: bold;
        }

        /* Polaroid Cards */
        .polaroid-card {
            background-color: #F9F9F9;
            color: #12141D;
            padding: 16px;
            margin: 12px 0;
            border-radius: 4px;
            box-shadow: 4px 6px 14px rgba(0,0,0,0.6);
            transform: rotate(-1.5deg);
            transition: all 0.2s ease;
        }
        .polaroid-card:hover {
            transform: rotate(1deg) scale(1.03);
        }
        .polaroid-video {
            width: 100%;
            height: 220px;
            background: #000;
            margin-bottom: 12px;
            border: 8px solid #fff;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
        }
        .polaroid-caption {
            font-family: 'Comic Neue', cursive;
            font-size: 15px;
            font-style: italic;
            border-bottom: 2px solid #333;
            padding-bottom: 8px;
            margin-bottom: 8px;
        }
        .polaroid-tags {
            color: #4DFFF3;
            font-size: 13px;
            font-weight: bold;
            font-family: 'Courier Prime', monospace;
        }

        /* Notices */
        .notice {
            padding: 14px 20px;
            border-radius: 4px;
            margin: 12px 0;
            font-family: 'Courier Prime', monospace;
        }
        .notice-success { background: #1A2D1A; border-left: 5px solid #4DFFF3; }
        .notice-error   { background: #2D1A1A; border-left: 5px solid #FF6B6B; }
        .notice-warn    { background: #2D2A1A; border-left: 5px solid #FFB84D; }

        /* Sidebar */
        .stSidebar {
            background-color: #1A1D29 !important;
            border-right: 2px solid #FFB84D;
        }
        .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2 {
            color: #FFB84D !important;
        }
    </style>
    """, unsafe_allow_html=True)

def init_state():
    defaults = [
        ("username", None),
        ("page", "home"),
        ("selected_bet", None),
        ("toast", None),
        ("show_onboarding", False),
    ]
    for key, default in defaults:
        if key not in st.session_state:
            st.session_state[key] = default

def set_toast(kind: str, msg: str):
    st.session_state.toast = (kind, msg)

def show_toast():
    if not st.session_state.toast:
        return
    kind, msg = st.session_state.toast
    css = {"success": "notice-success", "error": "notice-error", "warn": "notice-warn"}.get(kind, "notice")
    st.markdown(f'<div class="notice {css}">{msg}</div>', unsafe_allow_html=True)
    st.session_state.toast = None

def nav(page: str, bet_id=None):
    st.session_state.page = page
    if bet_id is not None:
        st.session_state.selected_bet = bet_id
    st.rerun()

def render_sidebar():
    """Updated sidebar with VTVault terminal aesthetic + Scraps"""
    if not st.session_state.username:
        return

    get_user, claim_daily_bonus, _, _, _, _ = _get_db()
    user = get_user(st.session_state.username)
    if not user:
        return

    with st.sidebar:
        st.markdown('<div style="font-family:Courier Prime;font-size:1.8rem;font-weight:700;color:#FFB84D;">⚙️ VTVault</div>', unsafe_allow_html=True)

        # Wallet — now shows Scraps
        st.markdown(f"""
        <div style="background:#12141D;border:2px solid #FFB84D;border-radius:8px;padding:18px;text-align:center;margin:20px 0;">
            <div style="font-size:0.8rem;color:#4DFFF3;">{st.session_state.username}</div>
            <div style="font-family:Courier Prime;font-size:2.4rem;font-weight:700;color:#FFB84D;">
                {user['coins']:,}
            </div>
            <div style="font-size:0.75rem;color:#E0E0E0;letter-spacing:1px;">SCRAPS</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Claim Daily Bonus (+250)", use_container_width=True, type="primary"):
            ok, msg = claim_daily_bonus(st.session_state.username)
            set_toast("success" if ok else "warn", msg)
            st.rerun()

        st.markdown("---")

        # Navigation
        pages = [
            ("Home", "home"),
            ("Bets", "bets"),
            ("Create Bet", "create_bet"),
            ("Clip Hub", "clips"),
            ("Achievements", "achievements"),
            ("Shop", "shop"),
            ("Leaderboard", "leaderboard"),
            ("My Profile", "my_profile"),
        ]
        for label, key in pages:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                nav(key)

        st.markdown("---")

        if st.button("Log out", use_container_width=True):
            st.session_state.username = None
            st.session_state.page = "home"
            st.rerun()

def show_onboarding_popup():
    if not st.session_state.get("show_onboarding"):
        return
    _, mid, _ = st.columns([1, 3, 1])
    with mid:
        st.markdown("Welcome to **VTVault**!")
        if st.button("Got it! Let's go", use_container_width=True):
            st.session_state.show_onboarding = False
            st.rerun()
