from tkinter import Tk, Label, Button
from views.bolsones_view import BolsonesPorLote
from views.registros_view import ListadoRegistros
from database import setup_database

class MainApp:
    def __init__(self, root):
        self.root = root
        setup_database()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del menú principal"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.title("Sistema de Registro de Bolsones")
        self.root.geometry("400x250")
        
        Label(self.root, text="Seleccione una opción:", font=("Arial", 12)).pack(pady=20)
        
        Button(
            self.root,
            text="REGISTRAR BOLSONES",
            command=self.abrir_registro_bolsones,
            width=20
        ).pack(pady=10)
        
        Button(
            self.root,
            text="VER REGISTROS",
            command=self.abrir_listado_registros,
            width=20
        ).pack(pady=10)
    
    def abrir_registro_bolsones(self):
        """Abre la ventana de registro de bolsones"""
        self.root.withdraw()
        BolsonesPorLote(self.root)
    
    def abrir_listado_registros(self):
        """Abre la ventana de listado de registros"""
        self.root.withdraw()
        ListadoRegistros(self.root)

    def show(self):
        """Muestra el menú principal"""
        self.setup_ui()
        self.root.deiconify()

if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    root.mainloop()