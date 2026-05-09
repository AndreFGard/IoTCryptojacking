import numpy as np
import tsfresh
import pandas as pd
import sklearn

def ML_Process(df_ML,x):
    """Train and evaluate ML models using extracted features.

    Parameters:
        df_ML (pandas.DataFrame): Feature matrix containing a 'class' target column.
        x (pandas.DataFrame): DataFrame used as a template for collecting results.

    Returns:
        pandas.DataFrame: Cross-validation metrics for the evaluated model(s).
    """
    df_results = x.copy() 
    print('let the ml starts')
  
    from sklearn import neighbors, metrics
    from sklearn.preprocessing import LabelEncoder

    #X = df_finalized[['Time', 'Length','Protocol']].values
    X = df_ML.drop('class',axis=1).to_numpy()
    #y = df_finalized[['Is_malicious']]
    y = df_ML['class'].to_numpy()



    #print(X,y)
    
    from sklearn.model_selection import train_test_split
    Le = LabelEncoder()
    for i in range(len(X[0])):
        X[:, i] = Le.fit_transform(X[:, i])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=8675309)

    
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import GaussianNB
    #from xgboost import XGBClassifier
    from sklearn import model_selection
    from sklearn.utils import class_weight
    from sklearn.metrics import classification_report
    from sklearn.metrics import confusion_matrix
    import numpy as np
    import pandas as pd
    y_train = y_train.ravel()
    dfs = []
    models = [
          #('LogReg', LogisticRegression()), 
          #('RF', RandomForestClassifier()),
          #('KNN', KNeighborsClassifier()),
          ('SVM', SVC())#, 
          #('GNB', GaussianNB())
          #('XGB', XGBClassifier())
            ]
    results = []
    names = []
    scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
    target_names = ['malignant', 'benign']
    for name, model in models:
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=90210)
        cv_results = model_selection.cross_validate(model, X_train, y_train, cv=kfold, 
                                                    scoring=scoring)

        clf = model.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        print(name)
        print(classification_report(y_test, y_pred, target_names=target_names))
        results.append(cv_results)
        names.append(name)
        this_df = pd.DataFrame(cv_results)
        this_df['model'] = name
        dfs.append(this_df)
        df_resulta = df_results.append(dfs)
        final = pd.concat(dfs, ignore_index=True)
        print(final)


    return(final)


def run_process(a,b,x):
    """Run feature extraction, feature selection, and model evaluation pipeline.

    Parameters:
        a (pandas.DataFrame): Malicious traffic dataset.
        b (pandas.DataFrame): Benign traffic dataset.
        x (pandas.DataFrame): DataFrame used to initialize/accumulate output metrics.

    Returns:
        pandas.DataFrame: Final model evaluation results returned by ML_Process.
    """
    
    df_malicious = a.copy()
    df_benign    = b.copy()
    
    from tsfresh import extract_features, select_features
    from tsfresh.utilities.dataframe_functions import impute
    from tsfresh import extract_features
    from tsfresh.feature_selection.relevance import calculate_relevance_table


    df_malicious.reset_index(drop=True, inplace=True) #reset index
    df_malicious['id']= np.floor(df_malicious.index.array/10)
    df_benign.reset_index(drop=True, inplace=True) #reset index
    df_benign['id']= np.floor(df_benign.index.array/10)
    

    tf1=tsfresh.extract_features(df_malicious,impute_function=impute, column_kind='Is_malicious',
                                 column_id='id',column_sort="Time",column_value = "Length")
    tf1['class']= 1


    
    
    tf2=tsfresh.extract_features(df_benign,impute_function=impute, column_kind='Is_malicious',
                                 column_id='id',column_sort="Time",column_value = "Length")
    tf2['class']= 0


    tf2.columns = tf1.columns

    features=pd.concat([tf1,tf2])
    #features.reset_index(drop=True, inplace=True) #reset index
    
#   best_features = pd.read_csv('/home/ege/Desktop/Mining_data/mining/new_captures/features_final.csv')

    features2 = features.copy()
    features2.reset_index(drop=True, inplace=True)
    
    y = pd.Series(data = features2['class'], index=features2.index)
    
    from tsfresh.examples import load_robot_execution_failures
    from tsfresh import extract_features, select_features
    from tsfresh.feature_selection.relevance import calculate_relevance_table

    relevance_table = calculate_relevance_table(features2, y)
    relevance_table = relevance_table[relevance_table.relevant]
    relevance_table.sort_values("p_value", inplace=True)

    relevance_table
    
    best_features = relevance_table[relevance_table['p_value'] <= 0.05]

    df_ML = pd.DataFrame()

    for pkt in best_features:
        df_ML[best_features.feature] = features[best_features.feature]

    final = ML_Process(df_ML,x)
    

    return final

