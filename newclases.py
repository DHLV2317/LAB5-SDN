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
                print("Implementar anadir eliminar alumno")
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
        case "6": #salir
            print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
            print("Saliendo...")
        case _:
            display2()

    

    

if __name__ == "__main__":
    main()
