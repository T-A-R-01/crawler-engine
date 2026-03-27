import streamlit as st
import requests

st.set_page_config(page_title="Mini Search Engine", page_icon="🔍", layout="wide")

# Custom styling
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .search-box {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🔍 Mini Search Engine</div>', unsafe_allow_html=True)

# Search input
query = st.text_input("Enter your search query", placeholder="e.g. life, love, inspiration")

# Search button
if st.button("Search"):
    if query:
        try:
            response = requests.get(
    f"https://crawler-engine-r1l2.onrender.com/search?q={query}"
)
            data = response.json()

            if not data:
                st.warning("No results found")
            else:
                st.success(f"Found {len(data)} results")

                for result in data:
                    st.markdown(f"### [{result['title']}]({result['url']})")
                    st.write(f"🔗 {result['url']}")
                    st.write(f"⭐ Score: {result['score']}")
                    st.markdown("---")

        except:
            st.error("Backend API not running. Please start FastAPI server.")