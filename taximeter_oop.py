import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit, QDialog, QListWidget, QFormLayout
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime


# Clase para la ventana de inicio de sesión
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Iniciar Sesión")
        self.setGeometry(100, 100, 300, 150)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Crear widgets
        self.label_usuario = QLabel("Usuario:", self)
        self.label_usuario.setStyleSheet("font-size: 14px; color: #333;")

        self.input_usuario = QLineEdit(self)
        self.input_usuario.setPlaceholderText("Ingrese su usuario")

        self.label_contrasena = QLabel("Contraseña:", self)
        self.label_contrasena.setStyleSheet("font-size: 14px; color: #333;")

        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setPlaceholderText("Ingrese su contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.Password)  # Ocultar contraseña

        self.btn_login = QPushButton("Iniciar Sesión", self)
        self.btn_login.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 14px; padding: 8px; border-radius: 5px;"
        )
        self.btn_login.clicked.connect(self.verificar_credenciales)

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.label_contrasena)
        layout.addWidget(self.input_contrasena)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def verificar_credenciales(self):
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()

        # Credenciales válidas (puedes cambiarlas o cargarlas desde una base de datos)
        if usuario == "admin" and contrasena == "1234":
            self.accept()  # Cerrar la ventana de inicio de sesión y permitir acceso
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")


# Clase para la ventana de configuración
class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Tarifas")
        self.setGeometry(100, 100, 300, 150)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Crear widgets
        self.label_tarifa_movimiento = QLabel("Tarifa de Movimiento (€/s):", self)
        self.input_tarifa_movimiento = QLineEdit(self)
        self.input_tarifa_movimiento.setPlaceholderText("Ej: 1.0")

        self.label_tarifa_detenido = QLabel("Tarifa de Detenido (€/s):", self)
        self.input_tarifa_detenido = QLineEdit(self)
        self.input_tarifa_detenido.setPlaceholderText("Ej: 0.2")

        self.btn_guardar = QPushButton("Guardar", self)
        self.btn_guardar.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 14px; padding: 8px; border-radius: 5px;"
        )
        self.btn_guardar.clicked.connect(self.guardar_tarifas)

        # Diseño de la interfaz
        layout = QFormLayout()
        layout.addRow(self.label_tarifa_movimiento, self.input_tarifa_movimiento)
        layout.addRow(self.label_tarifa_detenido, self.input_tarifa_detenido)
        layout.addRow(self.btn_guardar)

        self.setLayout(layout)

    def guardar_tarifas(self):
        try:
            tarifa_movimiento = float(self.input_tarifa_movimiento.text())
            tarifa_detenido = float(self.input_tarifa_detenido.text())

            if tarifa_movimiento < 0 or tarifa_detenido < 0:
                raise ValueError("Las tarifas no pueden ser negativas.")

            # Guardar las tarifas en el taxímetro
            self.parent().taximetro.tarifa_movimiento = tarifa_movimiento
            self.parent().taximetro.tarifa_detenido = tarifa_detenido

            # Registrar el cambio de tarifas en el log
            self.parent().guardar_log(f"Tarifas actualizadas: Movimiento = {tarifa_movimiento}€/s, Detenido = {tarifa_detenido}€/s")

            QMessageBox.information(self, "Éxito", "Tarifas actualizadas correctamente.")
            self.close()
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Entrada inválida: {e}")


# Clase para la ventana de histórico de trayectos
class TrayectosWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Histórico de Trayectos")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Crear un QListWidget para mostrar los trayectos
        self.lista_trayectos = QListWidget(self)
        self.lista_trayectos.setStyleSheet("font-size: 14px; color: #333;")

        # Cargar los trayectos desde el archivo
        self.cargar_trayectos()

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.lista_trayectos)
        self.setLayout(layout)

    def cargar_trayectos(self):
        try:
            with open("trayectos.log", "r") as file:
                trayectos = file.read().split("\n\n")  # Separar por trayectos
                for trayecto in trayectos:
                    if trayecto.strip():  # Ignorar líneas vacías
                        self.lista_trayectos.addItem(trayecto)
        except FileNotFoundError:
            self.lista_trayectos.addItem("No hay trayectos registrados.")


