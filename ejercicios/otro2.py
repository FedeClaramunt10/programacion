import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Funciones de conexión y CRUD a MySQL
def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='tu_usuario',  # Cambia por tus datos
        password='tu_contraseña',
        database='gestion_internet'
    )

def obtener_clientes_bd():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def agregar_cliente_bd(nombre, apellido, dni, direccion, telefono, email):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre, apellido, dni, direccion, telefono, email) VALUES (%s,%s,%s,%s,%s,%s)",
            (nombre, apellido, dni, direccion, telefono, email))
        conn.commit()
        conn.close()
        return True, "Cliente agregado correctamente"
    except Exception as e:
        return False, str(e)

def eliminar_cliente_bd(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
    conn.commit()
    conn.close()

def editar_cliente_bd(cliente_id, nombre, apellido, dni, direccion, telefono, email):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE clientes SET nombre=%s, apellido=%s, dni=%s, direccion=%s, telefono=%s, email=%s WHERE id=%s''',
            (nombre, apellido, dni, direccion, telefono, email, cliente_id))
        conn.commit()
        conn.close()
        return True, "Cliente actualizado"
    except Exception as e:
        return False, str(e)

# --------- Ventana gestión clientes ---------
def ventana_clientes():
    global tree_clientes  # Declaro como variable global

    def cargar_clientes():
        for row in tree_clientes.get_children():
            tree_clientes.delete(row)
        clientes = obtener_clientes_bd()
        for c in clientes:
            tree_clientes.insert('', 'end', values=c)

    def limpiar_campos():
        for e in [entry_nombre, entry_apellido, entry_dni, entry_direccion, entry_telefono, entry_email]:
            e.delete(0, tk.END)

    def agregar():
        n = entry_nombre.get().strip()
        a = entry_apellido.get().strip()
        d = entry_dni.get().strip()
        dir = entry_direccion.get().strip()
        t = entry_telefono.get().strip()
        e_mail = entry_email.get().strip()
        if not n or not a or not d or not dir:
            messagebox.showwarning("Faltan datos", "Completar Nombre, Apellido, DNI y Dirección")
            return
        exito, msj = agregar_cliente_bd(n, a, d, dir, t, e_mail)
        if exito:
            cargar_clientes()
            limpiar_campos()
        messagebox.showinfo("Resultado", msj)

    def cargar_para_editar():
        sel = tree_clientes.focus()
        if not sel:
            return
        valores = tree_clientes.item(sel, 'values')
        for i, key in enumerate(['id','nombre','apellido','dni','direccion','telefono','email']):
            entries[key].delete(0, tk.END)
            entries[key].insert(0, valores[i])
        lbl_id.config(text=valores[0])

    def editar():
        cid = lbl_id.cget("text")
        if not cid:
            return
        n = entries['nombre'].get().strip()
        a = entries['apellido'].get().strip()
        d = entries['dni'].get().strip()
        dir = entries['direccion'].get().strip()
        t = entries['telefono'].get().strip()
        e_mail = entries['email'].get().strip()
        exito, msj = editar_cliente_bd(cid, n, a, d, dir, t, e_mail)
        if exito:
            cargar_clientes()
            limpiar_campos()
            lbl_id.config(text='')
        messagebox.showinfo("Resultado", msj)

    def eliminar():
        cid = lbl_id.cget("text")
        if not cid:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            eliminar_cliente_bd(cid)
            cargar_clientes()
            limpiar_campos()
            lbl_id.config(text='')

    ventana = tk.Toplevel