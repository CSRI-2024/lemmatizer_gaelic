import torch
import torch.nn as nn

# Defining the model (copy from the notebook)
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        # Example:
        # self.embedding = nn.Embedding(...)
        # self.lstm = nn.LSTM(...)
        # self.fc = nn.Linear(...)

    def forward(self, x):
        # Example:
        # x = self.embedding(x)
        # x, _ = self.lstm(x)
        # x = self.fc(x)
        return x

# Load the model weights
model = MyModel()
model.load_state_dict(torch.load("model.pth", map_location=torch.device('cpu')))
model.eval()

# Test inference
# input_tensor = torch.tensor([...])  # Prepare input same way as in the notebook
# output = model(input_tensor)
# print(output)
