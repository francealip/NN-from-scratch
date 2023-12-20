import numpy as np

from .grid_search import GridSearch
from src.main.utils import shuffle_data, log_experiment
from src.main.utils import mean_std_scores


def double_Kfold_CV(X, y, grid_search, k = 5, verbose = False ):
    """
    function that allow to compute the double kflod cross validation
    
    :param X: dataset to train the model
    :param y: target of the dataset
    :param k: number of fold
    :param grid_search: a grid search object
    :param verbose: verbose mode for fit function
    """
    
    X, y = shuffle_data(X, y)
    
    x_fold = np.array_split(X, k)
    y_fold = np.array_split(y, k)
    
    #grid_search = GridSearch().create_search_obejct(grid_search)

    test_scores = []
    models = []
    
    for i in range(k):
        x_train, x_test = np.concatenate(x_fold[:i] + x_fold[i + 1:]), x_fold[i]
        y_train, y_test = np.concatenate(y_fold[:i] + y_fold[i + 1:]), y_fold[i]  
        
        """train_mean, train_std, val_mean, val_std,""" 
        ((train_mean, train_std), (val_mean, val_std)), model = grid_search.run_search(x_train, y_train, verbose)
        
        model.fit(x_train, y_train, False)
        
        test_scores.append(model.evaluate(x_test, y_test))
        models.append(model)
        
    test_mean, test_std = mean_std_scores(test_scores)
            
    return train_mean, train_std, val_mean, val_std, test_mean, test_std#, models