from our_dataset import dataset,transforms
from sklearn import tree,metrics


def main():
    ds = dataset.load_dataset()
    print("finished loading \nstarting extraction")
    
    train, val, test, _ = transforms.pipeline_pycatch22(ds.df, 15, 0)
    print(train.columns)
    print(train["is_malicious"].describe())

    from sklearn.model_selection import GridSearchCV

    param_grid = {
        'max_depth': [3, 5, 8, 12,],
        'criterion': ['gini', 'entropy'],
        'class_weight': ['balanced']
    }

    grid = GridSearchCV(
        tree.DecisionTreeClassifier(random_state=42),
        param_grid,
        scoring='f1',
        cv=3,
        n_jobs=-1
    )
    print('starting grid search')


    train_x, train_y = train.drop(columns=ds.METADATA), train['is_malicious']
    print('starting to train')

    grid.fit(train_x, train_y)

    print("Best hyperparameters:", grid.best_params_)
    print(f"Best CV F1-score: {grid.best_score_:.4f}")

    best_model = grid.best_estimator_
    test_x, test_Y = test.drop(columns=ds.METADATA), test['is_malicious']

    pred_y = best_model.predict(test_x)

    print("\nTest set classification report:")
    print(metrics.classification_report(test_Y, pred_y))


main()