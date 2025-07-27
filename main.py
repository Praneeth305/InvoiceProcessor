import os, time, pandas as pd, sqlite3
from extract_utils import extract_invoice_data

INVOICE_DIR = "invoices"
EXCEL_PATH = "invoices_log.xlsx"
DB_FILE = "invoices.db"
PROCESSED = set()


# Delete old files each run (fresh start)
for file in ["invoices_log.xlsx", "invoices.db"]:
    if os.path.exists(file):
        os.remove(file)
        print(f"[🗑] Deleted old {file}")

def save_to_excel(data):
    df = pd.DataFrame([data])
    if not os.path.exists(EXCEL_PATH):
        df.to_excel(EXCEL_PATH, index=False)
    else:
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

def save_to_sqlite(data):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_number TEXT PRIMARY KEY,
            date TEXT,
            address TEXT,
            billing_to TEXT
        )
    ''')

    try:
        cur.execute('''
            INSERT INTO invoices (invoice_number, date, address, billing_to)
            VALUES (?, ?, ?, ?)
        ''', (data['invoice_number'], data['date'], data['address'], data['billing_to']))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"[!] Duplicate Invoice: {data['invoice_number']}")
    conn.close()

def watch_folder():
    print("[*] Watching 'invoices/' for new invoices...")
    while True:
        for file in os.listdir(INVOICE_DIR):
            if file.endswith(".pdf") and file not in PROCESSED:
                path = os.path.join(INVOICE_DIR, file)
                print(f"[+] Processing: {file}")
                data = extract_invoice_data(path)

                for field in ["invoice_number", "date", "address", "billing_to"]:
                    if not data.get(field):
                        data[field] = "N/A"

                save_to_excel(data)
                save_to_sqlite(data)
                PROCESSED.add(file)
        time.sleep(5)

if __name__ == "__main__":
    if not os.path.exists(INVOICE_DIR):
        os.makedirs(INVOICE_DIR)
    watch_folder()
