import streamlit as st
import requests
st.title("Welcome to Resource Finder Model 🚀")
st.header("Search for articles and youtube videos links")

user_input = st.text_input("search")

if not user_input:
    st.warning("Please enter a search query")
else:
    with st.spinner("Searching..."):
        try:
            end_point = f"https://resource-finder-model-3.onrender.com/search?query={user_input}"
            response = requests.get(end_point)
            if response.status_code == 200:
                data = response.json()

                # 📖 Article Links
                st.subheader("🔗 Article Links")
                for i,item in enumerate(data["web"],1):
                    st.markdown(f"**{i}. {item['title']}**")
                    st.markdown(f"[{item['url']}]({item['url']})")
                    st.caption(item.get("snippet", "No description available."))

                # 🎥 YouTube Video Links
                st.subheader("🎥 YouTube Video Links")
                for i,item in enumerate(data["web"],1):
                    st.markdown(f"**{i}. {item['title']}**")
                    st.markdown(f"[{item['url']}]({item['url']})")

            else:
                st.error("❌ Failed to fetch data from the API.")


        except Exception as e:
                st.warning(f"Unexpected error: {e}")