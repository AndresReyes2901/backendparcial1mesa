import re

def singularizar_palabra(palabra):
    if palabra.endswith('es'):
        palabra = palabra[:-2]
    elif palabra.endswith('s'):
        palabra = palabra[:-1]
    return palabra

def extraer_cantidad(texto):

    match = re.search(r'\d+', texto)
    if match:
        return int(match.group())


    palabras_a_numeros = {
        "uno": 1, "una": 1,
        "dos": 2,
        "tres": 3,
        "cuatro": 4,
        "cinco": 5,
        "seis": 6,
        "siete": 7,
        "ocho": 8,
        "nueve": 9,
        "diez": 10,
    }
    texto = texto.lower()
    for palabra, numero in palabras_a_numeros.items():
        if palabra in texto:
            return numero

    return None

def detectar_productos_en_texto(texto, productos_backend):
    palabras = texto.lower().split()
    productos_detectados = []

    for producto in productos_backend:
        nombre_producto = producto['name'].lower()

        if any(palabra in nombre_producto for palabra in palabras):
            cantidad = extraer_cantidad(texto) or 1
            productos_detectados.append({
                "product": producto['id'],
                "quantity": cantidad,
            })

    return productos_detectados