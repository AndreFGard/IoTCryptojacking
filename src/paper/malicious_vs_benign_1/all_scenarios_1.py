#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import tsfresh
import os
import json
import scapy
import numpy as np
import warnings
from timeit import default_timer as timer

from scapy.all import *

warnings.filterwarnings("ignore") #ignore warnings caused by 


#################################################################
#                                                               #
#               malicious csv files import                      #
#                                                               #
#################################################################


df1 = pd.read_csv('./Data/malicious/WebOS_binary.csv') #
df2 = pd.read_csv('./Data/malicious/Server_Binary.csv') #
df3 = pd.read_csv('./Data/malicious/Raspberry_Webmine_Robust.csv')
df4 = pd.read_csv('./Data/malicious/Raspberry_Binary.csv') #
df5 = pd.read_csv('./Data/malicious/Raspberry_Webmine_Aggressive.csv')
df6 = pd.read_csv('./Data/malicious/Raspberry_WebminePool_Aggressive.csv')
df7 = pd.read_csv('./Data/malicious/Server_WebminePool_Aggressive.csv') #
df32 = pd.read_csv('./Data/malicious/Server_WebminePool_Robust.csv') #
df33 = pd.read_csv('./Data/malicious/Raspberry_WebminePool_Stealthy.csv') #
df34 = pd.read_csv('./Data/malicious/Raspberry_WebminePool_Robust.csv') #
df35 = pd.read_csv('./Data/malicious/Desktop_WebminePool_Aggressive.csv') #


#################################################################
#                                                               #
#               benign-1 csv files import                         #
#                                                               #
#################################################################

df8 = pd.read_csv('./Data/benign-1/interactive_01.csv') #
df9 = pd.read_csv('./Data/benign-1/interactive_02.csv') #
df10 = pd.read_csv('./Data/benign-1/interactive_03.csv') #
df11 = pd.read_csv('./Data/benign-1/interactive_04.csv') #
df12 = pd.read_csv('./Data/benign-1/interactive_05.csv') #
df13 = pd.read_csv('./Data/benign-1/interactive_06.csv') #
df14 = pd.read_csv('./Data/benign-1/web_1page_01.csv') #
df15 = pd.read_csv('./Data/benign-1/web_1page_02.csv') #
df16 = pd.read_csv('./Data/benign-1/web_1page_03.csv') #
df17 = pd.read_csv('./Data/benign-1/web_1page_04.csv') #
df18 = pd.read_csv('./Data/benign-1/web_1page_05.csv') #
df19 = pd.read_csv('./Data/benign-1/bulk_xs_04.csv') #
df20 = pd.read_csv('./Data/benign-1/bulk_xs_05.csv') #
df21 = pd.read_csv('./Data/benign-1/video_180s480p_01.csv') #
df22 = pd.read_csv('./Data/benign-1/video_180s480p_02.csv') #
df23 = pd.read_csv('./Data/benign-1/video_x1_04.csv') #
df24 = pd.read_csv('./Data/benign-1/web_multiple_04.csv') #
df25 = pd.read_csv('./Data/benign-1/bulk_xs_01.csv') #
df26 = pd.read_csv('./Data/benign-1/bulk_xs_09.csv') #
df27 = pd.read_csv('./Data/benign-1/bulk_xs_06.csv') #
df28 = pd.read_csv('./Data/benign-1/bulk_xs_03.csv') #
df29 = pd.read_csv('./Data/benign-1/web_multiple_03.csv') #
df30 = pd.read_csv('./Data/benign-1/web_multiple_05.csv') #
df31 = pd.read_csv('./Data/benign-1/web_multiple_06.csv') #

df_results = pd.DataFrame()


# In[2]:


print("df1 -->> {}".format(len(df1)))
print("df2 -->> {}".format(len(df2)))
print("df3 -->> {}".format(len(df3)))
print("df4 -->> {}".format(len(df4)))
print("df5 -->> {}".format(len(df5)))
print("df6 -->> {}".format(len(df6)))
print("df7 -->> {}".format(len(df7)))
print("df32 -->> {}".format(len(df32)))
print("df33 -->> {}".format(len(df33)))
print("df34 -->> {}".format(len(df34)))
print("df35 -->> {}".format(len(df35)))
print("/////////////////////////////////////////////////")


