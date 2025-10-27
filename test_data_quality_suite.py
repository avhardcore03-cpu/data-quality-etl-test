import pandas as pd
import numpy as np
import pytest

# ----------------------------------------------------------------------
# FASE 1: CONFIGURACIÓN principal (LA "FIXTURE" DE PYTEST)
# ----------------------------------------------------------------------

@pytest.fixture(scope="module")
def data_loader():
    print("\nCargando datos de prueba en DataFrames...")
    
    # --- Carga de 'customers_raw' ---
    customers_data = {
        'customer_id': [1, 2, 3, 4, 5],
        'name': ['Ana Torres', 'Juan Pérez', 'Laura Gómez', 'Juan Pérez', np.nan],
        'email': ['ana@email.com', np.nan, 'laura_gomez@email.com', 'juanperez@email.com', 'andres@email.com'],
        'country': ['Colombia', 'Mexico', np.nan, 'Mexico', 'Chile']
    }
    customers_raw_df = pd.DataFrame(customers_data)

    # --- Carga de 'transactions_raw' ---
    transactions_data = {
        'transaction_id': [100, 101, 102, 103, 104],
        'customer_id': [1, 2, 2, 3, 6], # El '6' es el huérfano
        'amount': [200.0, 150.0, 150.0, np.nan, 300.0],
        'date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-02', '2025-01-03', '2025-01-04'])
    }
    transactions_raw_df = pd.DataFrame(transactions_data)

    # --- Carga de 'transactions_clean' (Simulada con errores) ---
    transactions_clean_data = {
        'transaction_id': [100, 101, 102, 105],
        'amount': [200.0, 150.0, 140.0, 50.0], # Error: 140.0
        'country': ['Colombia', 'Mexico', 'Mexico', 'Argentina'] # Error: Argentina
    }
    transactions_clean_df = pd.DataFrame(transactions_clean_data)
    
    # Retornamos los datos como un diccionario para que los tests los usen
    return {
        "customers": customers_raw_df,
        "transactions": transactions_raw_df,
        "transactions_clean": transactions_clean_df
    }

# ----------------------------------------------------------------------
# FASE 2: IMPLEMENTACIÓN DE LOS TESTS (REGLAS DE LA PARTE 1)
# ----------------------------------------------------------------------

def test_1_completitud(data_loader):
    """
    Test 1: Valida que los campos obligatorios no tengan NULOS.
    """
    df = data_loader["customers"]
    df_trans = data_loader["transactions"]
    
    campos_obligatorios_cust = ['name', 'email', 'country']
    errores_completitud_cust = df[campos_obligatorios_cust].isnull().sum()
    errores_completitud_cust = errores_completitud_cust[errores_completitud_cust > 0]

    campos_obligatorios_trans = ['amount']
    errores_completitud_trans = df_trans[campos_obligatorios_trans].isnull().sum()
    errores_completitud_trans = errores_completitud_trans[errores_completitud_trans > 0]

    assert errores_completitud_cust.empty, f"Se encontraron NULOS en 'customers_raw': \n{errores_completitud_cust}"
    assert errores_completitud_trans.empty, f"Se encontraron NULOS en 'transactions_raw': \n{errores_completitud_trans}"


def test_2_unicidad_email(data_loader):
    """
    Test 2: Valida que no existan emails duplicados.
    """
    df = data_loader["customers"]
    
    df_sin_nulos = df.dropna(subset=['email'])
    filas_duplicadas = df_sin_nulos[df_sin_nulos.duplicated(subset=['email'], keep=False)]
    
    assert filas_duplicadas.empty, f"Se encontraron {len(filas_duplicadas)} emails duplicados. \n{filas_duplicadas['email']}"


def test_3_integridad_referencial(data_loader):
    """
    Test 3: Valida que no existan transacciones huérfanas.
    """
    df_trans = data_loader["transactions"]
    df_cust = data_loader["customers"]
    
    merged_df = pd.merge(
        df_trans,
        df_cust,
        on='customer_id',
        how='left',
        indicator=True
    )
    registros_huerfanos = merged_df[merged_df['_merge'] == 'left_only']
    
    assert registros_huerfanos.empty, f"Se encontraron {len(registros_huerfanos)} transacciones huérfanas: \n{registros_huerfanos['transaction_id']}"


def test_4_reconciliacion_totales(data_loader):
    """
    Test 4 (Extra): Valida la reconciliación de totales por país.
    """
    df_trans = data_loader["transactions"]
    df_cust = data_loader["customers"]
    df_clean = data_loader["transactions_clean"]

    # Fase 1: Totales Origen
    origen_merged = pd.merge(df_trans, df_cust, on='customer_id')
    origen_filtrado = origen_merged.dropna(subset=['amount', 'country'])
    totales_origen = origen_filtrado.groupby('country')['amount'].sum().reset_index()
    totales_origen = totales_origen.rename(columns={'amount': 'total_origen'})
    
    # Fase 2: Totales Destino
    totales_destino = df_clean.groupby('country')['amount'].sum().reset_index()
    totales_destino = totales_destino.rename(columns={'amount': 'total_destino'})
    
    # Fase 3: Comparación
    reporte_final = pd.merge(totales_origen, totales_destino, on='country', how='outer')
    reporte_final = reporte_final.fillna(0)
    reporte_final['diferencia'] = reporte_final['total_origen'] - reporte_final['total_destino']
    errores_reconciliacion = reporte_final[reporte_final['diferencia'] != 0]

    assert errores_reconciliacion.empty, f"Se encontraron discrepancias en la reconciliación: \n{errores_reconciliacion}"
    
