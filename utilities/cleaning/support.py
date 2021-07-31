import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


def classify_ids_no_always(d, ids):
    ids_inconsistentes = []
    ids_retiro_def = [] # No regresaron a la empresa
    ids_regresaron = []
    for ID in ids:
        tmp = d[["Fecha_Ingreso_Operacion", "Fecha_retiro"]]        [d["IdFuncionario"]==ID].dropna(subset=["Fecha_retiro"]).sort_values(by=["Fecha_Ingreso_Operacion","Fecha_retiro"])
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

    


def completar_fechas(d, col):
    dates = [d[col].min(), d[col].max()]

    cur_date = dates[0]

    fechas = []

    while cur_date < dates[1]:
        fechas.append(cur_date)
        cur_date += relativedelta(months=1)
    
    completo = pd.DataFrame(data = fechas).rename(columns={0:col})
    completo = completo.join(d.set_index(col), on=col).rename(columns={0:"value"})
    completo["value"] = np.where(completo["value"].isnull()==True, 0, completo["value"])
    
    return completo