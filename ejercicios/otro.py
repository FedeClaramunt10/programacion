import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
global tree_clientes
# Conexión a MySQL
def conectar():
    print('conectando')
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='gestion_internet'
    )

# ----------- Gestión Clientes --------------
def cargar_clientes():
    
    for row in tree_clientes.get_children():
        tree_clientes.delete(row)
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        for row in cursor:
            tree_clientes.insert('', 'end', values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def ventana_clientes():
    
    ventana = tk.Toplevel(root)
    ventana.title("Gestión de Clientes")
    ventana.geometry("750x400")

    # Formulario
    form_frame = tk.Frame(ventana)
    form_frame.pack(pady=10)

    labels = ['Nombre', 'Apellido', 'DNI', 'Dirección', 'Teléfono', 'Email']
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
        e = tk.Entry(form_frame, width=25)
        e.grid(row=i, column=1, padx=5, pady=2)
        entries[label] = e

    # Funciones internas
    def agregar_cliente():
        datos = [entries[l].get().strip() for l in labels]
        if not all(datos[:4]):  # Validar campos obligatorios
            messagebox.showwarning("Campos vacíos", "Completar Nombre, Apellido, DNI y Dirección")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clientes (nombre, apellido, dni, direccion, telefono, email)
                VALUES (%s, %s, %s, %s, %s, %s)''', datos)
            conn.commit()
            conn.close()
            cargar_clientes()
            for e in entries.values():
                e.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Cliente agregado")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def borrar_cliente():
        selected = tree_clientes.focus()
        if not selected:
            return
        valores = tree_clientes.item(selected, 'values')
        cliente_id = valores[0]
        if messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
                conn.commit()
                conn.close()
                cargar_clientes()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_cliente_para_editar():
        selected = tree_clientes.focus()
        if not selected:
            return
        valores = tree_clientes.item(selected, 'values')
        for i, l in enumerate(labels):
            entries[l].delete(0, tk.END)
            entries[l].insert(0, valores[i+1])

    def editar_cliente():
        selected = tree_clientes.focus()
        if not selected:
            return
        valores = tree_clientes.item(selected, 'values')
        cliente_id = valores[0]
        datos = [entries[l].get().strip() for l in labels]
        if not all(datos[:4]):
            messagebox.showwarning("Campos vacíos", "Completar Nombre, Apellido, DNI y Dirección")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE clientes SET nombre=%s, apellido=%s, dni=%s, direccion=%s, telefono=%s, email=%s WHERE id=%s''',
                (*datos, cliente_id))
            conn.commit()
            conn.close()
            cargar_clientes()
            messagebox.showinfo("Éxito", "Cliente actualizado")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Botones
    btn_frame = tk.Frame(ventana)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Agregar", command=agregar_cliente).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Editar", command=editar_cliente).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Eliminar", command=borrar_cliente).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Cargar Datos", command=cargar_cliente_para_editar).grid(row=0, column=3, padx=5)

    # Tabla
    columns = ('ID', 'Nombre', 'Apellido', 'DNI', 'Dirección', 'Teléfono', 'Email')
    tree_clientes = ttk.Treeview(ventana, columns=columns, show='headings')
    for col in columns:
        tree_clientes.heading(col, text=col)
        tree_clientes.column(col, width=100)
    tree_clientes.pack(fill='both', expand=True)
    cargar_clientes()

# ----------- Estado y Facturación (simples) --------------
def ventana_estado():
    ventana = tk.Toplevel(root)
    ventana.title("Estado del Servicio")
    ventana.geometry("400x300")
    tk.Label(ventana, text="Estado del Servicio - Aquí va la funcionalidad", font=('Arial', 12)).pack(pady=20)

def ventana_facturacion():
    ventana = tk.Toplevel(root)
    ventana.title("Facturación")
    ventana.geometry("400x300")
    tk.Label(ventana, text="Facturación - Aquí va la funcionalidad", font=('Arial', 12)).pack(pady=20)

# ======= Ventana principal =======
root = tk.Tk()
root.title("Gestión de Internet - Empresa")
root.geometry("350x250")

tk.Label(root, text="Sistema de Gestión", font=('Arial', 14, 'bold')).pack(pady=10)

tk.Button(root, text="Clientes", width=20, command=ventana_clientes).pack(pady=5)
tk.Button(root, text="Estado Servicio", width=20, command=ventana_estado).pack(pady=5)
tk.Button(root, text="Facturación", width=20, command=ventana_facturacion).pack(pady=5)

root.mainloop()
