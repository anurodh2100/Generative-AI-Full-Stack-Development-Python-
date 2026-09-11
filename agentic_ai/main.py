import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! I am AJ"

tokens = enc.encode(text)
#Tokens [25216, 3274, 0, 357, 939, 59598]
print("Tokens", tokens)


#reverse

decoded = enc.decode([25216, 3274, 0, 357, 939, 59598])

print("Decoded Text is ",decoded)