print("df8 -->> {}".format(len(df8)))
print("df9 -->> {}".format(len(df9)))
print("df10 -->> {}".format(len(df10)))
print("df11 -->> {}".format(len(df11)))
print("df12 -->> {}".format(len(df12)))
print("df13 -->> {}".format(len(df13)))
print("df14 -->> {}".format(len(df14)))
print("df15 -->> {}".format(len(df15)))
print("df16 -->> {}".format(len(df16)))
print("df17 -->> {}".format(len(df17)))
print("df18 -->> {}".format(len(df18)))
print("df19 -->> {}".format(len(df19)))
print("df20 -->> {}".format(len(df20)))
print("df21 -->> {}".format(len(df21)))
print("df22 -->> {}".format(len(df22)))
print("df23 -->> {}".format(len(df23)))
print("df24 -->> {}".format(len(df24)))
print("df25 -->> {}".format(len(df25)))
print("df26 -->> {}".format(len(df26)))
print("df27 -->> {}".format(len(df27)))
print("df28 -->> {}".format(len(df28)))
print("df29 -->> {}".format(len(df29)))
print("df30 -->> {}".format(len(df30)))
print("df31 -->> {}".format(len(df31)))


# In[3]:


#################################################################
#                                                               #
#                     Filtering                                 #
#                                                               #
#################################################################

# For WebOS = 18:56:80:17:d0:ef
index_names = df1[((df1['HW_dst'] != '18:56:80:17:d0:ef') & (df1['Hw_src'] != '18:56:80:17:d0:ef'))].index
df1.drop(index_names, inplace = True)

# Big_Server_Monero_mining_data = a4:bb:6d:ac:e1:fd

index_names = df2[((df2['HW_dst'] != 'a4:bb:6d:ac:e1:fd') & (df2['Hw_src'] != 'a4:bb:6d:ac:e1:fd'))].index
df2.drop(index_names, inplace = True)

# ege_data_rasberry = dc:a6:32:67:66:4b	

index_names = df3[((df3['HW_dst'] != 'dc:a6:32:67:66:4b') & (df3['Hw_src'] != 'dc:a6:32:67:66:4b'))].index
df3.drop(index_names, inplace = True)

# Rasberry_binary_monero_mining = dc:a6:32:68:35:8a

index_names = df4[((df4['HW_dst'] != 'dc:a6:32:68:35:8a') & (df4['Hw_src'] != 'dc:a6:32:68:35:8a'))].index
df4.drop(index_names, inplace = True)

# Rasberry_network_data_2 = dc:a6:32:67:66:4b

index_names = df5[((df5['HW_dst'] != 'dc:a6:32:67:66:4b') & (df5['Hw_src'] != 'dc:a6:32:67:66:4b'))].index
df5.drop(index_names, inplace = True)

# Rasberry-Webmine = dc:a6:32:67:66:4b
index_names = df6[((df6['HW_dst'] != 'dc:a6:32:67:66:4b') & (df6['Hw_src'] != 'dc:a6:32:67:66:4b'))].index
df6.drop(index_names, inplace = True)

# Server_Webmine_Network_data = a4:bb:6d:ac:e1:fd

index_names = df7[((df7['HW_dst'] != 'a4:bb:6d:ac:e1:fd') & (df7['Hw_src'] != 'a4:bb:6d:ac:e1:fd'))].index
df7.drop(index_names, inplace = True)

# Server_%50_Mining = a4:bb:6d:ac:e1:fd

index_names = df32[((df32['HW_dst'] != 'a4:bb:6d:ac:e1:fd') & (df32['Hw_src'] != 'a4:bb:6d:ac:e1:fd'))].index
df32.drop(index_names, inplace = True)

# Rasberry_webmine_%10 = dc:a6:32:67:66:4b

index_names = df33[((df33['HW_dst'] != 'dc:a6:32:67:66:4b') & (df33['Hw_src'] != 'dc:a6:32:67:66:4b'))].index
df33.drop(index_names, inplace = True)

# Rasberry_webmine_%50 = dc:a6:32:68:35:8a

index_names = df34[((df34['HW_dst'] != 'dc:a6:32:68:35:8a') & (df34['Hw_src'] != 'dc:a6:32:68:35:8a'))].index
df34.drop(index_names, inplace = True)

# Desktop_Webmine_%100 = dc:a6:32:68:35:8a

index_names = df35[((df35['HW_dst'] != 'd8:3b:bf:8f:ba:ba') & (df35['Hw_src'] != 'd8:3b:bf:8f:ba:ba'))].index
df35.drop(index_names, inplace = True)


# In[4]:


#################################################################
#                                                               #
#      Labeling Features for further calculations               #
#                                                               #
#################################################################

