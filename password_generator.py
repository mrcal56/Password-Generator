import random
import string
import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import os

# Funciones para manejar cifrado
def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as clave_archivo:
        clave_archivo.write(clave)

def cargar_clave():
    return open("clave.key", "rb").read()

def cifrar_mensaje(mensaje, clave):
    fernet = Fernet(clave)
    return fernet.encrypt(mensaje.encode())

def descifrar_mensaje(mensaje_cifrado, clave):
    fernet = Fernet(clave)
    return fernet.decrypt(mensaje_cifrado).decode()

def generar_contraseña(longitud, mayusculas, numeros, simbolos):
    caracteres = string.ascii_lowercase

    if mayusculas:
        caracteres += string.ascii_uppercase

    if numeros:
        caracteres += string.digits

    if simbolos:
        caracteres += string.punctuation

    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    
    return contraseña

def guardar_contraseña(nombre, contraseña):
    if not os.path.exists("clave.key"):
        generar_clave()

    clave = cargar_clave()
    contraseña_cifrada = cifrar_mensaje(contraseña, clave)
    with open("contraseñas.txt", "a") as archivo:
        archivo.write(f"{nombre}: {contraseña_cifrada.decode()}\n")

def leer_contraseñas():
    if not os.path.exists("clave.key"):
        return "La clave de cifrado no existe. Ejecuta el programa una vez para generar la clave."

    if not os.path.exists("contraseñas.txt"):
        return "No hay contraseñas almacenadas."

    clave = cargar_clave()
    contraseñas = []
    with open("contraseñas.txt", "r") as archivo:
        for linea in archivo:
            nombre, contraseña_cifrada = linea.strip().split(": ")
            contraseña = descifrar_mensaje(contraseña_cifrada.encode(), clave)
            contraseñas.append(f"{nombre}: {contraseña}")
    
    return "\n".join(contraseñas)

# Interfaz Gráfica
class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Contraseñas")
        self.geometry("500x500")
        
        self.create_widgets()

    def create_widgets(self):
        # Longitud
        tk.Label(self, text="Longitud de la contraseña:").pack(pady=5)
        self.longitud_entry = tk.Entry(self)
        self.longitud_entry.pack(pady=5)

        # Mayúsculas
        self.mayusculas_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Incluir mayúsculas", variable=self.mayusculas_var).pack(pady=5)

        # Números
        self.numeros_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Incluir números", variable=self.numeros_var).pack(pady=5)

        # Símbolos
        self.simbolos_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Incluir símbolos", variable=self.simbolos_var).pack(pady=5)

        # Botones
        tk.Button(self, text="Generar Contraseña", command=self.generar).pack(pady=5)
        tk.Button(self, text="Guardar Contraseña", command=self.guardar).pack(pady=5)
        tk.Button(self, text="Ver Contraseñas", command=self.ver).pack(pady=5)

        # Resultados
        self.resultado_texto = tk.Text(self, height=10, width=50)
        self.resultado_texto.pack(pady=5)

    def generar(self):
        try:
            longitud = int(self.longitud_entry.get())
            mayusculas = self.mayusculas_var.get()
            numeros = self.numeros_var.get()
            simbolos = self.simbolos_var.get()

            contraseña = generar_contraseña(longitud, mayusculas, numeros, simbolos)
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, f"Contraseña generada: {contraseña}\n")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa una longitud válida.")

    def guardar(self):
        nombre = tk.simpledialog.askstring("Nombre de la cuenta", "Introduce el nombre de la cuenta o servicio:")
        if nombre:
            contraseña = self.resultado_texto.get(1.0, tk.END).strip().replace("Contraseña generada: ", "")
            if contraseña:
                guardar_contraseña(nombre, contraseña)
                messagebox.showinfo("Éxito", "Contraseña guardada exitosamente.")
            else:
                messagebox.showerror("Error", "No hay ninguna contraseña generada para guardar.")
        else:
            messagebox.showerror("Error", "Debes ingresar un nombre para la cuenta.")

    def ver(self):
        contraseñas = leer_contraseñas()
        self.resultado_texto.delete(1.0, tk.END)
        self.resultado_texto.insert(tk.END, contraseñas)

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
