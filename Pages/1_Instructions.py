import streamlit as st

st.set_page_config(page_title="Instructions")

st.title("🧠 How to Add a PPT Slide Deck")

st.markdown("### 👇 Follow these steps to upload your Google Slides presentation:")

st.markdown("""
1. **Open your Google Slides deck**
   - Go to [Google Slides](https://slides.google.com)

2. **File → Share → Publish to web**
   - Choose the **Embed** tab.
   - Click **Publish** and confirm.

3. **Copy the embed code**
   - It looks like:
     ```html
     <iframe src="https://docs.google.com/presentation/d/e/.../pubembed?start=false&loop=false&delayms=3000"></iframe>
     ```

4. **Paste into the form**
   - In the **Upload New Slide Deck** tab.
   - Paste the iframe **or just the `src` link**, add title & date.

5. ✅ Done! It will appear in the archive.
""")

st.markdown("---")
st.markdown("### ✅ Example Embed Code:")

example = """
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vExampleLink/pubembed?start=false&loop=false&delayms=3000"
        frameborder="0" width="960" height="569" allowfullscreen></iframe>
"""
st.code(example, language="html")

st.markdown("### 💡 Tips")
st.markdown("""
- Only use embed links from **Google Slides**
- You can paste just the `src` portion
- Don’t use private or unshared decks
""")

st.markdown("---")
st.markdown("### 📬 Need Help?")
st.markdown("""
For assistance, contact:

**Aleeza Noor**  
📧 [aleeza.noor@publicissapient.com](mailto:aleeza.noor@publicissapient.com)
""")
