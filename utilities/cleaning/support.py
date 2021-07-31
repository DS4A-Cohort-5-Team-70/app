import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


def classify_ids_no_always(df, ids):
    """
    Input:
        df  - Dataframe
        ids - IDs a filtrar
    Output:
        Listas de IDs: ids_inconsistentes, ids_retiro_def, ids_regresaron.
        ids_inconsistentes contiene los IDs donde se encontró inconsistencias con fecha de ingreso o retiro
        ids_retiro_def contiene ID's de retirados de la compañía
        ids_regresaron contiene ID's de reingresados y trabajando actualmente en la compañía.
    """
    ids_inconsistentes = []
    ids_retiro_def = [] # No regresaron a la empresa
    ids_regresaron = []
    for ID in ids:
        tmp = df[["Fecha_Ingreso_Operacion", "Fecha_retiro"]][df["IdFuncionario"]==ID].dropna(subset=["Fecha_retiro"]).sort_values(by=["Fecha_Ingreso_Operacion","Fecha_retiro"])
        num_fechas_ingreso = tmp["Fecha_Ingreso_Operacion"].nunique() 
        num_fechas_retiro = tmp["Fecha_retiro"].nunique()
        if num_fechas_ingreso < num_fechas_retiro:
            ids_inconsistentes.append(ID)
        elif num_fechas_ingreso == num_fechas_retiro:
            if len(tmp[tmp["Fecha_Ingreso_Operacion"]<tmp["Fecha_retiro"]])<num_fechas_ingreso:
                ids_inconsistentes.append(ID)
            else:
                ids_retiro_def.append(ID)
        else:
            ids_regresaron.append(ID)
    return ids_inconsistentes, ids_retiro_def, ids_regresaron

    


def completar_fechas(df, col):
    """
    Input:
        df  - Dataframe de dos columnas: col | values
        col - Nombre de columna que representa meses. Ej: Cosecha_Ingreso_Operacion
    Output:
        Dataframe de dos columnas: col | values. Tiene filas agregadas donde no exista el mes en el dataframe de entrada.
    """
    dates = [df[col].min(), df[col].max()]

    cur_date = dates[0]

    fechas = []

    while cur_date < dates[1]:
        fechas.append(cur_date)
        cur_date += relativedelta(months=1)
    
    completo = pd.DataFrame(data = fechas).rename(columns={0:col})
    completo = completo.join(df.set_index(col), on=col).rename(columns={0:"value"})
    completo["value"] = np.where(completo["value"].isnull()==True, 0, completo["value"])
    
    return completo

def swap_day_month(IDs, df):
    """
    Input: 
        IDs - Lista de IDs
        df  - Dataframe
    Output:
        Cambia dia y mes en la fecha de retiro de los agentes contenidos en IDs
    """
    dates = df["Fecha_retiro"][df.IdFuncionario.isin(IDs)].dropna().\
    apply(lambda d: pd.to_datetime(str(d.year)+"-"+str(d.day)+"-"+str(d.month), format="%Y-%m-%d"))
    df.loc[dates.index, 'Fecha_retiro'] = dates
    return df