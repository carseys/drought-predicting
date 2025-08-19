import numpy as np
from torch.utils.data import Dataset
import torch
import torch.nn as nn
torch.manual_seed(1)

from data_import import *

class DroughtDataset(Dataset):
    """
    Readying Drought dataset for model.
    """
    def __init__(self, df):
        self.X = torch.tensor(df.iloc[:, (df.columns != 'score') & (df.columns != 'date')].values)
        self.y = torch.tensor(df.iloc[:, df.columns == 'score'].dropna().values)
        self.date = np.array(df.iloc[:, df.columns == 'date'].values)

    def __len__(self):
        return int(len(self.y))
    
    def __getitem__(self, index):
        output_X = self.X[7*index:7+7*index]
        output_y = self.y[index]
        output_date = self.date[7*index:7+7*index]

        return output_X, output_y, output_date
    
class LSTM_Model(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim = 1):
        super(LSTM_Model, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.output_layer = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, h_0=None, c_0=None):
        # managing hidden states and cell states
        if h_0 is None or c_0 is None:
            h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim)
            c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim)
        
        out, (h_n, c_n) = self.lstm(x, (h_0, c_0))
        out = self.output_layer(out[:, -1, :])
        return out

def train(num_epochs: int, model: nn.Module, loss_fn, optimizer, train_data_loader):
    """
    trains the model.

    Parameters
    ----------
    'num_epochs' : int
    'model' : nn.Module
    'train_data_loader'
    """

    total_steps = len(train_data_loader)

    for epoch in range(num_epochs):
        for batch, (soil_info, drought_rating, date) in enumerate(train_data_loader):
            output = model(soil_info)
            loss = loss_fn(output, drought_rating)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (batch+1)%10 == 0:
                print(f'Epoch: {epoch+1}; Batch: {batch+1} / {total_steps}; Loss: {loss.item():>4f}') # rounding the loss
    return None