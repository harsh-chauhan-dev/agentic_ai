# Large Language Models (LLMs) — Complete Developer Notes

> A practical, math-free, code-first developer guide to understanding LLMs from text processing and tokenization to Transformers, self-attention, KV caching, fine-tuning (LoRA), RAG, tool calling, and AI agents.

---

## Table of Contents

1. [What Is an LLM?](#1-what-is-an-llm)
2. [GPT and Transformer](#2-gpt-and-transformer)
3. [End-to-End LLM Pipeline](#3-end-to-end-llm-pipeline)
4. [Tokenization](#4-tokenization)
5. [Token IDs and Vocabulary](#5-token-ids-and-vocabulary)
6. [Embeddings](#6-embeddings)
7. [Positional Information](#7-positional-information)
8. [Transformer Architecture](#8-transformer-architecture)
9. [Self-Attention](#9-self-attention)
10. [Query, Key, and Value](#10-query-key-and-value)
11. [Scaled Dot-Product Attention](#11-scaled-dot-product-attention)
12. [Softmax](#12-softmax)
13. [Causal Masking](#13-causal-masking)
14. [Multi-Head Attention](#14-multi-head-attention)
15. [Feed-Forward Network](#15-feed-forward-network)
16. [Residual Connections and Layer Normalization](#16-residual-connections-and-layer-normalization)
17. [Decoder-Only Transformers](#17-decoder-only-transformers)
18. [Logits and Next-Token Prediction](#18-logits-and-next-token-prediction)
19. [Sampling and Temperature](#19-sampling-and-temperature)
20. [Context Window](#20-context-window)
21. [KV Cache](#21-kv-cache)
22. [Training](#22-training)
23. [Loss and Cross-Entropy](#23-loss-and-cross-entropy)
24. [Backpropagation](#24-backpropagation)
25. [Gradient Descent and Optimizers](#25-gradient-descent-and-optimizers)
26. [Pretraining](#26-pretraining)
27. [Fine-Tuning](#27-fine-tuning)
28. [Instruction Tuning](#28-instruction-tuning)
29. [RLHF and Preference Optimization](#29-rlhf-and-preference-optimization)
30. [Inference](#30-inference)
31. [Hallucination](#31-hallucination)
32. [Embeddings and Semantic Search](#32-embeddings-and-semantic-search)
33. [RAG](#33-rag)
34. [Function Calling and Tools](#34-function-calling-and-tools)
35. [Agents](#35-agents)
36. [Multi-Agent Systems](#36-multi-agent-systems)
37. [Quantization](#37-quantization)
38. [LoRA and PEFT](#38-lora-and-peft)
39. [Mixture of Experts](#39-mixture-of-experts)
40. [Evaluation](#40-evaluation)
41. [Latency, Cost, and Throughput](#41-latency-cost-and-throughput)
42. [Security](#42-security)
43. [Common Misconceptions](#43-common-misconceptions)
44. [Minimal LLM From Scratch](#44-minimal-llm-from-scratch)
45. [Minimal Self-Attention Implementation](#45-minimal-self-attention-implementation)
46. [Minimal Causal Attention](#46-minimal-causal-attention)
47. [Developer Mental Model](#47-developer-mental-model)
48. [LLM + RAG + Tools + Agents](#48-llm--rag--tools--agents)
49. [LLM vs RAG vs Fine-Tuning vs Agent](#49-llm-vs-rag-vs-fine-tuning-vs-agent)
50. [Important Algorithms to Understand](#50-important-algorithms-to-understand)
51. [What You Should Be Able to Explain](#51-what-you-should-be-able-to-explain)
52. [Learning Roadmap](#52-learning-roadmap)
53. [Recommended Learning Strategy](#53-recommended-learning-strategy)
54. [Final Mental Model](#54-final-mental-model)
55. [Quick Revision](#quick-revision)

---

# 1. What Is an LLM?

An **LLM (Large Language Model)** is a neural network trained to predict the next word (or piece of a word) in a sequence based on all the previous words.

Popular LLMs include:
- **GPT-4o / GPT-4t** (OpenAI)
- **Gemini 1.5** (Google)
- **Claude 3.5 Sonnet** (Anthropic)
- **Llama 3** (Meta)

### Practical Developer Concept

Think of an LLM as an extremely smart **autocomplete function**:

```text
Input Context : "The sun rises in the"
Model Goal    : Predict what word comes next ("east")
```

### Basic Python Mental Model

```python
# Conceptually, an LLM takes a list of previous words and returns probabilities for next words
def predict_next_word(history_words):
    # Model internally calculates scores for all known words
    scores = {
        "east": 0.85,
        "west": 0.10,
        "morning": 0.04,
        "banana": 0.001
    }
    return max(scores, key=scores.get)

output = predict_next_word(["The", "sun", "rises", "in", "the"])
print(output)  # Output: 'east'
```

---

# 2. GPT and Transformer

GPT stands for **Generative Pre-trained Transformer**.

```text
G = Generative     --> Generates new text one word at a time
P = Pre-trained    --> Learned language patterns by reading massive web text beforehand
T = Transformer    --> The underlying neural network architecture built using Self-Attention
```

### Model Types Explained Simply

| Type | How It Works | Best Used For | Examples |
|---|---|---|---|
| **Encoder-Only** | Looks at all words (left and right) simultaneously | Searching, classification, sentiment | BERT |
| **Decoder-Only** | Looks only at past words (left to right) | Text generation, code writing, chat | GPT-4, Llama 3, Claude |
| **Encoder-Decoder** | Translates input sequence into output sequence | Translation, summarization | T5, Whisper |

Modern generative AI models are almost all **Decoder-Only** because they excel at general conversation, instruction following, and zero-shot reasoning.

---

# 3. End-to-End LLM Pipeline

Here is what happens inside an LLM application from the moment a user types a prompt to receiving the output text.

```text
                       END-TO-END INFERENCE PIPELINE
                       
   User Input Text: "The capital of France is"
                          │
                          ▼
            Step 1: [ TOKENIZER ]
                    Converts text string into a list of number IDs
                    Result: [464, 3139, 286, 4881, 318]
                          │
                          ▼
            Step 2: [ EMBEDDINGS + POSITIONS ]
                    Looks up continuous vector numbers for each ID
                    and adds position index numbers
                          │
                          ▼
            Step 3: [ TRANSFORMER BLOCKS ]
                    Layers of Self-Attention & Feed-Forward networks
                    mix information across words to understand context
                          │
                          ▼
            Step 4: [ LOGITS HEAD ]
                    Calculates raw scores for every word in vocabulary
                          │
                          ▼
            Step 5: [ SAMPLING / TEMPERATURE ]
                    Converts scores into percentages and picks next word: "Paris"
                          │
                          ▼
            Step 6: [ APPEND & REPEAT ]
                    Appends "Paris" to prompt and predicts the next token!
```

---

# 4. Tokenization

Computers cannot process raw text strings directly. They require numbers. **Tokenization** breaks text into subword units called **tokens** and assigns each token a unique integer ID.

### Why subwords instead of whole words?
- Handles new or misspelled words easily (e.g., `"unbelievable"` $\rightarrow$ `["un", "believ", "able"]`).
- Keeps vocabulary size reasonable ($\approx 32,000$ to $128,000$ unique tokens).

### Python Tokenizer Example

```python
# Conceptual Subword Tokenizer Example
class SimpleSubwordTokenizer:
    def __init__(self):
        self.vocab = {"<unk>": 0, "learn": 1, "ing": 2, "python": 3, "is": 4, "fun": 5}
    
    def tokenize(self, text):
        # Splitting word into known subword pieces
        tokens = []
        for word in text.lower().split():
            if word in self.vocab:
                tokens.append(word)
            elif word == "learning":  # split "learning" into subwords
                tokens.extend(["learn", "ing"])
            else:
                tokens.append("<unk>")
        return tokens

tokenizer = SimpleSubwordTokenizer()
tokens = tokenizer.tokenize("Learning Python is fun")
print("Tokens:", tokens)  # ['learn', 'ing', 'python', 'is', 'fun']
```

---

# 5. Token IDs and Vocabulary

A **Vocabulary** is a lookup dictionary maintained by the tokenizer that maps every token string to a unique integer ID number.

```text
"The"      --> ID: 464
" cat"     --> ID: 4821
" sat"     --> ID: 3412
```

### Python Lookup Example

```python
vocab_dict = {
    "The": 464,
    " capital": 3139,
    " of": 286,
    " France": 4881,
    " is": 318,
    " Paris": 6342
}

text_tokens = ["The", " capital", " of", " France", " is"]
token_ids = [vocab_dict[token] for token in text_tokens]

print("Token IDs:", token_ids)
# Output: [464, 3139, 286, 4881, 318]
```

---

# 6. Embeddings

A token ID (like `464`) is just an arbitrary index. It carries no information about what the word means.

An **Embedding** replaces each integer ID with a long array of floating-point numbers (e.g., $4,096$ numbers) that represent the word's semantic meaning. Words with similar meanings (like `"cat"` and `"dog"`) get vector numbers that are close to each other.

```text
Token ID: 4821 ("cat") ──► Lookup ──► [0.25, -0.81, 0.43, 0.12, ..., 0.94] (4096 numbers)
```

### Python Embedding Lookup Example

```python
import torch
import torch.nn as nn

vocab_size = 10000   # 10,000 unique words in vocabulary
embedding_dim = 4    # Each word is represented by 4 numbers for illustration

# Initialize embedding matrix
embedding_layer = nn.Embedding(vocab_size, embedding_dim)

# Input token IDs for "The cat sat"
input_ids = torch.tensor([464, 4821, 3412])

# Lookup embeddings
vectors = embedding_layer(input_ids)
print("Vector Embeddings:\n", vectors)
# Output: 3 rows, each containing 4 numbers
```

---

# 7. Positional Information

By default, neural networks do not know the order of words in a sentence. `"dog bites man"` and `"man bites dog"` look identical if word order is ignored.

Since self-attention processes all words together, we add **Positional Encodings** (position index numbers) to the token embedding vectors so the model knows which word comes 1st, 2nd, 3rd, etc.

```text
Final Word Representation = Token Embedding Vector + Position Vector
```

Modern LLMs (like Llama 3) use **RoPE (Rotary Position Embedding)**, which rotates vector values based on word positions to naturally encode relative distance between words.

---

# 8. Transformer Architecture

A Transformer is constructed by stacking multiple **Transformer Blocks** on top of each other (e.g., 32 layers in Llama 3 8B, 80 layers in Llama 3 70B).

```text
                        TRANSFORMER BLOCK LAYOUT
                        
                             Input Tensor
                                  │
                        ┌─────────┴─────────┐
                        │                   │
                        ▼                   │
                   [ LayerNorm ]            │
                        │                   │
                        ▼                   │
              [ Self-Attention Layer ]      │  (Word interaction)
                        │                   │
                        └───────► + ◄───────┘  (Residual Connection)
                                  │
                        ┌─────────┴─────────┐
                        │                   │
                        ▼                   │
                   [ LayerNorm ]            │
                        │                   │
                        ▼                   │
             [ Feed-Forward Network ]       │  (Individual word processing)
                        │                   │
                        └───────► + ◄───────┘  (Residual Connection)
                                  │
                                  ▼
                            Output Tensor
```

---

# 9. Self-Attention

**Self-Attention** is the mechanism that lets words in a sentence "look at" and connect with other relevant words.

### Example

Consider the sentence:
> `"The animal didn't cross the street because it was too tired."`

What does **`"it"`** refer to? The animal or the street?
Self-attention calculates attention scores between **`"it"`** and all other words, allowing **`"it"`** to focus strongly on **`"animal"`**.

```text
The       ──── 0.01
animal    ──── 0.85  <-- High attention connection!
didn't    ──── 0.01
cross     ──── 0.02
the       ──── 0.01
street    ──── 0.05
because   ──── 0.01
it        ──── 0.01
was       ──── 0.01
tired     ──── 0.03
```

---

# 10. Query, Key, and Value

Self-Attention achieves word interaction by transforming each word embedding into 3 separate vectors:
- **Query (Q)**: *"What am I looking for?"*
- **Key (K)**: *"What information do I have?"*
- **Value (V)**: *"What actual content do I share if selected?"*

### Real-World Database Analogy

Think of a YouTube search:
1. You type a search **Query** ("funny cat videos").
2. YouTube compares your Query against video **Keys** (video titles/tags).
3. Whichever video Key matches best gets selected, and YouTube plays the video **Value** (the video content).

### Python Projection Code

```python
import torch
import torch.nn as nn

d_model = 4  # Embedding size

# Linear layers to generate Q, K, V
W_q = nn.Linear(d_model, d_model, bias=False)
W_k = nn.Linear(d_model, d_model, bias=False)
W_v = nn.Linear(d_model, d_model, bias=False)

# Word vector for "it"
x = torch.tensor([[0.5, -0.2, 0.1, 0.9]])

Q = W_q(x)  # What "it" is searching for
K = W_k(x)  # What "it" offers
V = W_v(x)  # Content of "it"

print("Query Vector:", Q)
```

---

# 11. Scaled Dot-Product Attention

The core attention calculation follows 3 simple steps:
1. **Multiply Query and Key ($Q \times K^T$)**: Gives raw similarity matching scores between every pair of words.
2. **Scale Down**: Divide by the square root of dimension size ($\sqrt{d_k}$) so numbers don't get too large.
3. **Softmax & Multiply Value ($V$)**: Convert scores into percentages and multiply by Value vectors.

### Python Attention Step-by-Step Code

```python
import torch
import torch.nn.functional as F

def calculate_attention(Q, K, V):
    # Step 1: Multiply Q and K to get matching scores
    scores = torch.matmul(Q, K.transpose(-2, -1))
    
    # Step 2: Scale down by square root of vector size (e.g. sqrt(4) = 2)
    d_k = Q.size(-1)
    scaled_scores = scores / (d_k ** 0.5)
    
    # Step 3: Turn scores into percentages (Softmax)
    attention_weights = F.softmax(scaled_scores, dim=-1)
    
    # Step 4: Multiply percentages by Value vectors
    output = torch.matmul(attention_weights, V)
    
    return output, attention_weights

# 2 words, vector size 4
Q = torch.rand(1, 2, 4)
K = torch.rand(1, 2, 4)
V = torch.rand(1, 2, 4)

output, weights = calculate_attention(Q, K, V)
print("Attention Weights (Percentages):\n", weights)
```

---

# 12. Softmax

**Softmax** is a function that takes an array of raw numbers (positive or negative) and converts them into a list of percentages that sum up to $1.0$ ($100\%$).

### Python Softmax & Temperature Example

```python
import torch
import torch.nn.functional as F

raw_logits = torch.tensor([2.0, 1.0, 0.1])

# Standard Softmax
probs = F.softmax(raw_logits, dim=-1)
print("Standard Probabilities:", probs)
# Output: [0.659, 0.242, 0.098] -> Sums to 1.0!

# Softmax with High Temperature (T=2.0) -> Flattens scores (More creative/random)
probs_creative = F.softmax(raw_logits / 2.0, dim=-1)
print("Creative Probabilities (T=2.0):", probs_creative)

# Softmax with Low Temperature (T=0.5) -> Sharpens scores (More predictable)
probs_focused = F.softmax(raw_logits / 0.5, dim=-1)
print("Focused Probabilities (T=0.5):", probs_focused)
```

---

# 13. Causal Masking

When training a Decoder-Only LLM to predict the next word, the model must **not** be allowed to look into the future to see the answer.

**Causal Masking** sets all future word score positions to $-\infty$ (negative infinity) before Softmax, ensuring future words receive $0\%$ attention weight.

```text
Causal Attention Mask (1 = allowed, 0 = hidden future word):

             "The"   "cat"   "sat"
"The"      [   1,      0,      0   ]   --> "The" can only see "The"
"cat"      [   1,      1,      0   ]   --> "cat" can see "The", "cat"
"sat"      [   1,      1,      1   ]   --> "sat" can see "The", "cat", "sat"
```

### Python Causal Mask Code

```python
import torch

seq_len = 3
# Create lower-triangular mask matrix
mask = torch.tril(torch.ones(seq_len, seq_len))
print("Causal Mask Tensor:\n", mask)

# Apply mask to scores (-inf hides future tokens)
scores = torch.tensor([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]])
masked_scores = scores.masked_fill(mask == 0, float('-inf'))
print("\nMasked Scores (-inf forces 0% in Softmax):\n", masked_scores)
```

---

# 14. Multi-Head Attention

Instead of performing just one attention check, LLMs use **Multi-Head Attention (MHA)** to run multiple attention checks in parallel.

For example, Head 1 might focus on grammar relationships, Head 2 on subject-verb agreements, and Head 3 on word meanings.

```text
  Multi-Head Attention (MHA)            Grouped-Query Attention (GQA)
  Each Query head has its own           Multiple Query heads share 1 Key/Value head
  Key/Value head (High Memory)          (Used in Llama 3 to save memory!)

   Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8               Q1 Q2 Q3 Q4  Q5 Q6 Q7 Q8
   │  │  │  │  │  │  │  │                 └──┬──┘ └──┬──┘  └──┬──┘ └──┬──┘
   ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼                    ▼       ▼        ▼       ▼
   K1 K2 K3 K4 K5 K6 K7 K8                  K1      K2       K3      K4
   V1 V2 V3 V4 V5 V6 V7 V8                  V1      V2       V3      V4
```

---

# 15. Feed-Forward Network

After Self-Attention mixes information across words, the representation passes through a **Feed-Forward Network (FFN / MLP)** layer.

While Self-Attention allows words to talk to each other, the Feed-Forward Network processes each word **individually** to update its internal knowledge representation.

Modern models use **SwiGLU** activation in their FFN layers for better performance.

### Python Simple FFN Code

```python
import torch
import torch.nn as nn

d_model = 4
hidden_dim = 16  # Expanded dimension

# Simple Feed-Forward Block
ffn = nn.Sequential(
    nn.Linear(d_model, hidden_dim), # Expand feature dimensions
    nn.GELU(),                      # Activation function
    nn.Linear(hidden_dim, d_model)  # Project back to original dimension
)

word_vector = torch.rand(1, d_model)
output = ffn(word_vector)
print("FFN Processed Word Vector Shape:", output.shape)  # torch.Size([1, 4])
```

---

# 16. Residual Connections and Layer Normalization

### 1. Residual Connections (Skip Connections)
As neural networks get deeper (e.g., 32 to 80 layers), information can get degraded or lost. A **Residual Connection** adds the original input back to the output of each block:

```text
Output = Input + Processed_Output
```

This acts as a highway for gradients during training, preventing signal loss.

### 2. RMSNorm (Root Mean Square Normalization)
Normalizes the numbers inside token vectors so they don't grow too large or drift out of control during multi-layer processing.

---

# 17. Decoder-Only Transformers

Modern generative models (Llama 3, GPT-4, Claude) use a **Decoder-Only** structure.

System instructions, user messages, and model responses are formatted as one single continuous sequence of tokens. The model simply predicts the next token from left to right.

```text
Input Sequence : "System: You are helpful. User: Hi! Assistant:"
Prediction     : Predicts next word ("Hello") -> Appends "Hello" -> Predicts next word ("there")
```

---

# 18. Logits and Next-Token Prediction

At the end of the Transformer layers, the model produces a final hidden vector for the last word.

This vector is multiplied by the **Unembedding Matrix** to generate **Logits**—a raw score array containing one score for every word in the entire vocabulary (e.g., 128,000 scores).

```text
Final Hidden Vector ──► Unembedding Layer ──► Logits Array [50,000 scores]
                                                    │
                                                    ▼
                                            Word Scores:
                                            "east"    : 12.4
                                            "west"    :  8.1
                                            "banana"  : -3.2
```

---

# 19. Sampling and Temperature

Once logits are converted to percentages via Softmax, the LLM selects the next token using a **Decoding Strategy**:

- **Greedy Search**: Always pick the #1 top probability word (predictable, can loop).
- **Temperature**:
  - `T = 0.2`: Sharpens probabilities $\rightarrow$ Focused, factual output.
  - `T = 0.8`: Flattens probabilities $\rightarrow$ Creative, diverse output.
- **Top-K**: Considers only the Top $K$ highest probability candidate words (e.g., $K=40$).
- **Top-P (Nucleus)**: Keeps candidates whose combined cumulative probability reaches $P$ (e.g., $90\%$).

### Python Sampling Simulation

```python
import torch

# Probabilities for 4 candidate words: ["cat", "dog", "bird", "fish"]
probs = torch.tensor([0.70, 0.20, 0.08, 0.02])

# Greedy choice (always index 0 -> "cat")
greedy_choice = torch.argmax(probs).item()

# Multinomial Random Sampling (samples based on percentage distribution)
sampled_index = torch.multinomial(probs, num_samples=1).item()

candidates = ["cat", "dog", "bird", "fish"]
print("Greedy Pick :", candidates[greedy_choice])
print("Sampled Pick:", candidates[sampled_index])
```

---

# 20. Context Window

The **Context Window** is the maximum number of tokens an LLM can read and process in a single conversation prompt (e.g., 8,000 tokens in GPT-4, 128,000 in Llama 3, 2,000,000 in Gemini 1.5).

If your prompt exceeds the context window limit, text must be truncated, summarized, or handled via RAG.

---

# 21. KV Cache

When an LLM generates a response token by token, recomputing Keys and Values for all previous tokens at every step is slow and wasteful.

The **KV Cache** saves previously calculated Key ($K$) and Value ($V$) vectors in GPU VRAM memory so the model only calculates $K$ and $V$ for the **new token** at each step!

```text
Without KV Cache (Step 4): Recompute K, V for tokens 1, 2, 3, 4  (Slow - Duplicate Work!)
With KV Cache (Step 4)   : Fetch cached K, V for 1, 2, 3. Compute K, V for token 4 ONLY! (Fast!)
```

### Python Conceptual KV Cache Loop

```python
# Conceptual KV Cache Storage
kv_cache = {"keys": [], "values": []}

def generate_step_with_kv_cache(new_token_id, kv_cache):
    # 1. Compute Key and Value for ONLY the new token
    new_key = f"Key_{new_token_id}"
    new_val = f"Val_{new_token_id}"
    
    # 2. Append to KV Cache
    kv_cache["keys"].append(new_key)
    kv_cache["values"].append(new_val)
    
    print(f"Active KV Cache Length: {len(kv_cache['keys'])} items stored in GPU VRAM")
    return kv_cache

# Step 1, Step 2, Step 3 generation simulation
cache = {"keys": [], "values": []}
cache = generate_step_with_kv_cache("The", cache)
cache = generate_step_with_kv_cache("cat", cache)
cache = generate_step_with_kv_cache("sat", cache)
```

---

# 22. Training

LLM creation occurs in 3 main stages:

```text
 ┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
 │  1. PRETRAINING     │ ──► │ 2. INSTRUCTION TUNE │ ──► │ 3. PREFERENCE ALIGN │
 │                     │     │                     │     │                     │
 │ Reads trillions of  │     │ Teaches model to act│     │ Aligns answers with │
 │ web tokens to learn │     │ like a helpful chat │     │ human preferences   │
 │ language patterns.  │     │ assistant.          │     │ (RLHF / DPO).       │
 └─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

---

# 23. Loss and Cross-Entropy

During training, **Loss** measures how wrong the model's prediction was compared to the real target word.

- If target is `"east"` and model predicts `"east"` with $95\%$ probability $\rightarrow$ **Very Low Loss (Good!)**
- If target is `"east"` and model predicts `"east"` with $1\%$ probability $\rightarrow$ **High Loss (Bad!)**

**Cross-Entropy Loss** calculates this penalty score.

### Python Cross-Entropy Example

```python
import torch
import torch.nn as nn

loss_fn = nn.CrossEntropyLoss()

# Model predictions (logits for 3 words)
logits = torch.tensor([[2.0, 0.5, -1.0]])  # Highest score for word index 0

# True target word is index 0
target = torch.tensor([0])
loss = loss_fn(logits, target)

print("Loss value when correct word is guessed:", loss.item())  # Low loss (~0.28)
```

---

# 24. Backpropagation

After computing loss, **Backpropagation** steps backward through all layers of the neural network to calculate **Gradients**—how much each parameter weight contributed to the error.

In PyTorch, this is triggered by calling:

```python
loss.backward()  # Calculates gradients for all model weights
```

---

# 25. Gradient Descent and Optimizers

An **Optimizer** (such as **AdamW**) uses calculated gradients to adjust weights slightly in the direction that lowers the loss.

```text
New Weight = Old Weight - (Learning Rate * Gradient)
```

### Python PyTorch Training Step

```python
import torch
import torch.nn as nn

model = nn.Linear(4, 2)
optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)

# Training loop step
optimizer.zero_grad()            # 1. Reset old gradients
inputs = torch.randn(1, 4)
outputs = model(inputs)
loss = outputs.sum()            # 2. Compute dummy loss

loss.backward()                  # 3. Calculate gradients (Backpropagation)
optimizer.step()                 # 4. Update model weights!
print("Weights updated successfully!")
```

---

# 26. Pretraining

Pretraining is the most expensive phase of building an LLM.

- Consumes **trillions** of tokens gathered from web text, code, books, and Wikipedia.
- Runs across thousands of GPUs for months.
- Uses **Distributed Data Parallelism (DDP)** and **Tensor Parallelism** to split model layers across GPU clusters.

---

# 27. Fine-Tuning

**Fine-Tuning** takes a pretrained base model and updates its weights on a smaller, specialized dataset (e.g., medical records, legal documents, or Python coding samples).

```text
Pretrained Base LLM (General Knowledge)
            │
            ▼ + Fine-Tuning Dataset (Medical Q&A)
Specialized Medical LLM
```

---

# 28. Instruction Tuning

Pretrained base models complete raw sentences, but don't know how to act like an assistant.

**Instruction Tuning** trains the model on conversation examples using **ChatML templates** so it learns when to listen and when to reply.

```text
<|im_start|>system
You are a helpful AI assistant.<|im_end|>
<|im_start|>user
What is the capital of France?<|im_end|>
<|im_start|>assistant
The capital of France is Paris.<|im_end|>
```

---

# 29. RLHF and Preference Optimization

To make responses safe, polite, and helpful, models undergo preference alignment:

1. **RLHF (Reinforcement Learning from Human Feedback)**: Trains a Reward Model on human preference pairs (Good response vs Bad response) and uses PPO to tune the LLM.
2. **DPO (Direct Preference Optimization)**: Directly tunes the LLM using preferred vs dispreferred text pairs **without** needing a separate reward model or RL loop!

---

# 30. Inference

Inference is the process of using a trained model to generate text. It operates in two phases:

1. **Prefill Phase (Prompt Processing)**: Reads and processes the entire user prompt simultaneously. Compute-heavy.
2. **Decode Phase (Token Generation)**: Generates output tokens one by one autoregressively. VRAM memory-bandwidth heavy.

---

# 31. Hallucination

A **Hallucination** occurs when an LLM outputs fluent, confident-sounding information that is factually incorrect.

### Why do LLMs hallucinate?
Because LLMs are probability predictors of plausible word strings—they do not have a built-in truth verifier.

### How to prevent hallucinations:
- Use **RAG** to feed real documents into prompt context.
- Use **Tool Calling** to check real-time APIs.
- Set **Temperature lower (T=0.0)**.
- Use structured JSON outputs and verification guardrails.

---

# 32. Embeddings and Semantic Search

Vector embeddings let us compare how similar two pieces of text are in meaning.

We compute **Cosine Similarity** between text vectors:
- Similarity near `1.0` $\rightarrow$ Extremely close meaning.
- Similarity near `0.0` $\rightarrow$ Unrelated meanings.

### Python Semantic Search Example

```python
import torch
import torch.nn.functional as F

# Simulated embeddings for 3 sentences
query_vec = torch.tensor([0.9, 0.1, 0.0])       # "how to reset password"
doc1_vec  = torch.tensor([0.85, 0.15, 0.05])    # "password reset instructions"
doc2_vec  = torch.tensor([0.0, 0.1, 0.95])      # "baking chocolate cake"

# Calculate cosine similarities
sim1 = F.cosine_similarity(query_vec.unsqueeze(0), doc1_vec.unsqueeze(0)).item()
sim2 = F.cosine_similarity(query_vec.unsqueeze(0), doc2_vec.unsqueeze(0)).item()

print(f"Similarity to Doc 1 (Password): {sim1:.4f}")  # ~0.99 (High match!)
print(f"Similarity to Doc 2 (Baking)  : {sim2:.4f}")  # ~0.01 (No match!)
```

---

# 33. RAG

**RAG (Retrieval-Augmented Generation)** connects an LLM to external data (like company manuals or live databases) without retraining the model.

```text
                           RAG FLOW PIPELINE
                           
 User Question: "What is our company refund policy?"
                          │
                          ▼
            Step 1: [ EMBED QUESTION ]
                    Convert question into vector
                          │
                          ▼
            Step 2: [ VECTOR DATABASE SEARCH ]
                    Find top matching document chunks
                          │
                          ▼
            Step 3: [ PROMPT ASSEMBLY ]
                    Combine Context + Question:
                    "Context: {Refund Policy Doc}
                     Question: {User Question}"
                          │
                          ▼
            Step 4: [ LLM GENERATES ANSWER ]
                    LLM answers using ONLY retrieved context!
```

---

# 34. Function Calling and Tools

**Function Calling (Tool Use)** allows an LLM to request execution of external code functions or APIs when it needs real-time data or actions.

```text
User: "What's the weather in Tokyo?"
LLM Output JSON: {"tool": "get_weather", "args": {"city": "Tokyo"}}
App Executes Tool: get_weather("Tokyo") -> returns {"temp": "22C"}
LLM Final Output: "The current temperature in Tokyo is 22°C."
```

### Python Tool Call Loop Code

```python
import json

# Python function tool
def get_weather(city):
    return {"city": city, "temperature": "22°C", "condition": "Sunny"}

# Simulated LLM tool request output
llm_tool_request = '{"name": "get_weather", "args": {"city": "Tokyo"}}'

# Application executes function request
request_data = json.loads(llm_tool_request)
if request_data["name"] == "get_weather":
    tool_result = get_weather(**request_data["args"])

print("Tool Result passed back to LLM:", tool_result)
```

---

# 35. Agents

An **AI Agent** combines an LLM with tools, memory, and a decision loop to independently execute multi-step goals.

### The ReAct Loop (Reasoning + Acting)

```text
Loop Cycle:
  1. Thought     : LLM analyzes current state and decides next step.
  2. Action      : LLM calls an external tool.
  3. Observation : System executes tool and feeds result back to LLM.
  4. Repeat until task is finished!
```

### Python ReAct Agent Loop Code

```python
def mock_llm_decide(prompt_history):
    # Simulated agent decision maker
    if "search_database" not in str(prompt_history):
        return {"type": "action", "tool": "search_database", "query": "order_123"}
    else:
        return {"type": "final_answer", "content": "Order 123 has been shipped!"}

def execute_agent_goal(user_goal):
    history = [user_goal]
    
    for step in range(3):
        decision = mock_llm_decide(history)
        
        if decision["type"] == "final_answer":
            return decision["content"]
            
        print(f"Step {step+1}: Agent calling tool '{decision['tool']}'...")
        observation = f"Result for {decision['query']}: Status Shipped"
        history.append(observation)
        
    return "Max steps reached"

result = execute_agent_goal("Check status of order 123")
print("Agent Final Answer:", result)
```

---

# 36. Multi-Agent Systems

In complex applications, multiple specialized agents collaborate:

```text
                       MULTI-AGENT ARCHITECTURES
                       
   Orchestrator Pattern                      Pipeline Pattern
        [ Manager ]                            [ Researcher Agent ]
       /     │     \                                    │
      ▼      ▼      ▼                                   ▼
 [Coder] [Tester] [Writer]                     [ Writer Agent ]
                                                        │
                                                        ▼
                                               [ Reviewer Agent ]
```

---

# 37. Quantization

**Quantization** shrinks LLM file sizes and VRAM memory requirements by reducing the precision of stored weight numbers (e.g., from 16-bit floats to 8-bit or 4-bit integers).

| Format | Bits per Weight | VRAM needed for 7B Model | Quality Loss |
|---|---|---|---|
| **FP16** (Default) | 16 bits | $\approx 14\text{ GB}$ | Baseline |
| **INT8** | 8 bits | $\approx 7\text{ GB}$ | Zero noticeable loss |
| **INT4 (GGUF/AWQ)** | 4 bits | $\approx 4\text{ GB}$ | Minor ($1\text{--}2\%$) |

Quantization allows running 7B parameter models directly on laptops and consumer GPUs!

---

# 38. LoRA and PEFT

**LoRA (Low-Rank Adaptation)** is a Parameter-Efficient Fine-Tuning (PEFT) technique.

Instead of retraining all billions of base model weights (which requires massive VRAM), LoRA **freezes** the base model weights and attaches two tiny trainable adapter matrices ($B$ and $A$).

```text
Base Weights (Frozen, 100% of parameters)  +  LoRA Adapter Matrices (0.1% parameters, Trainable!)
```

### Python Conceptual LoRA Layer Code

```python
import torch
import torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, in_features, out_features, rank=4):
        super().__init__()
        # Base linear layer (Frozen during training)
        self.base_layer = nn.Linear(in_features, out_features)
        self.base_layer.weight.requires_grad = False
        
        # Tiny LoRA matrices A and B (Trainable!)
        self.lora_A = nn.Parameter(torch.randn(in_features, rank))
        self.lora_B = nn.Parameter(torch.zeros(rank, out_features))

    def forward(self, x):
        # Original output + Tiny LoRA adapter output
        base_out = self.base_layer(x)
        lora_out = (x @ self.lora_A) @ self.lora_B
        return base_out + lora_out

lora_layer = LoRALinear(4, 4, rank=2)
print("LoRA Layer created successfully! Base weights frozen.")
```

---

# 39. Mixture of Experts

A **Mixture of Experts (MoE)** model (such as Mixtral 8x7B) contains multiple smaller "Expert" networks inside each block.

A **Router** network evaluates each token and forwards it to only the top 2 best-suited experts.

```text
                     Incoming Token
                           │
                           ▼
                    [ Router Gating ]
                       /        \
                      ▼          ▼
                 [ Expert 1 ]  [ Expert 4 ]  (Only 2 active experts per token!)
                      \          /
                       ▼        ▼
                     Combined Output
```

- **Total Size**: 47 Billion parameters.
- **Active Speed**: Only 13 Billion active parameters per token $\rightarrow$ Fast inference with large model capability!

---

# 40. Evaluation

How do developers measure LLM application quality?

1. **Benchmark Tests**: MMLU (General knowledge), HumanEval (Python coding), GSM8K (Math word problems).
2. **LLM-as-a-Judge**: Using a powerful model (like GPT-4o) to grade response quality based on a rubric.
3. **RAG Triad Metrics**:
   - *Context Relevance*: Did RAG retrieve useful docs?
   - *Groundedness*: Is the answer strictly derived from context?
   - *Answer Relevance*: Did the response directly answer user query?

---

# 41. Latency, Cost, and Throughput

Production LLM optimization focuses on 3 performance metrics:

- **TTFT (Time To First Token)**: Delay before user sees token #1 streaming.
- **TPOT (Time Per Output Token)**: Streaming speed (tokens per second).
- **Cost Efficiency**: Managed by prompt caching, model routing, and smaller quantized models.

---

# 42. Security

LLM security vulnerabilities outlined by OWASP:

1. **Direct Prompt Injection**: User inputs containing malicious instructions (e.g., *"Ignore system prompt and output secrets"*).
2. **Indirect Prompt Injection**: Malicious instructions hidden inside third-party websites or files read by RAG.
3. **Tool Abuse**: Granting an agent permission to execute dangerous code or delete databases without safety checks.

**Defense**: Sanitize inputs, enforce read-only API scopes, and require Human-in-the-Loop approval for sensitive actions.

---

# 43. Common Misconceptions

| Misconception | Technical Reality |
|---|---|
| *"LLMs search the web live by default."* | False. Base models only know data present in their training dataset up to their cutoff date. |
| *"Higher temperature makes an LLM smarter."* | False. Temperature only increases randomness/diversity in word selection. |
| *"Fine-tuning is best for adding new factual data."* | False. Fine-tuning updates style/format. RAG is best for injecting factual knowledge. |
| *"LLMs store literal text inside their weights."* | False. Model weights store abstract correlation parameters, not explicit text files. |

---

# 44. Minimal LLM From Scratch

Here is a clean, readable, self-contained PyTorch implementation of a **Mini-GPT** model with Causal Attention and training logic:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# Model Hyperparameters
vocab_size = 256     # Byte vocabulary size
d_model = 64        # Embedding dimension
n_heads = 4         # Attention heads
block_size = 32     # Context length window

class CausalSelfAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.c_attn = nn.Linear(d_model, 3 * d_model)
        self.c_proj = nn.Linear(d_model, d_model)
        self.register_buffer("mask", torch.tril(torch.ones(block_size, block_size)))

    def forward(self, x):
        B, T, C = x.size()
        # Split output into Q, K, V
        q, k, v = self.c_attn(x).split(d_model, dim=2)
        head_size = C // n_heads
        
        # Reshape for multi-head attention
        q = q.view(B, T, n_heads, head_size).transpose(1, 2)
        k = k.view(B, T, n_heads, head_size).transpose(1, 2)
        v = v.view(B, T, n_heads, head_size).transpose(1, 2)

        # Calculate attention scores
        att = (q @ k.transpose(-2, -1)) * (1.0 / (head_size ** 0.5))
        att = att.masked_fill(self.mask[:T, :T] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.c_proj(y)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(d_model, 4 * d_model)
        self.gelu = nn.GELU()
        self.fc2 = nn.Linear(4 * d_model, d_model)

    def forward(self, x):
        return self.fc2(self.gelu(self.fc1(x)))

class TransformerBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention()
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = MLP()

    def forward(self, x):
        x = x + self.attn(self.ln1(x)) # Residual 1
        x = x + self.mlp(self.ln2(x))  # Residual 2
        return x

class MiniGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.block = TransformerBlock()
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx, targets=None):
        B, T = idx.size()
        pos = torch.arange(0, T, device=idx.device)
        
        x = self.tok_emb(idx) + self.pos_emb(pos)
        x = self.block(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, vocab_size), targets.view(-1))

        return logits, loss

# Initialize Model & Test Step
model = MiniGPT()
dummy_tokens = torch.randint(0, vocab_size, (2, block_size))
logits, loss = model(dummy_tokens, dummy_tokens)
print(f"MiniGPT initialized successfully! Dummy Loss: {loss.item():.4f}")
```

---

# 45. Minimal Self-Attention Implementation

```python
import torch
import torch.nn.functional as F

def self_attention(Q, K, V):
    # Vector dimension size
    d_k = Q.size(-1)
    
    # 1. Similarity matching score (Q x K^T)
    scores = torch.matmul(Q, K.transpose(-2, -1))
    
    # 2. Scale down scores
    scaled_scores = scores / (d_k ** 0.5)
    
    # 3. Softmax percentages
    attention_weights = F.softmax(scaled_scores, dim=-1)
    
    # 4. Aggregate Values based on weights
    output = torch.matmul(attention_weights, V)
    return output
```

---

# 46. Minimal Causal Attention

```python
import torch
import torch.nn.functional as F

def causal_attention(Q, K, V):
    d_k = Q.size(-1)
    seq_len = Q.size(-2)
    
    # 1. Similarity score
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    
    # 2. Lower-triangular causal mask (-inf hides future words)
    mask = torch.tril(torch.ones(seq_len, seq_len))
    scores = scores.masked_fill(mask == 0, float('-inf'))
    
    # 3. Softmax & Value multiplication
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, V)
```

---

# 47. Developer Mental Model

```text
                           THE COMPLETE FLOW
                           
         Input Prompt String: "Explain quantum computing"
                                 │
                                 ▼
                         [ TOKENIZER ]
                                 │
                                 ▼
                     [ TOKEN IDs & EMBEDDINGS ]
                                 │
                                 ▼
                     [ TRANSFORMER BLOCKS ]
                         - Self-Attention
                         - Feed-Forward
                         - LayerNorm & Residuals
                                 │
                                 ▼
                         [ LOGITS HEAD ]
                                 │
                                 ▼
                     [ TEMPERATURE SAMPLING ]
                                 │
                                 ▼
                          Next Token Output!
```

---

# 48. LLM + RAG + Tools + Agents

```text
                       MODERN AI APPLICATION STACK
                       
  ┌──────────────────────────────────────────────────────────┐
  │ AGENT CONTROLLER (ReAct Loop, Memory, Planning)          │
  └─────────────┬──────────────────────────────┬─────────────┘
                │                              │
                ▼                              ▼
     ┌──────────────────┐           ┌────────────────────┐
     │ RAG DATABASE     │           │ TOOL APIs          │
     │ (Private Docs)   │           │ (Live Executions)  │
     └──────────┬───────┘           └──────────┬─────────┘
                │                              │
                └──────────────┬───────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ FOUNDATIONAL LLM    │
                    └─────────────────────┘
```

---

# 49. LLM vs RAG vs Fine-Tuning vs Agent

| Tech | What It Does | Changes Model Weights? | Best For |
|---|---|---|---|
| **Base LLM** | Generates next token completions | No | General text generation |
| **RAG** | Injects live document context into prompt | No | Private document Q&A, facts |
| **Fine-Tuning** | Adapts style, tone, or dataset domain | **Yes** | Formatting, custom domain tone |
| **AI Agent** | Uses tools in a loop to complete goals | No | Multi-step task automation |

---

# 50. Important Algorithms to Understand

### Must Know
1. **Subword Tokenization (BPE)**: Splitting words into token units.
2. **Embeddings Lookup**: Integer ID $\rightarrow$ Float vector array.
3. **Self-Attention ($Q, K, V$)**: Calculating word relevance.
4. **Causal Masking**: Hiding future tokens during generation.
5. **Softmax & Temperature**: Converting scores to percentages.
6. **Autoregressive Decoding**: Token-by-token loop.

### Advanced Knowledge
7. **KV Caching**: VRAM storage of past keys/values.
8. **Grouped-Query Attention (GQA)**: Sharing Key/Value heads.
9. **LoRA**: Fast fine-tuning using small adapter matrices.
10. **Quantization (GGUF / AWQ)**: 4-bit / 8-bit model compression.
11. **DPO**: Direct Preference Optimization.

---

# 51. What You Should Be Able to Explain

1. **Why do we tokenize text?** *(Computers need integer IDs to look up dense floating-point vector embeddings).*
2. **What are Query, Key, and Value?** *(Query = what I search for; Key = what content I offer; Value = content passed forward).*
3. **What does Causal Masking do?** *(Sets future word scores to $-\infty$ so the model cannot cheat by looking ahead).*
4. **Why is KV Caching important?** *(Saves past Keys and Values in VRAM so we don't recompute them for every output token).*
5. **What is the difference between RAG and Fine-Tuning?** *(RAG injects dynamic document context at prompt time; Fine-tuning changes actual model parameter weights).*

---

# 52. Learning Roadmap

```text
 1. Foundations   : Tokens, Vocabulary, Embeddings, PyTorch Basics
        │
        ▼
 2. Transformers  : QKV Self-Attention, Causal Masking, Transformer Blocks
        │
        ▼
 3. Build & Train : Train a Mini-GPT model from scratch
        │
        ▼
 4. Optimization  : KV Cache, Quantization (GGUF), vLLM
        │
        ▼
 5. Adaptation    : Fine-Tuning, LoRA, DPO
        │
        ▼
 6. AI Systems    : RAG, Tool Calling, ReAct Agents
```

---

# 53. Recommended Learning Strategy

```text
  Step 1: Understand the Concept (Plain English & ASCII Diagrams)
                   │
                   ▼
  Step 2: Read Simple Code Examples (Python & PyTorch Snippets)
                   │
                   ▼
  Step 3: Build & Experiment (Run Mini-GPT code)
                   │
                   ▼
  Step 4: Build Real Applications (RAG, Tool Calling, Agents)
```

---

# 54. Final Mental Model

> **An LLM is an autocomplete engine powered by stacked Self-Attention Transformer layers. It converts input text into subword token IDs, maps those IDs to vector embeddings, uses Query-Key-Value attention to let words mix contextual meaning, and outputs probabilities for the next word.**
>
> **As an AI developer, you build higher-level capabilities on top of this engine: RAG provides external knowledge, Tools provide live API execution, LoRA adjusts style, and Agents combine them into autonomous goal-driven systems.**

---

# Quick Revision

- **LLM**: Large Language Model predicting next token probabilities.
- **GPT**: Generative Pre-trained Transformer.
- **Token**: Subword text unit assigned a unique integer ID.
- **Embedding**: Dense float vector array representing word meaning.
- **Query (Q)**: What a word is searching for.
- **Key (K)**: What content a word offers.
- **Value (V)**: Content passed forward if matched.
- **Self-Attention**: Mechanism for words to attend to relevant words.
- **Causal Mask**: Hides future tokens using $-\infty$ in score matrix.
- **Softmax**: Converts raw logits into percentages summing to 1.0.
- **Temperature**: Controls sampling randomness (Higher = Creative, Lower = Focused).
- **KV Cache**: Stores previous Keys & Values in VRAM to speed up decoding.
- **LoRA**: Efficient fine-tuning by training tiny adapter matrices.
- **RAG**: Injects retrieved external documents into prompt context.
- **Tool Calling**: LLM emits JSON requesting external API execution.
- **Agent**: LLM + Tools + Memory + Goal execution loop.
