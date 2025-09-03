import streamlit as st
import requests
from api_config import APIConfig


st.title("Recommendation System")

user_id = st.text_input("Enter user_id:")

# -------------------------------
# Normal Recommendation Section
# -------------------------------
if st.button("Get Recommendation"):
    if user_id:
        url = f"{APIConfig.API_BASE_URL}/ml/recommend"
        response = requests.get(url, params={"user_id": user_id, "top_n": 10})

        st.write("Raw response:", response.text)  # Debugging

        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                st.error(f"Failed to parse JSON: {e}")
                st.stop()

            recs = data.get("recommendations", [])
            st.write("Recommendations:")
            try:
                import pandas as pd

                df = pd.DataFrame(recs)
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name=f"recommendations_user_{user_id}.csv",
                    mime="text/csv",
                )
            except Exception:
                st.write(recs)
        else:
            try:
                data = response.json()
                st.write(f"Error: {data.get('error_code')} - {data.get('message')}")
            except Exception:
                st.error(f"Backend returned status {response.status_code}: {response.text}")
    else:
        st.write("Please enter a user_id.")

st.markdown("---")

# -------------------------------
# AI Recommendation Section
# -------------------------------
st.subheader("AI-Powered Recommendations (New)")
if st.button("Get AI Recommendations"):
    if user_id:
        url = f"{APIConfig.API_BASE_URL}/ml/recommend/ai"
        response = requests.get(url, params={"user_id": user_id, "top_n": 10})

        st.write("Raw response:", response.text)  # Debugging

        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                st.error(f"Failed to parse JSON: {e}")
                st.stop()

            recs = data.get("recommendations", [])
            try:
                import pandas as pd

                df = pd.DataFrame(recs)
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download AI CSV",
                    data=csv,
                    file_name=f"ai_recommendations_user_{user_id}.csv",
                    mime="text/csv",
                )
            except Exception:
                st.write(recs)
        else:
            try:
                data = response.json()
                st.write(f"Error: {data.get('error_code')} - {data.get('message')}")
            except Exception:
                st.error(f"Backend returned status {response.status_code}: {response.text}")
    else:
        st.write("Please enter a user_id.")


