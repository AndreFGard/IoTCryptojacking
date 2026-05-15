import logging
import pandas as pd
from typing import Sequence
def load_dataset() -> Sequence[pd.DataFrame] :
    #################################################################
    #                                                               #
    #               malicious csv files import                      #
    #                                                               #
    #################################################################

    df1 = pd.read_csv('Data/malicious/WebOS_binary.csv') #
    df2 = pd.read_csv('Data/malicious/Server_Binary.csv') #
    df3 = pd.read_csv('Data/malicious/Raspberry_Webmine_Robust.csv')
    df4 = pd.read_csv('Data/malicious/Raspberry_Binary.csv') #
    df5 = pd.read_csv('Data/malicious/Raspberry_Webmine_Aggressive.csv')
    df6 = pd.read_csv('Data/malicious/Raspberry_WebminePool_Aggressive.csv')
    df7 = pd.read_csv('Data/malicious/Server_WebminePool_Aggressive.csv') #

    df32 = pd.read_csv('Data/malicious/Server_WebminePool_Robust.csv') #
    df33 = pd.read_csv('Data/malicious/Raspberry_WebminePool_Stealthy.csv') #
    df34 = pd.read_csv('Data/malicious/Raspberry_WebminePool_Robust.csv') #
    df35 = pd.read_csv('Data/malicious/Desktop_WebminePool_Aggressive.csv') #


    #################################################################
    #                                                               #
    #               benign csv files import                         #
    #                                                               #
    #################################################################

    ############### LAPTOP #############

    df8 = pd.read_csv('Data/benign-2/Laptop/Laptop_download_benign.csv')
    df9 = pd.read_csv('Data/benign-2/Laptop/Laptop_idle_benign.csv')
    df10 = pd.read_csv('Data/benign-2/Laptop/Laptop_interactive_benign.csv')
    df11 = pd.read_csv('Data/benign-2/Laptop/Laptop_video_benign.csv')
    df12 = pd.read_csv('Data/benign-2/Laptop/Laptop_webbrowsing_benign.csv')

    ############### Raspberry ##########

    df13 = pd.read_csv('Data/benign-2/Raspberry/Raspberry_download_benign.csv')
    df14 = pd.read_csv('Data/benign-2/Raspberry/Raspberry_idle_benign.csv')
    df15 = pd.read_csv('Data/benign-2/Raspberry/Raspberry_interactive_benign.csv')
    df16 = pd.read_csv('Data/benign-2/Raspberry/Raspberry_video_benign.csv')
    df17 = pd.read_csv('Data/benign-2/Raspberry/Raspberry_webbrowsing_benign.csv')

    ############### Server ############


    df18 = pd.read_csv('Data/benign-2/Server/Server_download_benign.csv')
    df19 = pd.read_csv('Data/benign-2/Server/Server_idle_benign.csv')
    df20 = pd.read_csv('Data/benign-2/Server/Server_interactive_benign.csv')
    df21 = pd.read_csv('Data/benign-2/Server/Server_video_benign.csv')
    df22 = pd.read_csv('Data/benign-2/Server/Server_webbrowsing_benign.csv')

    ############### WebOS ############

    df23 = pd.read_csv('Data/benign-2/WebOS/Webos_video(live&normal)_benign.csv')


    df_results = pd.DataFrame()

    logging.info("Finished importing csv files")

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

    print(" LAPTOP ")


    print("df8 -->> {}".format(len(df8)))
    print("df9 -->> {}".format(len(df9)))
    print("df10 -->> {}".format(len(df10)))
    print("df11 -->> {}".format(len(df11)))
    print("df12 -->> {}".format(len(df12)))

    print(" Raspberry ")


    print("df13 -->> {}".format(len(df13)))
    print("df14 -->> {}".format(len(df14)))
    print("df15 -->> {}".format(len(df15)))
    print("df16 -->> {}".format(len(df16)))
    print("df17 -->> {}".format(len(df17)))

    print(" Server ")

    print("df18 -->> {}".format(len(df18)))
    print("df19 -->> {}".format(len(df19)))
    print("df20 -->> {}".format(len(df20)))
    print("df21 -->> {}".format(len(df21)))
    print("df22 -->> {}".format(len(df22)))

    print(" WebOS ")

    print("df23 -->> {}".format(len(df23)))


    df_malicious = pd.concat([df1,df2,df3,df4,df5,df6,df7,df32,df33,df34,df35])
    
    df_benign = pd.concat([df8,df9,df10,df11,df12,df13,df14,df15,df16,df17,df18,df19,df20,df21,df22,df23])

    print("malicious: {}".format(len(df_malicious)))
    print("benign: {}".format(len(df_benign)))

    logging.info("finished concatenating csv files")


    # Prune the datasets for labeling process for malicious data


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


    logging.info("Finished pruning datasets for labeling process")

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

    # ========================================================


    df32.insert(7, "Is_malicious", 1)
    df33.insert(7, "Is_malicious", 1)
    df34.insert(7, "Is_malicious", 1)
    df35.insert(7, "Is_malicious", 1)

    logging.info("Finished labeling features")
    return df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17, df18, df19, df20, df21, df22, df23, df32, df33, df34, df35
