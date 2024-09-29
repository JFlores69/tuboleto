from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Ruta correcta al ChromeDriver
driver_path = 'C:/Users/tu_en/Downloads/chromedriver-win64/chromedriver.exe'  # Cambia esto a la ruta correcta de tu chromedriver.exe

# Configuración de opciones del navegador
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Crear un objeto Service con la ruta al ChromeDriver
service = Service(driver_path)

# Inicializa el controlador del navegador Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Abre la página web
    driver.get('https://tuboleto.cultura.pe/llaqta_machupicchu')

    # Esperar a que la página esté completamente cargada
    WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    # Esperar hasta que el primer mat-select esté visible
    wait = WebDriverWait(driver, 30)  # Aumenté el tiempo de espera a 30 segundos
    circuit_select = wait.until(EC.visibility_of_element_located((By.ID, 'mat-select-0')))  # ID correcto del primer mat-select

    # Hacer clic en el primer mat-select para desplegar las opciones
    circuit_select.click()

    # Esperar a que las opciones del primer mat-select estén visibles
    options = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//mat-option")))

    # Crear una matriz para almacenar las opciones del segundo mat-select por cada opción del primero
    matriz = []

    # Recorrer las opciones del primer mat-select
    for i, option in enumerate(options):
        # Seleccionar cada opción del primer mat-select
        option.click()
        print(f"Seleccionando opción {i + 1} del primer mat-select: {option.text}")

        # Esperar un pequeño lapso de tiempo para evitar errores de sincronización
        time.sleep(1.5)  # Simula un comportamiento más humano

        # Volver a buscar el segundo mat-select cada vez para evitar el error stale element
        second_select = wait.until(EC.visibility_of_element_located((By.ID, 'mat-select-2')))
        second_select.click()  # Hacer clic en el segundo mat-select

        # Esperar a que las nuevas opciones del segundo mat-select estén visibles
        second_options = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//mat-option")))

        # Crear un array temporal para almacenar las opciones del segundo mat-select para esta opción del primero
        second_options_array = []

        # Recorrer las opciones del segundo mat-select
        for second_option in second_options:
            # Volver a buscar el texto del segundo option, en caso de que haya sido actualizado
            second_options_array.append(second_option.text)

        # Agregar las opciones del segundo mat-select a la matriz
        matriz.append(second_options_array)

        # Imprimir las opciones del segundo mat-select
        print(f"Opciones del segundo mat-select para la opción {i + 1}: {second_options_array}")

        # Usar JavaScript para cerrar el segundo mat-select
        driver.execute_script("arguments[0].click();", second_select)

        # Esperar un pequeño lapso de tiempo para evitar errores de sincronización
        time.sleep(1.5)  # Simula un comportamiento más humano

        # *** SOLUCIÓN: Interactuar con el backdrop si está presente ***
        try:
            backdrop = driver.find_element(By.CLASS_NAME, 'cdk-overlay-backdrop')
            driver.execute_script("arguments[0].click();", backdrop)  # Cierra el backdrop
            time.sleep(1)  # Espera un pequeño lapso para asegurar que se cierre
        except Exception as e:
            print("No se encontró el backdrop, continuando...")

        # Volver a abrir el primer mat-select para seleccionar la siguiente opción
        circuit_select = wait.until(EC.visibility_of_element_located((By.ID, 'mat-select-0')))
        circuit_select.click()

        # Esperar un pequeño lapso de tiempo para evitar errores de sincronización
        time.sleep(1.5)  # Simula un comportamiento más humano

    # Imprimir la matriz final con el formato solicitado
    print("\nMatriz final de todas las opciones:")
    for idx, rutas in enumerate(matriz):
        print(f"Opción {idx + 1}:")
        for ruta in rutas:
            print(f" - {ruta}")

finally:
    # Cerrar el navegador
    driver.quit()
