import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime
from fpdf import FPDF  # Importa la clase FPDF

clientes = []
archivo_clientes = "base_de_datos_clientes.txt"

def cargar_desde_archivo():
    global clientes
    if os.path.exists(archivo_clientes):
        try:
            with open(archivo_clientes, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    parametros = linea.strip().split("|")
                    if len(parametros) == 5:  # includes fecha_instalacion
                        try:
                            datetime.datetime.strptime(parametros[4], '%m/%d/%Y')  # validate date
                            clientes.append(tuple(parametros))
                        except ValueError:
                            print(f"Advertencia: Ignorando línea debido a formato de fecha inválido: {linea}")
                    else:
                        print(f"Advertencia: Ignorando línea debido a número incorrecto de campos: {linea}")
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
    fecha_instalacion = entry_fecha_instalacion.get().strip()  # added
    try:
        datetime.datetime.strptime(fecha_instalacion, '%m/%d/%Y')
    except ValueError:
        messagebox.showwarning("Formato de fecha incorrecto", "Por favor, introduce la fecha en formato MM/DD/YYYY.")
        return
    if not all([nombre, apellido, dni, direccion, fecha_instalacion]):
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
        return
    clientes.append((nombre, apellido, dni, direccion, fecha_instalacion))  # added
    guardar_en_archivo()
    actualizar_tabla_clientes()
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_fecha_instalacion.delete(0, tk.END)

def actualizar_tabla_clientes():
    for row in tree_clientes.get_children():
        tree_clientes.delete(row)
    for idx, cliente in enumerate(clientes, start=1):
        nombre, apellido, dni, direccion, fecha_instalacion = cliente  # added
        tree_clientes.insert('', tk.END, values=(idx, nombre, apellido, dni, direccion, fecha_instalacion))  # added

def registrar_pago(nombre, apellido, mes, monto, ventana_facturacion):
    filename = f"{nombre}_{apellido}_pagos.txt"
    filepath = os.path.join("", filename)

    try:
        with open(filepath, "a", encoding="utf-8") as archivo_pagos:
            archivo_pagos.write(f"{mes}|{datetime.date.today().year}|{monto}\n")
        messagebox.showinfo("Pago registrado", f"Pago de {monto} registrado para {mes}.")

        # --- Generación de PDF ---
        pdf = FPDF()  # Crea un nuevo objeto PDF
        pdf.add_page()  # Agrega una página
        pdf.set_font("Arial", size=12)  # Establece la fuente

        # Detalles de la Factura
        pdf.cell(200, 10, txt=f"Factura de Pago", ln=1, align="C") # Título
        pdf.cell(200, 10, txt=f"Cliente: {nombre} {apellido}", ln=1, align="L") # Nombre del Cliente
        pdf.cell(200, 10, txt=f"Mes: {mes}", ln=1, align="L") # Mes
        pdf.cell(200, 10, txt=f"Fecha de Pago: {datetime.date.today().strftime('%m/%d/%Y')}", ln=1, align="L") # Fecha de pago
        pdf.cell(200, 10, txt=f"Monto: ${monto}", ln=1, align="L") # Monto del pago

        # Guarda el PDF (personaliza el nombre del archivo)
        invoice_filename = f"Factura_{nombre}_{apellido}_{mes}.pdf"
        try:
            pdf.output(invoice_filename)  # Guarda el PDF
            messagebox.showinfo("Factura generada", f"Factura generada como {invoice_filename}")
        except Exception as pdf_e:
            messagebox.showerror("Error al guardar la factura", f"Error al guardar la factura: {pdf_e}")


    except Exception as e:
        messagebox.showerror("Error al guardar pago", f"Error al guardar el pago: {e}")

def ventana_registrar_pago():
    selected_item = tree_clientes.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar cliente", "Por favor, selecciona un cliente de la tabla.")
        return

    cliente_index = tree_clientes.index(selected_item[0])
    nombre, apellido, _, _, _ = clientes[cliente_index]

    ventana_pago = tk.Toplevel(root)
    ventana_pago.title(f"Registrar Pago para {nombre} {apellido}")
    ventana_pago.geometry("300x300")  # setting geometry for the window
    ventana_pago.configure(bg="#ADD8E6")  # setting the backgroung color
    ventana_pago.resizable(False, False)  # setting to non resizable

    frame_ventana_pago = tk.Frame(ventana_pago, bg="#ADD8E6")  # setting the frame and its color
    frame_ventana_pago.pack(expand=True, fill="both")  # Use pack with expand and fill

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    tk.Label(frame_ventana_pago, text="Mes de Pago:", bg="#ADD8E6").pack(pady=2)
    mes_seleccionado = ttk.Combobox(frame_ventana_pago, values=meses, state="readonly")
    mes_seleccionado.pack(pady=2)
    mes_seleccionado.set(meses[(datetime.date.today().month) - 1])

    tk.Label(frame_ventana_pago, text="Monto Pagado:", bg="#ADD8E6").pack(pady=2)
    monto_entry = tk.Entry(frame_ventana_pago)
    monto_entry.pack(pady=2)

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

        registrar_pago(nombre, apellido, mes, monto, ventana_pago)
        ventana_pago.destroy()

    # adding style
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), background="#FFFFFF", relief="raised", borderwidth=2, padding=8)

    btn_guardar_pago = ttk.Button(frame_ventana_pago, text="Registrar Pago", command=guardar_pago, style="TButton")
    btn_guardar_pago.pack(pady=5)

    btn_atras = ttk.Button(frame_ventana_pago, text="Atrás", command=ventana_pago.destroy, style="TButton")
    btn_atras.pack(pady=5)


