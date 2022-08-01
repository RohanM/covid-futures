import torch
from torch import nn, optim
from app.lib.lambda_layer import Lambda
from torch.optim.lr_scheduler import OneCycleLR

class MLModel:
    def __init__(self, input_window=30, output_window=30):
        """
        Parameters:
        input_window: Size of the input data (in days)
        output_window: Length of the prediction (in days)
        """
        def add_channel(x): return x.unsqueeze(dim=1)
        def flatten(x): return x.view(x.shape[0], -1)

        num_filters = 32

        self.__model = nn.Sequential(
            Lambda(add_channel),
            nn.Conv1d(          1, num_filters, 7,  padding=3), nn.ReLU(),
            nn.Conv1d(num_filters, num_filters, 5,  padding=2), nn.ReLU(),
            nn.Conv1d(num_filters, num_filters, 3,  padding=1), nn.ReLU(),
            nn.Conv1d(num_filters, num_filters, 3,  padding=1), nn.ReLU(),

            Lambda(flatten),
            nn.Linear(input_window*num_filters, output_window),
        ).cuda()
        # Actual learning rate will be defined by the scheduler when fitting
        self.__opt = optim.SGD(self.__model.parameters(), lr=0.01)

    def fit(self, epochs, dataloader_train, dataloader_valid):
        train_losses, valid_losses = [], []
        scheduler = OneCycleLR(self.__opt, 0.01, total_steps=epochs, steps_per_epoch=1)
        loss_func = nn.MSELoss()

        for epoch in range(epochs):
            train_losses.append(
                self.__train(dataloader_train, loss_func)
            )
            valid_losses.append(
                self.__evaluate(dataloader_valid, loss_func)
            )
            print(f"{epoch}, {train_losses[-1]}, {valid_losses[-1]}")
            scheduler.step()

        return train_losses, valid_losses

    def save(self, path):
        torch.save(self.__model.state_dict(), path)

    def load(self, path):
        self.__model.load_state_dict(torch.load(path))
        self.__model.eval()

    def __train(self, dataloader, loss_func):
        """Perform one training cycle and return the average loss."""
        self.__model.train()
        total_loss = 0.
        for xb, yb in dataloader:
            loss = loss_func(self.__model(xb), yb)
            total_loss += loss
            loss.backward()
            self.__opt.step()
            self.__opt.zero_grad()
        return (total_loss / len(dataloader)).item()

    def __evaluate(self, dataloader, loss_func):
        self.__model.eval()
        with torch.no_grad():
            total_loss = 0.
            for xb, yb in dataloader:
                pred = self.__model(xb)
                total_loss += loss_func(pred, yb)
        return (total_loss / len(dataloader)).item()
