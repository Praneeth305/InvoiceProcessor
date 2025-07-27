# 📥 Automated Invoice Processing System

An all-in-one Python application that:
- ✅ Connects to Gmail via IMAP and downloads **invoice PDFs**
- ✅ Extracts **Invoice Number, Date, Billed To, and Address** using `pdfplumber` + regex
- ✅ Saves all extracted data into:
  - **Excel** file (`invoices_log.xlsx`)
  - **SQLite** database (`invoices.db`)
- ✅ Runs continuously (checks Gmail every 5 mins)
- ✅ Optionally prints all invoices in CSV format

---

## 🚀 Features
✔ **Automatic Gmail Fetching** – No manual upload needed  
✔ **PDF Parsing** – Uses `pdfplumber` to read text from invoices  
✔ **Key Field Extraction** – Regex-based detection of key info  
✔ **Excel + SQLite Logging** – Perfect for record keeping  
✔ **Easily Expandable** – Add reporting or dashboards later

---

## 📦 Tech Stack
- **Python 3.9+**
- **pdfplumber** – PDF text extraction
- **pandas + openpyxl** – Excel writing
- **SQLite3** – Lightweight DB
- **imaplib & ssl** – Gmail IMAP access
- **regex (re)** – Pattern matching

---

## 📂 Project Structure

InvoiceProcessor/
│── invoice_processor.py  🚀 Main automation script
│── README.md  📘 This file
│── requirements.txt  📦 Required dependencies
│── invoices/  📂 Auto-downloaded PDFs
│── invoices_log.xlsx  📊 Excel log (auto-generated)
│── invoices.db  🗄 SQLite DB (auto-generated)
--- 
## 🔧 Setup Instructions

### 1️⃣ Clone or Download the Repository

git clone https://github.com/yourusername/InvoiceProcessor.git
cd InvoiceProcessor

2️⃣ Install Required Dependencies

pip install -r requirements.txt

requirements.txt

pdfplumber
pandas
openpyxl

3️⃣ Configure Gmail Login
Use a Gmail App Password (not your normal password).

Generate one here 👉 https://myaccount.google.com/apppasswords

Update these lines in invoice_processor.py:

EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_16_char_app_password"

▶️ How to Run
✅ Start the Automation
python invoice_processor.py

✅ What happens:
Connects to Gmail
Downloads new invoice PDFs → saves them to invoices/
Extracts invoice fields → saves them into Excel + SQLite
Stop anytime with CTRL + C


📄 View Saved Invoices
python invoice_processor.py view

Example output:

invoicenumber,date,billedto,address
INV-001,2025-05-31,John Doe,"123 Main Street, City, Country"
INV-002,2025-06-02,Jane Smith,"456 Market Road, LA, USA"

🏗 Future Enhancements
📊 Monthly summary reports
📧 Email alerts for missing invoice fields

👨‍💻 Author
Praneeth– AI Student
📧 Contact: praneeth0530@gmail.com
