import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MaxAbsScaler
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import classification_report, precision_recall_curve, roc_auc_score, roc_curve, plot_confusion_matrix, accuracy_score

from skopt import BayesSearchCV
from imblearn.over_sampling import SMOTE
from skopt.space import Categorical, Integer

randomState = 42


def load_data() -> pd.DataFrame:
    """

    @return:
    """
    df = pd.read_parquet('./data/data/process/df_clean.parquet')
    df.drop(['IdFuncionario', 'Cosecha_Liquidacion'], axis=1, inplace=True)

    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=randomState, shuffle=True)

    params = optimize(DecisionTreeClassifier(), X_train, X_test, y_train, y_test, False)
    clf = DecisionTreeClassifier(**params)
    clf.fit(X, y)

    # Dumps model
    with open('./data/model/model/trained_model.pickle', 'wb') as f:
        pickle.dump(clf, f, pickle.HIGHEST_PROTOCOL)

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
    df_metrics = pd.DataFrame()

    # Preds
    y_pred = clf.predict(X)
    y_scores = cross_val_predict(clf, X, y, cv=3, method="predict_proba")[:, 1]

    # Classification Report
    clf_report = pd.DataFrame(classification_report(y, y_pred, output_dict=True)).transpose()
    clf_report.to_parquet('./data/model/metrics/clf_report.parquet')

    # Accuracy
    df_metrics['Accuracy'] = round(accuracy_score(y, y_pred), 3)
    # ROC AUC
    df_metrics['ROC - AUC'] = round(roc_auc_score(y, y_scores), 3)
    df_metrics.to_parquet('./data/model/metrics/basic_metrics.parquet')

    # Precision - Recall
    df_metrics = pd.DataFrame()
    df_metrics['Precisions'], df_metrics['Recalls'], _ = precision_recall_curve(y, y_scores)
    df_metrics.to_parquet('./data/model/metrics/precision_recall.parquet')

    # ROC
    df_metrics = pd.DataFrame()
    df_metrics['False Positive Rate'], df_metrics['True Positive Rate'], df_metrics['Thresholds'] = roc_curve(y, y_scores)
    df_metrics.to_parquet('./data/model/metrics/ROC.parquet')

    # Feature Importance
    df_metrics = pd.DataFrame()
    df_metrics['Feature'] = list(X.columns)
    df_metrics['Feature'] = list(clf.feature_importances_)
    df_metrics.to_parquet('./data/model/metrics/Feature Importance.parquet')


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

    # Df to store predictions
    df_preds = df[['IdFuncionario', 'Cosecha_Liquidacion']]
    df_preds['Cosecha_Liquidacion'] = max_date + pd.DateOffset(months=1)
    df.drop(['Renuncio', 'IdFuncionario', 'Cosecha_Liquidacion'], axis=1, inplace=True)

    with open('./data/model/model/trained_model.pickle', 'rb') as f:
        clf = pickle.load(f)

    # Carry out inference
    df_preds['Probability'] = clf.predict_proba(df)[:, 1]
    df_preds.to_parquet('./data/data/serving/df_preds.parquet')
