import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from app.models.autoencoder import LogAutoEncoder

df = pd.read_csv('data/logs.csv')
X = torch.tensor(df.values, dtype=torch.float32)

model = LogAutoEncoder(input_dim=X.shape[1])
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
loader = DataLoader(TensorDataset(X), batch_size=2, shuffle=True)

for epoch in range(10):
    for batch in loader:
        inp = batch[0]
        out = model(inp)
        loss = criterion(out, inp)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

torch.save(model.state_dict(), "model.pt")