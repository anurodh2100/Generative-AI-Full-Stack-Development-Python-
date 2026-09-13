from transformers import pipeline

pipe = pipeline(
    task="text-generation",
    model="google/gemma-2b",
    device_map="auto",
)

result = pipe(
    "LLMs generate text through a process known as",
    max_new_tokens=50
)

print(result)