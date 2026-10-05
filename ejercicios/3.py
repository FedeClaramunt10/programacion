import tkinter as tk
from tkinter import ttk, messagebox
import os

clientes = []

# Ruta del archivo
archivo_clientes = "base_de_datos_clientes.txt"

# Función para cargar clientes desde archivo
def cargar_desde_archivo():
    global clientes
    if os.path.exists(archivo_clientes):
        with open(archivo_clientes, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                parametros = linea.strip().split("|")
                if len(parametros) == 4:
                    clientes.append(tuple(parametros))
    else:
        # Si no existe, crea el archivo vacío
        with open(archivo_clientes, "w", encoding="utf-8") as archivo:
            pass

# Función para guardar clientes en archivo
def guardar_en_archivo():
    with open(archivo_clientes, "w", encoding="utf-8") as archivo:
        for cliente in clientes:
            linea = "|".join(cliente)
            archivo.write(linea + "\n")


def agregar_cliente():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni = entry_dni.get().strip()
    direccion = entry_direccion.get().strip()
    if not all([nombre, apellido, dni, direccion]):
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
        return
    clientes.append((nombre, apellido, dni, direccion))
    guardar_en_archivo()  # Guardar cuando agregamos
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

# CARGA los clientes del archivo cuando inicia la app
cargar_desde_archivo()

# Resto de la interfaz (menú principal, etc.)
root = tk.Tk()
root.title("Menú Principal")

main_menu = tk.Menu(root)
file_menu = tk.Menu(main_menu, tearoff=0)
file_menu.add_command(label="Gestión de Clientes", command=ventana_cliente)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)
main_menu.add_cascade(label="Archivo", menu=file_menu)
root.config(menu=main_menu)

root.mainloop()
