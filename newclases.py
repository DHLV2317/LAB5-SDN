import yaml

class Alumno:
    def __init__(self, nombre, codigo, mac):
        self.nombre = nombre
        self.codigo = codigo
        self.mac = mac

class Curso:
    def __init__(self, codigo, estado, nombre):
        self.codigo = codigo
        self.estado = estado
        self.nombre = nombre
        self.alumnos = []
        self.servidores = []

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def añadir_servidor(self, servidor):
        self.servidores.append(servidor)

class Servidor:
    def __init__(self, nombre, ip):
        self.nombre = nombre
        self.ip = ip
        self.servicios = []

class Servicio:
    def __init__(self, nombre, protocolo, puerto):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def getAlumnos(datos):
    #objetos Alumno
    alumnos = [Alumno(al['nombre'], al['codigo'], al['mac']) for al in datos['alumnos']] #se creo correctamente 
    return alumnos

def getServicios(datos):
    #objetos servicios
    for sr in datos['servidores']:
        tm = sr['servicios']
        servicios = [Servicio(sv['nombre'], sv['protocolo'],sv['puerto']) for sv in tm]
    return servicios

def getServidores(datos,servicios):
    # objetos Servidor
    servidores = [Servidor(s['nombre'], s['ip']) for s in datos['servidores']]
    for x in servidores:
        x.servicios.extend(servicios)
    return servidores

def getCursos(datos,alumnos,servidores):
     # objetos cursos
    cursos = []
    alumnos_dict = {alumno.codigo: alumno for alumno in alumnos}  # Crear un diccionario para acceso rápido a los alumnos por código
    servidores_dict = {servidor.nombre: servidor for servidor in servidores}  # Diccionario para acceder a servidores por nombre

    for c in datos['cursos']:
        curso = Curso(c['codigo'], c['estado'], c['nombre'])

    # Agregar alumnos al curso
        for codigo_alumno in c['alumnos']:
            if codigo_alumno in alumnos_dict:
                curso.agregar_alumno(alumnos_dict[codigo_alumno])

        # Agregar servidores al curso con servicios permitidos
        for servidor_info in c['servidores']:
            servidor_nombre = servidor_info['nombre']
            if servidor_nombre in servidores_dict:
                servidor = servidores_dict[servidor_nombre]

             # Filtrar servicios permitidos
                servicios_permitidos = [
                    servicio for servicio in servidor.servicios
                    if servicio.nombre in servidor_info['servicios_permitidos']
                ]

                # Clonar el servidor para el curso y asociarle solo los servicios permitidos
                servidor_curso = Servidor(servidor.nombre, servidor.ip)
                servidor_curso.servicios.extend(servicios_permitidos)
                curso.añadir_servidor(servidor_curso)

        cursos.append(curso)
    return cursos


def actualizar_curso(cursos, alumnos):
    codigo_curso = input("Ingrese el código del curso: ")
    curso = next((c for c in cursos if c.codigo == codigo_curso), None)
    if curso:
        print("1) Agregar Alumno\n2) Eliminar Alumno")
        op = input(">>> ")
        if op == "1":
            codigo_alumno = input("Ingrese el código del alumno: ")
            alumno = next((a for a in alumnos if a.codigo == codigo_alumno), None)
            if alumno:
                curso.agregar_alumno(alumno)
                print(f"Alumno {alumno.nombre} agregado al curso {curso.nombre}")
            else:
                print("Alumno no encontrado.")
        elif op == "2":
            codigo_alumno = input("Ingrese el código del alumno: ")
            alumno = next((a for a in curso.alumnos if a.codigo == codigo_alumno), None)
            if alumno:
                curso.alumnos.remove(alumno)
                print(f"Alumno {alumno.nombre} eliminado del curso {curso.nombre}")
            else:
                print("Alumno no encontrado en el curso.")
        else:
            print("Opción inválida.")
    else:
        print("Curso no encontrado.")



