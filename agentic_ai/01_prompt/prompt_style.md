# Prompt Style
# 1. Alpaca-Style Prompting

**What?**
Structured prompt format:

```text id="a1"
Instruction → What to do
Input       → Data / Question
Response    → Expected output
```

**Example:**

```text id="a2"
### Instruction:
Translate the sentence to Hindi.

### Input:
I am learning Python.

### Response:
मैं Python सीख रहा हूँ।
```

**Who uses it?**
Originally popularized through **Stanford Alpaca** and instruction-tuning datasets.

**Key:**
**Alpaca = Instruction + Input + Response**

---

# 2. ChatML

**What?**
Format for representing conversations using **roles**:

```text id="a3"
system → Rules / behavior
user → User message
assistant → Model response
```

**Example:**

```text id="a4"
<|system|>
You are a Python tutor.

<|user|>
What is a list in Python?

<|assistant|>
A list is an ordered, mutable collection.
```

**Who uses it?**
Popularized by **OpenAI** for structured chat-style interactions.

**Key:**
**ChatML = Role + Message**

---

# 3. Instruction Prompting

**What?**
Directly telling the LLM **what task to perform**.

**Example:**

```text id="a5"
Instruction:
Summarize the following text in 3 bullet points.

Input:
[Text]
```

**Who uses it?**
Used broadly by **OpenAI, Google, Anthropic, Meta**, and other LLM systems.

**Key:**
**Instruction Prompting = Clear command to the model**

---

### Quick Revision

| Style                     | Main Idea                      | Common Association |
| ------------------------- | ------------------------------ | ------------------ |
| **Alpaca**                | Instruction + Input + Response | Stanford Alpaca    |
| **ChatML**                | Roles + Messages               | OpenAI             |
| **Instruction Prompting** | Direct task instruction        | Most modern LLMs   |
