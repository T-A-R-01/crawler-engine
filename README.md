# 🔍 Mini Search Engine

> 🚀 Built a full-stack search engine from scratch — including crawler, ranking algorithm, and deployed system

---

## 🚀 Live Demo
- 🌐 UI: https://crawler-engine-ui.streamlit.app  
- ⚙️ API: https://crawler-engine-r1l2.onrender.com/search?q=life  

---

## ✨ Features
- 🔎 Web crawler (async)
- 🧠 TF-IDF based ranking
- 🗄️ PostgreSQL (Neon) database
- ⚡ FastAPI backend
- 🎨 Streamlit UI
- 🌐 Fully deployed

---

## 🏗️ Architecture

Crawler → Parser → Database → Ranking → API → UI

---

## ⚙️ Tech Stack

- Python
- FastAPI
- PostgreSQL (Neon)
- Streamlit
- Asyncio
- Requests / BeautifulSoup

---

## 🔍 How Search Works

1. Crawl pages and store:
   - URL
   - Title
   - Content

2. Process query:
   - Compute TF (term frequency)
   - Compute IDF (inverse document frequency)

3. Rank results:
   - TF × IDF scoring
   - Boost exact matches

---

## 📸 Screenshots

<img width="1919" height="590" alt="image" src="https://github.com/user-attachments/assets/52576a55-65c2-41a5-ae18-c6677c9a1acf" />
<img width="1908" height="1023" alt="image" src="https://github.com/user-attachments/assets/d093eac7-7b0e-45c8-83d4-dbc8c7818712" />

---

## 🧠 What I Learned

- Building async crawlers
- Database design for search
- Ranking algorithms (TF-IDF)
- Deploying full-stack apps
- Debugging real-world issues

---

## 🔮 Future Improvements

- Pagination
- Stopword removal
- Stemming
- Better ranking algorithms
- UI enhancements

---

## 🚀 Why this project matters

This project demonstrates how a real-world search system works end-to-end:

- Data collection (crawler)
- Processing (parser)
- Storage (database)
- Ranking (TF-IDF)
- Serving (API)
- Presentation (UI)

It is not just a UI project — it is a full system design implementation.

---

## ⚡ Challenges Faced

- Fixing PostgreSQL constraint errors
- Handling async crawling properly
- Debugging deployment issues (Render + Streamlit)
- Getting TF-IDF scores correct (initially returning 0)
  
---

## 📬 Contact

LinkedIn: https://www.linkedin.com/in/tushar-rai-7b8b792b8?utm_source=share_via&utm_content=profile&utm_medium=member_android 

---

⭐ If you like this project, consider starring the repo!
