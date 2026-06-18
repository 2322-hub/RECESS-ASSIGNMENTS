import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd



class ContactManager:
    def __init__(self):
        self.conn = sqlite3.connect("contacts.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT
        )
        """)
        self.conn.commit()

    def _is_valid_phone(self, phone):
        return all(c in "0123456789-+" for c in phone)

    def _is_valid_email(self, email):
        return "@" in email and "." in email

    def add_contact(self, name, phone, email):
        if not self._is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone format")
            return
        if email and not self._is_valid_email(email):
            messagebox.showerror("Error", "Invalid email")
            return

        self.cursor.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
            (name, phone, email)
        )
        self.conn.commit()

    def update_contact(self, contact_id, name, phone, email):
        if not self._is_valid_phone(phone):
            messagebox.showerror("Error", "Invalid phone format")
            return
        if email and not self._is_valid_email(email):
            messagebox.showerror("Error", "Invalid email")
            return

        self.cursor.execute("""
        UPDATE contacts
        SET name=?, phone=?, email=?
        WHERE id=?
        """, (name, phone, email, contact_id))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM contacts")
        return self.cursor.fetchall()

    def delete_contact(self, contact_id):
        self.cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        self.conn.commit()

    def search(self, keyword):
        keyword = f"%{keyword}%"
        self.cursor.execute("""
        SELECT * FROM contacts
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
        """, (keyword, keyword, keyword))
        return self.cursor.fetchall()

    # ✅ EXPORT TO EXCEL
    def export_to_excel(self, file_name="contacts.xlsx"):
        self.cursor.execute("SELECT * FROM contacts")
        data = self.cursor.fetchall()

        if not data:
            return False

        df = pd.DataFrame(data, columns=["ID", "Name", "Phone", "Email"])
        df.to_excel(file_name, index=False)

        return True



class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.selected_id = None

        root.title("📇 Contact Manager")
        root.geometry("720x500")

        # 🌙 DARK MODE
        bg = "#1e1e2f"
        fg = "#ffffff"

        root.configure(bg=bg)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#2e2e3e",
                        fieldbackground="#2e2e3e",
                        foreground="white")

        style.configure("Treeview.Heading",
                        background="#444",
                        foreground="white")

        main = tk.Frame(root, bg=bg)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        form = tk.LabelFrame(main, text="Contact Details", bg=bg, fg=fg)
        form.pack(fill="x", pady=5)

        tk.Label(form, text="Name", bg=bg, fg=fg).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form, text="Phone", bg=bg, fg=fg).grid(row=0, column=2, padx=5)
        tk.Label(form, text="Email", bg=bg, fg=fg).grid(row=1, column=0, padx=5)

        self.name_entry = tk.Entry(form, bg="#2e2e3e", fg="white", insertbackground="white")
        self.phone_entry = tk.Entry(form, bg="#2e2e3e", fg="white", insertbackground="white")
        self.email_entry = tk.Entry(form, bg="#2e2e3e", fg="white", insertbackground="white")

        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=0, column=3)
        self.email_entry.grid(row=1, column=1)

        
        tk.Label(main, text="🔍 Search:", bg=bg, fg=fg).pack(anchor="w")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.live_search)

        search_entry = tk.Entry(main, textvariable=self.search_var,
                                bg="#2e2e3e", fg="white",
                                insertbackground="white")
        search_entry.pack(fill="x", pady=5)

        btn_frame = tk.Frame(main, bg=bg)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="➕ Add", bg="#4CAF50", fg="white",
                  command=self.add_contact).pack(side="left", padx=5)

        tk.Button(btn_frame, text="✏️ Update", bg="#2196F3", fg="white",
                  command=self.update_contact).pack(side="left", padx=5)

        tk.Button(btn_frame, text="📋 Show All", bg="#9C27B0", fg="white",
                  command=self.load_contacts).pack(side="left", padx=5)

        tk.Button(btn_frame, text="❌ Delete", bg="#f44336", fg="white",
                  command=self.delete_contact).pack(side="left", padx=5)

        tk.Button(btn_frame, text="📁 Export", bg="#FF9800", fg="white",
                  command=self.export_contacts).pack(side="left", padx=5)

      
        self.tree = ttk.Treeview(main,
                                 columns=("ID", "Name", "Phone", "Email"),
                                 show="headings")

        for col in ("ID", "Name", "Phone", "Email"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.on_select)

        self.load_contacts()

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and phone required")
            return

        self.manager.add_contact(name, phone, email)
        self.clear()
        self.load_contacts()

    def update_contact(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select contact")
            return

        self.manager.update_contact(
            self.selected_id,
            self.name_entry.get(),
            self.phone_entry.get(),
            self.email_entry.get()
        )

        messagebox.showinfo("Success", "Contact updated")
        self.clear()
        self.load_contacts()

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact")
            return

        contact_id = self.tree.item(selected[0])["values"][0]
        self.manager.delete_contact(contact_id)
        self.load_contacts()

    def load_contacts(self):
        self.tree.delete(*self.tree.get_children())
        for c in self.manager.get_all():
            self.tree.insert("", "end", values=c)

    def live_search(self, *args):
        keyword = self.search_var.get()
        results = self.manager.search(keyword)

        self.tree.delete(*self.tree.get_children())

        for c in results:
            self.tree.insert("", "end", values=c)

    def export_contacts(self):
        success = self.manager.export_to_excel()

        if success:
            messagebox.showinfo("Success", "Exported to contacts.xlsx")
        else:
            messagebox.showwarning("Warning", "No data to export")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]

            self.selected_id = values[0]

            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            self.name_entry.insert(0, values[1])
            self.phone_entry.insert(0, values[2])
            self.email_entry.insert(0, values[3])

    def clear(self):
        self.selected_id = None
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)



def main():
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()