import re


def singularizar_palabra(palabra):
    if palabra.endswith('es'):
        palabra = palabra[:-2]
    elif palabra.endswith('s'):
        palabra = palabra[:-1]
    return palabra


def extraer_cantidad(texto):
    texto = texto.lower()

    patrones_cantidad = [

        r'(\d+)\s+(unidades|productos|camaras|cámaras|webcams|unidad)',

        r'(quiero|necesito|agregar|añadir|comprar)\s+(\d+)(?!\s*[a-z0-9])',
    ]

    for patron in patrones_cantidad:
        match = re.search(patron, texto)
        if match:
            grupos = match.groups()
            if patron.startswith(r'(\d+)'):
                return int(grupos[0])
            else:
                return int(grupos[1])

    palabras_a_numeros = {
        "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4,
        "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10
    }

    for palabra, valor in palabras_a_numeros.items():
        patron = rf'(quiero|necesito|agregar|añadir|comprar)\s+{palabra}'
        if re.search(patron, texto):
            return valor

    primeras_palabras = texto.split()[:2]
    for palabra in primeras_palabras:
        if palabra in palabras_a_numeros:
            return palabras_a_numeros[palabra]

    return 1


def detectar_productos_en_texto(texto, productos_backend):
    texto = texto.lower()

    # Palabras a ignorar
    stopwords = ['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o',
                 'a', 'ante', 'con', 'de', 'desde', 'en', 'para', 'por', 'sin',
                 'sobre', 'quiero', 'necesito', 'agregar', 'añadir', 'comprar', 'mi']

    palabras = texto.split()
    palabras_significativas = [p for p in palabras if len(p) > 2 and p not in stopwords]

    productos_detectados = []

    for producto in productos_backend:
        nombre_producto = producto['name'].lower()

        # Buscar coincidencias de frases completas
        if nombre_producto in texto:
            cantidad = extraer_cantidad(texto)
            productos_detectados.append({
                "product": producto['id'],
                "quantity": cantidad,
            })
        else:

            palabras_nombre = nombre_producto.split()
            coincidencias = sum(1 for p in palabras_significativas if p in palabras_nombre)

            if coincidencias >= 2:
                cantidad = extraer_cantidad(texto)
                productos_detectados.append({
                    "product": producto['id'],
                    "quantity": cantidad,
                })

    return productos_detectados
