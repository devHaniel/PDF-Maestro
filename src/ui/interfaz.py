import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
import os

from util.logger_configuracion import setup_logger
from conversor.conversor import convertir_word_pdf
from uniones.uniones_pdfs import unir_pdfs


class App(tb.Window):
    def __init__(self):
        super().__init__(title="Convertir y Unir Archivos", themename="darkly")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.log = setup_logger()

        # Listas
        self.archivos = []
        self.pdfs = []
        self.words = []
        self.cards = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_frames()

    def crear_frames(self):

        self.frame_subida = tb.Frame(self, padding=20, bootstyle="dark")
        self.frame_subida.grid(row=0, column=0, sticky="ns")
        self.frame_subida.configure(width=350)

        tb.Label(self.frame_subida, text="Subir Archivos",
                 font=("Helvetica", 18, "bold"),
                 bootstyle="light").pack(pady=15)

        tb.Button(self.frame_subida,
                  text="Agregar Archivo",
                  command=self.agregar_archivo,
                  bootstyle="primary-outline").pack(fill=X, pady=5)

        self.lista_archivos = tk.Listbox(
            self.frame_subida,
            height=15,
            bg="#2b2b2b",
            fg="white",
            selectbackground="#444444",
            relief="flat"
        )
        self.lista_archivos.pack(fill=BOTH, expand=True, pady=15)

        tb.Button(self.frame_subida,
                  text="Convertir Word a PDF",
                  command=self.convertir_pdf,
                  bootstyle="success-outline").pack(fill=X, pady=5)

        self.frame_union = tb.Frame(self, padding=20, bootstyle="dark")
        self.frame_union.grid(row=0, column=1, sticky="nsew")

        tb.Label(self.frame_union, text="Archivos PDF",
                 font=("Helvetica", 18, "bold"),
                 bootstyle="light").pack(pady=10)

        # Scroll horizontal
        self.canvas = tk.Canvas(self.frame_union, height=240,
                                bg="#1f1f1f", highlightthickness=0)

        self.scroll_frame = tb.Frame(self.canvas, bootstyle="dark")
        self.scroll_x = tk.Scrollbar(self.frame_union,
                                     orient="horizontal",
                                     command=self.canvas.xview)

        self.canvas.configure(xscrollcommand=self.scroll_x.set)

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.canvas.create_window((0, 0),
                                  window=self.scroll_frame,
                                  anchor="nw")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )

        tb.Button(self.frame_union,
                  text="Unir PDFs",
                  command=self.unir_pdfs,
                  bootstyle="success").pack(pady=20, fill=X)

    def agregar_archivo(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[
                ("Archivos Word", "*.docx"),
                ("Archivos PDF", "*.pdf")
            ]
        )

        for file_path in file_paths:
            if file_path not in self.archivos:
                self.archivos.append(file_path)
                self.lista_archivos.insert(tk.END, os.path.basename(file_path))

                if file_path.lower().endswith(".pdf"):
                    self.pdfs.append(file_path)
                    self.crear_card(file_path)

                if file_path.lower().endswith(".docx"):
                    self.words.append(file_path)

    def crear_card(self, filepath):

        colores_borde = ["primary", "info", "warning", "secondary"]
        color = colores_borde[len(self.cards) % len(colores_borde)]

        # Frame exterior (borde de color)
        outer = tb.Frame(
            self.scroll_frame,
            bootstyle=color,
            padding=1
        )
        outer.pack(side=LEFT, padx=15, pady=25)

        # Frame interior (card real)
        card = tb.Frame(
            outer,
            width=190,
            height=170,
            padding=20,
            bootstyle="dark"
        )
        card.pack()
        card.pack_propagate(False)

        nombre = os.path.basename(filepath)

        tb.Label(card,
                 text="PDF",
                 font=("Helvetica", 9, "bold"),
                 bootstyle="secondary").pack()

        tb.Label(card,
                 text=nombre,
                 wraplength=160,
                 font=("Helvetica", 11, "bold"),
                 bootstyle="light").pack(pady=12)

        btn_frame = tb.Frame(card, bootstyle="dark")
        btn_frame.pack()

        tb.Button(btn_frame,
                  text="<",
                  width=3,
                  bootstyle="secondary-outline",
                  command=lambda c=outer: self.mover_izquierda(c)
                  ).pack(side=LEFT, padx=4)

        tb.Button(btn_frame,
                  text=">",
                  width=3,
                  bootstyle="secondary-outline",
                  command=lambda c=outer: self.mover_derecha(c)
                  ).pack(side=LEFT, padx=4)

        tb.Button(btn_frame,
                  text="X",
                  width=3,
                  bootstyle="danger-outline",
                  command=lambda c=outer, f=filepath:
                  self.eliminar_card(c, f)
                  ).pack(side=LEFT, padx=4)

        self.cards.append(outer)

    def mover_izquierda(self, card):
        idx = self.cards.index(card)
        if idx > 0:
            self.cards[idx], self.cards[idx - 1] = self.cards[idx - 1], self.cards[idx]
            self.pdfs[idx], self.pdfs[idx - 1] = self.pdfs[idx - 1], self.pdfs[idx]
            self.redibujar_cards()

    def mover_derecha(self, card):
        idx = self.cards.index(card)
        if idx < len(self.cards) - 1:
            self.cards[idx], self.cards[idx + 1] = self.cards[idx + 1], self.cards[idx]
            self.pdfs[idx], self.pdfs[idx + 1] = self.pdfs[idx + 1], self.pdfs[idx]
            self.redibujar_cards()

    def eliminar_card(self, card, filepath):
        idx = self.cards.index(card)
        card.destroy()
        self.cards.pop(idx)
        self.pdfs.pop(idx)

    def redibujar_cards(self):
        for c in self.scroll_frame.winfo_children():
            c.pack_forget()
        for c in self.cards:
            c.pack(side=LEFT, padx=10, pady=20)

    def convertir_pdf(self):
        bandera = convertir_word_pdf(*self.words)

        if not bandera['senal']:
            messagebox.showerror("Error", bandera["mensaje"])
        else:
            messagebox.showinfo("Éxito", bandera["mensaje"])

    def unir_pdfs(self):
        if len(self.pdfs) > 1:
            ruta_salida = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF", "*.pdf")]
            )

            if not ruta_salida:
                return

            senal = unir_pdfs(self.pdfs, ruta_salida)

            if not senal['senal']:
                messagebox.showerror("Error", senal["mensaje"])
            else:
                messagebox.showinfo("Éxito", senal["mensaje"])

if __name__ == "__main__":
    app = App()
    app.mainloop()
