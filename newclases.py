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
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error al leer el archivo YAML: {e}")
        return None

def getAlumnos(datos):
    if 'alumnos' not in datos:
        return []
    return [Alumno(al['nombre'], al['codigo'], al['mac']) for al in datos['alumnos']]

def getServicios(datos):
    servicios = []
    if 'servidores' in datos:
        for servidor in datos['servidores']:
            if 'servicios' in servidor:
                servicios.extend([Servicio(sv['nombre'], sv['protocolo'], sv['puerto']) 
                                for sv in servidor['servicios']])
    return servicios

def getServidores(datos, servicios):
    if 'servidores' not in datos:
        return []
    servidores = [Servidor(s['nombre'], s['ip']) for s in datos['servidores']]
    for servidor in servidores:
        servidor.servicios.extend(servicios)
    return servidores

def getCursos(datos, alumnos, servidores):
    cursos = []
    alumnos_dict = {alumno.codigo: alumno for alumno in alumnos}
    servidores_dict = {servidor.nombre: servidor for servidor in servidores}

    if 'cursos' not in datos:
        return []

    for c in datos['cursos']:
        curso = Curso(c['codigo'], c['estado'], c['nombre'])
        
        # Agregar alumnos al curso
        for codigo_alumno in c.get('alumnos', []):
            if codigo_alumno in alumnos_dict:
                curso.agregar_alumno(alumnos_dict[codigo_alumno])

        # Agregar servidores al curso con servicios permitidos
        for servidor_info in c.get('servidores', []):
            servidor_nombre = servidor_info['nombre']
            if servidor_nombre in servidores_dict:
                servidor = servidores_dict[servidor_nombre]
                servicios_permitidos = [
                    servicio for servicio in servidor.servicios
                    if servicio.nombre in servidor_info.get('servicios_permitidos', [])
                ]
                servidor_curso = Servidor(servidor.nombre, servidor.ip)
                servidor_curso.servicios.extend(servicios_permitidos)
                curso.añadir_servidor(servidor_curso)

        cursos.append(curso)
    return cursos

def actualizar_curso(cursos, alumnos):
    codigo_curso = input("Ingrese el código del curso: ")
    curso = next((c for c in cursos if c.codigo == codigo_curso), None)
    
    if curso is None:
        print("Curso no encontrado.")
        return

    print("1) Agregar Alumno\n2) Eliminar Alumno")
    op = input(">>> ")
    
    if op == "1":
        codigo_alumno = input("Ingrese el código del alumno: ")
        alumno = next((a for a in alumnos if a.codigo == codigo_alumno), None)
        
        if alumno is None:
            print("Alumno no encontrado.")
            return
            
        if any(a.codigo == alumno.codigo for a in curso.alumnos):
            print(f"El alumno {alumno.nombre} ya está registrado en el curso {curso.nombre}")
            return
            
        curso.agregar_alumno(alumno)
        print(f"Alumno {alumno.nombre} agregado al curso {curso.nombre}")
        
    elif op == "2":
        codigo_alumno = input("Ingrese el código del alumno: ")
        alumno = next((a for a in curso.alumnos if a.codigo == codigo_alumno), None)
        
        if alumno is None:
            print("Alumno no encontrado en el curso.")
            return
            
        curso.alumnos.remove(alumno)
        print(f"Alumno {alumno.nombre} eliminado del curso {curso.nombre}")
        
    else:
        print("Opción inválida.")

