import graphviz
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt

from sklearn import tree
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.preprocessing import MaxAbsScaler, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_predict, ShuffleSplit
from sklearn.metrics import classification_report, precision_recall_curve, roc_auc_score, roc_curve, plot_confusion_matrix, accuracy_score

from skopt import BayesSearchCV
from imblearn.over_sampling import SMOTE
from skopt.space import Real, Categorical, Integer
# Lee de ingestion
def load_data() -> pd.DataFrame:
    # TODO: CAMBIAR POR AWS
    df = pd.read_csv('./data/data/ingestion/asesor.csv', parse_dates=['Fecha_Ingreso_Operacion', 'Fecha_retiro', 'FechaNacimiento'],encoding='Latin1')
    df.sort_values(by=['Cosecha_Ingreso_Operacion', 'IdFuncionario', 'Cosecha_Liquidacion'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def preprocessing(df) -> pd.DataFrame:
    # Standarization
    df[["Cosecha_Ingreso_Operacion", "Cosecha_Liquidacion"]] = df[["Cosecha_Ingreso_Operacion", "Cosecha_Liquidacion"]].apply(lambda x: pd.to_datetime(x, format='%Y%m'))

    # Creation of target variable
    df['Renuncio'] = df['Fecha_retiro'].fillna(0)
    df['Renuncio'] = df['Renuncio'].apply(lambda x: 0 if x == 0 else 1)

    # Age calculation
    df['Fecha_retiro'].fillna(np.datetime64('today'), inplace=True)
    df['Edad'] = df['Fecha_retiro'].dt.year - df['FechaNacimiento'].dt.year
    df.drop(labels=['Fecha_retiro'], axis=1, inplace=True)

    # Cleaning based on age oldies and freshers
    df = df[(df['Edad'] < 100) & (df['Edad'] >= 18)]
    df.drop(['FechaNacimiento'], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def impute_cols(df: pd.DataFrame) -> pd.DataFrame:
    # Following values can be filled with zeroes
    cols_to_fill = ['CantidadHijos', 'Meta_Recaudo', 'Cumpl_Individual', 'Dias_Asistencia', 'TiempoConectado',
                    'TiempoProductivo', 'TiempoUtil']
    for i in cols_to_fill:
        df[i].fillna(0, inplace=True)

    df[cols_to_fill] = df[cols_to_fill].apply(lambda x: abs(x))
    df['Ausentismo'].fillna(df['Ausentismo'].median(), inplace=True)
    df['Dias_habiles_Mes'].fillna(df['Dias_habiles_Mes'].mean(), inplace=True)

    # Columns with less than 60% of Nulls will be kept
    df = df.loc[:, df.isin([np.nan]).mean() < .6]

    # Following Columns will not add any value to subsequent steps, based on chi2 analysis and correlated columns
    df.drop(axis=1, inplace=True, labels=['Cargo_Generico', 'UCN', 'UCP', 'Fecha_Ingreso_Operacion',
                                          'Cosecha_Ingreso_Operacion', 'Ausentismo', 'Recaudo_Total',
                                          'Cumpl_Individual', 'TiempoConectado', 'TiempoProductivo'])

    return df


def feature_eng(df: pd.DataFrame) -> pd.DataFrame:
    # Calculated Columns
    df['%_Asistencia_Mes'] = df['Dias_Asistencia'] / df['Dias_habiles_Mes']
    df.drop(['Dias_Asistencia', 'Dias_habiles_Mes'], axis=1, inplace=True)
    df.sort_values(by=['IdFuncionario', 'Cosecha_Liquidacion'], inplace=True)

    df.drop(['Canal', 'Segmento', 'LineaNegocio'], axis=1, inplace=True)
    df.sort_values(by=['IdFuncionario', 'Cosecha_Liquidacion'], inplace=True)
    
    df.reset_index(drop=True, inplace=True)

    return df


# Sube a la tabla process
def dump_data(df: pd.DataFrame, path_filename: str) -> None:
    df.to_parquet(f'{path_filename}')
