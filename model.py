import streamlit as st
import pandas as pd
import random
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="CBSL Compliance Engine", layout="wide")

# --- HEADER ---
st.title("🇱🇰 CBSL Transaction Compliance Engine")
st.markdown("**Status:** System Online | **Mode:** Local Privacy (On-Premise)")
st.markdown("---")

# --- 1. MOCK DATA GENERATOR (Simulating Core Banking) ---
@st.cache_data
def load_data():
    data = [
        {"txn_id": "TXN-1001", "date": "2025-10-27", "desc": "LN_PMT: AUTO LOAN 5501", "amount": 25000.00, "currency": "LKR", "type": "INTERNAL"},
        {"txn_id": "TXN-1002", "date": "2025-10-27", "desc": "Payment for AWS Web Services", "amount": 150.00, "currency": "USD", "type": "CROSS_BORDER"},
        {"txn_id": "TXN-1003", "date": "2025-10-27", "desc": "School fees for son - Royal College", "amount": 45000.00, "currency": "LKR", "type": "LOCAL_TRANSFER"},
        {"txn_id": "TXN-1004", "date": "2025-10-27", "desc": "ATM W/D COLOMBO 07", "amount": 5000.00, "currency": "LKR", "type": "CASH"},
        {"txn_id": "TXN-1005", "date": "2025-10-27", "desc": "Consulting fees for Oct Project", "amount": 1200000.00, "currency": "LKR", "type": "LOCAL_TRANSFER"}, # High Value
    ]
    return pd.DataFrame(data)

# --- 2. THE LOGIC ENGINE ---
def process_transactions(df):
    results = []
    
    for index, row in df.iterrows():
        status = "Auto-Cleared"
        category = "Unclassified"
        itrs_code = "N/A"
        flag = "None"
        confidence = "High"

        # RULE 1: Product Mapping (Hard Logic)
        if "LN_PMT" in row['desc']:
            category = "Loan Repayment"
            status = "Auto-Cleared"
        
        # RULE 2: Cash Logic
        elif "ATM W/D" in row['desc']:
            category = "Cash Withdrawal"
            status = "Auto-Cleared"
        
        # RULE 3: AI Simulation (Local LLM Logic)
        elif "AWS" in row['desc']:
            category = "Software/IT Services"
            itrs_code = "1215" # CBSL Code
            status = "Auto-Cleared"
        
        elif "School" in row['desc']:
            category = "Education Services"
            itrs_code = "2210" # CBSL Code
            status = "Auto-Cleared"

        # RULE 4: AML Threshold Check (> 1 Million LKR)
        if row['amount'] >= 1000000:
            flag = "⚠️ goAML Threshold"
            status = "Manual Review Required"
            confidence = "Low"
        
        # Fallback for vague items
        if category == "Unclassified":
            status = "Manual Review Required"
            confidence = "Low"

        results.append({
            "Txn ID": row['txn_id'],
            "Description": row['desc'],
            "Amount": f"{row['amount']:,.2f}",
            "Currency": row['currency'],
            "Predicted Category": category,
            "ITRS Code": itrs_code,
            "Status": status,
            "Risk Flag": flag
        })
    
    return pd.DataFrame(results)

# --- 3. UI DASHBOARD ---

# Sidebar
st.sidebar.header("⚙️ Configuration")
st.sidebar.selectbox("Select Model", ["Llama-3-Local (Ollama)", "Mistral-7B-Quantized"])
st.sidebar.slider("AML Threshold (LKR)", 500000, 2000000, 1000000)
uploaded_file = st.sidebar.file_uploader("Upload Daily Extract (CSV)", type="csv")

# Main Area
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", "5")
col2.metric("Auto-Classified", "80%", "4/5")
col3.metric("Pending Review", "1", "-goAML Alert", delta_color="inverse")

st.subheader("📝 Transaction Review Queue")
df_raw = load_data()
df_processed = process_transactions(df_raw)

# Highlighting Logic
def highlight_status(val):
    color = '#ffcdd2' if val == 'Manual Review Required' else '#c8e6c9'
    return f'background-color: {color}'

st.dataframe(df_processed.style.applymap(highlight_status, subset=['Status']))

# Action Buttons
st.subheader("📤 Submission")
c1, c2 = st.columns([1,4])
if c1.button("Generate FinNet XML"):
    st.success("XML File generated: `cbsl_return_20251027.xml` ready for upload.")
if c2.button("Generate goAML Report"):
    st.warning("1 High-Value Transaction detected. Generating STR/CTR report...")

# --- FOOTER ---
st.markdown("---")
st.caption("🔒 Architecture Note: This system runs entirely offline. No customer data leaves the local network.")
