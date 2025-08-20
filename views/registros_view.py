import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from models.bolson_model import BolsonModel

class ListadoRegistros(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.model = BolsonModel()
        self.title("LISTADO DE REGISTROS - BOLSONES")
        self.geometry("1200x700")
        self.configure(bg='#f0f0f0')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Frame de filtros
        filter_frame = tk.Frame(self, bg='#e0e0e0', padx=10, pady=10)
        filter_frame.pack(fill=tk.X)

        # Configuración de estilo
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", font=('Arial', 9), rowheight=25)

        # Filtros
        tk.Label(filter_frame, text="Filtrar por:", bg='#e0e0e0').grid(row=0, column=0, padx=5)
        
        tk.Label(filter_frame, text="Lote ADECO:", bg='#e0e0e0').grid(row=0, column=1, padx=5)
        self.filter_lote = tk.Entry(filter_frame, width=20, font=('Arial', 10))
        self.filter_lote.grid(row=0, column=2, padx=5)
        self.filter_lote.bind('<Return>', lambda e: self.apply_filters())

        tk.Label(filter_frame, text="Proveedor:", bg='#e0e0e0').grid(row=0, column=3, padx=5)
        self.filter_proveedor = tk.Entry(filter_frame, width=20, font=('Arial', 10))
        self.filter_proveedor.grid(row=0, column=4, padx=5)
        self.filter_proveedor.bind('<Return>', lambda e: self.apply_filters())

        # Botones de acción
        ttk.Button(filter_frame, text="Aplicar Filtros", 
                  command=self.apply_filters).grid(row=0, column=5, padx=5)
        ttk.Button(filter_frame, text="Limpiar Filtros", 
                  command=self.clear_filters).grid(row=0, column=6, padx=5)
        ttk.Button(filter_frame, text="Exportar Excel", 
                  command=self.export_to_excel).grid(row=0, column=7, padx=5)

        # Frame para botones de acción
        action_frame = tk.Frame(self, bg='#e0e0e0', padx=10, pady=5)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Editar Seleccionado", 
                  command=self.editar_registro).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Eliminar Seleccionado", 
                  command=self.eliminar_registro).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Nuevo Registro", 
                  command=self.nuevo_registro).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Volver al Menú", 
                  command=self.on_closing).pack(side='left', padx=5)

        # Treeview con scrollbars
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(self.tree_frame, columns=(
            'ID', 'Proveedor', 'Kg', 'Lote', 'LoteADECO', 'DIT', 
            'Reutilizable', 'Fecha', 'Repeticiones'
        ), show='headings', selectmode='browse')

        # Configuración de columnas
        columns_config = [
            ('ID', 50, 'center'),
            ('Proveedor', 150, 'w'),
            ('Kg', 60, 'center'),
            ('Lote', 100, 'center'),
            ('LoteADECO', 120, 'center'),
            ('DIT', 80, 'center'),
            ('Reutilizable', 90, 'center'),
            ('Fecha', 150, 'center'),
            ('Repeticiones', 80, 'center')
        ]

        for col, width, anchor in columns_config:
            self.tree.column(col, width=width, anchor=anchor)
            self.tree.heading(col, text=col)

        # Scrollbars
        y_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Bind doble click para editar
        self.tree.bind('<Double-1>', self.editar_registro)

    def load_data(self, filters=None):
        """Carga datos desde el modelo"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        registros = self.model.obtener_registros(filters)
        
        for row in registros:
            self.tree.insert('', tk.END, values=(
                row['id'], row['proveedor'], row['kilogramos'],
                row['numero_lote'], row['lote_adeco'], row['numero_dit'],
                row['reutilizable'], row['fecha_registro'], row['repeticiones']
            ))

    def apply_filters(self):
        """Aplica los filtros ingresados"""
        filters = {}
        if self.filter_lote.get().strip():
            filters['lote_adeco'] = self.filter_lote.get().strip()
        if self.filter_proveedor.get().strip():
            filters['proveedor'] = self.filter_proveedor.get().strip()
            filters['exact_match'] = True
            
        self.load_data(filters)

    def clear_filters(self):
        """Limpia todos los filtros"""
        self.filter_lote.delete(0, tk.END)
        self.filter_proveedor.delete(0, tk.END)
        self.load_data()

    def export_to_excel(self):
        """Exporta los datos visibles a Excel"""
        try:
            items = self.tree.get_children()
            if not items:
                messagebox.showwarning("Advertencia", "No hay datos para exportar")
                return

            columns = [
                'ID', 'Proveedor', 'Kilogramos', 'Número Lote', 
                'Lote ADECO', 'Número DIT', 'Reutilizable', 
                'Fecha Registro', 'Repeticiones'
            ]
            
            data = [self.tree.item(item)['values'] for item in items]
            
            df = pd.DataFrame(data, columns=columns)
            
            filepath = filedialog.asksaveasfilename(
                defaultextension='.xlsx',
                filetypes=[
                    ("Excel files", "*.xlsx"),
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ],
                title="Exportar registros",
                initialfile="registros_bolsones.xlsx"
            )
            
            if filepath:
                if filepath.endswith('.csv'):
                    df.to_csv(filepath, index=False)
                else:
                    df.to_excel(filepath, index=False)
                
                messagebox.showinfo(
                    "Exportación exitosa", 
                    f"Datos exportados correctamente a:\n{filepath}"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error en exportación", 
                f"No se pudo exportar los datos:\n{str(e)}"
            )

    def editar_registro(self, event=None):
        """Abre ventana para editar registro seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un registro para editar")
            return
            
        item = seleccion[0]
        registro_id = self.tree.item(item, 'values')[0]
        
        # Obtener datos completos del registro
        registro = self.model.obtener_registro_por_id(registro_id)
        if not registro:
            messagebox.showerror("Error", "No se pudo cargar el registro seleccionado")
            return
        
        # Crear ventana de edición
        edit_win = tk.Toplevel(self)
        edit_win.title(f"Editar Registro ID: {registro_id}")
        edit_win.geometry("400x500")
        
        # Función para centrar widgets
        def center_widget(widget):
            widget.pack(pady=5, padx=10, fill=tk.X)
        
        # Campos editables
        tk.Label(edit_win, text="Proveedor:").pack()
        proveedor = tk.Entry(edit_win)
        proveedor.insert(0, registro['proveedor'])
        center_widget(proveedor)
        
        tk.Label(edit_win, text="Kilogramos:").pack()
        kilogramos = tk.Entry(edit_win)
        kilogramos.insert(0, registro['kilogramos'])
        center_widget(kilogramos)
        
        tk.Label(edit_win, text="Número de Lote:").pack()
        lote = tk.Entry(edit_win)
        lote.insert(0, registro['numero_lote'])
        center_widget(lote)
        
        tk.Label(edit_win, text="Lote ADECO:").pack()
        lote_adeco = tk.Entry(edit_win)
        lote_adeco.insert(0, registro['lote_adeco'])
        center_widget(lote_adeco)
        
        tk.Label(edit_win, text="Número DIT:").pack()
        dit = tk.Entry(edit_win)
        dit.insert(0, registro['numero_dit'])
        center_widget(dit)
        
        tk.Label(edit_win, text="Reutilizable (SI/NO):").pack()
        reutilizable = tk.Entry(edit_win)
        reutilizable.insert(0, registro['reutilizable'])
        center_widget(reutilizable)
        
        tk.Label(edit_win, text="Repeticiones:").pack()
        repeticiones = tk.Entry(edit_win)
        repeticiones.insert(0, str(registro['repeticiones']))
        center_widget(repeticiones)
        
        def guardar_cambios():
            nuevos_datos = (
                proveedor.get(),
                kilogramos.get(),
                lote.get(),
                lote_adeco.get(),
                dit.get(),
                reutilizable.get(),
                int(repeticiones.get())
            )
            if self.model.actualizar_registro(registro_id, nuevos_datos):
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                self.load_data()  # Refrescar datos
                edit_win.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el registro")
        
        tk.Button(edit_win, text="Guardar Cambios", command=guardar_cambios).pack(pady=20)
        tk.Button(edit_win, text="Cancelar", command=edit_win.destroy).pack(pady=10)

    def eliminar_registro(self):
        """Elimina el registro seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
            return
            
        item = seleccion[0]
        registro_id = self.tree.item(item, 'values')[0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
            if self.model.eliminar_registro(registro_id):
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.load_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro")

    def nuevo_registro(self):
        """Abre ventana para nuevo registro"""
        self.destroy()
        self.parent.deiconify()
        if hasattr(self.parent, 'abrir_registro_bolsones'):
            self.parent.abrir_registro_bolsones()

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.destroy()
        self.parent.deiconify()