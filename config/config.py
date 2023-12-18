import os

MONK_BENCHMARK_PATH = "/data_for_testing/monk/monk-{}"
ML_CUP_PATH = "/data_for_testing/cup"
HPARAMS_ROOT = "/hyperparams/{}.yaml"

# PROJECT FOLDER PATH
PROJECT_FOLDER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MONK BENCHMARK PATH
MONK_BENCHMARK_PATH = PROJECT_FOLDER_PATH + MONK_BENCHMARK_PATH

# ML CUP PATH
ML_CUP_PATH = PROJECT_FOLDER_PATH + ML_CUP_PATH

# HYPERPARAMETERS PATH
HPARAMS_ROOT = PROJECT_FOLDER_PATH + HPARAMS_ROOT

