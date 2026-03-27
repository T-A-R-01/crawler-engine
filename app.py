import streamlit as st
import requests
import re

# 🔥 CONFIG
API_URL = "https://crawler-engine-r1l2.onrender.com/search"


# 🔥 HIGHLIGHT FUNCTION
def highlight(text, query):
    if not text:
        return ""
    return re.sub(
        f"({query})",
        r"<mark>\1</mark>",
        text,
        flags=re.IGNORECASE
    )


# 🔥 UI DESIGN
st.set_page_config(page_title="Mini Search Engine", layout="wide")

st.markdown("<h1 style='text-align:center;'>🔎 Mini Search Engine</h1>", unsafe_allow_html=True)

query = st.text_input("Enter your search query", placeholder="e.g. life, love, inspiration")

if st.button("Search") and query:

    with st.spinner("Searching... 🔍"):
        try:
            response = requests.get(f"{API_URL}?q={query}")

            if response.status_code == 200:
                results = response.json()

                st.success(f"Found {len(results)} results")

                for r in results:
                    st.markdown(f"### [{r['title']}]({r['url']})")

                    st.caption(r["url"])

                    # Highlighted snippet
                    snippet = highlight(r["snippet"], query)
                    st.markdown(snippet + "...", unsafe_allow_html=True)

                    # Score
                    st.write(f"⭐ Relevance Score: **{r['score']}**")

                    st.divider()

            else:
                st.error("Backend API error")

        except Exception as e:
            st.error("Backend API not reachable")