def detallesCurso(cursos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    for curso in cursos:
        print(f"Código: {curso.codigo}")
        print(f"Estado: {curso.estado}")
        print(f"Nombre: {curso.nombre}")
        print("Alumnos:")
        for alumno in curso.alumnos:
            print(f"    - {alumno.nombre} ({alumno.codigo})")
        print("Servidores:")
        for servidor in curso.servidores:
            print(f"    - Nombre: {servidor.nombre}")
            print("      Servicios permitidos:")
            for servicio in servidor.servicios:
                print(f"        - {servicio.nombre} ({servicio.protocolo}:{servicio.puerto})")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def listarCursos(cursos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    if not cursos:
        print("No hay cursos registrados.")
        return
    for curso in cursos:
        print(f"Código: {curso.codigo}")
        print(f"Nombre: {curso.nombre}")
        print(f"Estado: {curso.estado}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def listarAlumnos(alumnos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    if not alumnos:
        print("No hay alumnos registrados.")
        return
    for alumno in alumnos:
        print(f"Nombre: {alumno.nombre}")
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def detalleAlumnos(alumnos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    if not alumnos:
        print("No hay alumnos registrados.")
        return
    for alumno in alumnos:
        print(f"Nombre: {alumno.nombre}")
        print(f"Código: {alumno.codigo}")
        print(f"Dirección MAC: {alumno.mac}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def listarServidores(servidores):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    if not servidores:
        print("No hay servidores registrados.")
        return
    for servidor in servidores:
        print(f"Nombre: {servidor.nombre}")
        print(f"Dirección IP: {servidor.ip}")
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def detalleServidor(servidores):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    if not servidores:
        print("No hay servidores registrados.")
        return
    for servidor in servidores:
        print(f"Nombre: {servidor.nombre}")
        print(f"Dirección IP: {servidor.ip}")
        print("Servicios:")
        print('*--*--*--*--*')
        for servicio in servidor.servicios:
            print(f'   Servicio: {servicio.nombre}')
            print(f'   Protocolo: {servicio.protocolo}')
            print(f'   Puerto: {servicio.puerto}')
            print('*--*--*--*--*')
        print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")

def crear_conexion(cursos, alumno_mac, servidor_ip, servicio_nombre):
    # Validar autorización del alumno
    autorizado = False
    curso_autorizado = None
    servidor_autorizado = None
    servicio_autorizado = None

    for curso in cursos:
        if curso.estado != "DICTANDO":
            continue
            
        alumno_encontrado = any(alumno.mac == alumno_mac for alumno in curso.alumnos)
        if not alumno_encontrado:
            continue

        for servidor in curso.servidores:
            if servidor.ip == servidor_ip:
                for servicio in servidor.servicios:
                    if servicio.nombre == servicio_nombre:
                        autorizado = True
                        curso_autorizado = curso
                        servidor_autorizado = servidor
                        servicio_autorizado = servicio
                        break
                if autorizado:
                    break
        if autorizado:
            break

    if not autorizado:
        print("Error: El alumno no está autorizado para acceder a este servicio.")
        return None

    conexion = {
        "alumno_mac": alumno_mac,
        "servidor_ip": servidor_ip,
        "servicio": servicio_nombre,
        "protocolo": servicio_autorizado.protocolo,
        "puerto": servicio_autorizado.puerto
    }

    print(f"Conexión establecida entre {alumno_mac} y {servidor_ip} para el servicio {servicio_nombre}.")
    return conexion

def listar_conexiones(conexiones):
    if not conexiones:
        print("No hay conexiones activas.")
        return

    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    print("Conexiones activas:")
    for i, conexion in enumerate(conexiones, 1):
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

    listar_conexiones(conexiones)
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

def displayMenu():
    print()
    print('##############################################')
    print('Network Policy Manager de la USPM')
    print('##############################################')
    print()
    print("Seleccione una opción:")
    print("1) Importar")
    print("2) Cursos")
    print("3) Alumnos")
    print("4) Servidores")
    print("5) Conexiones")
    print("6) Salir")
    return input('>>> ')

def display1():
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    print("Seleccione una opción:")
    print("1) Listar")
    print("2) Mostrar detalle")

def display2():
    print("*--*Valor inválido*--*")
    print("Saliendo...")
    print()

def crear_alumno(alumnos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    print("Crear nuevo alumno")
    nombre = input("Ingrese el nombre del alumno: ")
    codigo = input("Ingrese el código del alumno: ")
    mac = input("Ingrese la dirección MAC del alumno: ")
    
    # Validar que el código no exista
    if any(a.codigo == codigo for a in alumnos):
        print("Error: Ya existe un alumno con ese código.")
        return
    
    # Validar que la MAC no exista
    if any(a.mac == mac for a in alumnos):
        print("Error: Ya existe un alumno con esa dirección MAC.")
        return
        
    nuevo_alumno = Alumno(nombre, codigo, mac)
    alumnos.append(nuevo_alumno)
    print(f"Alumno {nombre} creado exitosamente.")
    guardar_cambios(alumnos)

def actualizar_alumno(alumnos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    codigo = input("Ingrese el código del alumno a actualizar: ")
    alumno = next((a for a in alumnos if a.codigo == codigo), None)
    
    if alumno is None:
        print("Alumno no encontrado.")
        return
        
    print(f"Actualizando datos de {alumno.nombre}")
    print("Deje en blanco para mantener el valor actual")
    
    nuevo_nombre = input(f"Nuevo nombre [{alumno.nombre}]: ")
    nueva_mac = input(f"Nueva dirección MAC [{alumno.mac}]: ")
    
    if nuevo_nombre:
        alumno.nombre = nuevo_nombre
    if nueva_mac:
        # Validar que la nueva MAC no exista
        if any(a.mac == nueva_mac and a.codigo != codigo for a in alumnos):
            print("Error: Ya existe un alumno con esa dirección MAC.")
            return
        alumno.mac = nueva_mac
    
    print("Alumno actualizado exitosamente.")
    guardar_cambios(alumnos)

def borrar_alumno(alumnos, cursos):
    print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
    codigo = input("Ingrese el código del alumno a eliminar: ")
    alumno = next((a for a in alumnos if a.codigo == codigo), None)
    
    if alumno is None:
        print("Alumno no encontrado.")
        return
        
    # Verificar si el alumno está inscrito en algún curso
    for curso in cursos:
        if any(a.codigo == codigo for a in curso.alumnos):
            print("Error: No se puede eliminar el alumno porque está inscrito en uno o más cursos.")
            return
            
    alumnos.remove(alumno)
    print(f"Alumno {alumno.nombre} eliminado exitosamente.")
    guardar_cambios(alumnos)

def guardar_cambios(alumnos):
    try:
        # Leer el archivo actual
        with open('database.yaml', 'r') as file:
            datos = yaml.safe_load(file)
        
        # Actualizar la sección de alumnos
        datos['alumnos'] = [
            {
                'nombre': alumno.nombre,
                'codigo': alumno.codigo,
                'mac': alumno.mac
            }
            for alumno in alumnos
        ]
        
        # Guardar los cambios
        with open('database.yaml', 'w') as file:
            yaml.dump(datos, file, default_flow_style=False)
            
    except Exception as e:
        print(f"Error al guardar los cambios: {e}")
        

def main():
    # Inicialización
    datos = load_yaml('database.yaml')
    if datos is None:
        print("Error al cargar la base de datos. Saliendo...")
        return

    conexiones = []
    alumnos = getAlumnos(datos)
    servicios = getServicios(datos)
    servidores = getServidores(datos, servicios)
    cursos = getCursos(datos, alumnos, servidores)

    while True:
        op = displayMenu()

        match op:
            case "1":
                print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
                print("Importar")
                print()
            case "2":  # Cursos
                display1()
                print("3) Actualizar")
                op2 = input('>>> ')
                print()
                match op2:
                    case "1":
                        listarCursos(cursos)
                    case "2":
                        detallesCurso(cursos)
                    case "3":
                        actualizar_curso(cursos, alumnos)
                    case _:
                        display2()
            
            case "3":  # Alumnos
                print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
                print("Seleccione una opción:")
                print("1) Listar")
                print("2) Mostrar detalle")
                print("3) Crear")
                print("4) Actualizar")
                print("5) Borrar")
                op3 = input('>>> ')
                print()
                match op3:
                    case "1":
                        listarAlumnos(alumnos)
                    case "2":
                        detalleAlumnos(alumnos)
                    case "3":
                        crear_alumno(alumnos)
                    case "4":
                        actualizar_alumno(alumnos)
                    case "5":
                        borrar_alumno(alumnos, cursos)
                    case _:
                        display2()

                display1()
                op3 = input('>>> ')
                print()
                match op3:
                    case "1":
                        listarAlumnos(alumnos)
                    case "2":
                        detalleAlumnos(alumnos)
                    case _:
                        display2()
            case "4":  # Servidores
                display1()
                op4 = input('>>> ')
                print()
                match op4:
                    case "1":
                        listarServidores(servidores)
                    case "2":
                        detalleServidor(servidores)
                    case _:
                        display2()
            case "5":  # Conexiones
                print("*--*--*--*--*--*--*--*--*--*--*")
                print("Seleccione una opción:")
                print("1) Crear")
                print("2) Listar")
                print("3) Borrar")
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
            case "6":  # Salir
                print("*--*--*--*--*--*--*--*--*--*--*--*--*--*")
                print("Saliendo...")
                break  # Rompe el bucle y termina el programa
            case _:
                display2()

    

if __name__ == "__main__":
    main()
