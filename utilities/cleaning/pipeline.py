import pandas as pd
import numpy as np
from datetime import datetime

# Lee de ingestion
def load_data():
    # TODO: CAMBIAR POR AWS
    return pd.read_csv('./data/asesor.csv',\
    parse_dates=['Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'], encoding='Latin1')

def preprocessing(df_):
    #TODO: Es necesario hacer una copia del dataframe df_?
    data_raw = df_.copy()
    # Fijar formato datetime en Cosecha_Liquidacion y Cosecha_Ingreso_Operacion
    data_raw["Cosecha_Ingreso_Operacion"] = pd.to_datetime(data_raw["Cosecha_Ingreso_Operacion"], format='%Y%m')
    data_raw["Cosecha_Liquidacion"] = pd.to_datetime(data_raw["Cosecha_Liquidacion"], format='%Y%m')

    #TODO: 9801, 13554 sólo tiene un registro. Eliminar.
    #TODO: ID's: 10247, 10287, 10366, 10453, 11648, 11717, 11720, 11722, 11925 Swap día-mes
    #TODO: ID's: 9356, 10102, 10431, 11928, 13430 imputarlos. Otra fecha ingreso con sentido.

    # Columna edad calculada a principio de cada mes
    #TODO: Si el agente se retira en ese mes, calcular la edad respecto a fecha retiro y no respecto a Cosecha_Liquidacion
    data_raw["Edad"] = ((data_raw['Cosecha_Liquidacion'].dt.date-data_raw["FechaNacimiento"].dt.date)/np.timedelta64(1, 'Y')).astype(int)

    # Se quitan los registros de funcionarios cuya fecha de nacimiento no tiene sentido (edades como -1, 1 ó 6)
    #TODO: Preguntarle a Refinancia sobre esos registros para hacer una imputación y no tener que eliminarlos.
    data_raw.drop(index=[4458, 7927, 12792], inplace=True)

    # Registros con cantidad de hijos=-1 se cambia a 1 porque columna Hijos tiene valor SI para esos agentes.
    #TODO: Preguntarle a Refinancia sobre esos registros
    data_raw.at[[10184, 13768, 13966],'CantidadHijos'] = 1




# Sube a la tabla proces
def dump_data(df):
    df.to_parquet('./data/asesor.parquet')