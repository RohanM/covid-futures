import torch
from torch import nn, optim, tensor
from app.lib import get_device
from app.lib.lambda_layer import Lambda
from torch.optim.lr_scheduler import OneCycleLR

class ResBlock(nn.Module):
    def __init__(self, num_channels, kernel_size, first=False):
        super().__init__()
        self.conv1 = nn.Conv1d(1 if first else num_channels, num_channels, kernel_size, padding=kernel_size//2)
        self.relu = nn.ReLU()

        kern2 = kernel_size if kernel_size <= 3 else kernel_size-2
        pad2 = 1 if kern2 <= 3 else (kern2 // 2)
        self.conv2 = nn.Conv1d(num_channels, num_channels, kern2, padding=pad2)
        #print(f"nn.Conv1d({1 if first else num_channels}, {num_channels}, {kernel_size}, padding={kernel_size//2})")
        #print(f"nn.Conv1d({num_channels}, {num_channels}, {kern2}, padding={pad2})")

    def forward(self, x):
        identity = x
        out = self.conv1(x)
        out = self.relu(out)
        out = self.conv2(out)
        out += identity
        out = self.relu(out)
        return out

class MLModel:
    def __init__(self, input_window=30, output_window=30, data_mean=0, data_std=1):
        """
        Parameters:
        input_window: Size of the input data (in days)
        output_window: Length of the prediction (in days)
        """
        self.data_mean = data_mean
        self.data_std = data_std
        self.device = get_device()

        def add_channel(x): return x.unsqueeze(dim=1)
        def flatten(x): return x.view(x.shape[0], -1)

        num_filters = 32

        self.__model = nn.Sequential(
            Lambda(add_channel),

            ResBlock(num_filters, 15, first=True),
            ResBlock(num_filters, 11),
            ResBlock(num_filters,  7),
            ResBlock(num_filters,  3),

            Lambda(flatten),
            nn.Linear(input_window*num_filters, output_window),
        )
        self.__model.to(get_device())

        # Actual learning rate will be defined by the scheduler when fitting
        self.__opt = optim.SGD(self.__model.parameters(), lr=0.01)

    def find_lr(self, dataloader, start_lr=1e-7, epochs_per_step=3):
        lrs, losses = [], []
        loss_func = nn.MSELoss()

        self.__opt.param_groups[0]['lr'] = start_lr

        self.__model.train()
        i = 0
        while self.__opt.param_groups[0]['lr'] < 10:
            loss = self.__train(dataloader, loss_func)
            lrs.append(self.__opt.param_groups[0]['lr'])
            losses.append(loss)
            if i % epochs_per_step == 0:
                self.__opt.param_groups[0]['lr'] *= 1.2
                print(self.__opt.param_groups[0]['lr'])
            i += 1

        return lrs, losses

    def fit(self, epochs, dataloader_train, dataloader_valid):
        train_losses, valid_losses = [], []
        scheduler = OneCycleLR(self.__opt, 0.028, total_steps=epochs, steps_per_epoch=1)
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

    def predict(self, x):
        """Given a list of history data, performs inference and returns predictions"""
        if type(x) == list: x = tensor(x)
        if len(x.shape) == 1: x = x.unsqueeze()
        x = x.float().to(get_device())
        normalised_x = (x - self.data_mean) / self.data_std
        offsets = self.__model(normalised_x).squeeze() * self.data_std
        return offsets + x[-1]

    def save(self, path):
        checkpoint = {
            'data_mean': self.data_mean,
            'data_std': self.data_std,
            'model': self.__model.state_dict(),
        }
        torch.save(checkpoint, path)

    def load(self, path):
        checkpoint = torch.load(path)
        self.data_mean = checkpoint['data_mean']
        self.data_std = checkpoint['data_std']
        self.__model.load_state_dict(checkpoint['model'])
        self.__model.eval()

    def __train(self, dataloader, loss_func):
        """Perform one training cycle and return the average loss."""
        self.__model.train()
        total_loss = 0.
        for xb, yb in dataloader:
            xb = xb.to(self.device)
            yb = yb.to(self.device)
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
                xb = xb.to(self.device)
                yb = yb.to(self.device)
                pred = self.__model(xb)
                total_loss += loss_func(pred, yb)
        return (total_loss / len(dataloader)).item()
