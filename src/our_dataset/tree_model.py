from our_dataset import dataset,transforms
from sklearn import tree,metrics


def main():
    ds = dataset.load_dataset()
    print("finished loading \nstarting extraction")
    
    train, val, test = transforms.pipeline_pycatch22(ds.df, 15, 0)
    print(train.columns)
    print(train["is_malicious"].describe())

    model = tree.DecisionTreeClassifier(max_depth=3,)
    train_x, train_y = train.drop(columns=ds.METADATA), train['is_malicious']
    print('starting to train')

    model.fit(train_x,train_y)
    test_x, test_Y = test.drop(columns=ds.METADATA), test['is_malicious']

    pred_y = model.predict(test_x)

    print(metrics.classification_report(test_Y, pred_y))


main()