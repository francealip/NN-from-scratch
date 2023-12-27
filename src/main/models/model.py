import numpy as np
from .layers.layer import Layer
from src.main.metric import Metric, metrics_dict
from src.main.optimizer import Optimizer, optimizer_dict
from src.main.callback import Callback, callback_dict
from src.main.loss import Loss, loss_dict
from src.main.regularizer import Regularizer, regularizer_dict


class Model:

    def __init__(self):
        """
        Constructor for the model. Initializes the optimizer, the metrics and the loss to None.
        These fields will be initialized when the model is compiled.
        Layers can be added to the model with the add method.
        """
        self.optimizer = None
        self.callback = None
        self.metrics = None
        self.loss = None
        self.regularizer = None
        self.layers = []

    def add(self, layer: Layer):
        """
        Adds a layer to the model.

        :param layer: the layer to add
        """
        self.layers.append(layer)

    def compile(
            self,
            optimizer: str | Optimizer,
            callback: str | Callback,
            loss: str | Loss,
            metrics: list[str | Metric],
            regularizer: str | Regularizer = None,
    ):
        """
        Prepares the model for fitting with an optimizer, a loss and a list of metrics.

        :param optimizer: the optimizer to use
        :param loss: the loss to use
        :param metrics: the list of metrics to use
        :param regularizer: the regularizer to use
        """
        if isinstance(optimizer, str):
            optimizer = optimizer_dict.get(optimizer)
            if optimizer is None:
                raise ValueError("Invalid optimizer")
          
        if isinstance(callback, str):
            callback = callback_dict.get(callback)
            if callback is None:
                raise ValueError("Invalid callback")

        if isinstance(loss, str):
            loss = loss_dict.get(loss)
            if loss is None:
                raise ValueError("Invalid loss")

        if not isinstance(metrics, list):
            raise ValueError("Metrics must be a list")

        metrics = list(map(lambda x: metrics_dict.get(x) if isinstance(x, str) else x, metrics))

        if regularizer is not None:
            if isinstance(regularizer, str):
                regularizer = regularizer_dict.get(regularizer)
                if regularizer is None:
                    raise ValueError("Invalid regularizer")

        self.optimizer = optimizer
        self.callback = callback
        self.loss = loss
        self.metrics = metrics
        self.regularizer = regularizer

    def fit(self, x_train: np.ndarray, y_train: np.ndarray, x_val: np.ndarray, y_val: np.ndarray, 
            epochs=256, batch_size=20, verbose=False):
        """
        Fits the model using the training data.

        :param x_train: the input data for training
        :param y_train: the target data for training
        :param x_val: the input data for validation
        :param y_val: the target data for validation
        :param epochs: the number of epochs to train the model
        :param batch_size: the size of the batch to process at each epoch
        :param verbose: whether to print the progress of the training
        """
                
        for epoch in range(epochs):
            for batch in range(len(x_train) // batch_size):
                
                x_batch = x_train[batch * batch_size: (batch + 1) * batch_size]
                y_batch = y_train[batch * batch_size: (batch + 1) * batch_size]

                # shuffle the data
                idx = np.random.permutation(len(x_batch))
                x_batch = x_batch[idx]
                y_batch = y_batch[idx]

                self.train_one_step(x_batch, y_batch)
                                
            if(self.callback is not None):
                val_score = self.evaluate(x_val, y_val)
                self.callback.update_val_history(val_score)
                self.callback.increment_counter()
                                
                if(self.callback.check_stop()):
                    print("Early Stopping Triggered at iter: ", self.callback.get_counter())
                    self.callback.reset()
                    break
        
                
            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch + 1}/{epochs} - Loss: {self.evaluate(x_train, y_train)}")
        
        if(self.callback is not None):
            self.callback.reset()

    def train_one_step(self, x: np.ndarray, y: np.ndarray):
        """
        Trains the model on one batch of data.

        :param x: the input data
        :param y: the target data
        """

        # Forward Pass
        y_pred = self.forward(x)

        # Compute Loss derivative to propagate back
        delta = self.loss.backward(y_pred, y)

        # Backward Pass
        self.backward(delta)

        # Update Parameters
        for layer in reversed(self.layers):
            self.optimizer.update_parameters(layer, self.regularizer)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Performs a forward pass of the model, by calling the forward method of each layer.

        :param x: the input data_for_testing
        :return: the prediction of the model
        """
        for layer in self.layers:
            x = layer.forward(x)

        return x

    def backward(self, delta: np.ndarray) -> np.ndarray:
        """
        Performs a backward pass of the model, by calling the backward method of each layer.

        :param delta: the error to propagate back
        :return: the error to propagate to the previous layer
        """
        for layer in reversed(self.layers):
            delta = layer.backward(delta)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Performs a prediction on the input data_for_testing.

        :param x: the input data_for_testing
        :return: the prediction of the model
        """
        return self.forward(x)

    def evaluate(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Evaluates the model on the input data_for_testing.

        :param x: the input data_for_testing
        :param y: the target data_for_testing
        :return: the value of the loss and the metrics
        """

        y_pred = self.predict(x)

        model_score = {}

        for metric in self.metrics:
            model_score[metric.to_string()] = metric.evaluate(y_pred, y)

        model_score["loss"] = self.loss.forward(y_pred, y)

        return model_score

    def summary(self):
        """
        Prints a summary of the model.
        """
        print("\nModel Summary:")
        print(f"Optimizer: {self.optimizer.to_string()}")
        print(f"Loss: {self.loss.to_string()}")
        print(f"Metrics: {list(map(lambda x: x.to_string(), self.metrics))}")
        print(" ")
        for layer in self.layers:
            layer.summary()
        print(" ")