def consultar_pagos():
    selected_item = tree_clientes.selection()
    if not selected_item:
        messagebox.showwarning("Seleccionar cliente", "Por favor, selecciona un cliente de la tabla.")
        return

    cliente_index = tree_clientes.index(selected_item[0])
    nombre, apellido, _, _, _ = clientes[cliente_index]

    filename = f"{nombre}_{apellido}_pagos.txt"
    filepath = os.path.join("", filename)

    try:
        with open(filepath, "r", encoding="utf-8") as archivo_pagos:
            pagos = archivo_pagos.readlines()
    except FileNotFoundError:
        messagebox.showinfo("Sin pagos", "No se encontraron pagos registrados para este cliente.")
        return
    except Exception as e:
        messagebox.showerror("Error al leer pagos", f"Error al leer el archivo de pagos: {e}")
        return

    ventana_consulta = tk.Toplevel(root)
    ventana_consulta.title(f"Pagos de {nombre} {apellido}")
    ventana_consulta.geometry("500x400")  # setting geometry for the window
    ventana_consulta.configure(bg="#ADD8E6")  # setting the backgroung color
    ventana_consulta.resizable(False, False)  # setting to non resizable

    frame_ventana_consulta = tk.Frame(ventana_consulta, bg="#ADD8E6")  # setting the frame and its color
    frame_ventana_consulta.pack(expand=True, fill="both")  # Use pack with expand and fill

    tree_pagos = ttk.Treeview(frame_ventana_consulta, columns=('Mes', 'Año', 'Monto'), show='headings')
    tree_pagos.heading('Mes', text='Mes')
    tree_pagos.heading('Año', text='Año')
    tree_pagos.heading('Monto', text='Monto')

    if 'pagos' in locals():
        for pago in pagos:
            mes, año, monto = pago.strip().split("|")
            tree_pagos.insert('', tk.END, values=(mes, año, monto))
    else:
        messagebox.showinfo("Sin pagos", "No se encontraron pagos registrados para este cliente.")
        return

    tree_pagos.pack(pady=10)

    # adding style
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), background="#FFFFFF", relief="raised", borderwidth=2, padding=8)

    btn_atras = ttk.Button(frame_ventana_consulta, text="Atrás", command=ventana_consulta.destroy, style="TButton")
    btn_atras.pack(pady=5)


