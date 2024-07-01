import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class RentalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de gestion des locations")
        self.create_widgets()
        self.update_stock()
        self.update_current_rentals()
        self.update_history()

    def create_widgets(self):
        # Frame pour les équipements
        stock_frame = ttk.LabelFrame(self.root, text="Équipements en stock")
        stock_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.stock_tree = ttk.Treeview(stock_frame, columns=("ID", "Nom", "Quantité"))
        self.stock_tree.heading("#0", text="", anchor=tk.CENTER)
        self.stock_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.stock_tree.heading("Nom", text="Nom", anchor=tk.CENTER)
        self.stock_tree.heading("Quantité", text="Quantité", anchor=tk.CENTER)
        self.stock_tree.column("#0", width=0, stretch=tk.NO)
        self.stock_tree.column("ID", width=50, anchor=tk.CENTER)
        self.stock_tree.column("Nom", width=150, anchor=tk.W)
        self.stock_tree.column("Quantité", width=100, anchor=tk.CENTER)
        self.stock_tree.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        stock_scrollbar = ttk.Scrollbar(stock_frame, orient=tk.VERTICAL, command=self.stock_tree.yview)
        stock_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.stock_tree.configure(yscrollcommand=stock_scrollbar.set)

        self.stock_tree.bind('<Double-1>', self.load_selected_equipment)

        add_equipment_frame = ttk.Frame(stock_frame)
        add_equipment_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)

        ttk.Label(add_equipment_frame, text="Nom:").grid(row=0, column=0, padx=5, pady=5)
        self.equipment_name_entry = ttk.Entry(add_equipment_frame)
        self.equipment_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_equipment_frame, text="Quantité:").grid(row=1, column=0, padx=5, pady=5)
        self.stock_entry = ttk.Entry(add_equipment_frame)
        self.stock_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(add_equipment_frame, text="Ajouter", command=self.add_equipment).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(add_equipment_frame, text="Modifier", command=self.modify_equipment).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(add_equipment_frame, text="Supprimer", command=self.delete_equipment).grid(row=2, column=2, padx=5, pady=5)

        # Frame pour les locations actuelles
        current_rentals_frame = ttk.LabelFrame(self.root, text="Locations en cours")
        current_rentals_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

        self.current_rentals_tree = ttk.Treeview(current_rentals_frame, columns=("ID", "Équipement", "Locataire", "Prise", "Retour", "Retourné"))
        self.current_rentals_tree.heading("#0", text="", anchor=tk.CENTER)
        self.current_rentals_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.current_rentals_tree.heading("Équipement", text="Équipement", anchor=tk.CENTER)
        self.current_rentals_tree.heading("Locataire", text="Locataire", anchor=tk.CENTER)
        self.current_rentals_tree.heading("Prise", text="Prise", anchor=tk.CENTER)
        self.current_rentals_tree.heading("Retour", text="Retour", anchor=tk.CENTER)
        self.current_rentals_tree.heading("Retourné", text="Retourné", anchor=tk.CENTER)
        self.current_rentals_tree.column("#0", width=0, stretch=tk.NO)
        self.current_rentals_tree.column("ID", width=50, anchor=tk.CENTER)
        self.current_rentals_tree.column("Équipement", width=150, anchor=tk.W)
        self.current_rentals_tree.column("Locataire", width=150, anchor=tk.W)
        self.current_rentals_tree.column("Prise", width=150, anchor=tk.CENTER)
        self.current_rentals_tree.column("Retour", width=150, anchor=tk.CENTER)
        self.current_rentals_tree.column("Retourné", width=100, anchor=tk.CENTER)
        self.current_rentals_tree.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.current_rentals_tree.bind('<Double-1>', self.load_selected_rental)

        current_rentals_scrollbar = ttk.Scrollbar(current_rentals_frame, orient=tk.VERTICAL, command=self.current_rentals_tree.yview)
        current_rentals_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.current_rentals_tree.configure(yscrollcommand=current_rentals_scrollbar.set)

        # Bouton pour le retour manuel des locations
        return_rental_frame = ttk.Frame(current_rentals_frame)
        return_rental_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)
        ttk.Button(return_rental_frame, text="Retourner l'équipement", command=self.return_equipment).grid(row=0, column=0, padx=5, pady=5)

        # Frame pour l'ajout/modification des locations
        rental_frame = ttk.LabelFrame(self.root, text="Ajouter/Modifier une location")
        rental_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)

        ttk.Label(rental_frame, text="Équipement:").grid(row=0, column=0, padx=5, pady=5)
        self.rental_equipment_name_entry = ttk.Entry(rental_frame)
        self.rental_equipment_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(rental_frame, text="Locataire:").grid(row=1, column=0, padx=5, pady=5)
        self.renter_name_entry = ttk.Entry(rental_frame)
        self.renter_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(rental_frame, text="Date de prise:").grid(row=2, column=0, padx=5, pady=5)
        self.take_date_entry = ttk.Entry(rental_frame)
        self.take_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(rental_frame, text="Heure de prise:").grid(row=3, column=0, padx=5, pady=5)
        self.take_time_combobox = ttk.Combobox(rental_frame, values=self.get_time_slots())
        self.take_time_combobox.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(rental_frame, text="Date de retour:").grid(row=4, column=0, padx=5, pady=5)
        self.return_date_entry = ttk.Entry(rental_frame)
        self.return_date_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(rental_frame, text="Heure de retour:").grid(row=5, column=0, padx=5, pady=5)
        self.return_time_combobox = ttk.Combobox(rental_frame, values=self.get_time_slots())
        self.return_time_combobox.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(rental_frame, text="Ajouter", command=self.add_rental).grid(row=6, column=0, padx=5, pady=5)

        # Frame pour l'historique des locations
        history_frame = ttk.LabelFrame(self.root, text="Historique des locations")
        history_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.NSEW)

        self.history_tree = ttk.Treeview(history_frame, columns=("ID", "Équipement", "Locataire", "Prise", "Retour", "Retourné"))
        self.history_tree.heading("#0", text="", anchor=tk.CENTER)
        self.history_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.history_tree.heading("Équipement", text="Équipement", anchor=tk.CENTER)
        self.history_tree.heading("Locataire", text="Locataire", anchor=tk.CENTER)
        self.history_tree.heading("Prise", text="Prise", anchor=tk.CENTER)
        self.history_tree.heading("Retour", text="Retour", anchor=tk.CENTER)
        self.history_tree.heading("Retourné", text="Retourné", anchor=tk.CENTER)
        self.history_tree.column("#0", width=0, stretch=tk.NO)
        self.history_tree.column("ID", width=50, anchor=tk.CENTER)
        self.history_tree.column("Équipement", width=150, anchor=tk.W)
        self.history_tree.column("Locataire", width=150, anchor=tk.W)
        self.history_tree.column("Prise", width=150, anchor=tk.CENTER)
        self.history_tree.column("Retour", width=150, anchor=tk.CENTER)
        self.history_tree.column("Retourné", width=100, anchor=tk.CENTER)
        self.history_tree.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        history_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)

        # Bouton pour mettre à jour l'historique des locations
        ttk.Button(history_frame, text="Mettre à jour l'historique", command=self.update_history).grid(row=1, column=0, padx=5, pady=5)

    def get_time_slots(self):
        time_slots = [f"{hour:02d}:00" for hour in range(24)]
        return time_slots

    def add_equipment(self):
        name = self.equipment_name_entry.get()
        stock = self.stock_entry.get()
        if not name or not stock:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs pour ajouter un équipement.")
            return

        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()
        c.execute("INSERT INTO equipments (name, stock) VALUES (?, ?)", (name, stock))
        conn.commit()
        conn.close()

        self.update_stock()
        self.equipment_name_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)

    def modify_equipment(self):
        selected_item = self.stock_tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un équipement à modifier.")
            return

        name = self.equipment_name_entry.get()
        stock = self.stock_entry.get()
        equipment_id = self.stock_tree.item(selected_item[0], "values")[0]
        if not name or not stock:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs pour modifier un équipement.")
            return

        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()
        c.execute("UPDATE equipments SET name = ?, stock = ? WHERE id = ?", (name, stock, equipment_id))
        conn.commit()
        conn.close()

        self.update_stock()
        self.equipment_name_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)

    def delete_equipment(self):
        selected_item = self.stock_tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un équipement à supprimer.")
            return

        equipment_id = self.stock_tree.item(selected_item[0], "values")[0]

        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()
        c.execute("DELETE FROM equipments WHERE id = ?", (equipment_id,))
        conn.commit()
        conn.close()

        self.update_stock()

    def load_selected_equipment(self, event):
        selected_item = self.stock_tree.selection()
        if not selected_item:
            return

        equipment = self.stock_tree.item(selected_item[0], "values")
        self.equipment_name_entry.delete(0, tk.END)
        self.equipment_name_entry.insert(0, equipment[1])
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, equipment[2])

    def add_rental(self):
        equipment_name = self.rental_equipment_name_entry.get()
        renter_name = self.renter_name_entry.get()
        take_date = self.take_date_entry.get()
        take_time = self.take_time_combobox.get()
        return_date = self.return_date_entry.get()
        return_time = self.return_time_combobox.get()
        if not equipment_name or not renter_name or not take_date or not take_time or not return_date or not return_time:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs pour ajouter une location.")
            return

        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()

        c.execute("SELECT id, stock FROM equipments WHERE name = ?", (equipment_name,))
        equipment = c.fetchone()
        if not equipment:
            messagebox.showerror("Erreur", "L'équipement spécifié n'existe pas.")
            conn.close()
            return

        equipment_id, stock = equipment
        if stock <= 0:
            messagebox.showerror("Erreur", "Stock insuffisant pour l'équipement sélectionné.")
            conn.close()
            return

        c.execute('''INSERT INTO rentals (equipment_id, renter_name, take_time, return_time, returned)
                     VALUES (?, ?, ?, ?, 0)''', (equipment_id, renter_name, f"{take_date} {take_time}", f"{return_date} {return_time}"))
        c.execute("UPDATE equipments SET stock = stock - 1 WHERE id = ?", (equipment_id,))
        conn.commit()
        conn.close()

        self.update_stock()
        self.update_current_rentals()

        self.rental_equipment_name_entry.delete(0, tk.END)
        self.renter_name_entry.delete(0, tk.END)
        self.take_date_entry.delete(0, tk.END)
        self.take_time_combobox.set('')
        self.return_date_entry.delete(0, tk.END)
        self.return_time_combobox.set('')

    def load_selected_rental(self, event):
        selected_item = self.current_rentals_tree.selection()
        if not selected_item:
            return

        rental = self.current_rentals_tree.item(selected_item[0], "values")
        self.rental_equipment_name_entry.delete(0, tk.END)
        self.rental_equipment_name_entry.insert(0, rental[1])
        self.renter_name_entry.delete(0, tk.END)
        self.renter_name_entry.insert(0, rental[2])
        self.take_date_entry.delete(0, tk.END)
        self.take_date_entry.insert(0, rental[3].split()[0])
        self.take_time_combobox.set(rental[3].split()[1])
        self.return_date_entry.delete(0, tk.END)
        self.return_date_entry.insert(0, rental[4].split()[0])
        self.return_time_combobox.set(rental[4].split()[1])

    def update_stock(self):
        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()
        c.execute("SELECT id, name, stock FROM equipments")
        rows = c.fetchall()
        self.stock_tree.delete(*self.stock_tree.get_children())
        for row in rows:
            self.stock_tree.insert('', tk.END, values=row)
        conn.close()

    def update_current_rentals(self):
        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()
        c.execute('''SELECT rentals.id, equipments.name, rentals.renter_name, rentals.take_time, rentals.return_time, rentals.returned
                     FROM rentals
                     JOIN equipments ON rentals.equipment_id = equipments.id
                     WHERE rentals.returned = 0''')
        rows = c.fetchall()
        self.current_rentals_tree.delete(*self.current_rentals_tree.get_children())
        for row in rows:
            self.current_rentals_tree.insert('', tk.END, values=row)
        conn.close()

    def update_history(self):
        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()
        c.execute('''SELECT rentals.id, equipments.name, rentals.renter_name, rentals.take_time, rentals.return_time, rentals.returned
                     FROM rentals
                     JOIN equipments ON rentals.equipment_id = equipments.id''')
        rows = c.fetchall()
        self.history_tree.delete(*self.history_tree.get_children())
        for row in rows:
            self.history_tree.insert('', tk.END, values=row)
        conn.close()

    def return_equipment(self):
        selected_item = self.current_rentals_tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une location à retourner.")
            return

        rental_id = self.current_rentals_tree.item(selected_item[0], "values")[0]
        conn = sqlite3.connect('rentals.db')
        c = conn.cursor()
        c.execute("UPDATE rentals SET returned = 1 WHERE id = ?", (rental_id,))
        c.execute("UPDATE equipments SET stock = stock + 1 WHERE id = (SELECT equipment_id FROM rentals WHERE id = ?)", (rental_id,))
        conn.commit()
        conn.close()
        self.update_stock()
        self.update_current_rentals()
        self.update_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = RentalManagementSystem(root)
    root.mainloop()