# Clase principal del taxímetro
class TaximetroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.taximetro = Taximetro()
        self.historial_estados = []  # Lista para almacenar los últimos 5 estados
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Taxímetro")
        self.setGeometry(100, 100, 400, 500)  # Aumentamos el tamaño de la ventana
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Configurar ícono de la ventana
        self.setWindowIcon(QIcon("taxi_icon.png"))

        # Crear widgets
        self.label_estado = QLabel("Estado: No iniciado", self)
        self.label_estado.setStyleSheet("font-size: 18px; color: #333; font-weight: bold;")
        self.label_estado.setAlignment(Qt.AlignCenter)

        # Crear un QLabel para el ícono de estado
        self.icono_estado = QLabel(self)
        self.icono_estado.setPixmap(QPixmap("stop_icon.png").scaled(64, 64))
        self.icono_estado.setAlignment(Qt.AlignCenter)

        # Crear un QListWidget para el historial de estados
        self.lista_historial = QListWidget(self)
        self.lista_historial.setStyleSheet("font-size: 14px; color: #777;")  # Texto más claro
        self.lista_historial.setMaximumHeight(100)  # Limitar la altura del historial

        # Diseño vertical para el ícono y el texto de estado
        estado_layout = QVBoxLayout()
        estado_layout.addWidget(self.icono_estado)
        estado_layout.addWidget(self.label_estado)
        estado_layout.setAlignment(Qt.AlignCenter)

        # Botones
        self.btn_iniciar = QPushButton("Iniciar Travesía", self)
        self.btn_iniciar.setIcon(QIcon("start_icon.png"))
        self.btn_iniciar.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )

        self.btn_movimiento = QPushButton("En Movimiento (m)", self)
        self.btn_movimiento.setIcon(QIcon("move_icon.png"))
        self.btn_movimiento.setStyleSheet(
            "background-color: #2196F3; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )

        self.btn_detenido = QPushButton("Detenido (s)", self)
        self.btn_detenido.setIcon(QIcon("stop_icon.png"))
        self.btn_detenido.setStyleSheet(
            "background-color: #f44336; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )

        self.btn_finalizar = QPushButton("Finalizar Travesía (e)", self)
        self.btn_finalizar.setIcon(QIcon("end_icon.png"))
        self.btn_finalizar.setStyleSheet(
            "background-color: #FF9800; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )

        # Botón de configuración
        self.btn_configuracion = QPushButton("Configuración", self)
        self.btn_configuracion.setIcon(QIcon("config_icon.png"))  # Asegúrate de tener un archivo "config_icon.png"
        self.btn_configuracion.setStyleSheet(
            "background-color: #9C27B0; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )
        self.btn_configuracion.clicked.connect(self.abrir_configuracion)

        # Botón de histórico de trayectos
        self.btn_trayectos = QPushButton("Ver Trayectos", self)
        self.btn_trayectos.setIcon(QIcon("history_icon.png"))  # Asegúrate de tener un archivo "history_icon.png"
        self.btn_trayectos.setStyleSheet(
            "background-color: #607D8B; color: white; font-size: 16px; padding: 10px; border-radius: 5px;"
        )
        self.btn_trayectos.clicked.connect(self.abrir_trayectos)

        # Conectar botones a funciones
        self.btn_iniciar.clicked.connect(self.iniciar_travesia)
        self.btn_movimiento.clicked.connect(self.indicar_movimiento)
        self.btn_detenido.clicked.connect(self.indicar_detenido)
        self.btn_finalizar.clicked.connect(self.finalizar_travesia)

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addLayout(estado_layout)
        layout.addWidget(self.lista_historial)  # Añadir el historial de estados
        layout.addSpacing(10)
        layout.addWidget(self.btn_iniciar)
        layout.addWidget(self.btn_movimiento)
        layout.addWidget(self.btn_detenido)
        layout.addWidget(self.btn_finalizar)
        layout.addWidget(self.btn_configuracion)  # Añadir el botón de configuración
        layout.addWidget(self.btn_trayectos)  # Añadir el botón de histórico de trayectos

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def abrir_configuracion(self):
        # Abrir la ventana de configuración
        config_window = ConfigWindow(self)
        config_window.exec_()

    def abrir_trayectos(self):
        # Abrir la ventana de histórico de trayectos
        trayectos_window = TrayectosWindow(self)
        trayectos_window.exec_()

    def actualizar_historial(self, mensaje):
        # Limpiar el historial si el mensaje es "Travesía iniciada. ¡Buen viaje!"
        if mensaje == "Travesía iniciada. ¡Buen viaje!":
            self.historial_estados.clear()
            self.lista_historial.clear()
            return

        # Verificar si el mensaje es una excepción (estado repetido)
        if self.historial_estados and mensaje == self.historial_estados[-1]:
            return  # No añadir al historial si es el mismo estado

        # Añadir el nuevo estado al historial
        self.historial_estados.append(mensaje)

        # Mantener solo los últimos 5 estados
        if len(self.historial_estados) > 5:
            self.historial_estados.pop(0)

        # Actualizar la lista de historial
        self.lista_historial.clear()
        for estado in self.historial_estados:
            self.lista_historial.addItem(estado)

    def guardar_log(self, mensaje):
        # Obtener la fecha y hora actual
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar el mensaje en el archivo de log con fecha y hora
        with open("taximetro_log.txt", "a") as log_file:
            log_file.write(f"[{fecha_hora}] {mensaje}\n")

    def guardar_trayecto(self, inicio, duracion, coste):
        # Guardar el trayecto en el archivo de trayectos
        with open("trayectos.log", "a") as trayectos_file:
            trayectos_file.write(
                f"Inicio: {inicio}\n"
                f"Duración: {duracion:.2f} segundos\n"
                f"Coste: {coste:.2f}€\n\n"
            )

    def iniciar_travesia(self):
        mensaje = self.taximetro.iniciar_travesia()
        self.label_estado.setText(f"Estado: {mensaje}")
        self.icono_estado.setPixmap(QPixmap("start_icon.png").scaled(64, 64))
        self.actualizar_historial(mensaje)
        self.guardar_log(mensaje)  # Guardar en el log con fecha y hora

    def indicar_movimiento(self):
        mensaje = self.taximetro.indicar_movimiento()
        self.label_estado.setText(f"Estado: {mensaje}")
        self.icono_estado.setPixmap(QPixmap("move_icon.png").scaled(64, 64))
        self.actualizar_historial(mensaje)
        self.guardar_log(mensaje)  # Guardar en el log con fecha y hora

    def indicar_detenido(self):
        mensaje = self.taximetro.indicar_detenido()
        self.label_estado.setText(f"Estado: {mensaje}")
        self.icono_estado.setPixmap(QPixmap("stop_icon.png").scaled(64, 64))
        self.actualizar_historial(mensaje)
        self.guardar_log(mensaje)  # Guardar en el log con fecha y hora

    def finalizar_travesia(self):
        if self.taximetro.travesia_iniciada:
            tiempo_transcurrido = time.time() - self.taximetro.tiempo_inicio
            if self.taximetro.en_movimiento:
                self.taximetro.coste_total += tiempo_transcurrido * self.taximetro.tarifa_movimiento
            else:
                self.taximetro.coste_total += tiempo_transcurrido * self.taximetro.tarifa_detenido
            mensaje = f"Travesía finalizada. Coste total: {self.taximetro.coste_total:.2f}€"

            # Guardar el trayecto antes de reiniciar el coste (CORRECCIÓN APLICADA AQUÍ)
            inicio = datetime.fromtimestamp(self.taximetro.tiempo_inicio).strftime("%Y-%m-%d %H:%M:%S")
            duracion = tiempo_transcurrido
            coste = self.taximetro.coste_total
            self.guardar_trayecto(inicio, duracion, coste)

            # Reiniciar el estado del taxímetro
            self.taximetro.travesia_iniciada = False
            self.taximetro.en_movimiento = False
            self.taximetro.coste_total = 0.0

            # Mostrar el mensaje y actualizar la interfaz
            QMessageBox.information(self, "Fin de la travesía", mensaje)
            self.label_estado.setText("Estado: No iniciado")
            self.icono_estado.setPixmap(QPixmap("stop_icon.png").scaled(64, 64))
            self.actualizar_historial(mensaje)
            self.guardar_log(mensaje)  # Guardar en el log con fecha y hora
        else:
            mensaje = "No hay ninguna travesía en curso."
            QMessageBox.information(self, "Error", mensaje)


# Clase para la lógica del taxímetro
class Taximetro:
    def __init__(self):
        self.en_movimiento = False
        self.travesia_iniciada = False
        self.coste_total = 0.0
        self.tiempo_inicio = 0
        self.tarifa_movimiento = 0.5  # Tarifa por defecto para movimiento
        self.tarifa_detenido = 0.2    # Tarifa por defecto para detenido
        
    def iniciar_travesia(self):
        if not self.travesia_iniciada:
            self.travesia_iniciada = True
            self.tiempo_inicio = time.time()
            print("Travesía iniciada. ¡Buen viaje!")
            self.indicar_movimiento
        else:
            return "La travesía ya está en curso."
        
    def indicar_movimiento(self):
        if self.travesia_iniciada:
            if not self.en_movimiento:
                self.en_movimiento = True
                return f"El taxi está en movimiento. Coste por segundo: {self.tarifa_movimiento}€"
            else:
                return "El taxi ya está en movimiento."
        else:
            return "Primero debes iniciar la travesía."

    def indicar_detenido(self):
        if self.travesia_iniciada:
            if self.en_movimiento:
                self.en_movimiento = False
                return f"El taxi se ha detenido. Coste por segundo: {self.tarifa_detenido}€"
            else:
                return "El taxi ya está detenido."
        else:
            return "Primero debes iniciar la travesía."

    def finalizar_travesia(self):
        if self.travesia_iniciada:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            if self.en_movimiento:
                self.coste_total += tiempo_transcurrido * self.tarifa_movimiento
            else:
                self.coste_total += tiempo_transcurrido * self.tarifa_detenido
            mensaje = f"Travesía finalizada. Coste total: {self.coste_total:.2f}€"
            self.travesia_iniciada = False
            self.en_movimiento = False
            self.coste_total = 0.0
            return mensaje
        else:
            return "No hay ninguna travesía en curso."


# Función principal
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Mostrar la ventana de inicio de sesión
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        # Si las credenciales son correctas, mostrar la ventana principal
        ventana = TaximetroApp()
        ventana.show()
        sys.exit(app.exec_())