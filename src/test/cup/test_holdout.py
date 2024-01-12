from src.main.evaluation.holdout_CV import holdout_CV
from src.main.evaluation.grid_search import RandomGridSearch
from src.main.utilities.utils import load_hparams, setup_experiment, log_experiment, predictions_to_csv
from src.main.utilities.dataset_handler import get_cup_dataset


def print_score(mean, std):
    for key in mean.keys():
        print(key, "\t", mean[key], "+\-", std[key])


x_train, y_train, x_test = get_cup_dataset()

hyperparameters = load_hparams("cup")
grid_search = RandomGridSearch(hyperparameters, 70)
train_mean, train_std, val_mean, val_std, test_mean, test_std, model, (epochs, batch_size), histories, top5 = (
    holdout_CV(x_train, y_train, grid_search, verbose=False)
)

exp_dir = setup_experiment("cup")

log_experiment(
    exp_dir,
    model, epochs, batch_size,
    train_mean, train_std, val_mean, val_std, test_mean, test_std, histories
)

predictions = model.predict(x_test)
predictions_to_csv(predictions, filename="chiacchieroni_ML-CUP-23-TS.csv")

print("------ Train scores: ------ ")
print_score(train_mean, train_std)
print("------ Validation scores: ------ ")
print_score(val_mean, val_std)
print("------ Test scores: ------ ")
print_score(test_mean, test_std)

for (i, best_result) in enumerate(top5):
    exp_dir = setup_experiment(f"cup/top5/{i + 1}")
    ((train_m, train_var), (validation_mean, validation_var)) = best_result[0]
    m = best_result[1]
    ep, b_size = best_result[2]
    t_score = {}
    t_std = {}
    for key in validation_mean.keys():
        t_score[key] = 0.0
        t_std[key] = 0.0
    log_experiment(
        exp_dir,
        model, epochs, batch_size,
        train_m, train_var, validation_mean, validation_var, t_score, t_std, None
    )
