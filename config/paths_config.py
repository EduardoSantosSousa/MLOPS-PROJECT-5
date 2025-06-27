import os 

#-----------------------------------------------
#Project root path
#-----------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..'))

#------------------------------------------------
#File and directory configuration
#------------------------------------------------

# Path to general configuration file
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config', 'config.yml')

# Directories and data files
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'raw')
RAW_DATA = os.path.join(RAW_DATA_DIR, 'data.csv')

PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'processed')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'artifacts', 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'model.pkl')

SCALER_PATH =  os.path.join(PROCESSED_DIR, 'scaler.pkl')
