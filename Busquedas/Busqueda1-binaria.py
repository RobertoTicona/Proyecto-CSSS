import os
import pandas as pd
import time  # Importar el módulo para medir el tiempo


def buscar_dato_excel_binario(base_path, year_month, dni_buscado):
    try:
        # Iniciar la medición del tiempo
        inicio_tiempo = time.time()

        # Inicializar contador de interacciones
        interacciones = 0

        # Desglosar el año y mes
        year, mes = year_month.split("-")

        # Ruta del archivo Excel
        ruta_archivo = os.path.join(base_path, 'NOMINAL.xlsx')

        # Verificar si el archivo existe
        if not os.path.exists(ruta_archivo):
            print(f"No se encontró el archivo {ruta_archivo}.")
            return

        # Leer el archivo Excel
        df = pd.read_excel(ruta_archivo, header=None)

        # Buscar el índice de la fila correspondiente al año y mes
        inicio_mes = None
        fin_mes = None
        for index, row in df.iterrows():
            interacciones += 1  # Contar interacciones
            if row[0] == f"{year}-{mes}":  # Buscar el encabezado del mes
                inicio_mes = index + 1  # Los datos comienzan en la fila siguiente
                continue
            if inicio_mes is not None and isinstance(row[0], str) and "-" in row[0]:
                fin_mes = index  # El siguiente encabezado marca el fin del mes actual
                break

        if inicio_mes is None:
            print(f"No se encontró el mes {year}-{mes} en el archivo.")
            return

        fin_mes = fin_mes if fin_mes is not None else len(df)

        # Extraer datos del mes
        datos_mes = df.iloc[inicio_mes:fin_mes].reset_index(drop=True)
        datos_mes.columns = [
            "DNI", "Apellidos y Nombres", "Historial Clínica", "Fecha de Nacimiento",
            "Edad Actual", "1er Mes de Tratamiento", "HB Corregida", "DX", 
            "2do Mes de Tratamiento", "Columna Extra 1", "Columna Extra 2", "Columna Extra 3"
        ]

        # Limpiar los espacios y convertir los DNI en texto
        datos_mes["DNI"] = datos_mes["DNI"].astype(str).str.strip()
        dni_buscado = str(dni_buscado).strip()

        # Ordenar los datos por la columna DNI
        datos_ordenados = datos_mes.sort_values("DNI").reset_index(drop=True)

        # Implementar la búsqueda binaria
        inicio = 0
        fin = len(datos_ordenados) - 1
        encontrado = False
        resultado = None

        while inicio <= fin:
            interacciones += 1  # Contar interacciones
            medio = (inicio + fin) // 2
            dni_actual = datos_ordenados.iloc[medio]["DNI"]

            if dni_actual == dni_buscado:
                encontrado = True
                resultado = datos_ordenados.iloc[medio]
                break
            elif dni_actual < dni_buscado:
                inicio = medio + 1
            else:
                fin = medio - 1

        # Calcular el tiempo transcurrido
        fin_tiempo = time.time()
        tiempo_transcurrido = fin_tiempo - inicio_tiempo

        if encontrado:
            # Extraer información específica
            print(f"Resultados encontrados para el DNI {dni_buscado} en el mes {year}-{mes}:")
            print(f"- Apellidos y Nombres: {resultado['Apellidos y Nombres']}")
            print(f"- Historial Clínica: {resultado['Historial Clínica']}")
            print(f"- Fecha de Nacimiento: {resultado['Fecha de Nacimiento']}")
            print(f"- Edad Actual: {resultado['Edad Actual']}")
            print(f"- 1er Mes de Tratamiento: {resultado['1er Mes de Tratamiento']}")
            print(f"- HB Corregida: {resultado['HB Corregida']}")
            print(f"- DX: {resultado['DX']}")
            print(f"- 2do Mes de Tratamiento: {resultado['2do Mes de Tratamiento']}")
        else:
            print(f"No se encontró el DNI {dni_buscado} en los datos del mes {year}-{mes}.")

        print(f"\nTiempo transcurrido: {tiempo_transcurrido:.4f} segundos.")
        print(f"Interacciones realizadas: {interacciones}")
        print(f"Complejidad estimada: O(log n) para la búsqueda binaria con n = {len(datos_ordenados)}.")
        print(f"Además, el ordenamiento tiene complejidad O(n log n).")

    except Exception as e:
        print(f"Error: {e}")


# Datos de entrada
base_path = input("Ingrese la ruta base donde se encuentra la carpeta 'Datos': ")
year_month = input("Ingrese el año y mes (AAAA-MM): ")  # Año y mes en formato 'YYYY-MM' (por ejemplo, '2022-01')
dni_buscado = input("Ingrese el DNI que desea buscar: ")  # DNI a buscar

# Ejecutar la función
buscar_dato_excel_binario(base_path, year_month, dni_buscado)
