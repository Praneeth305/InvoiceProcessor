import pdfplumber
import re
import pandas as pd
import os

def extract_invoice_data(pdf_path):
    pairs = {}

    # Read PDF text
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    # Extract key:value pairs
    lines = [line.strip() for line in text.split("\n") if ":" in line]
    for line in lines:
        if re.match(r".+?:\s*.+", line):
            key, value = line.split(":", 1)
            key_clean = re.sub(r"[^A-Za-z0-9 ]+", "", key).strip().lower()
            pairs[key_clean] = value.strip()

    # Normalized output
    normalized = {
        "invoice_number": None,
        "date": None,
        "address": None,
        "billing_to": None
    }

    for k, v in pairs.items():
        if "invoice" in k and ("no" in k or "number" in k):
            normalized["invoice_number"] = v
        elif "date" in k:
            normalized["date"] = v
        elif "address" in k:
            normalized["address"] = v
        elif ("billing" in k or "bill to" in k or "billed to" in k or 
              "billto" in k or "billedto" in k or "customer" in k):
            normalized["billing_to"] = v

    # Save raw extracted data for reference
    csv_path = "invoices_data.csv"
    df = pd.DataFrame([pairs])
    write_header = not os.path.exists(csv_path)
    df.to_csv(csv_path, mode='a', index=False, header=write_header)

    return normalized
