import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# --- CONFIGURATION ---
CBSL_CONFIG = {
    "AML_THRESHOLD": 1000000.00,
    "LOCAL_LLM_URL": "http://localhost:11434/api/generate",
    "MODEL": "llama3"
}

# --- STATIC MAPS (TIER 1 & 2) ---
# Map Core Banking System codes directly to Regulatory Categories
PRODUCT_CODE_MAP = {
    "INT_CR": {"category": "Interest Income", "itrs_code": "N/A", "risk": "Low"},
    "CHG_SMS": {"category": "Bank Charges", "itrs_code": "N/A", "risk": "Low"},
    "LN_PMT": {"category": "Loan Repayment", "itrs_code": "N/A", "risk": "Low"},
    "TAX_WHT": {"category": "Withholding Tax", "itrs_code": "N/A", "risk": "Low"},
}

class ComplianceEngine:
    def __init__(self):
        print("Engine Initialized. Connected to Local LLM.")

    def get_llm_classification(self, narration, amount):
        """
        TIER 3: AI Classification for vague user descriptions.
        """
        prompt = f"""
        You are a CBSL Compliance Officer. Classify this transaction description.
        Description: "{narration}"
        Amount: {amount}
        
        Select closest category:
        1. Family Maintenance (4010)
        2. Software/IT Services (1215)
        3. Education Fees (2210)
        4. Medical Expenses (2250)
        5. Merchandise Import (1000)
        
        Return ONLY the code (e.g., 1215).
        """
        try:
            response = requests.post(CBSL_CONFIG["LOCAL_LLM_URL"], json={
                "model": CBSL_CONFIG["MODEL"], "prompt": prompt, "stream": False
            })
            return response.json()['response'].strip()
        except:
            return "MANUAL_REVIEW"

    def process_transaction(self, row):
        """
        The Waterfall Logic
        """
        result = {
            "txn_id": row['txn_id'],
            "original_desc": row['description'],
            "final_category": None,
            "itrs_code": None,
            "source": None # 'ProductMap', 'Rule', or 'AI'
        }

        # --- STEP 1: Product Code Mapping (Fastest) ---
        if row['tran_code'] in PRODUCT_CODE_MAP:
            mapping = PRODUCT_CODE_MAP[row['tran_code']]
            result['final_category'] = mapping['category']
            result['itrs_code'] = mapping['itrs_code']
            result['source'] = 'Tier1_ProductMap'
            return result

        # --- STEP 2: Regex/Keyword Rules (Medium) ---
        desc_upper = row['description'].upper()
        if "ATM" in desc_upper and "WITHDRAWAL" in desc_upper:
            result['final_category'] = "Cash Withdrawal"
            result['source'] = 'Tier2_Rule'
            return result
        
        # --- STEP 3: Local LLM (For ambiguous transfers) ---
        # Only use AI if it's a transfer that isn't system generated
        result['itrs_code'] = self.get_llm_classification(row['description'], row['amount'])
        result['final_category'] = "Customer Transfer"
        result['source'] = 'Tier3_LocalAI'
        
        return result

    def generate_finnet_csv(self, processed_data):
        df = pd.DataFrame(processed_data)
        filename = f"FinNet_Return_{datetime.now().strftime('%Y%m%d')}.csv"
        # CBSL Format: AccountNo, Date, Currency, Amount, ITRSCode, Description
        df.to_csv(filename, index=False)
        print(f"Generated {filename}")

# --- MOCK DATA EXECUTION ---
if __name__ == "__main__":
    # Simulating data from Core Banking (Oracle DB)
    daily_txns = [
        {"txn_id": 1, "tran_code": "INT_CR", "description": "SAVINGS INTEREST", "amount": 540.00},
        {"txn_id": 2, "tran_code": "TRF_IB", "description": "Payment for web design course", "amount": 25000.00},
        {"txn_id": 3, "tran_code": "LN_PMT", "description": "AUTO LOAN 40404", "amount": 15000.00},
        {"txn_id": 4, "tran_code": "TRF_OT", "description": "family support monthly", "amount": 150000.00},
    ]

    engine = ComplianceEngine()
    results = [engine.process_transaction(row) for row in daily_txns]
    
    # Output for Verification
    print(pd.DataFrame(results))
    engine.generate_finnet_csv(results)