def consultar_facturacion():
    ventana_seleccion_cliente = tk.Toplevel(root)
    ventana_seleccion_cliente.title("Seleccionar Cliente para Facturación")
    ventana_seleccion_cliente.geometry("700x400")
    ventana_seleccion_cliente.configure(bg="#ADD8E6")  # setting the backgroung color
    ventana_seleccion_cliente.resizable(False, False)  # setting to non resizable

    frame_ventana_seleccion_cliente = tk.Frame(ventana_seleccion_cliente, bg="#ADD8E6")  # setting the frame and its color
    frame_ventana_seleccion_cliente.pack(expand=True, fill="both")  # Use pack with expand and fill

    columns = ('#', 'Nombre', 'Apellido', 'DNI', 'Dirección', 'Fecha Instalación')
    tree_clientes_facturacion = ttk.Treeview(frame_ventana_seleccion_cliente, columns=columns, show='headings')
    for col in columns:
        tree_clientes_facturacion.heading(col, text=col)
        tree_clientes_facturacion.column(col, width=100 if col not in ('#') else 50, anchor='center')
    tree_clientes_facturacion.pack(pady=10, padx=10)

    # Populate the treeview
    for idx, cliente in enumerate(clientes, start=1):
        nombre, apellido, dni, direccion, fecha_instalacion = cliente
        tree_clientes_facturacion.insert('', tk.END, values=(idx, nombre, apellido, dni, direccion, fecha_instalacion))

    def verificar_pago():
        selected_item = tree_clientes_facturacion.selection()
        if not selected_item:
            messagebox.showwarning("Seleccionar cliente", "Por favor, selecciona un cliente de la tabla.")
            return

        cliente_index = tree_clientes_facturacion.index(selected_item[0])
        try:
            nombre, apellido, _, _, fecha_instalacion_str = clientes[cliente_index]
            fecha_instalacion = datetime.datetime.strptime(fecha_instalacion_str, '%m/%d/%Y').date()
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Error al seleccionar el cliente.")
            return

        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes_actual_num = datetime.date.today().month
        mes_actual = meses[mes_actual_num - 1]
        año_actual = datetime.date.today().year

        # Calculate the due date
        dia_instalacion = fecha_instalacion.day
        try:
            fecha_vencimiento = datetime.date(año_actual, mes_actual_num, dia_instalacion)
        except ValueError:
            # Handle cases where the day is invalid for the month (e.g., Feb 30)
            # Get the last day of the month
            if mes_actual_num == 12:
                mes_siguiente = 1
                año_siguiente = año_actual + 1
            else:
                mes_siguiente = mes_actual_num + 1
                año_siguiente = año_actual

            try:
                fecha_vencimiento = datetime.date(año_siguiente, mes_siguiente, 1) + datetime.timedelta(days=-1)
            except ValueError:
                fecha_vencimiento = None  # if an error persist.

        filename = f"{nombre}_{apellido}_pagos.txt"
        filepath = os.path.join("", filename)

        pago_encontrado = False
        if fecha_vencimiento:  # If an end date was found, continue
            try:
                with open(filepath, "r", encoding="utf-8") as archivo_pagos:
                    for pago in archivo_pagos:
                        mes, año, _ = pago.strip().split("|")
                        if mes == mes_actual and int(año) == año_actual:
                            pago_encontrado = True
                            break
            except FileNotFoundError:
                pass  # No hay archivo, así que no ha pagado
            except Exception as e:
                messagebox.showerror("Error al leer pagos", f"Error al leer el archivo de pagos: {e}")
                return

        ventana_facturacion = tk.Toplevel(root)
        ventana_facturacion.title(f"Facturación de {nombre} {apellido}")
        ventana_facturacion.geometry("300x350")  # setting geometry for the window
        ventana_facturacion.configure(bg="#ADD8E6")  # setting the backgroung color
        ventana_facturacion.resizable(False, False)  # setting to non resizable

        frame_ventana_facturacion = tk.Frame(ventana_facturacion, bg="#ADD8E6")  # setting the frame and its color
        frame_ventana_facturacion.pack(expand=True, fill="both")  # Use pack with expand and fill

        if fecha_vencimiento:
            tk.Label(frame_ventana_facturacion, text=f"Fecha de Vencimiento: {fecha_vencimiento.strftime('%m/%d/%Y')}", bg="#ADD8E6").pack(pady=5)
        else:
            tk.Label(frame_ventana_facturacion, text="Fecha de Vencimiento: No se pudo calcular", bg="#ADD8E6").pack(pady=5)

        if pago_encontrado:
            tk.Label(frame_ventana_facturacion, text=f"El cliente ya pagó el mes de {mes_actual}.", bg="#ADD8E6").pack(pady=5)
        else:
            tk.Label(frame_ventana_facturacion, text=f"El cliente NO ha pagado el mes de {mes_actual}.", bg="#ADD8E6").pack(pady=5)

            tk.Label(frame_ventana_facturacion, text="Monto a pagar:", bg="#ADD8E6").pack(pady=2)
            monto_entry = tk.Entry(frame_ventana_facturacion)
            monto_entry.pack(pady=2)

            def pagar_mes():
                monto = monto_entry.get()
                if not monto:
                    messagebox.showwarning("Monto requerido", "Por favor, introduce el monto a pagar.")
                    return
                try:
                    monto = float(monto)
                    if monto <= 0:
                        raise ValueError("El monto debe ser mayor que cero.")
                except ValueError as e:
                    messagebox.showwarning("Monto inválido", "Por favor, introduce un monto válido y mayor que cero.")
                    return

                registrar_pago(nombre, apellido, mes_actual, monto, ventana_facturacion)
                ventana_facturacion.destroy()
                ventana_seleccion_cliente.destroy()

            # adding style
            style = ttk.Style()
            style.configure("TButton", font=("Arial", 12), background="#FFFFFF", relief="raised", borderwidth=2, padding=8)

            btn_pagar = ttk.Button(frame_ventana_facturacion, text="Registrar Pago", command=pagar_mes, style="TButton")
            btn_pagar.pack(pady=5)

        btn_atras = ttk.Button(frame_ventana_facturacion, text="Atrás", command=ventana_facturacion.destroy, style="TButton")
        btn_atras.pack(pady=5)

        ventana_seleccion_cliente.destroy()  # Close the selection window after processing

    # adding style
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), background="#FFFFFF", relief="raised", borderwidth=2, padding=8)

    btn_verificar = ttk.Button(frame_ventana_seleccion_cliente, text="Verificar Pago", command=verificar_pago, style="TButton")
    btn_verificar.pack(pady=10)

    btn_atras = ttk.Button(frame_ventana_seleccion_cliente, text="Atrás", command=ventana_seleccion_cliente.destroy, style="TButton")
    btn_atras.pack(pady=5)


