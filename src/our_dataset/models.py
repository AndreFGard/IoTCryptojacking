
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier

class SVCFactory:
    name = "SVC"

    def __init__(self):
        self.param_grids = [
            {
                "C": [1, 2],
                "kernel": ["linear"],
                "gamma": ["scale"],
                "class_weight": ["balanced", None],
            },
            {
                "C": [1, 2],
                "kernel": ["poly", "rbf", "sigmoid"],
                "gamma": ["scale", "auto"],
                "class_weight": ["balanced", None],
            },
        ]

    def make_model(self, **params):
        C = params["C"]
        kernel = params["kernel"]
        class_weight = params.get("class_weight", None)
        gamma = params.get("gamma", "scale")
        comb_name = f"SVC - {C} - {kernel} - {gamma} - {class_weight}"

        if kernel == "linear":
            model = LinearSVC(
                C=C,
                loss="hinge",
                class_weight=class_weight,
                random_state=42,
                dual=True,
                max_iter=10000,
            )
        else:
            model = SVC(
                C=C,
                kernel=kernel,
                gamma=gamma,
                class_weight=class_weight,
                random_state=42,
            )
        return self.name, comb_name, model


class RandomForestFactory:
    name = "RandomForest"

    def __init__(self):
        self.param_grids = [
            {
                "n_estimators": [50, 100, 200],
                "max_depth": [
                    None,
                    10,
                ],
                "min_samples_split": [2, 5],
                "class_weight": ["balanced_subsample", None],
            }
        ]

    def make_model(self, **params):
        n_estimators = params["n_estimators"]
        max_depth = params["max_depth"]
        min_samples_split = params["min_samples_split"]
        class_weight = params.get("class_weight", None)

        comb_name = (
            f"RF - {n_estimators} - {max_depth} - {min_samples_split} - {class_weight}"
        )

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            class_weight=class_weight,
            random_state=42,
            n_jobs=-1,
        )
        return self.name, comb_name, model
