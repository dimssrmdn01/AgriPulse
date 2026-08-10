import streamlit as st

def apply_design_tokens(is_home=False):
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
      --bg: #211814;
      --bg-soft: #2A1F19;
      --surface: #2C221C;
      --border: #4A392F;
      --border-soft: rgba(242,233,222,0.10);
      --text: #F2E9DE;
      --text-dim: #B8A793;
      --text-faint: #806F5F;

      --karet: #E7DCC4;
      --karet-bg: rgba(231,220,196,0.08);
      --pinang: #C1622D;
      --pinang-bg: rgba(193,98,45,0.12);
      --gambir: #A34A3A;
      --gambir-bg: rgba(163,74,58,0.12);

      --good: #7BA05B;
      --good-bg: rgba(123,160,91,0.12);
      --neutral: #C1943D;
      --pending: #C1943D;
      --pending-bg: rgba(193,148,61,0.12);
      --bad: #B0554A;
      --bad-bg: rgba(176,85,74,0.10);

      --font-display: 'Fraunces', Georgia, serif;
      --font-sans: 'IBM Plex Sans', sans-serif;
      --font-mono: 'IBM Plex Mono', monospace;
    }

    .stApp { color: var(--text); font-family: var(--font-sans); }
    .block-container { padding-top: 2.5rem; max-width: 1180px; }
    section[data-testid="stSidebar"] { background: var(--bg-soft); border-right: 1px solid var(--border-soft); }

    .ap-eyebrow { font-family: var(--font-mono); font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 12px; }
    .ap-header { font-family: var(--font-display); font-weight: 600; font-size: 36px; color: var(--text); margin-bottom: 8px; line-height: 1.1; }
    .ap-header em { font-style: italic; }
    .ap-sub { font-size: 16px; color: var(--text-dim); line-height: 1.65; max-width: 680px; margin-bottom: 32px; }
    .ap-divider { border: none; border-top: 1px solid var(--border-soft); margin: 30px 0; }
    .ap-section-label { font-family: var(--font-mono); font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-faint); margin-bottom: 6px; }
    .ap-section-title { font-family: var(--font-display); font-weight: 600; font-size: 21px; color: var(--text); margin-bottom: 18px; }
    .ap-section-desc { color: var(--text-dim); font-size: 14.5px; line-height: 1.6; max-width: 680px; margin-bottom: 30px; }
    .ap-highlight { font-style: italic; }

    .metric-card, .ap-stat { background: var(--surface); border: 1px solid var(--border-soft); border-radius: 12px; padding: 20px; text-align: center; height: 100%; }
    .metric-label, .ap-stat-label { font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-faint); margin-bottom: 8px; }
    .metric-value, .ap-stat-value { font-family: var(--font-mono); font-size: 26px; font-weight: 600; color: var(--text); }
    .ap-stat-value.accent { color: var(--gambir); }

    div[data-testid="stForm"] { background: var(--surface); border: 1px solid var(--border-soft); border-radius: 14px; padding: 8px 6px 4px; }
    div[data-testid="stForm"] label p { color: var(--text-dim) !important; font-size: 13.5px; }
    div[data-testid="stForm"] input, div[data-testid="stForm"] textarea, div[data-testid="stForm"] div[data-baseweb="select"] > div { background: var(--bg-soft) !important; border-color: var(--border) !important; color: var(--text) !important; border-radius: 8px !important; }
    div[data-testid="stFormSubmitButton"] button { background: var(--gambir) !important; color: var(--bg) !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; width: 100%; }
    div[data-testid="stFormSubmitButton"] button:hover { opacity: 0.9; }

    .ap-alert { border-radius: 10px; padding: 12px 16px; font-size: 14px; margin-top: 10px; border-left: 3px solid; }
    .ap-alert.ok { background: var(--good-bg); border-color: var(--good); color: var(--text); }
    .ap-alert.err { background: var(--bad-bg); border-color: var(--bad); color: var(--text); }
    .ap-badge { font-family: var(--font-mono); font-size: 10.5px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; padding: 4px 10px; border-radius: 999px; white-space: nowrap; border: 1px solid transparent; }
    .ap-badge.approved { background: var(--good-bg); color: var(--good); border-color: var(--good); }
    .ap-badge.pending { background: var(--pending-bg); color: var(--pending); border-color: var(--pending); }
    .ap-badge.rejected { background: var(--bad-bg); color: var(--bad); border-color: var(--bad); }

    .ap-empty { background: var(--surface); border: 1px dashed var(--border); border-radius: 12px; padding: 28px; text-align: center; color: var(--text-dim); font-size: 14px; }
    .ap-log-entry { display: flex; align-items: center; gap: 16px; padding: 14px 4px; border-bottom: 1px solid var(--border-soft); }
    .ap-log-entry:last-child { border-bottom: none; }
    .ap-log-price { font-family: var(--font-mono); font-weight: 600; font-size: 17px; color: var(--text); min-width: 118px; }
    .ap-log-meta { flex: 1; min-width: 0; }
    .ap-log-region { font-size: 14.5px; color: var(--text); font-weight: 500; }
    .ap-log-note { font-size: 12.5px; color: var(--text-faint); margin-top: 2px; }
    .ap-log-time { font-family: var(--font-mono); font-size: 11.5px; color: var(--text-faint); white-space: nowrap; }

    .ap-hero-title { font-family: var(--font-display); font-weight: 600; font-size: clamp(36px, 5vw, 56px); line-height: 1.08; letter-spacing: -0.01em; color: var(--text); margin: 0 0 16px 0; opacity: 0; animation: apFadeUp .7s ease forwards; }
    .ap-hero-title em { font-style: italic; color: var(--pinang); }
    .ap-hero-sub { font-size: 16.5px; line-height: 1.65; color: var(--text-dim); max-width: 620px; opacity: 0; animation: apFadeUp .7s ease .16s forwards; }
    .ap-card { background: var(--surface); border: 1px solid var(--border-soft); border-radius: 14px; padding: 26px 24px 22px; height: 100%; position: relative; transition: transform .25s ease, border-color .25s ease; }
    .ap-card:hover { transform: translateY(-3px); border-color: var(--accent-color, var(--border)); }
    .ap-card-top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 18px; }
    .ap-card-icon { width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; background: var(--accent-bg); }
    .ap-stamp { font-family: var(--font-mono); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent-color); border: 1.5px dashed var(--accent-color); border-radius: 999px; padding: 5px 11px; transform: rotate(-4deg); white-space: nowrap; opacity: 0.85; }
    .ap-card-name { font-family: var(--font-display); font-weight: 600; font-size: 20px; color: var(--text); margin-bottom: 2px; }
    .ap-card-status { font-family: var(--font-mono); font-size: 13px; color: var(--accent-color); margin-bottom: 14px; }
    .ap-card-meta { font-family: var(--font-mono); font-size: 12px; color: var(--text-faint); margin-bottom: 14px; padding-bottom: 14px; border-bottom: 1px solid var(--border-soft); }
    .ap-card-caption { font-size: 13.5px; line-height: 1.6; color: var(--text-dim); }
    .ap-cta { background: var(--surface); border: 1px solid var(--border-soft); border-left: 3px solid var(--pinang); border-radius: 10px; padding: 18px 22px; font-size: 14.5px; color: var(--text-dim); margin-top: 8px; }
    .ap-cta b { color: var(--text); }
    @keyframes apFadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    
    @media (prefers-reduced-motion: reduce){ *{ animation: none !important; transition: none !important; } }
    </style>
    """

    if is_home:
        css += """
        <style>
        .stApp { background: radial-gradient(ellipse 70% 40% at 15% 0%, rgba(193,98,45,0.10), transparent 60%), radial-gradient(ellipse 60% 40% at 85% 10%, rgba(163,74,58,0.08), transparent 60%), var(--bg); }
        .ap-eyebrow { color: var(--pinang); }
        </style>
        """
    else:
        css += "<style>.stApp { background: var(--bg); }</style>"

    st.markdown(css, unsafe_allow_html=True)