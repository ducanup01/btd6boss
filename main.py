import streamlit as st
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track(unsafe_password="ducanup01"):
    st.set_page_config()
    st.logo("image/logo.webp")
    

    home_page = st.Page(
        page="code/home.py",
        title="Home",
        icon=":material/home:",
    )
    page_1 = st.Page(
        page="code/page1.py",
        title="Boss Activity Leaderboard",
        icon=":material/leaderboard:",
        default=True,
    )
    page_2 = st.Page(
        page="code/page2.py",
        title="Elite Boss Activity Leaderboard",
        icon=":material/leaderboard:"
    )
    page_5 = st.Page(
        page="code/page5.py",
        title="About",
        icon=":material/info:"
    )
    pg = st.navigation(
        {
        "Home ": [home_page],
        "Menu ": [page_1, page_2],
        "Index ": [page_5],
        }
    )
    pg.run()