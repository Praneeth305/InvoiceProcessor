import sqlite3

DB_FILE = "invoices.db"

def view_invoices():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT invoice_number, date, billing_to, address FROM invoices")
    rows = cur.fetchall()
    conn.close()

    print("invoicenumber,date,billedto,address")
    for invoice_number, date, billed_to, address in rows:
        print(f'{invoice_number},{date},{billed_to},"{address}"')

if __name__ == "__main__":
    view_invoices()
