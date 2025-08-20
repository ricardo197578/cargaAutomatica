import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
from datetime import datetime
from models.bolson_model import BolsonModel

class BolsonesPorLote(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.model = BolsonModel()
        self.title("REGISTRO DE BOLSONES")
        self.geometry("300x650")
        self.font_style = ("Arial", 12)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

    def create_widgets(self):
        # Frame principal con scroll
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Función para centrar widgets
        def center_widget(widget):
            widget.pack(pady=5, padx=10, fill=tk.X, expand=True)

        # Función para crear campos con auto-mayúsculas
        def create_upper_entry(label_text):
            tk.Label(scrollable_frame, text=label_text, font=self.font_style).pack(pady=5)
            entry = tk.Entry(scrollable_frame, font=self.font_style)
            entry.bind('<KeyRelease>', lambda e: self.convert_to_upper(entry))
            center_widget(entry)
            return entry

        # Campos del formulario
        self.entry_proveedor = create_upper_entry("Proveedor:")
        self.entry_kilogramos = create_upper_entry("Kilogramos:")
        self.entry_lote = create_upper_entry("Número de Lote:")
        self.entry_lote_adeco = create_upper_entry("Lote ADECO:")
        self.entry_dit = create_upper_entry("Número DIT:")
        self.entry_reutilizable = create_upper_entry("¿Reutilizable? (SI/NO):")

        # Campo de repeticiones
        tk.Label(scrollable_frame, text="Repeticiones (1-20):", font=self.font_style).pack(pady=5)
        self.entry_repeticiones = tk.Entry(scrollable_frame, font=self.font_style)
        center_widget(self.entry_repeticiones)

        # Frame para botones
        button_frame = tk.Frame(scrollable_frame)
        button_frame.pack(pady=20, fill=tk.X, expand=True)

        # Botones
        tk.Button(button_frame, text="Iniciar Proceso", 
                 command=self.iniciar_proceso_automatico,
                 font=self.font_style).pack(side='left', padx=5, fill=tk.X, expand=True)
        
        tk.Button(button_frame, text="Limpiar", 
                 command=self.limpiar_campos,
                 font=self.font_style).pack(side='left', padx=5, fill=tk.X, expand=True)
        
        tk.Button(button_frame, text="Volver", 
                 command=self.on_closing,
                 font=self.font_style).pack(side='left', padx=5, fill=tk.X, expand=True)

    def convert_to_upper(self, entry_widget):
        """Convierte texto a mayúsculas mientras se escribe"""
        current_pos = entry_widget.index(tk.INSERT)
        text = entry_widget.get()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, text.upper())
        entry_widget.icursor(current_pos)

    def iniciar_proceso_automatico(self):
        """Ejecuta la carga automática múltiple"""
        try:
            repeticiones = int(self.entry_repeticiones.get())
            if not (1 <= repeticiones <= 20):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Repeticiones debe ser un número entre 1 y 20")
            return

        if not all([self.entry_proveedor.get(), self.entry_lote.get(), self.entry_reutilizable.get()]):
            messagebox.showerror("Error", "Complete los campos obligatorios")
            return

        if not messagebox.askyesno("Confirmar", f"¿Iniciar el proceso de {repeticiones} registros?"):
            return

        try:
            messagebox.showinfo("Instrucción", "Posicione el cursor en el primer campo del formulario destino. El proceso comenzará en 5 segundos.")
            time.sleep(5)
            
            # Obtener valores
            proveedor = self.entry_proveedor.get()
            kilogramos = self.entry_kilogramos.get()
            lote = self.entry_lote.get()
            dit = self.entry_dit.get()
            reutilizable = self.entry_reutilizable.get()
            
            # Ejecutar repeticiones
            for _ in range(repeticiones):
                pyautogui.write(proveedor)
                pyautogui.press('tab')
                pyautogui.write(kilogramos)
                pyautogui.press('tab', presses=2)
                pyautogui.write(lote)
                pyautogui.press('tab', presses=2)
                pyautogui.write(dit)
                pyautogui.press('tab', presses=4)
                pyautogui.write(reutilizable)
                pyautogui.press('enter')
                time.sleep(1)

            # Guardar en BD
            datos = (
                proveedor,
                kilogramos,
                lote,
                self.entry_lote_adeco.get(),
                dit,
                reutilizable,
                datetime.now(),
                repeticiones
            )

            if self.model.guardar_registro(datos):
                messagebox.showinfo("Éxito", f"Proceso completado: {repeticiones} registros")
                self.limpiar_campos()
            else:
                messagebox.showwarning("Advertencia", "Proceso completado pero error al guardar en BD")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante el proceso: {str(e)}")

    def limpiar_campos(self):
        """Limpia todos los campos"""
        self.entry_proveedor.delete(0, tk.END)
        self.entry_kilogramos.delete(0, tk.END)
        self.entry_lote.delete(0, tk.END)
        self.entry_lote_adeco.delete(0, tk.END)
        self.entry_dit.delete(0, tk.END)
        self.entry_reutilizable.delete(0, tk.END)
        self.entry_reutilizable.insert(0, "SI")
        self.entry_repeticiones.delete(0, tk.END)
        self.entry_proveedor.focus_set()

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.destroy()
        self.parent.deiconify()