import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.distributed as dist
from alive_progress import alive_bar
from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_response(model, tokenizer, input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    logits = model(input_ids).last_hidden_state
    response_ids = torch.multinomial(torch.softmax(logits[0, -1]), 1)
    response_text = tokenizer.decode(response_ids.tolist()[0])
    return response_text

def train(model, data, epochs=15, temperature=0.8, local_rank=-1):
    num = 1
    optimizer = optim.Adam(model.parameters(), lr=0.00002)
    criterion = nn.CrossEntropyLoss()
    model.train()

    if local_rank != -1:
        model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[local_rank], output_device=local_rank)

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

    if local_rank == 0:
        torch.save(model.state_dict(), 'model.pt')
        print("Training complete.")

if __name__ == "__main__":
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    dist.init_process_group(backend="nccl")

    with open("data/dataset.txt", "r") as f:
        data = f.readlines()
    train(model, data, 15, local_rank=local_rank)

    while True:
        prompt = input("You: ")
        response = generate_response(model, tokenizer, prompt)
        print("Crystal: ", response)