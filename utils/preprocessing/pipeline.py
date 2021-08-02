


import numpy as np
import pandas as pd
import datetime as dt
from sklearn.preprocessing import MaxAbsScaler, StandardScaler

from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import classification_report, precision_recall_curve, roc_auc_score, roc_curve, plot_confusion_matrix, accuracy_score

from support import swap_day_month
# Lee de ingestion
def load_data() -> pd.DataFrame:
    # TODO: CAMBIAR POR AWS
    df = pd.read_csv('./data/asesor.csv', parse_dates=['Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'],
                     encoding='Latin1')
    return df


def preprocessing(df) -> pd.DataFrame:
    data_raw = df.copy()
    # Fijar formato datetime en Cosecha_Liquidacion y Cosecha_Ingreso_Operacion
    data_raw["Cosecha_Ingreso_Operacion"] = pd.to_datetime(data_raw["Cosecha_Ingreso_Operacion"], format='%Y%m')
    data_raw["Cosecha_Liquidacion"] = pd.to_datetime(data_raw["Cosecha_Liquidacion"], format='%Y%m')

    # DONE: 9801, 13554 sólo tiene un registro y sus fechas de ingreso no tienen sentido. Eliminar.
    # TODO: automatizar con una lógica que permita hacerlo sin hard-code
    data_raw.drop(index=[9801, 13554], inplace=True)

    # DONE: ID's: 10247, 10287, 10366, 10453, 11648, 11717, 11720, 11722, 11925 Swap día-mes
    # TODO: automatizar con una lógica que permita hacerlo sin hard-code
    IDs_for_swapping = [10247, 10287, 10366, 10453, 11648, 11717, 11720, 11722, 11925]
    data_raw = swap_day_month(IDs_for_swapping, data_raw)

    # TODO: ID's: 9356, 10102, 10431, 11928, 13430 imputarlos. Otra fecha ingreso con sentido.
    # TODO: automatizar con una lógica que permita hacerlo sin hard-code
    # Columna edad calculada a principio de cada mes
    # TODO: Si el agente se retira en ese mes, calcular la edad respecto a fecha retiro y no respecto a Cosecha_Liquidacion
    data_raw["Edad"] = ((data_raw['Cosecha_Liquidacion'].dt.date - data_raw["FechaNacimiento"].dt.date) / np.timedelta64(1,'Y')).astype(
        int)

    # Se quitan los registros de funcionarios cuya fecha de nacimiento no tiene sentido (edades como -1, 1 ó 6)
    # TODO: automatizar con una lógica que permita hacerlo sin hard-code
    data_raw.drop(index=[4458, 7927, 12792], inplace=True)

    # Registros con cantidad de hijos=-1 se cambia a 1 porque columna Hijos tiene valor SI para esos agentes.
    # TODO: automatizar con una lógica que permita hacerlo sin hard-code
    data_raw.at[[10184, 13768, 13966], 'CantidadHijos'] = 1

    # TODO: Id funcionario a categórica


    # Alejandro - Pipe
    df = data_raw.copy()

    df.sort_values(by=['IDFuncionario', 'Fecha_retiro'], inplace=True)
    df_unique = df[df.duplicated(subset=['IDFuncionario'], keep='last')]
    df_unique.reset_index(drop=True, inplace=True)
    kept_cols = ['Vr_Comision', 'Meta_Recaudo', 'Recaudo_Total', 'Cumpl_Individual', 'edad', 'Fecha_retiro']
    df_unique = df_unique[kept_cols]
    df_unique = df_unique.fillna(0)
    df_unique['Fecha_retiro'] = df_unique['Fecha_retiro'].apply(lambda x: 0 if x == 0 else 1)

    return df_unique


# Sube a la tabla process
def dump_data(df):
    df.to_parquet('./data/df_clean.parquet')
