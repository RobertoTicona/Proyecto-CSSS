import os
import pandas as pd
import time  # Importar el módulo para medir el tiempo
import math  # Para cálculos matemáticos


def buscar_dato_excel_fibonacci(base_path, year_month, dni_buscado):
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
            if row[0] == f"{year}-{mes}":  # Buscar el encabezado del mes
                inicio_mes = index + 1  # Los datos comienzan en la fila siguiente
                break

        if inicio_mes is None:
            print(f"No se encontró el mes {year}-{mes} en el archivo.")
            return

        # Determinar el fin del mes
        for i in range(inicio_mes, len(df)):
            if isinstance(df.iloc[i, 0], str) and "-" in df.iloc[i, 0]:
                fin_mes = i
                break

        fin_mes = fin_mes if fin_mes is not None else len(df)

        # Extraer los datos del mes
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

        # Implementar la búsqueda de Fibonacci
        n = len(datos_ordenados)
        fib_m_minus_2 = 0  # Fib(n-2)
        fib_m_minus_1 = 1  # Fib(n-1)
        fib_m = fib_m_minus_1 + fib_m_minus_2  # Fib(n)

        # Calcular el número de Fibonacci más cercano al tamaño del conjunto de datos
        while fib_m < n:
            fib_m_minus_2 = fib_m_minus_1
            fib_m_minus_1 = fib_m
            fib_m = fib_m_minus_1 + fib_m_minus_2

        prev = -1  # Índice previo
        encontrado = False
        resultado = None

        # Realizar la búsqueda de Fibonacci
        while fib_m > 1:
            i = min(prev + fib_m_minus_2, n - 1)  # Índice a comparar
            interacciones += 1  # Incrementar solo al realizar una comparación

            # Comparar el DNI en la posición actual
            if datos_ordenados.iloc[i]["DNI"] == dni_buscado:
                encontrado = True
                resultado = datos_ordenados.iloc[i]
                break

            elif datos_ordenados.iloc[i]["DNI"] < dni_buscado:
                fib_m = fib_m_minus_1
                fib_m_minus_1 = fib_m_minus_2
                fib_m_minus_2 = fib_m - fib_m_minus_2
                prev = i

            else:
                fib_m = fib_m_minus_2
                fib_m_minus_1 = fib_m_minus_1 - fib_m_minus_2
                fib_m_minus_2 = fib_m - fib_m_minus_1

        # Verificar el último índice si el rango se reduce a uno
        if fib_m == 1 and prev < n - 1 and datos_ordenados.iloc[prev + 1]["DNI"] == dni_buscado:
            encontrado = True
            resultado = datos_ordenados.iloc[prev + 1]

        # Mostrar el resultado
        if encontrado:
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

        # Calcular el tiempo transcurrido
        fin_tiempo = time.time()
        tiempo_transcurrido = fin_tiempo - inicio_tiempo

        print(f"\nTiempo transcurrido: {tiempo_transcurrido:.4f} segundos.")
        print(f"Iteraciones realizadas: {interacciones}")
        print(f"Complejidad estimada: O(log n).")

    except Exception as e:
        print(f"Error: {e}")


# Datos de entrada
base_path = input("Ingrese la ruta base donde se encuentra la carpeta 'Datos': ")
year_month = input("Ingrese el año y mes (AAAA-MM): ")  # Año y mes en formato 'YYYY-MM' (por ejemplo, '2022-01')
dni_buscado = input("Ingrese el DNI que desea buscar: ")  # DNI a buscar

# Ejecutar la función
buscar_dato_excel_fibonacci(base_path, year_month,dni_buscado)
