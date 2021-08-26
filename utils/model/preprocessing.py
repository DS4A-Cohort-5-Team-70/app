import pickle
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MaxAbsScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import classification_report, precision_recall_curve, roc_auc_score, roc_curve, plot_confusion_matrix, accuracy_score


randomState = 42


def load_data() -> pd.DataFrame:
    """

    @return:
    """
    df = pd.DataFrame()
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """

    @param df:
    @return:
    """
    df_unique = df.copy()
    scaler = MaxAbsScaler()
    df_scaled_ = df_unique.drop(['Fecha_retiro'], axis=1)
    df_scaled = pd.DataFrame(scaler.fit_transform(df_scaled_.values), columns=df_scaled_.columns,
                             index=df_scaled_.index)
    df_scaled['Target'] = df_unique['Fecha_retiro']
    X = df_scaled.drop(['Target'], axis=1)
    y = df_scaled['Target']

    oversample = SMOTE()
    X, y = oversample.fit_resample(X, y)
    df = X
    df['Target'] = y
    #TODO: Implement dump_data "transformed dataset"
    return df


def training(df: pd.DataFrame) -> dict:
    """

    @param df:
    @return:
    """
    metrics_dict = {}
    df_training = df.copy()

    X = df_training.drop(['Target'], axis=1)
    y = df_training['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=randomState,shuffle=True)
    clf = RandomForestClassifier(random_state=randomState, n_jobs=-1, verbose=1)
    clf.fit(X_train, y_train)

    # Metrics Before Optimize
    metrics_dict['Default'] = metrics(clf, X_train, X_test, y_train, y_test)

    # Metrics After Optimize
    params = optimize(clf, X_train, X_test, y_train, y_test)
    clf = RandomForestClassifier(**params)
    clf.fit(X_train, y_train)
    metrics_dict['Optimized'] = metrics(clf, X_train, X_test, y_train, y_test)

    return metrics_dict


def metrics(clf: RandomForestClassifier, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> dict:
    """

    @param clf:
    @param X_train:
    @param X_test:
    @param y_train:
    @param y_test:
    @return:
    """
    metrics_dict = {}
    y_pred = clf.predict(X_train)
    y_scores = cross_val_predict(clf, X_train, y_train, cv=5, method="predict_proba")[:, 1]
    precisions, recalls, thresholds_PR = precision_recall_curve(y_train, y_scores)
    fpr, tpr, thresholds_ROC = roc_curve(y_train, y_scores)

    metrics_dict['Train'] = {
        'Recalls': recalls,
        'Precisions': precisions,
        'True Positive Rate': tpr,
        'False Positive Rate': fpr,
        'Thresholds PR': thresholds_PR,
        'Thresholds ROC': thresholds_ROC,
        'ROC AUC': roc_auc_score(y_train, y_scores),
        'Accuracy': accuracy_score(y_train, y_pred),
        'Classification Report': pd.DataFrame(classification_report(y_train, y_scores, output_dict=True)).transpose()
    }

    y_pred = clf.predict(X_test)
    y_scores = cross_val_predict(clf, X_test, y_test, cv=5, method="predict_proba")[:, 1]
    precisions, recalls, thresholds_PR = precision_recall_curve(y_test, y_scores)
    fpr, tpr, thresholds_ROC = roc_curve(y_test, y_scores)
    metrics_dict['Test'] = {
        'Recalls': recalls,
        'Precisions': precisions,
        'True Positive Rate': tpr,
        'False Positive Rate': fpr,
        'Thresholds PR': thresholds_PR,
        'Thresholds ROC': thresholds_ROC,
        'ROC AUC': roc_auc_score(y_test, y_scores),
        'Accuracy': accuracy_score(y_test, y_pred),
        'Classification Report': pd.DataFrame(classification_report(y_test, y_scores, output_dict=True)).transpose()
    }

    return metrics_dict


def optimize(clf: RandomForestClassifier, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> dict:
    """
    Uses Bayes Search CV to optimize hyperparameters.
    @param clf: A classifier
    @param X_train:
    @param X_test:
    @param y_train:
    @param y_test:
    @return: A dict which contains best hyperparameters.
    """
    params = {}

    return params


def inference() -> pd.DataFrame():
    df = pd.DataFrame()
    return df


def dump_model(clf: RandomForestClassifier, dir_filename) -> None:
    pickle.dumps()


def dump_predictions() -> pd.DataFrame:
    df = pd.DataFrame()
    return df
