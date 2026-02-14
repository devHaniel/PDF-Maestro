from tkinter.filedialog import FileDialog

import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from util.logger_configuracion import setup_logger
from conversor.conversor import convertir_word_pdf
from uniones.uniones_pdfs import unir_pdfs

class App(tb.Window):
    def __init__(self):
        super().__init__(title="Convertir y Unir Archivos", themename="darkly")
        self.geometry("1000x600")

        self.log = setup_logger()

        # Listas de archivos
        self.archivos = []
        self.pdfs = []
        self.words = []
        self.cards = []  # guardamos referencias a las cards

        # Cargar icono PDF redimensionado
        self.pdf_icon = self.cargar_icono("./img/PDF_file_icon.svg.png", (60, 60))

        # Configurar grid de la ventana
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Crear frames principales
        self.crear_frames()

    def crear_frames(self):
        # ===== Frame izquierdo: Subida y conversión =====
        self.frame_subida = tb.Frame(self, padding=15, bootstyle="dark")
        self.frame_subida.grid(row=0, column=0, sticky="ns")
        self.frame_subida.configure(width=350)

        tb.Label(self.frame_subida, text="Subir Archivos", font=("Helvetica", 16, "bold"), bootstyle="light").pack(pady=10)

        self.btn_agregar = tb.Button(self.frame_subida, text="Agregar Archivo", command=self.agregar_archivo, bootstyle="primary")
        self.btn_agregar.pack(pady=5, fill=X)

        self.lista_archivos = tk.Listbox(self.frame_subida, height=15, bg="#333333", fg="white", selectbackground="#555555")
        self.lista_archivos.pack(fill=BOTH, expand=True, pady=10)

        self.btn_convertir = tb.Button(self.frame_subida, text="Convertir Word a PDF", command=self.convertir_pdf, bootstyle="success")
        self.btn_convertir.pack(pady=5, fill=X)

        # ===== Frame derecho: PDFs y unión =====
        self.frame_union = tb.Frame(self, padding=15, bootstyle="dark")
        self.frame_union.grid(row=0, column=1, sticky="nsew")

        self.frame_union.grid_rowconfigure(0, weight=1)
        self.frame_union.grid_columnconfigure(0, weight=1)

        tb.Label(self.frame_union, text="Archivos PDF", font=("Helvetica", 16, "bold"), bootstyle="light").pack(pady=10)

        # Scroll horizontal para tarjetas
        self.canvas = tk.Canvas(self.frame_union, height=220, bg="#222222", highlightthickness=0)
        self.scroll_frame = tb.Frame(self.canvas, bootstyle="dark")
        self.scroll_frame.pack(fill=BOTH, expand=True)

        self.scroll_x = tk.Scrollbar(self.frame_union, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)
        self.canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Botón unir PDFs
        self.btn_unir = tb.Button(self.frame_union, text="Unir PDFs", command=self.unir_pdfs, bootstyle="success")
        self.btn_unir.pack(pady=15, fill=X)

    # ===== Funciones de botones =====
    def agregar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos Word", "*.docx"), ("Archivos PDF", "*.pdf")])
        if file_path:
            self.archivos.append(file_path)
            self.lista_archivos.insert(tk.END, file_path)

            if file_path.lower().endswith(".pdf"):
                self.pdfs.append(file_path)
                self.crear_card(file_path)

            if file_path.lower().endswith(".docx"):
                self.words.append(file_path)

    def crear_card(self, filepath):
        # Card individual para PDF
        card = tb.Frame(self.scroll_frame, width=120, height=200, padding=5, bootstyle="light")
        card.pack(side=LEFT, padx=5, pady=5)

        label_img = tb.Label(card, image=self.pdf_icon)
        label_img.pack(pady=5)

        nombre = filepath.split("/")[-1]
        tb.Label(card, text=nombre, wraplength=100, font=("Helvetica",10), bootstyle="light").pack(pady=5)

        # Botones de acción
        btn_frame = tb.Frame(card)
        btn_frame.pack(pady=5)

        tb.Button(btn_frame, text="<", width=3, bootstyle="secondary", command=lambda c=card: self.mover_izquierda(c)).pack(side=LEFT, padx=2)
        tb.Button(btn_frame, text=">", width=3, bootstyle="secondary", command=lambda c=card: self.mover_derecha(c)).pack(side=LEFT, padx=2)
        tb.Button(btn_frame, text="X", width=3, bootstyle="danger", command=lambda c=card, f=filepath: self.eliminar_card(c, f)).pack(side=LEFT, padx=2)

        # Guardar referencia de la card
        self.cards.append(card)

    # ===== Funciones de acción de las cards =====
    def mover_izquierda(self, card):
        idx = self.cards.index(card)
        if idx > 0:
            # Intercambiar en lista de cards
            self.cards[idx], self.cards[idx-1] = self.cards[idx-1], self.cards[idx]
            # Intercambiar en lista de pdfs
            self.pdfs[idx], self.pdfs[idx-1] = self.pdfs[idx-1], self.pdfs[idx]
            self.redibujar_cards()

    def mover_derecha(self, card):
        idx = self.cards.index(card)
        if idx < len(self.cards)-1:
            self.cards[idx], self.cards[idx+1] = self.cards[idx+1], self.cards[idx]
            self.pdfs[idx], self.pdfs[idx+1] = self.pdfs[idx+1], self.pdfs[idx]
            self.redibujar_cards()

    def eliminar_card(self, card, filepath):
        card.destroy()
        idx = self.cards.index(card)
        self.cards.pop(idx)
        if filepath in self.pdfs:
            self.pdfs.pop(idx)  # eliminamos del mismo índice

    def redibujar_cards(self):
        for c in self.scroll_frame.winfo_children():
            c.pack_forget()
        for c in self.cards:
            c.pack(side=LEFT, padx=5, pady=5)

    def convertir_pdf(self):
        bandera = convertir_word_pdf(*self.words)

        if not bandera['senal']:
            messagebox.showerror("Erro", bandera["mensaje"])
        else:
            messagebox.showinfo("Exito", bandera["mensaje"])

    def unir_pdfs(self):
        if len(self.cards) > 1:
            ruta_salida = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
            senal = unir_pdfs(self.pdfs, ruta_salida)

            if not senal['senal']:
                messagebox.showerror("Erro", senal["mensaje"])
            else:
                messagebox.showinfo("Exito", senal["mensaje"])

    def cargar_icono(self, ruta, tamaño):
        img = Image.open(ruta)
        img = img.resize(tamaño, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
