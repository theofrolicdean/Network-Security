import yaml
from networksecurity.exception.exception import NetworkException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import numpy as np
import dill
import sys
import os

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as file_obj:
            return yaml.safe_load(file_obj)
    except Exception as err:
            raise NetworkException(error_message=str(err), error_detail=sys)

def write_yaml_file(file_path: str,
                    content: object,
                    replace: bool = False) -> None:
     try:
        if replace:
               if os.path.exists(file_path):
                    os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  
        with open(file_path, "w") as file_obj:
             yaml.dump(content, file_obj)
     except Exception as err:
        raise NetworkException(error_message=str(err), error_detail=sys)

def load_numpy_array_data(file_path: str) -> np.array:
     try:
          with open(file_path, "rb") as file_obj:
               return np.load(file_obj)
     except Exception as err:
          raise NetworkException(error_message=str(err), error_detail=sys)
     
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as err:
        raise NetworkException(str(err), sys) 

def load_object(file_path: str) -> object:
    try:    
        if not os.path.exists(file_path):
            raise NetworkException(f"The file: {file_path} is not exists", sys) 
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)
            return obj
    except Exception as err:
         raise NetworkException(error_message=str(err), error_detail=sys)

def evaluate_model(X_train, y_train, X_test, y_test, 
                   models: dict, 
                   params: dict) -> dict:
    try:
        report = {}

        for name, model in models.items():
            print(f"Training Model: {name} ")
            model_param = params[name]
            grid_search = GridSearchCV(estimator=model, param_grid=model_param, cv=5)
            grid_search.fit(X_train, y_train)
            model.set_params(**grid_search.best_params_)
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_r2_score = r2_score(y_train, y_train_pred)
            test_r2_score = r2_score(y_test, y_test_pred)
            print(f"Train R2 Score: {train_r2_score}\nTest R2 Score: {test_r2_score}")
            report[name] = test_r2_score

        return report
    except Exception as err:    
        raise NetworkException(error_message=str(err), error_detail=sys)