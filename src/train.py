import argparse
import logging
import numpy as np
import os
import pandas as pd
import pickle
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeRegressor


def load_data(path):
    return pd.read_csv(path)


def main(input_dir, output_dir):
    # Load the data
    housing_prepared = load_data(os.path.join(input_dir, "housing_prepared.csv"))
    housing_labels = load_data(os.path.join(input_dir, "housing_labels.csv"))

    # Linear Regression
    lin_reg = LinearRegression()
    lin_reg.fit(housing_prepared, housing_labels)

    housing_predictions = lin_reg.predict(housing_prepared)
    lin_mse = mean_squared_error(housing_labels, housing_predictions)
    lin_rmse = np.sqrt(lin_mse)
    logging.info(f"Linear Regression RMSE: {lin_rmse}")

    # Decision Tree Regressor
    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(housing_prepared, housing_labels)

    housing_predictions = tree_reg.predict(housing_prepared)
    tree_mse = mean_squared_error(housing_labels, housing_predictions)
    tree_rmse = np.sqrt(tree_mse)
    logging.info(f"Decision Tree RMSE: {tree_rmse}")

    # Random Forest with RandomizedSearchCV
    param_distribs = {
        "n_estimators": randint(low=1, high=200),
        "max_features": randint(low=1, high=8),
    }
    forest_reg = RandomForestRegressor(random_state=42)
    rnd_search = RandomizedSearchCV(
        forest_reg,
        param_distributions=param_distribs,
        n_iter=10,
        cv=5,
        scoring="neg_mean_squared_error",
        random_state=42,
    )
    rnd_search.fit(housing_prepared, housing_labels)
    cvres = rnd_search.cv_results_
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        logging.info(f"RandomizedSearchCV - RMSE: {np.sqrt(-mean_score)}, Params: {params}")

    # Random Forest with GridSearchCV
    param_grid = [
        {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
        {"bootstrap": [False], "n_estimators": [3, 10], "max_features": [2, 3, 4]},
    ]
    forest_reg = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(
        forest_reg,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    grid_search.fit(housing_prepared, housing_labels)

    cvres = grid_search.cv_results_
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        logging.info(f"GridSearchCV - RMSE: {np.sqrt(-mean_score)}, Params: {params}")

    feature_importances = grid_search.best_estimator_.feature_importances_
    importance_scores = sorted(zip(feature_importances, housing_prepared.columns), reverse=True)
    for score in importance_scores:
        logging.info(f"Feature: {score[1]}, Importance: {score[0]}")

    # Save the best model
    final_model = grid_search.best_estimator_
    with open(os.path.join(output_dir, "best_model.pkl"), "wb") as f:
        pickle.dump(final_model, f)

    logging.info(f'Saved the best model to {os.path.join(output_dir, "best_model.pkl")}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, help="Input directory.")
    parser.add_argument("--output_dir", type=str, help="Output directory.")
    args = parser.parse_args()
    log_dir = "/home/pushvinder/mle_training/logs/"
    logging.basicConfig(
        filename=os.path.join(log_dir, "train.log"),
        level=logging.INFO,
        format="%(levelname)s:%(message)s",
    )
    logging.info("Started training.")
    main(args.input_dir, args.output_dir)
    logging.info("Finished training.")
