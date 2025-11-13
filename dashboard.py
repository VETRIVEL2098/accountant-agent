import streamlit as st
import pandas as pd
import requests
import json

# ------------------------------
# CONFIG
# ------------------------------
API_BASE = "http://127.0.0.1:5000"

st.set_page_config(page_title="💼 AI Accountant Agent", layout="wide")

st.title("💼 AI Accountant Agent — Financial Insights & Chat")

st.markdown("""
This smart assistant lets you:
- 📂 Upload monthly transaction CSVs  
- 📊 View spending summaries, anomalies & insights  
- 💬 Ask natural questions like *“Which category has the highest spend?”*  
""")

# ------------------------------
# 1️⃣ File Upload Section
# ------------------------------
uploaded_file = st.file_uploader("Upload your transactions CSV", type=["csv"])

if uploaded_file:
    with st.spinner("📤 Uploading and analyzing your file..."):
        # Save the file locally
        files = {"file": uploaded_file}
        upload_res = requests.post(f"{API_BASE}/upload", files=files)

        if upload_res.status_code == 200:
            filename = upload_res.json().get("filename")
            st.success(f"✅ File '{filename}' uploaded successfully!")

            # Process file using backend API
            process_res = requests.post(f"{API_BASE}/process", json={"filename": filename})

            if process_res.status_code == 200:
                result = process_res.json()

                # Display total spend and summary
                st.header("📊 Financial Summary")
                st.metric("Total Spend", f"₹{int(result['total_spend']):,}")
                st.write(result["summary"])

                # Show top categories as chart
                st.subheader("🏷️ Top Spending Categories")
                top_df = pd.DataFrame(list(result["top_categories"].items()), columns=["Category", "Amount"])
                st.bar_chart(top_df.set_index("Category"))

                # Show anomalies if any
                if result["anomalies"]:
                    st.warning("⚠️ Anomalies Detected:")
                    for a in result["anomalies"]:
                        st.write(f"- {a}")
                else:
                    st.info("✅ No anomalies detected this month.")

                # Show human insights
                insights = result["human_insights"]
                st.header("💡 AI Insights & Suggestions")

                if "financial_summary" in insights:
                    st.write("**Summary Observations:**")
                    for obs in insights["financial_summary"].get("observations", []):
                        st.write(f"- {obs}")

                if "insights" in insights:
                    st.write("**Actionable Recommendations:**")
                    for i in insights["insights"]:
                        st.write(f"- {i['insight']} → _{i['recommendation']}_")

                if "alternate_plan" in insights and insights["alternate_plan"]:
                    st.write("**Alternate Cost Plans:**")
                    for plan in insights["alternate_plan"]:
                        st.write(f"- 💰 {plan['area']}: {plan['suggestion']} ({plan['estimated_savings']})")

                st.success(insights.get("profit_opportunity_summary", "No summary available."))
            else:
                st.error("❌ Error while processing the CSV file.")
        else:
            st.error("❌ File upload failed. Please try again.")

# ------------------------------
# 2️⃣ Conversational Query Section
# ------------------------------
st.header("💬 Ask Your Accountant")

query = st.text_input("Ask a question about your finances (e.g. 'Which category has the highest spending?')")

if st.button("Ask"):
    if not uploaded_file:
        st.warning("⚠️ Please upload a CSV file first.")
    elif query:
        filename = uploaded_file.name
        with st.spinner("🤔 Thinking..."):
            q_res = requests.post(f"{API_BASE}/query", json={"filename": filename, "query": query})
            if q_res.status_code == 200:
                st.success(q_res.json().get("response", "No response."))
            else:
                st.error("❌ Error while querying data.")
