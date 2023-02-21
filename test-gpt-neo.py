import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

torch.cuda.empty_cache()
print('torch.cuda.is_available():', torch.cuda.is_available())

print('Loading model...')
model = model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

print('Loading tokenizer...')
tokenizer = tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

print('Transfering model to GPU...')
device = torch.device("cuda")
model.to(device)

print('Generating prompt...')
query = "climate change"
max_terms = 5
prompt = f"Generate up to {max_terms} additional relevant terms for the query '{query}'."

print('Tokenizing...')
tokenized = tokenizer(prompt, return_tensors="pt")
input_ids = tokenized.input_ids.to(device)
attention_mask = tokenized.attention_mask.to(device)

print('Generating answer...')
with torch.no_grad():
    gen_tokens = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=False,
        temperature=1,
        max_length=2048,
    )

print('Decoding answer...')
gen_text = tokenizer.batch_decode(gen_tokens)[0]

# extract the terms
import re
terms = re.findall(r"'(.*?)'", gen_text)

# remove duplicate terms
terms = list(set(terms))

# print up to 5 terms
print(terms[:5])

