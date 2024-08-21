# Proyecto de Reconocimiento Facial

## Descripción

Este proyecto utiliza la biblioteca `face_recognition` junto con `opencv` y `watchdog` para monitorear un directorio en busca de nuevas imágenes y realizar el reconocimiento facial en tiempo real.

## Dependencias

- `time`: Para manejar el tiempo.
- `os`: Para operaciones del sistema de archivos.
- `watchdog.observers.Observer`, `watchdog.events.FileSystemEventHandler`: Para monitorear cambios en el sistema de archivos.
- `face_recognition`: Para el reconocimiento facial.
- `numpy`: Para operaciones numéricas.
- `cv2` (OpenCV): Para procesamiento de imágenes.

## Clases y Funciones

### Clase `Watcher`

Esta clase se encarga de observar un directorio específico (`faces_recognition`) en busca de cambios (nuevos archivos).

- **DIRECTORY_TO_WATCH**: Especifica el directorio a monitorear.
- **`__init__`**: Inicializa el observador.
- **`run`**: Configura el manejador de eventos (`Handler`) y comienza a observar el directorio. Si ocurre una excepción, detiene el observador.

### Clase `Handler`

Esta clase maneja los eventos del sistema de archivos.

- **`on_created`**: Método estático que se ejecuta cuando se crea un nuevo archivo en el directorio monitoreado. Llama a la función `classify_face` para procesar la nueva imagen.

### Función `classify_face`

Esta función se encarga de procesar una imagen y realizar el reconocimiento facial.

- **`image_path`**: Convierte la ruta de la imagen a una ruta absoluta y verifica si la imagen se carga correctamente.
- **`face_locations`**: Encuentra las ubicaciones de las caras en la imagen.
- **`unknown_face_encodings`**: Obtiene las codificaciones faciales de las caras encontradas.
- **`face_names`**: Lista para almacenar los nombres de las caras reconocidas.
- **`matches`**: Compara las codificaciones faciales desconocidas con las codificaciones conocidas.
- **`face_distances`**: Calcula las distancias entre las codificaciones faciales.
- **`best_match_index`**: Encuentra el índice de la mejor coincidencia.
- **`cv2.rectangle` y `cv2.putText`**: Dibuja rectángulos y nombres alrededor de las caras reconocidas en la imagen.
- **`cv2.imshow`**: Muestra la imagen procesada en una ventana.

### Función `load_known_faces`

Esta función carga las caras conocidas desde el directorio `faces`.

- **`faces_encoded`**: Lista para almacenar las codificaciones faciales conocidas.
- **`known_face_names`**: Lista para almacenar los nombres de las caras conocidas.
- **`os.listdir("faces")`**: Itera sobre los archivos en el directorio `faces`.
- **`cv2.imread`**: Carga cada imagen y obtiene sus codificaciones faciales.
- **`os.path.splitext(image_name)[0]`**: Usa el nombre del archivo (sin extensión) como el nombre de la cara.

### Bloque Principal

- **`faces_encoded, known_face_names = load_known_faces()`**: Carga las caras conocidas.
- **`w = Watcher()`**: Crea una instancia de la clase `Watcher`.
- **`w.run()`**: Inicia el observador para monitorear el directorio `faces_recognition`.

## Uso

1. Coloca las imágenes de las caras conocidas en el directorio `faces`.
2. Ejecuta el script.
3. Coloca nuevas imágenes en el directorio `faces_recognition` para que sean procesadas y reconocidas automáticamente.
