import torch
from alive_progress import alive_bar
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Load and preprocess the training data
with open('./data/dataset.txt', 'r') as f:
    text = f.read()

# Tokenize the text data
inputs = tokenizer(text, return_tensors='pt')

# Set up the training parameters
epochs = 10
learning_rate = 5e-5
batch_size = 4

# Set up the optimizer and the training data loader
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
data_loader = torch.utils.data.DataLoader(inputs['input_ids'], batch_size=batch_size, shuffle=True)

# Train the model
model.train()
with alive_bar(epochs, force_tty=True) as BarE:
    for epoch in range(epochs):
        print('Training epoch:', epoch)
        with alive_bar(len(data_loader), force_tty=True) as bar:
            for i, batch in enumerate(data_loader):
                optimizer.zero_grad()
                outputs = model(input_ids=batch, labels=batch)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                if i % 50 == 0:
                    print('Batch:', i, 'Loss:', loss.item())
                bar()
        BarE()

# Save the trained model
model.save_pretrained('crystal_model')