df1.insert(7, "Is_malicious", 1)
df2.insert(7, "Is_malicious", 1)
df3.insert(7, "Is_malicious", 1)
df4.insert(7, "Is_malicious", 1)
df5.insert(7, "Is_malicious", 1)
df6.insert(7, "Is_malicious", 1)
df7.insert(7, "Is_malicious", 1)

# ========================================================

df8.insert(7, "Is_malicious", 0)
df9.insert(7, "Is_malicious", 0)
df10.insert(7, "Is_malicious", 0)
df11.insert(7, "Is_malicious", 0)
df12.insert(7, "Is_malicious", 0)
df13.insert(7, "Is_malicious", 0)
df14.insert(7, "Is_malicious", 0)
df15.insert(7, "Is_malicious", 0)
df16.insert(7, "Is_malicious", 0)
df17.insert(7, "Is_malicious", 0)
df18.insert(7, "Is_malicious", 0)
df19.insert(7, "Is_malicious", 0)
df20.insert(7, "Is_malicious", 0)
df21.insert(7, "Is_malicious", 0)
df22.insert(7, "Is_malicious", 0)
df23.insert(7, "Is_malicious", 0)
df24.insert(7, "Is_malicious", 0)


# ========================================================

df25.insert(7, "Is_malicious", 0)
df26.insert(7, "Is_malicious", 0)
df27.insert(7, "Is_malicious", 0)
df28.insert(7, "Is_malicious", 0)
df29.insert(7, "Is_malicious", 0)
df30.insert(7, "Is_malicious", 0)
df31.insert(7, "Is_malicious", 0)

df32.insert(7, "Is_malicious", 1)
df33.insert(7, "Is_malicious", 1)
df34.insert(7, "Is_malicious", 1)
df35.insert(7, "Is_malicious", 1)


# In[5]:


print("df1 -->> {}".format(len(df1.dropna())))
print("df2 -->> {}".format(len(df2.dropna())))
print("df3 -->> {}".format(len(df3.dropna())))
print("df4 -->> {}".format(len(df4.dropna())))
print("df5 -->> {}".format(len(df5.dropna())))
print("df6 -->> {}".format(len(df6.dropna())))
print("df7 -->> {}".format(len(df7.dropna())))
print("df8 -->> {}".format(len(df8.dropna())))
print("df9 -->> {}".format(len(df9.dropna())))
print("df10 -->> {}".format(len(df10.dropna())))
print("df11 -->> {}".format(len(df11.dropna())))
print("df12 -->> {}".format(len(df12.dropna())))
print("df13 -->> {}".format(len(df13.dropna())))
print("df14 -->> {}".format(len(df14.dropna())))
print("df15 -->> {}".format(len(df15.dropna())))
print("df16 -->> {}".format(len(df16.dropna())))
print("df17 -->> {}".format(len(df17.dropna())))
print("df18 -->> {}".format(len(df18.dropna())))
print("df19 -->> {}".format(len(df19.dropna())))
print("df20 -->> {}".format(len(df20.dropna())))
print("df21 -->> {}".format(len(df21.dropna())))
print("df22 -->> {}".format(len(df22.dropna())))
print("df23 -->> {}".format(len(df23.dropna())))
print("df24 -->> {}".format(len(df24.dropna())))
print("df25 -->> {}".format(len(df25.dropna())))
print("df26 -->> {}".format(len(df26.dropna())))
print("df27 -->> {}".format(len(df27.dropna())))
print("df28 -->> {}".format(len(df28.dropna())))
print("df29 -->> {}".format(len(df29.dropna())))
print("df30 -->> {}".format(len(df30.dropna())))
print("df31 -->> {}".format(len(df31.dropna())))
print("df32 -->> {}".format(len(df32.dropna())))
print("df33 -->> {}".format(len(df33.dropna())))
print("df34 -->> {}".format(len(df34.dropna())))
print("df35 -->> {}".format(len(df35.dropna())))


# In[6]:


def run_process(a,b,x):

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


# In[7]:


def ML_Process(df_ML,x):
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
          ('LogReg', LogisticRegression()), 
          #('RF', RandomForestClassifier()),
          ('KNN', KNeighborsClassifier()),
          ('SVM', SVC()), 
          ('GNB', GaussianNB())
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


# In[17]:


## S0: All Combined 

df_malicious = pd.concat([df1,df2,df3,df4,df5,df6,df7,df32,df33,df34,df35])

df_benign = pd.concat([df8,df9,df11,df10,df12,df13,df15,df16,df17,df18,df19,df20,df21,df22,df23,df24,df25,df30,df27,df29])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))


