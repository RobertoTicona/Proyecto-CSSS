import os
import pandas as pd
import time  # Importar el módulo para medir el tiempo


def buscar_dato_excel(base_path, year_month, dni_buscado):
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

        # Implementación de búsqueda exponencial para localizar inicio del mes
        inicio_mes = None
        fin_mes = None

        # Fase exponencial para localizar un rango probable
        n = len(df)
        step = 1
        while step < n and not (isinstance(df.iloc[step, 0], str) and df.iloc[step, 0] == f"{year}-{mes}"):
            interacciones += 1
            step *= 2

        # Determinar el rango para la búsqueda lineal
        low = step // 2
        high = min(step, n)

        # Fase lineal para encontrar inicio del mes dentro del rango
        for i in range(low, high):
            interacciones += 1
            if df.iloc[i, 0] == f"{year}-{mes}":
                inicio_mes = i + 1
                break

        if inicio_mes is None:
            print(f"No se encontró el mes {year}-{mes} en el archivo.")
            return

        # Determinar fin del mes
        for i in range(inicio_mes, n):
            interacciones += 1
            if isinstance(df.iloc[i, 0], str) and "-" in df.iloc[i, 0]:
                fin_mes = i
                break

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

        # Buscar el DNI en los datos del mes
        fila = datos_mes[datos_mes["DNI"] == dni_buscado]
        interacciones += len(datos_mes)  # Contar interacciones de la búsqueda en DataFrame

        if fila.empty:
            print(f"No se encontró el DNI {dni_buscado} en los datos del mes {year}-{mes}.")
        else:
            # Extraer información específica
            nombres = fila.iloc[0]["Apellidos y Nombres"]
            historial_clinica = fila.iloc[0]["Historial Clínica"]
            fecha_nacimiento = fila.iloc[0]["Fecha de Nacimiento"]
            edad_actual = fila.iloc[0]["Edad Actual"]
            primer_mes_tratamiento = fila.iloc[0]["1er Mes de Tratamiento"]
            hb_corregida = fila.iloc[0]["HB Corregida"]
            dx = fila.iloc[0]["DX"]
            segundo_mes_tratamiento = fila.iloc[0]["2do Mes de Tratamiento"]

            # Calcular el tiempo transcurrido
            fin_tiempo = time.time()
            tiempo_transcurrido = fin_tiempo - inicio_tiempo

            print(f"Resultados encontrados para el DNI {dni_buscado} en el mes {year}-{mes}:")
            print(f"- Apellidos y Nombres: {nombres}")
            print(f"- Historial Clínica: {historial_clinica}")
            print(f"- Fecha de Nacimiento: {fecha_nacimiento}")
            print(f"- Edad Actual: {edad_actual}")
            print(f"- 1er Mes de Tratamiento: {primer_mes_tratamiento}")
            print(f"- HB Corregida: {hb_corregida}")
            print(f"- DX: {dx}")
            print(f"- 2do Mes de Tratamiento: {segundo_mes_tratamiento}")
            print(f"\nTiempo transcurrido para encontrar el DNI: {tiempo_transcurrido:.4f} segundos.")
            print(f"Interacciones realizadas: {interacciones}")
            print(f"Complejidad estimada: O(log n) para la fase exponencial + búsqueda lineal.")

    except Exception as e:
        print(f"Error: {e}")


# Datos de entrada
base_path = input("Ingrese la ruta base donde se encuentra la carpeta 'Datos': ")
year_month = input("Ingrese el año y mes (AAAA-MM): ")  # Año y mes en formato 'YYYY-MM' (por ejemplo, '2022-01')
dni_buscado = input("Ingrese el DNI que desea buscar: ")  # DNI a buscar

# Ejecutar la función
buscar_dato_excel(base_path, year_month,dni_buscado)