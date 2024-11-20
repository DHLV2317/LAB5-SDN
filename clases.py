class Servicio:
    def __init__(self, nombre, protocolo, puerto):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto

class Servidor:
    def __init__(self, nombre, direccion_ip):
        self.nombre = nombre
        self.direccion_ip = direccion_ip
        self.servicios = []  # Lista de objetos Servicio

class Alumno:
    def __init__(self, nombre, mac):
        self.nombre = nombre
        self.mac = mac  # Dirección MAC del PC

class Curso:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "activo"  # Por defecto el curso está activo
        self.alumnos = []  # Lista de objetos Alumno
        self.servidores = []  # Lista de objetos Servidor