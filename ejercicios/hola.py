import tkinter as tk
from tkinter import ttk, messagebox

clientes = []  # Lista temporal para almacenar clientes

def agregar_cliente():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni = entry_dni.get().strip()
    direccion = entry_direccion.get().strip()
    if not all([nombre, apellido, dni, direccion]):
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
        return
    clientes.append((nombre, apellido, dni, direccion))
    actualizar_tabla_clientes()
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)

def actualizar_tabla_clientes():
    for row in tree_clientes.get_children():
        tree_clientes.delete(row)
    for idx, (nombre, apellido, dni, direccion) in enumerate(clientes, start=1):
        tree_clientes.insert('', tk.END, values=(idx, nombre, apellido, dni, direccion))

def ventana_cliente():
    global entry_nombre, entry_apellido, entry_dni, entry_direccion, tree_clientes
    ventana = tk.Toplevel(root)
    ventana.title("Gestión de Clientes")
    ventana.geometry("540x350")

    frame_agregar = tk.Frame(ventana)
    frame_agregar.pack(pady=10)

    tk.Label(frame_agregar, text="Nombre:").grid(row=0, column=0, padx=5, pady=2)
    entry_nombre = tk.Entry(frame_agregar, width=14)
    entry_nombre.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_agregar, text="Apellido:").grid(row=0, column=2, padx=5, pady=2)
    entry_apellido = tk.Entry(frame_agregar, width=14)
    entry_apellido.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(frame_agregar, text="DNI:").grid(row=1, column=0, padx=5, pady=2)
    entry_dni = tk.Entry(frame_agregar, width=14)
    entry_dni.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(frame_agregar, text="Dirección:").grid(row=1, column=2, padx=5, pady=2)
    entry_direccion = tk.Entry(frame_agregar, width=14)
    entry_direccion.grid(row=1, column=3, padx=5, pady=2)

    btn_agregar = tk.Button(ventana, text="Agregar Cliente", width=20, command=agregar_cliente)
    btn_agregar.pack(pady=5)

    columns = ('#', 'Nombre', 'Apellido', 'DNI', 'Dirección')
    tree_clientes = ttk.Treeview(ventana, columns=columns, show='headings', height=8)
    for col in columns:
        tree_clientes.heading(col, text=col)
        tree_clientes.column(col, width=100 if col != '#' else 40, anchor='center')
    tree_clientes.pack(pady=10)
    actualizar_tabla_clientes()

def ventana_estado():
    ventana = tk.Toplevel(root)
    ventana.title("Estado del Servicio")
    ventana.geometry("300x200")
    tk.Label(ventana, text="Aquí va el estado del servicio", font=('Arial', 12)).pack(pady=30)

def ventana_facturacion():
    ventana = tk.Toplevel(root)
    ventana.title("Facturación")
    ventana.geometry("300x200")
    tk.Label(ventana, text="Aquí va la facturación", font=('Arial', 12)).pack(pady=30)

root = tk.Tk()
root.title("Internet Service - Gestión")
root.geometry("340x270")
root.resizable(False, False)

tk.Label(root, text="Gestión de Negocio de Internet", font=('Arial', 14, 'bold')).pack(pady=20)

btn_cliente = tk.Button(root, text="Cliente", width=20, height=2, command=ventana_cliente)
btn_cliente.pack(pady=10)

btn_estado = tk.Button(root, text="Estado", width=20, height=2, command=ventana_estado)
btn_estado.pack(pady=10)

btn_facturacion = tk.Button(root, text="Facturación", width=20, height=2, command=ventana_facturacion)
btn_facturacion.pack(pady=10)

root.mainloop()
