import streamlit as st
import requests

# ✅ FIXED API URL
API_URL = "https://crawler-engine-r1l2.onrender.com/search"

st.set_page_config(page_title="Mini Search Engine", page_icon="🔍", layout="wide")

# ---------------- STYLES ----------------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 20px;
}
.result-card {
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
    background-color: #f9f9f9;
}
.result-title {
    font-size: 20px;
    font-weight: bold;
    color: #1a0dab;
}
.result-link {
    font-size: 14px;
    color: green;
}
.snippet {
    font-size: 14px;
    color: #444;
}
.score {
    font-size: 12px;
    color: #888;
}
.highlight {
    background-color: yellow;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="title">🔍 Mini Search Engine</div>', unsafe_allow_html=True)

# ---------------- SEARCH ----------------
query = st.text_input("Enter your search query", placeholder="e.g. life, inspiration")

if st.button("Search"):
    if query:
        try:
            # ✅ API CALL
            response = requests.get(API_URL, params={"q": query})
            data = response.json()

            results = data.get("results", [])
            count = data.get("count", 0)

            if count == 0:
                st.warning("No results found")
            else:
                st.success(f"Found {count} results")

                for r in results:
                    title = r.get("title", "No title")
                    url = r.get("url", "")
                    snippet = r.get("snippet", "")
                    score = round(r.get("score", 0), 5)

                    # -------- HIGHLIGHT QUERY --------
                    snippet = snippet.replace(
                        query,
                        f"<span class='highlight'>{query}</span>"
                    )

                    # -------- CARD UI --------
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">{title}</div>
                        <div class="result-link">{url}</div>
                        <div class="snippet">{snippet}</div>
                        <div class="score">⭐ Score: {score}</div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error("Backend API not reachable")