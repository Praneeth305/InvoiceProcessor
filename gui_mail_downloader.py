import imaplib, ssl, email, os
from pathlib import Path
from tkinter import Tk, Label, Entry, Button, StringVar

FOLDER_PATH = "invoices"
Path(FOLDER_PATH).mkdir(parents=True, exist_ok=True)

def download_invoices(email_user, email_pass):
    context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL("imap.gmail.com", port=993, ssl_context=context)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    status, messages = mail.search(None, '(SUBJECT "Invoice")')
    email_ids = messages[0].split()

    if not email_ids:
        status_label.set("No invoices found.")
    else:
        status_label.set(f"{len(email_ids)} invoices found.")
        for email_id in email_ids:
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename and filename.endswith(".pdf"):
                    filepath = os.path.join(FOLDER_PATH, filename)
                    if not os.path.isfile(filepath):
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Downloaded: {filename}")
    mail.logout()

#  GUI
root = Tk()
root.title("Invoice Mail Downloader")

Label(root, text="Gmail:").pack()
email_entry = Entry(root, width=30)
email_entry.pack()

Label(root, text="App Password:").pack()
password_entry = Entry(root, width=30, show="*")
password_entry.pack()

status_label = StringVar()
Label(root, textvariable=status_label).pack(pady=10)

def trigger_download():
    user = email_entry.get()
    pwd = password_entry.get()
    if user and pwd:
        download_invoices(user, pwd)
        status_label.set("Download complete.")

Button(root, text="Download Invoices", command=trigger_download).pack(pady=5)
root.mainloop()
