import streamlit as st
import requests

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
            response = requests.get(API_URL, params={"q": query})
            results = response.json()

            if len(results) == 0:
                st.warning("No results found")
            else:
                st.success(f"Found {len(results)} results")

                for r in results:
                    title = r.get("title", "No title")
                    url = r.get("url", "")
                    content = r.get("content", "")
                    score = round(r.get("score", 0), 5)

                    # -------- SMART SNIPPET --------
                    if query.lower() in content.lower():
                        idx = content.lower().index(query.lower())
                        start = max(0, idx - 80)
                        end = idx + 120
                        snippet = content[start:end] + "..."
                    else:
                        snippet = content[:200] + "..."

                    # -------- HIGHLIGHT --------
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
                        <div class="score"> Score: {score}</div>
                    </div>
                    """, unsafe_allow_html=True)

        except:
            st.error("Backend API not reachable")