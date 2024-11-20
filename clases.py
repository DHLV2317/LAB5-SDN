import yaml

class Alumno:
    def __init__(self, nombre: str, mac_address: str):
        self.nombre = nombre
        self.pc_mac = mac_address

class Servicio:
    def __init__(self, nombre: str, protocolo: str, puerto: int):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto

class Servidor:
    def __init__(self, nombre: str, ip: str, servicios: list[Servicio] = None):
        self.nombre = nombre
        self.direccion_ip = ip
        self.servicios = servicios if servicios is not None else []

class Curso:
    def __init__(self, nombre: str, estado: str):
        self.nombre = nombre
        self.estado = estado
        self.alumnos = []
        self.servidores = []
    
    def agregar_alumno(self, alumno: Alumno) -> None:
        if alumno not in self.alumnos:
            self.alumnos.append(alumno)
    
    def remover_alumno(self, alumno: Alumno) -> None:
        if alumno in self.alumnos:
            self.alumnos.remove(alumno)
    
    def agregar_servidor(self, servidor: Servidor) -> None:
        if servidor not in self.servidores:
            self.servidores.append(servidor)

def main():
    try:
        # Leer el archivo YAML
        with open('database.yaml', 'r') as file:
            data = yaml.safe_load(file)
            
            # Imprimir solo los nombres de los servidores
            print("Nombres de los servidores:")
            for servidor in data['servidores']:
                print(f"- {servidor['nombre']}")
            
            print("\nCreando instancias de objetos con los datos del YAML...")
            
            # Crear servicios
            servicios = []
            for servicio_data in data.get('servicios', []):
                servicio = Servicio(
                    nombre=servicio_data['nombre'],
                    protocolo=servicio_data['protocolo'],
                    puerto=servicio_data['puerto']
                )
                servicios.append(servicio)
            
            # Crear servidores
            servidores = []
            for servidor_data in data['servidores']:
                # Encontrar los servicios correspondientes a este servidor
                servicios_servidor = [s for s in servicios if s.nombre in servidor_data.get('servicios', [])]
                
                servidor = Servidor(
                    nombre=servidor_data['nombre'],
                    ip=servidor_data['ip'],
                    servicios=servicios_servidor
                )
                servidores.append(servidor)
            
            # Crear alumnos
            alumnos = []
            for alumno_data in data.get('alumnos', []):
                alumno = Alumno(
                    nombre=alumno_data['nombre'],
                    mac_address=alumno_data['mac']
                )
                alumnos.append(alumno)
            
            # Crear curso
            curso = Curso(
                nombre=data.get('curso', {}).get('nombre', 'Curso SDN'),
                estado=data.get('curso', {}).get('estado', 'Activo')
            )
            
            # Agregar alumnos y servidores al curso
            for alumno in alumnos:
                curso.agregar_alumno(alumno)
            for servidor in servidores:
                curso.agregar_servidor(servidor)
            
            # Mostrar la información cargada
            print(f"\nInformación del curso {curso.nombre}:")
            print(f"Estado: {curso.estado}")
            
            print("\nAlumnos:")
            for alumno in curso.alumnos:
                print(f"- {alumno.nombre} (MAC: {alumno.pc_mac})")
            
            print("\nServidores y sus servicios:")
            for servidor in curso.servidores:
                print(f"\nServidor: {servidor.nombre} (IP: {servidor.direccion_ip})")
                print("Servicios:")
                for servicio in servidor.servicios:
                    print(f"- {servicio.nombre} ({servicio.protocolo}/{servicio.puerto})")

    except FileNotFoundError:
        print("Error: No se encontró el archivo datos.yaml")
    except yaml.YAMLError as e:
        print(f"Error al parsear el archivo YAML: {e}")
    except KeyError as e:
        print(f"Error: Falta una clave requerida en el archivo YAML: {e}")

if __name__ == "__main__":
    main()