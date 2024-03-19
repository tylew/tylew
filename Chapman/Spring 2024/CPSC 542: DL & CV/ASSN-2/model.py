import torch
import torch.nn as nn
import torch.optim as optim

class Model(nn.Module):
    def __init__(self,inChannels,dropout):
        super(Model, self).__init__()

        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout)
        
        self.conv1 = nn.Conv2d(in_channels=inChannels, out_channels=12, kernel_size=5, padding=2)
        self.conv2 = nn.Conv2d(12, 10, kernel_size=5, padding=2)
        self.conv3 = nn.Conv2d(10, 8, kernel_size=5, padding=2)
        self.convX = nn.Conv2d(8, 4, kernel_size=5, padding=2)
        self.conv4 = nn.Conv2d(4, 1, kernel_size=5, padding=2)
        
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.conv2(x)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.conv3(x)
        x = self.relu(x)
        x = self.dropout(x)

        x = self.convX(x)
        x = self.relu(x)
        x = self.dropout(x)
        
        x = self.conv4(x)
        x = self.sigmoid(x)

        x = x.squeeze(1)  # Remove the channel dimension for seg map

        return x
