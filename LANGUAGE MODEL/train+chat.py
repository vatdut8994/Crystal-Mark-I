try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from alive_progress import alive_bar
    from transformers import GPT2Tokenizer, GPT2LMHeadModel
except ModuleNotFoundError:
    import os
    os.system("pip install -r requirements.txt")


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Set the model to evaluation mode
model.eval()

def generate_response(model, tokenizer, input_text):
    # Encode the input text into token indices
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Pass the input through the model to generate the logits
    logits = model(input_ids).last_hidden_state

    # Generate the response text by sampling from the logits
    response_ids = torch.multinomial(torch.softmax(logits[0, -1]), 1)
    response_text = tokenizer.decode(response_ids.tolist()[0])

    return response_text

def train(model, data, epochs=15, temperature=0.8):
    num = 1
    optimizer = optim.Adam(model.parameters(), lr=0.00002)
    criterion = nn.CrossEntropyLoss()
    print("TRAINING")
    for epoch in range(epochs):
        total_loss = 0
        with alive_bar(len(data), force_tty=True, title="Epoch"+str(num)) as bar:
            for i, line in enumerate(data):
                optimizer.zero_grad()
                input_ids = tokenizer.encode(line, add_special_tokens=True)
                input_ids = torch.tensor(input_ids).unsqueeze(0)
                outputs = model(input_ids)
                loss = criterion(outputs[0].view(-1, 50257), input_ids.view(-1))
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                bar()

        if epoch % 5 == 0:
            print(f'Epoch: {epoch} | Loss: {total_loss/len(data)}')
        num += 1

    torch.save(model.state_dict(), 'model.pt')
    print("Training complete.")

if __name__ == "__main__":
    with open("data/dataset.txt", "r") as f:
        data = f.readlines()
    train(model, data, 15)
    while True:
        prompt = input("You: ")
        response = generate_response(model, prompt)
        print("Crystal: ", response)