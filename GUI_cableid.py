import tkinter as tk
from tkinter import ttk
import sqlite3

class App:
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        self.root.title("Search for cable ID")

        self.select_vars = []
        self.select_ids = []
        self.select_widgets = []

        tables = ["description", "conductor", "manufacture", "temperature", "voltage", "main"]
        for i, table in enumerate(tables):
            if table != 'main':
                label = tk.Label(root, text=f"Select {table}:")
            else:
                label = tk.Label(root, text=f"Select gauge:")
            label.grid(row=i, column=0)

            var = tk.StringVar()
            self.select_vars.append(var)
            self.select_ids.append(None) #Inicializa com None

            select = ttk.Combobox(root, textvariable=var, state="readonly")
            select.grid(row=i, column=1)
            self.select_widgets.append(select)
            if table != "main":
                self.load_select_data(select, table)
            else:
                self.load_select_gauge(select, table)

            # Bind for update ID when select changes
            select.bind("<<ComboboxSelected>>", lambda event, index=i: self.update_select_id(index))

        self.button = tk.Button(root, text="Seek", command=self.seek)
        self.button.grid(row=len(tables), columnspan=2)

        self.label_text = tk.StringVar()
        self.label = tk.Label(root, textvariable=self.label_text)
        self.label.grid(row=len(tables) + 1, columnspan=2)

        # Textbox option
        self.text_area = tk.Text(root, height=5, width=40)
        self.text_area.grid(row=len(tables) + 2, columnspan=2)

    def load_select_data(self, select, table):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, name FROM {table}")
            data = cursor.fetchall()
            conn.close()

            select["values"] = [row[1] for row in data]
            select.data = {row[1]: row[0] for row in data} # Store the mapping name -> id

        except sqlite3.Error as e:
            print(f"An error occurred when loading the data: {e}")

    def load_select_gauge(self, select, table):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT DISTINCT gauge FROM {table}")
            data = cursor.fetchall()
            conn.close()

            select["values"] = [str(row[0]) for row in data]
            select.data = {str(row[0]): row[0] for row in data} # Store the mapping name -> id
            print("S")

        except sqlite3.Error as e:
            print(f"An error occurred when loading the data: {e}")

    def update_select_id(self, index):
        selected_name = self.select_vars[index].get()
        if selected_name:
            self.select_ids[index] = self.select_widgets[index].data[selected_name]
        else:
            self.select_ids[index] = None
        self.seek()

    def seek(self):
        if any(id is None for id in self.select_ids):
            self.label_text.set("Please select all values.")
            self.text_area.delete(1.0, tk.END) #Limpa a caixa de texto
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Query SQL for main table and foreign keys searches
            query = f"""SELECT id FROM main
            WHERE description_id = ? AND conductor_id = ? AND manufacture_id = ? AND temperature_id = ? AND voltage_id = ? AND gauge = ?
            """
            cursor.execute(query, self.select_ids)
            result = cursor.fetchone()
            conn.close()

            if result:
                #self.label_text.set(f"ID: {result[0]}, Descrição: {result[1]}")
                self.label_text.set(f"ID: {result[0]}")
                self.text_area.delete(1.0, tk.END)  # Limpa o texto anterior
               #self.text_area.insert(tk.END, f"ID: {result[0]}, Descrição: {result[1]}") #Insere o resultado na caixa de texto
                self.text_area.insert(tk.END, f"ID: {result[0]}") #Insere o resultado na caixa de texto
            else:
                self.label_text.set("Cable ID not found.")
                self.text_area.delete(1.0, tk.END) # Clean the textbox
        except sqlite3.Error as e:
            self.label_text.set(f"An error occurred when searching: {e}")
            self.text_area.delete(1.0, tk.END) # Clean the textbox

if __name__ == "__main__":
    db_path = "databases/mt.db"  # path/database.db
    root = tk.Tk()
    app = App(root, db_path)
    root.mainloop()