import re
import requests
import streamlit as st

try:
    from config_secret import WEBHOOKURL
except ImportError:
    WEBHOOKURL = None  # fallback if the file is missing

def contact_form():
    with st.form("contact_form"):
        message = st.text_area("Any feedback you might have for this website")
        improve = st.text_area("How would you like the website to improve?")
        submit_button = st.form_submit_button("Send")

        if submit_button:
            if not WEBHOOKURL:
                st.error("Email service is not set up. Please try again layer")
                st.stop

            if not message:
                st.error("Please comment something")
                st.stop()

            data = {"message": message, "improve": improve}
            response = requests.post(WEBHOOKURL, json=data)

            if response.status_code == 200:
                st.success("Thanks for the feedback!")
            else:
                st.error("Some error occurred x.x")