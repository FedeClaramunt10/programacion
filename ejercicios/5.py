
import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime  # Import the datetime module

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
                if len(parametros) == 5:  # Existing entries with fecha_pago
                    clientes.append(tuple(parametros))
                elif len(parametros) == 4:  # Older entries without fecha_pago
                    clientes.append(tuple(parametros + [""]))  # Add empty string for fecha_pago
                else:
                    print(f"Warning: Ignoring line due to incorrect number of fields: {linea}")
    else:
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
    # Initialize fecha_pago to None when a new client is added
    clientes.append((nombre, apellido, dni, direccion, ""))  # Add an empty string for fecha_pago
    guardar_en_archivo()  # Guardar cuando agregamos
    actualizar_tabla_clientes()
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)


def actualizar_tabla_clientes():
    for row in tree_clientes.get_children():
        tree_clientes.delete(row)
    for idx, cliente in enumerate(clientes, start=1):
        nombre, apellido, dni, direccion, fecha_pago = cliente  # unpack the tuple
        tree_clientes.insert('', tk.END, values=(idx, nombre, apellido, dni, direccion, fecha_pago)) # include fecha_pago

def registrar_pago():
    selected_item = tree_clientes.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar cliente", "Por favor, selecciona un cliente de la tabla.")
        return

    cliente_index = tree_clientes.index(selected_item[0])  # Get the index of the selected item

    # Get the current date and format it
    fecha_pago = datetime.date.today().strftime("%m/%d/%Y")

    # Update the fecha_pago in the clientes list
    cliente = list(clientes[cliente_index])  # Convert to list for modification
    cliente[4] = fecha_pago  # Update the fecha_pago element (index 4)
    clientes[cliente_index] = tuple(cliente)  # Convert back to tuple

    guardar_en_archivo()
    actualizar_tabla_clientes()
    messagebox.showinfo("Pago registrado", f"Pago registrado para el cliente en fecha: {fecha_pago}")



def ventana_cliente():
    global entry_nombre, entry_apellido, entry_dni, entry_direccion, tree_clientes
    ventana = tk.Toplevel(root)
    ventana.title("Gestión de Clientes")
    ventana.geometry("650x400")  # Increased height to accommodate the button

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

    columns = ('#', 'Nombre', 'Apellido', 'DNI', 'Dirección', 'Fecha Pago')  # Added 'Fecha Pago'
    tree_clientes = ttk.Treeview(ventana, columns=columns, show='headings', height=8)
    for col in columns:
        tree_clientes.heading(col, text=col)
        tree_clientes.column(col, width=100 if col not in ('#', 'Fecha Pago') else 80, anchor='center') # adjusted widths
    tree_clientes.pack(pady=10)
    actualizar_tabla_clientes()

    btn_registrar_pago = tk.Button(ventana, text="Registrar Pago", width=20, command=registrar_pago)
    btn_registrar_pago.pack(pady=5)


# CARGA los clientes del archivo cuando inicia la app
cargar_desde_archivo()

# Resto de la interfaz (botones en lugar del menú principal)
root = tk.Tk()
root.title("Menú Principal")

# Configure root window for a specific size and make it non-resizable
root.geometry("300x200")  # Set initial size
root.resizable(False, False)  # Make the window non-resizable

# Set background color for the root window
root.configure(bg="#ADD8E6")  # Light Blue

# Frame for the buttons (centered and with padding)
frame_botones = tk.Frame(root, bg="#ADD8E6")  # Ensure frame has the same background
frame_botones.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

# Botón para Gestión de Clientes
btn_gestion_clientes = tk.Button(frame_botones, text="Gestión de Clientes", width=18, command=ventana_cliente,
                                  bg="#FFFFFF", relief=tk.RAISED, borderwidth=2)  # Style the button
btn_gestion_clientes.pack(pady=5, padx=10)  # Add padding

# Botón para Salir
btn_salir = tk.Button(frame_botones, text="Salir", width=10, command=root.quit,
                       bg="#FFFFFF", relief=tk.RAISED, borderwidth=2)  # Style the button
btn_salir.pack(pady=5, padx=10)  # Add padding

root.mainloop()