def detallesCurso(cursos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    for curso in cursos:
        print(f"codigo: {curso.codigo}")
        print(f"estado: {curso.estado}")
        print(f"nombre: {curso.nombre}")
        print("alumnos:")
        for alumno in curso.alumnos:
            print(f"    - {alumno.codigo}")
            print("servidores:")
        for servidor in curso.servidores:
            print(f"    - nombre: {servidor.nombre}")
            print("      servicios_permitidos:")
            for servicio in servidor.servicios:
                print(f"          - {servicio.nombre}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def listarCursos(cursos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    for curso in cursos:
        print(f"Codigo: {curso.codigo}")
        print(f"Nombre: {curso.nombre}")
        print(f"Estado: {curso.estado}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")      

def listarAlumnos(alumnos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    for al in alumnos:
        print(al.nombre)
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def detalleAlumnos(alumnos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    for al in alumnos:
        print(f"Nombre: {al.nombre}")
        print(f"Codigo: {al.codigo}")
        print(f"Direccion MAC: {al.mac}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def listarServidores(servidores):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    for sr in servidores:
        print(f"Nombre: {sr.nombre}")
        print(f"Direccion IP: {sr.ip}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def detalleServidor(servidores):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    for sr in servidores:
        print(f"Nombre: {sr.nombre}")
        print(f"Direccion IP: {sr.ip}")
        print("Servicios: ")
        print('*--*--*--*--*')
        for sv in sr.servicios:
            print(f'   Servicio: {sv.nombre}')
            print(f'   Protocolo: {sv.protocolo}')
            print(f'   Puerto: {sv.puerto}')
            print('*--*--*--*--*')
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    
def displayMenu():
    print()
    print('##############################################')
    print('Network Policy manager de la USPM')
    print('##############################################')
    print()
    print("Seleccione una opcion:")
    print("1) Importar")
    print("2) Cursos")
    print("3) Alumnos")
    print("4) Servidores")
    print("5) Conexiones")
    print("6) Salir")
    op = input('>>>')
    print()
    return op

def display1():
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    print("Seleccione una opcion:")
    print("1) Listar")
    print("2) Mostrar detalle")

def display2():
    print("*--*Valor invalido*--*")
    print("Saliendo...")
    print()



def crear_conexion(cursos, alumno_mac, servidor_ip, servicio_nombre):
    # Validar autorización del alumno
    autorizado = False
    for curso in cursos:
        if any(alumno.mac == alumno_mac for alumno in curso.alumnos) and curso.estado == "DICTANDO":
            for servidor in curso.servidores:
                if servidor.direccion_ip == servidor_ip:
                    if any(servicio.nombre == servicio_nombre for servicio in servidor.servicios):
                        autorizado = True
                        break
            if autorizado:
                break
        
    if not autorizado:
        print("Error: El alumno no está autorizado para acceder a este servicio.")
        return

    # Establecer la ruta (simulación aquí, deberías integrar con Floodlight)
    print(f"Estableciendo conexión entre {alumno_mac} y {servidor_ip} para el servicio {servicio_nombre}.")
    # Aquí iría la llamada a build_route()

def listar_conexiones(conexiones):
    if not conexiones:
        print("No hay conexiones activas.")
        return
    
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    print("Conexiones activas:")
    for i, conexion in enumerate(conexiones, start=1):
        print(f"Conexión {i}:")
        print(f"  Alumno (MAC): {conexion['alumno_mac']}")
        print(f"  Servidor (IP): {conexion['servidor_ip']}")
        print(f"  Servicio: {conexion['servicio']}")
        print(f"  Protocolo: {conexion['protocolo']}")
        print(f"  Puerto: {conexion['puerto']}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def borrar_conexion(conexiones):
    if not conexiones:
        print("No hay conexiones activas para borrar.")
        return
    
    listar_conexiones(conexiones)  # Mostrar las conexiones activas
    try:
        num = int(input("Ingrese el número de la conexión que desea borrar: "))
        if 1 <= num <= len(conexiones):
            conexion_eliminada = conexiones.pop(num - 1)
            print(f"Conexión eliminada:")
            print(f"  Alumno (MAC): {conexion_eliminada['alumno_mac']}")
            print(f"  Servidor (IP): {conexion_eliminada['servidor_ip']}")
            print(f"  Servicio: {conexion_eliminada['servicio']}")
        else:
            print("Número inválido.")
    except ValueError:
        print("Por favor, ingrese un número válido.")

conexiones = [
    {
        "alumno_mac": "00:44:11:22:44:A7:2A",
        "servidor_ip": "10.0.0.3",
        "servicio": "ssh",
        "protocolo": "TCP",
        "puerto": 23
    },
    # poner mas conexiones
]


def main():
    datos = load_yaml('inf_final/database.yaml')  # Asegúrate de usar la ruta correcta a tu archivo YAML
    
    #Se pasa de yaml a objetos
    alumnos = getAlumnos(datos)
    servicios = getServicios(datos)
    servidores = getServidores(datos,servicios)
    cursos = getCursos(datos,alumnos,servidores)
    #implementar actualizar cursos
    
    op = displayMenu()
    
    match op:
        case "1":
            print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
            print("importar")
            print()
        case "2": #cursos
            display1()
            print("3) Actualizar")
            op2 = input('>>>')
            print()
            if(op2=="1"):
                listarCursos(cursos)
            elif(op2=="2"):
                detallesCurso(cursos)
            elif(op2=="3"):
                actualizar_curso(cursos, alumnos)
            else:
                display2()
        case "3": #alumnos
            display1()
            op3 = input('>>>')
            print()
            if(op3=="1"):
                listarAlumnos(alumnos)
            elif(op3=="2"):
                detalleAlumnos(alumnos)
            else:
                display2()
        case "4": #servidores
            display1()
            op4 = input('>>>')
            print()
            if(op4=="1"):
                listarServidores(servidores)
            elif(op4=="2"):
                detalleServidor(servidores)
            else:
                display2()
        case "5": #rutas
            print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
            print("Seleccione una opcion:")
            print("1) Crear")
            print("2) Listar")
            print("3)Borrar")
            op5 = input('>>>')
            if op5 == "1":
                alumno_mac = input("Ingrese la MAC del alumno: ")
                servidor_ip = input("Ingrese la IP del servidor: ")
                servicio_nombre = input("Ingrese el nombre del servicio: ")
                crear_conexion(cursos, alumno_mac, servidor_ip, servicio_nombre)
            elif op5 == "2":
                print("Listando conexiones...")
                listar_conexiones(conexiones)
            elif op5 == "3":
                print("Borrando conexión...")
                borrar_conexion(conexiones)
            else:
                display2()
        case "6": #salir
            print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
            print("Saliendo...")
        case _:
            display2()

    

    

if __name__ == "__main__":
    main()
