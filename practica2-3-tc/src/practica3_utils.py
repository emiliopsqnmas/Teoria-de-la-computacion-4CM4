def validar_lote_cadenas(automata, ruta_archivo_entrada, ruta_archivo_salida):
    """Lee un archivo con una cadena por línea, valida cada una y genera un informe (Ejercicio 2.5)."""
    resultados = []
    with open(ruta_archivo_entrada, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    for linea in lineas:
        cadena = linea.strip()
        aceptada, _ = automata.simular_cadena(cadena)
        estado_str = "ACEPTADA" if aceptada else "RECHAZADA"
        resultados.append(f"Cadena: '{cadena}' -> {estado_str}\n")

    with open(ruta_archivo_salida, 'w', encoding='utf-8') as f:
        f.writelines(resultados)
    
    return len(resultados)