# Prueba Técnica: Automatización de Pruebas de Calidad de Datos (ETL)

Este repositorio contiene la solución completa a la prueba técnica diseñada para el rol de Especialista en Automatización de Pruebas de Datos (Data Quality ETL Tester).

El objetivo de las pruebas es demostrar la capacidad de:

* Diseñar lógicas de auditoría de datos complejas usando SQL.
* Implementar un framework de pruebas automatizadas mantenible y escalable usando Python, Pandas y Pytest.

---

## 🎯 El Desafío

A partir de dos conjuntos de datos de ingesta (`customers_raw` y `transactions_raw`) que contienen problemas de calidad de datos comunes (valores NULL, registros duplicados y violaciones de integridad referencial), el desafío se dividió en dos partes:

1.  **Parte 1 (Diseño):** Escribir consultas SQL para identificar 4 reglas de negocio clave.
2.  **Parte 2 (Automatización):** Implementar un framework en Python que ejecute automáticamente estas validaciones y genere un reporte de PASS/FAIL.

---

## 🛠️ Solución Implementada

La solución se abordó en dos fases, replicando un flujo de trabajo profesional.

### Parte 1: Diseño de la Lógica de Auditoría (SQL)

Se diseñaron 4 consultas de auditoría SQL robustas, centrándose en la eficiencia y la robustez de la lógica:

* **Completitud:** Se utilizó `UNION ALL` para crear un manifiesto de auditoría unificado de todos los campos nulos, siendo más rápido que `UNION`.
* **Unicidad:** Se utilizó `GROUP BY / HAVING` con un filtro `WHERE ... IS NOT NULL` para aislar correctamente la regla de negocio de unicidad de la regla de completitud.
* **Integridad Referencial:** Se implementó el patrón `LEFT JOIN / WHERE IS NULL`, que es más performante y seguro ante NULLs que las alternativas (ej. `NOT IN`).
* **Reconciliación:** Se usó una arquitectura de 3 fases con CTEs (cláusulas `WITH`) y un `FULL OUTER JOIN`. Este patrón es el estándar de la industria, ya que detecta los tres tipos de errores de reconciliación: datos alterados, datos faltantes y datos "fantasma".

### Parte 2: Framework de Automatización (Pytest + Pandas)

La lógica de auditoría diseñada en SQL se implementó como un framework de automatización usando Pytest y Pandas.

* **Pandas** se utilizó para la manipulación y lógica de datos, traduciendo la sintaxis SQL a operaciones de DataFrames (ej. `pd.merge` para JOINs, `.groupby().sum()` para agregaciones, `.isnull().sum()` para validaciones de nulos).
* **Pytest** se utilizó como el corredor de pruebas (Test Runner) para:
    * Gestionar la carga de datos de prueba de forma eficiente usando una *fixture* (`@pytest.fixture`).
    * Definir cada regla de negocio como una función de prueba (`test_...`) independiente.
    * Usar `assert` para fallar automáticamente la prueba y detener un pipeline de CI/CD si la calidad de los datos no se cumple.
    * Generar un reporte de ejecución legible en la consola.

---

## 💻 Tecnologías Utilizadas

* **Python 3.x**
* **Pandas** (Para la manipulación y análisis de datos)
* **Pytest** (Para el framework de automatización y aserciones)
* **SQL** (Para el diseño de la lógica de auditoría)
* **Jupyter Notebook** (Usado como entorno de desarrollo y exploración)

---

## 🚀 Cómo Ejecutar este Proyecto

Para replicar los resultados y ejecutar el framework de pruebas automatizadas:

1.  **Clonar el repositorio:**
  
    ```bash
    git clone [https://github.com/avhardcore03-cpu/data-quality-etl-test.git](https://github.com/avhardcore03-cpu/data-quality-etl-test.git)
    cd data-quality-etl-test
    ```

2.  **(Opcional pero recomendado) Crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Mac/Linux
    .\venv\Scripts\activate   # En Windows
    ```

3.  **Instalar las dependencias:**
    *(Se incluye un archivo requirements.txt con las librerías necesarias).*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el Framework de Pruebas:**
    Invoca a `pytest` desde tu terminal. El flag `-v` (verbose) mostrará un reporte detallado.
    ```bash
    pytest -v
    ```

5.  **Ver el Reporte:**
    La consola mostrará la salida de Pytest, indicando qué pruebas pasaron (PASSED) y cuáles fallaron (FAILED), junto con el detalle de los datos que causaron el error.

---

## 📁 Archivos del Repositorio

* test_data_quality_suite.py: El framework de automatización con Pytest.
*Sustentacion_Prueba_Tecnica_QA.ipynb: El Notebook de Jupyter con la exploración y ejecución.
*README.md: Este archivo.
*requirements.txt: Las librerías de Python necesarias.
*.gitignore: Archivo para excluir archivos de caché de Python y Jupyter.
*Prueba_Tecnica_Data_Quality_ETL_Tester.pdf: El PDF original del desafío.
