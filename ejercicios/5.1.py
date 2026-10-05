import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime

clientes = []
archivo_clientes = "base_de_datos_clientes.txt"

def cargar_desde_archivo():
    global clientes
    if os.path.exists(archivo_clientes):
        try:
            with open(archivo_clientes, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    parametros = linea.strip().split("|")
                    if len(parametros) == 4:
                        clientes.append(tuple(parametros))
                    else:
                        print(f"Warning: Ignoring line due to incorrect number of fields: {linea}")
        except Exception as e:
            messagebox.showerror("Error al cargar", f"Error al cargar clientes desde el archivo: {e}")
    else:
        try:
            with open(archivo_clientes, "w", encoding="utf-8") as archivo:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el archivo: {e}")

def guardar_en_archivo():
    try:
        with open(archivo_clientes, "w", encoding="utf-8") as archivo:
            for cliente in clientes:
                linea = "|".join(cliente)
                archivo.write(linea + "\n")
    except Exception as e:
        messagebox.showerror("Error al guardar", f"Error al guardar clientes en el archivo: {e}")

def agregar_cliente():
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni = entry_dni.get().strip()
    direccion = entry_direccion.get().strip()
    if not all([nombre, apellido, dni, direccion]):
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
        return
    clientes.append((nombre, apellido, dni, direccion))
    guardar_en_archivo()
    actualizar_tabla_clientes()
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)

def actualizar_tabla_clientes():
    for row in tree_clientes.get_children():
        tree_clientes.delete(row)
    for idx, cliente in enumerate(clientes, start=1):
        nombre, apellido, dni, direccion = cliente
        tree_clientes.insert('', tk.END, values=(idx, nombre, apellido, dni, direccion))

def registrar_pago():
    selected_item = tree_clientes.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar cliente", "Por favor, selecciona un cliente de la tabla.")
        return

    cliente_index = tree_clientes.index(selected_item[0])
    nombre, apellido, _, _ = clientes[cliente_index]

    ventana_pago = tk.Toplevel(root)
    ventana_pago.title("Registrar Pago")

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    tk.Label(ventana_pago, text="Mes de Pago:").grid(row=0, column=0, padx=5, pady=2)
    mes_seleccionado = ttk.Combobox(ventana_pago, values=meses, state="readonly")
    mes_seleccionado.grid(row=0, column=1, padx=5, pady=2)
    mes_seleccionado.set(meses[(datetime.date.today().month) - 1])

    tk.Label(ventana_pago, text="Monto Pagado:").grid(row=1, column=0, padx=5, pady=2)
    monto_entry = tk.Entry(ventana_pago)
    monto_entry.grid(row=1, column=1, padx=5, pady=2)

    def guardar_pago():
        mes = mes_seleccionado.get()
        monto = monto_entry.get()
        if not mes or not monto:
            messagebox.showwarning("Datos incompletos", "Por favor, selecciona el mes y el monto.")
            return
        try:
            monto = float(monto)
            if monto <= 0:
                raise ValueError("El monto debe ser mayor que cero.")
        except ValueError as e:
            messagebox.showwarning("Monto inválido", "Por favor, introduce un monto válido y mayor que cero.")
            return

        filename = f"{nombre}_{apellido}_pagos.txt"
        filepath = os.path.join("", filename)

        try:
            with open(filepath, "a", encoding="utf-8") as archivo_pagos:
                archivo_pagos.write(f"{mes}|{datetime.date.today().year}|{monto}\n")
            messagebox.showinfo("Pago registrado", f"Pago de {monto} registrado para {mes}.")
            ventana_pago.destroy()
        except Exception as e:
            messagebox.showerror("Error al guardar pago", f"Error al guardar el pago: {e}")

    btn_guardar_pago = tk.Button(ventana_pago, text="Registrar Pago", command=guardar_pago)
    btn_guardar_pago.grid(row=2, column=0, columnspan=2, pady=10)

def ventana_cliente():
    global entry_nombre, entry_apellido, entry_dni, entry_direccion, tree_clientes
    ventana = tk.Toplevel(root)
    ventana.title("Gestión de Clientes")
    ventana.geometry("650x400")

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
        tree_clientes.column(col, width=100 if col != '#' else 50, anchor='center')
    tree_clientes.pack(pady=10)
    actualizar_tabla_clientes()

    btn_registrar_pago = tk.Button(ventana, text="Registrar Pago", width=20, command=registrar_pago)
    btn_registrar_pago.pack(pady=5)

cargar_desde_archivo()

root = tk.Tk()
root.title("Menú Principal")
root.geometry("300x200")
root.resizable(False, False)
root.configure(bg="#ADD8E6")

frame_botones = tk.Frame(root, bg="#ADD8E6")
frame_botones.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

btn_gestion_clientes = tk.Button(frame_botones, text="Gestión de Clientes", width=18, command=ventana_cliente,
                                  bg="#FFFFFF", relief=tk.RAISED, borderwidth=2)
btn_gestion_clientes.pack(pady=5, padx=10)

btn_salir = tk.Button(frame_botones, text="Salir", width=10, command=root.quit,
                       bg="#FFFFFF", relief=tk.RAISED, borderwidth=2)
btn_salir.pack(pady=5, padx=10)

root.mainloop()