def ventana_cliente():
    global entry_nombre, entry_apellido, entry_dni, entry_direccion, tree_clientes, entry_fecha_instalacion  # added
    ventana = tk.Toplevel(root)
    ventana.title("Gestión de Clientes")
    ventana.geometry("600x550")  # set the geometry for the window to be larger and more space for everything.
    ventana.configure(bg="#ADD8E6") # setting the backgroung color
    ventana.resizable(False, False) # setting to non resizable

    frame_ventana = tk.Frame(ventana, bg="#ADD8E6") # setting the frame and its color
    frame_ventana.pack(expand=True, fill="both") # Use pack with expand and fill

    frame_agregar = tk.Frame(frame_ventana, bg="#ADD8E6") # setting the frame and its color
    frame_agregar.pack(pady=10)

    tk.Label(frame_agregar, text="Nombre:", bg="#ADD8E6").grid(row=0, column=0, padx=5, pady=2)
    entry_nombre = tk.Entry(frame_agregar, width=14)
    entry_nombre.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_agregar, text="Apellido:", bg="#ADD8E6").grid(row=0, column=2, padx=5, pady=2)
    entry_apellido = tk.Entry(frame_agregar, width=14)
    entry_apellido.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(frame_agregar, text="DNI:", bg="#ADD8E6").grid(row=1, column=0, padx=5, pady=2)
    entry_dni = tk.Entry(frame_agregar, width=14)
    entry_dni.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(frame_agregar, text="Dirección:", bg="#ADD8E6").grid(row=1, column=2, padx=5, pady=2)
    entry_direccion = tk.Entry(frame_agregar, width=14)
    entry_direccion.grid(row=1, column=3, padx=5, pady=2)

    # New field for installation date
    tk.Label(frame_agregar, text="Fecha Instalación (MM/DD/YYYY):", bg="#ADD8E6").grid(row=2, column=0, padx=5, pady=2)
    entry_fecha_instalacion = tk.Entry(frame_agregar, width=14)
    entry_fecha_instalacion.grid(row=2, column=1, padx=5, pady=2)

    columns = ('#', 'Nombre', 'Apellido', 'DNI', 'Dirección', 'Fecha Instalación')  # added
    tree_clientes = ttk.Treeview(frame_agregar, columns=columns, show='headings')  # added
    for col in columns:
        tree_clientes.heading(col, text=col)
        tree_clientes.column(col, width=100 if col not in ('#') else 50, anchor='center')
    tree_clientes.grid(row=3, column=0, columnspan=4, pady=10, padx=10)
    actualizar_tabla_clientes()

    # adding style
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), background="#FFFFFF", relief="raised", borderwidth=2, padding=8)

    buttons_frame = tk.Frame(frame_ventana, bg="#ADD8E6")  # setting the frame and its color
    buttons_frame.pack(expand=True, fill="both") # Use pack with expand and fill

    btn_atras = ttk.Button(buttons_frame, text="Atrás", width=10, command=ventana.destroy, style="TButton")
    btn_atras.pack(side=tk.LEFT, padx=5, pady=5)

    btn_agregar = ttk.Button(buttons_frame, text="Agregar Cliente", width=10, command=agregar_cliente, style="TButton")
    btn_agregar.pack(side=tk.LEFT, padx=5, pady=5)

    btn_registrar_pago = ttk.Button(buttons_frame, text="Registrar Pago", width=10, command=ventana_registrar_pago, style="TButton")
    btn_registrar_pago.pack(side=tk.LEFT, padx=5, pady=5)

    btn_consultar_pagos = ttk.Button(buttons_frame, text="Consultar Pagos", width=10, command=consultar_pagos, style="TButton")
    btn_consultar_pagos.pack(side=tk.LEFT, padx=5, pady=5)


cargar_desde_archivo()

root = tk.Tk()
root.title("Menú Principal")
root.geometry("300x400")  # Increased height
root.resizable(False, False)
root.configure(bg="#ADD8E6")

frame_botones = tk.Frame(root, bg="#ADD8E6")
frame_botones.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Add a ttk style
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), background="#FFFFFF", relief="raised", borderwidth=2, padding=8)

btn_gestion_clientes = ttk.Button(frame_botones, text="Gestión de Clientes", width=18, command=ventana_cliente, style="TButton")
btn_gestion_clientes.pack(pady=5, padx=10)

btn_consultar_facturacion = ttk.Button(frame_botones, text="Consultar Facturación", width=18, command=consultar_facturacion, style="TButton")
btn_consultar_facturacion.pack(pady=5, padx=10)

btn_salir = ttk.Button(frame_botones, text="Salir", width=10, command=root.quit, style="TButton")
btn_salir.pack(pady=5, padx=10)


root.mainloop()


