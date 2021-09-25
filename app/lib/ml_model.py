from torch import nn, optim
from app.lib.lambda_layer import Lambda

class MLModel:
    def __init__(self):
        def add_channel(x): return x.unsqueeze(dim=1)
        def flatten(x): return x.view(x.shape[0], -1)

        self.__model = nn.Sequential(
            Lambda(add_channel),

            nn.Conv1d(1,  32, 15, padding=7), nn.ReLU(),
            nn.Conv1d(32, 32, 13, padding=6), nn.ReLU(),
            nn.Conv1d(32, 32, 11, padding=5), nn.ReLU(),
            nn.Conv1d(32, 32, 9,  padding=4), nn.ReLU(),
            nn.Conv1d(32, 32, 7,  padding=3), nn.ReLU(),
            nn.Conv1d(32, 32, 5,  padding=2), nn.ReLU(),
            nn.Conv1d(32, 32, 3,  padding=1), nn.ReLU(),
            nn.Conv1d(32, 32, 3,  padding=1), nn.ReLU(),

            Lambda(flatten),
            nn.Linear(960, 30),
        )
        # Actual learning rate will be defined by the scheduler when fitting
        self.__opt = optim.SGD(self.__model.parameters(), lr=0.01)
