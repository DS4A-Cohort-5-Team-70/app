import pickle
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MaxAbsScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import classification_report, precision_recall_curve, roc_auc_score, roc_curve, \
    plot_confusion_matrix, accuracy_score
from sklearn.model_selection import learning_curve

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
from sklearn.metrics import classification_report, precision_recall_curve, roc_auc_score, roc_curve, \
    plot_confusion_matrix, accuracy_score

from skopt import BayesSearchCV
from imblearn.over_sampling import SMOTE
from skopt.space import Real, Categorical, Integer

randomState = 42


def load_data() -> pd.DataFrame:
    """

    @return:
    """
    df = pd.read_parquet('./data/data/process/df_clean.parquet')
    df.drop(['IdFuncionario', 'Cosecha_Liquidacion'], axis=1, inplace=True)

    return df


def scale_df(df: pd.DataFrame) -> pd.DataFrame:
    """

    @param df:
    @return:
    """
    scaler = MaxAbsScaler()
    df = pd.DataFrame(scaler.fit_transform(df.values), columns=df.columns, index=df.index)

    return df


def training(df: pd.DataFrame) -> None:
    """

    @param df:
    @return:
    """
    X = df.drop(['Renuncio'], axis=1)
    y = df['Renuncio']

    oversample = SMOTE()
    X, y = oversample.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=randomState,
                                                        shuffle=True)

    params = optimize(DecisionTreeClassifier(), X_train, X_test, y_train, y_test, False)
    clf = DecisionTreeClassifier(**params)
    clf.fit(X, y)

    # Dumps model
    with open('./data/model/model/trained_model.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        data = pickle.load(f)

    # Gets metrics
    metrics(clf, X, y)


def metrics(clf: DecisionTreeClassifier, X: pd.DataFrame, y: pd.Series) -> None:
    """

    @param clf:
    @param X:
    @param y:
    @return:
    """

    # TODO: dump metrics in dataframes

    # Learning curve
    df_learning = pd.DataFrame()
    cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=randomState)
    df_learning['train_sizes'], df_learning['train_scores'], df_learning['test_scores'], df_learning['fit_times'], _ = learning_curve(clf, X, y, cv=cv, n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 5), return_times=True)

    # Accuracy
    y_pred = clf.predict(X)



def optimize(clf: DecisionTreeClassifier, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series,
             y_test: pd.Series, opt: bool = True) -> dict:
    """
    Uses Bayes Search CV to optimize hyperparameters.
    @param clf: A classifier
    @param X_train:
    @param X_test:
    @param y_train:
    @param y_test:
    @return: A dict which contains best hyperparameters.
    """

    if opt:
        bayes_optimizer = BayesSearchCV(
            estimator=clf,
            search_spaces={
                'max_depth': Integer(8, 32),
                'min_samples_leaf': Integer(1, 7),
                'criterion': ['gini', 'entropy'],
                'min_samples_split': Integer(2, 8),
                'max_features': Categorical(['auto', 'sqrt', 'log2', None]),
                'random_state': randomState
            },
            n_iter=32,
            n_points=1,
            random_state=randomState,
            verbose=1,
            n_jobs=-1)
        _ = bayes_optimizer.fit(X_train, y_train)
        params = bayes_optimizer.best_params_
    else:
        params = {
            'ccp_alpha': 0.0,
            'class_weight': None,
            'criterion': 'gini',
            'max_depth': 22,
            'max_features': None,
            'max_leaf_nodes': None,
            'min_impurity_decrease': 0.0,
            'min_impurity_split': None,
            'min_samples_leaf': 1,
            'min_samples_split': 2,
            'min_weight_fraction_leaf': 0.0,
            'presort': 'deprecated',
            'random_state': 42,
            'splitter': 'best'
        }

    return params


def inference() -> None:
    df = pd.read_parquet('./data/data/process/df_clean.parquet')
    max_date = df['Cosecha_Liquidacion'].max()
    df = df[df['Cosecha_Liquidacion'].isin([max_date])]
    df = df[df['Renuncio'].isin([0])]
    df.drop(['Renuncio'],axis=1, inplace=True)

    # Load model
    clf = {}
    # carry out inference
    preds = clf.predict(df)

    preds.to_parquet('./data/data/serving/')


def dump_model(clf: DecisionTreeClassifier, path_filename: str) -> None:
    pickle.dumps()


def dump_predictions(df: pd.DataFrame) -> None:
    df = pd.DataFrame()