start = timer()

results_all_combined_s0 = run_process(df_malicious,df_benign,df_results)

end = timer()
print(end - start)




# In[129]:


#scenario 1 :Devices
# 1) Server

df_malicious = pd.concat([df2,df7,df32])
df_benign = pd.concat([df10,df11,df13,df15,df16,df17,df18,df19,df21,df22,df23,df26,df30,df28])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_server_s1 = run_process(df_malicious,df_benign,df_results)

end = timer()
print(end - start)


# In[149]:


 #2) Laptop
df_malicious = pd.concat([df35])
df_benign = pd.concat([df8,df20,df19,df30])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_Laptop_s1 = run_process(df_malicious,df_benign,df_results)


end = timer()
print(end - start)


# In[178]:


#3) IoT

df_malicious = pd.concat([df4,df5,df6,df33,df34])
df_benign = pd.concat([df8,df9,df10,df11,df12,df15,df16,df17,df21])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_Raspberry_s1 = run_process(df_malicious,df_benign,df_results)


end = timer()
print(end - start)


# In[132]:


# Scenario 2; Throttles

    # 1) THR: %10 (Stealthy)

df_malicious = pd.concat([df33])
df_benign = pd.concat([df8,df10])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_THR_10_s2 = run_process(df_malicious,df_benign,df_results)


end = timer()
print(end - start)



# In[24]:


# 2) THR: %50 (Robust)

df_malicious = pd.concat([df3,df34])
df_benign = pd.concat([df29,df31])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_THR_50_s2 = run_process(df_malicious,df_benign,df_results)

end = timer()
print(end - start)


# In[134]:


 # 3) THR: %100 (Aggressive)

df_malicious = pd.concat([df1,df2,df4,df5,df6,df7,df35])
df_benign    = pd.concat([df11,df12,df13,df14,df16,df17,df21,df23,df26,df27,df28,df29,df30,df31])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_THR_100_s2 = run_process(df_malicious,df_benign,df_results)


end = timer()
print(end - start)


# In[135]:


## S3; In-browser VS Binary ##

  #1) In-Browser
df_malicious = pd.concat([df3,df5,df6,df7,df32,df33,df34,df35])
df_benign = pd.concat([df8,df9,df14,df15,df16,df17,df18,df19,df20,df14])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_In_s3 = run_process(df_malicious,df_benign,df_results)


end = timer()
print(end - start)


# In[136]:


#2) Binary
df_malicious = pd.concat([df1,df2,df4])
df_benign = pd.concat([df12,df13,df15,df17,df22,df23,df27,df28,df29])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

start = timer()

results_Host_s3 = run_process(df_malicious,df_benign,df_results)


end = timer()
print(end - start)


# In[137]:


## S4: Fully compromised (All)

df_malicious = pd.concat([df1,df2,df3,df4,df5,df6,df7,df32,df33,df34,df35])

df_benign = pd.concat([df8,df9,df11,df10,df12,df13,df15,df16,df17,df18,df19,df20,df21,df22,df23,df24,df25,df30,df27,df29])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))


start = timer()

results_all_combined_s0 = run_process(df_malicious,df_benign,df_results)

end = timer()
print(end - start)




# In[138]:


## S5: Partially compromised (IoT + Laptop)

df_malicious = pd.concat([df5,df35])

df_benign = pd.concat([df14,df16,df18,df19,df20])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))


start = timer()

results_all_combined_s0 = run_process(df_malicious,df_benign,df_results)

end = timer()
print(end - start)




# In[183]:


## S6: Single compromised (IoT) (Raspberry)

df_malicious = pd.concat([df5])

df_benign = pd.concat([df8,df9,df10])


print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))


start = timer()

results_all_combined_s0 = run_process(df_malicious,df_benign,df_results)

end = timer()
print(end - start)




# In[227]:


## S7: IoT compromised (IoT + IoT)

df_malicious = pd.concat([df1,df34])

df_benign = pd.concat([df8,df9,df10,df11,df12,df21])

print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))

print("{} NAN in malicious!".format(len(df_malicious[df_malicious.isna().any(axis=1)])))
print("{} NAN in benign!".format(len(df_benign[df_benign.isna().any(axis=1)])))

df_malicious = df_malicious.dropna()
df_benign = df_benign.dropna()

print("After droppping NAN rows: ")
print("malicious: {}".format(len(df_malicious)))
print("benign: {}".format(len(df_benign)))


start = timer()

results_all_combined_s0 = run_process(df_malicious,df_benign,df_results)

end = timer()
print(end - start)



