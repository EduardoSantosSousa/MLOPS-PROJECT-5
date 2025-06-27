import os 
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, roc_auc_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

import mlflow
import mlflow.sklearn


logger = get_logger(__name__)

class ModelTraining:

    def __init__(self, processed_data_path = PROCESSED_DIR ):
        self.processed_data_path = processed_data_path
        self.model_dir = MODELS_DIR
        os.makedirs(self.model_dir, exist_ok=True)

        logger.info("Model Training Initialization.....")

    def load_data(self):
        try:
            self.X_train = joblib.load(os.path.join(self.processed_data_path, 'X_train.pkl'))
            self.X_test = joblib.load(os.path.join(self.processed_data_path, 'X_test.pkl'))
            self.y_train = joblib.load(os.path.join(self.processed_data_path, 'y_train.pkl'))
            self.y_test = joblib.load(os.path.join(self.processed_data_path, 'y_test.pkl'))

            logger.info("Data loaded for Model")

        except Exception as e:
            logger.error(f"Error while loading for model {e}")
            raise CustomException("Failed to load data for model... ", e)
        
    def train_model(self):
        try:
            self.model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)  
            self.model.fit(self.X_train, self.y_train)

            joblib.dump(self.model, os.path.join(self.model_dir, "model.pkl"))

            logger.info("Model trained and saved sucesfully......")

        except Exception as e:
            logger.error(f"Error while loading data for model {e}")
            raise CustomException("Failed to load data for model....", e)

    def evaluate_model(self):
        try:
            y_pred = self.model.predict(self.X_test)

            is_binary = len(np.unique(self.y_test)) == 2
            y_proba = self.model.predict_proba(self.X_test)[:, 1] if is_binary else None

            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, pos_label='Yes')
            recall = recall_score(self.y_test, y_pred, pos_label='Yes')
            f1 = f1_score(self.y_test, y_pred, pos_label='Yes')

            mlflow.log_metric("Accuracy", accuracy)
            mlflow.log_metric("Precision", precision)
            mlflow.log_metric("Recall Score", recall)
            mlflow.log_metric("F1_score", f1)

            logger.info(f"Accuracy: {accuracy}; Precision: {precision}; Recall: {recall}; F1: {f1}")

            if is_binary:
                roc_auc = roc_auc_score(self.y_test.map({'No': 0, 'Yes': 1}), y_proba)
                mlflow.log_metric("ROC-AUC", roc_auc)

                logger.info(f"ROC-AUC Score: {roc_auc}")

            logger.info("Model evaluation done.....")

        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("Failed to evaluate model....", e)


    def run(self):
        self.load_data()
        self.train_model()
        self.evaluate_model()

if __name__=="__main__":
    with mlflow.start_run():
        trainer =ModelTraining()
        trainer.run()
           







