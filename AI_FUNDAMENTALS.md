# AI & LLM Fundamentals — Study Notes

A complete reference covering how modern AI models work: from tokenization to deployment. Each section has a **concise definition**, **key details**, and a **code example**.

## Table of Contents
- [AI \& LLM Fundamentals — Study Notes](#ai--llm-fundamentals--study-notes)
  - [Table of Contents](#table-of-contents)
  - [1. Large Language Models (LLMs)](#1-large-language-models-llms)
  - [2. Tokenization](#2-tokenization)
  - [3. Vectorization / Embeddings](#3-vectorization--embeddings)
  - [4. Attention Mechanism](#4-attention-mechanism)
  - [5. Self-Supervised Learning](#5-self-supervised-learning)
  - [6. Transformer Architecture](#6-transformer-architecture)
  - [7. Fine-tuning](#7-fine-tuning)
  - [8. Few-shot Prompting](#8-few-shot-prompting)
  - [9. Retrieval Augmented Generation (RAG)](#9-retrieval-augmented-generation-rag)
  - [10. Vector Databases](#10-vector-databases)
  - [11. Model Context Protocol (MCP)](#11-model-context-protocol-mcp)
  - [12. Context Engineering](#12-context-engineering)
  - [13. Agents](#13-agents)
  - [14. Reinforcement Learning (RLHF)](#14-reinforcement-learning-rlhf)
  - [15. Chain of Thought (CoT)](#15-chain-of-thought-cot)
  - [16. Reasoning Models](#16-reasoning-models)
  - [17. Multi-modal Models](#17-multi-modal-models)
  - [18. Small Language Models (SLMs)](#18-small-language-models-slms)
  - [19. Distillation](#19-distillation)
  - [20. Quantization](#20-quantization)
  - [Quick Reference Summary](#quick-reference-summary)

---

## 1. Large Language Models (LLMs)

**Definition:** Neural networks (usually Transformer-based) trained on massive text corpora to predict the next token, giving them broad language, reasoning, and knowledge capabilities.

- Parameters range from millions (small) to hundreds of billions (frontier models).
- Trained in stages: pretraining → fine-tuning → alignment (RLHF).
- Core capability: next-token prediction, scaled up until emergent behaviors (reasoning, coding, translation) appear.

```python
# Conceptual: an LLM is a function P(next_token | previous_tokens)
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

inputs = tokenizer("The capital of France is", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=5)
print(tokenizer.decode(outputs[0]))
```

---

## 2. Tokenization

**Definition:** Splitting raw text into smaller units (tokens) — words, subwords, or characters — that the model can process as numbers.

- Most LLMs use **subword tokenization** (BPE, WordPiece, SentencePiece) to balance vocabulary size vs. handling rare/unknown words.
- A token ≈ 0.75 words on average in English.
- Tokenization directly affects context window usage and cost (billed per token).

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokens = tokenizer.tokenize("Tokenization splits text into subwords.")
ids = tokenizer.encode("Tokenization splits text into subwords.")

print(tokens)  # ['Token', 'ization', 'Ġsplits', 'Ġtext', ...]
print(ids)     # [30642, 1634, 22394, ...]
```

---

## 3. Vectorization / Embeddings

**Definition:** Converting tokens into dense numeric vectors that capture semantic meaning — similar meanings end up close together in vector space.

- Each token/word/sentence → a fixed-size vector (e.g., 768, 1536 dimensions).
- Embeddings power similarity search, clustering, and RAG retrieval.
- Distance metrics: cosine similarity, dot product, Euclidean distance.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
v1 = model.encode("The cat sat on the mat")
v2 = model.encode("A feline rested on the rug")

cosine_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
print(cosine_sim)  # High value (~0.7+) — semantically similar
```

---

## 4. Attention Mechanism

**Definition:** A mechanism letting a model weigh how much each token should "attend to" every other token when computing its representation — this is what lets Transformers capture context and long-range dependencies.

- Core formula (Scaled Dot-Product Attention):

```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```

- **Q (Query), K (Key), V (Value)** — learned projections of the input.
- **Self-attention**: tokens attend to other tokens in the same sequence.
- **Multi-head attention**: runs several attention operations in parallel to capture different relationship types (syntax, semantics, position).

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, V), weights

Q = torch.rand(1, 4, 8)  # (batch, seq_len, d_k)
K = torch.rand(1, 4, 8)
V = torch.rand(1, 4, 8)
output, attn_weights = scaled_dot_product_attention(Q, K, V)
print(output.shape)  # torch.Size([1, 4, 8])
```

---

## 5. Self-Supervised Learning

**Definition:** Training paradigm where the model creates its own labels from raw, unlabeled data — no human annotation needed. This is how LLMs pretrain on the internet-scale text.

- **Causal LM objective** (GPT-style): predict the next token given previous tokens.
- **Masked LM objective** (BERT-style): predict masked/hidden tokens using surrounding context.
- Scales cheaply because raw text is abundant; human-labeled data isn't.

```python
# Simplified causal LM training loop
import torch.nn as nn

loss_fn = nn.CrossEntropyLoss()

def training_step(model, input_ids):
    # Shift labels by one position: predict next token
    labels = input_ids[:, 1:].contiguous()
    logits = model(input_ids[:, :-1]).logits
    loss = loss_fn(logits.view(-1, logits.size(-1)), labels.view(-1))
    return loss
```

---

## 6. Transformer Architecture

**Definition:** The neural network architecture (Vaswani et al., 2017, "Attention Is All You Need") underlying nearly all modern LLMs. Replaced RNNs by processing sequences in parallel using attention instead of recurrence.

**Key components:**
- **Input Embedding + Positional Encoding** — since there's no recurrence, position info is added explicitly.
- **Encoder** (bidirectional context — BERT-style) and/or **Decoder** (causal, autoregressive — GPT-style).
- **Multi-Head Self-Attention** layers.
- **Feed-Forward Networks (FFN)** per layer.
- **Layer Normalization + Residual Connections** for stable, deep training.
- Stacked N times (e.g., GPT-3 has 96 layers).

```python
import torch.nn as nn

class TransformerBlock(nn.Module):
    def __init__(self, d_model=512, n_heads=8, d_ff=2048):
        super().__init__()
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model)
        )
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x, mask=None):
        attn_out, _ = self.attn(x, x, x, attn_mask=mask)
        x = self.norm1(x + attn_out)          # residual + norm
        x = self.norm2(x + self.ffn(x))       # residual + norm
        return x
```

---

## 7. Fine-tuning

**Definition:** Continuing training a pretrained model on a smaller, task-specific dataset to specialize its behavior (e.g., customer support tone, medical QA, code generation).

- **Full fine-tuning**: update all weights — expensive, needs lots of GPU memory.
- **PEFT (Parameter-Efficient Fine-Tuning)**: update only a small subset of parameters.
  - **LoRA (Low-Rank Adaptation)**: injects small trainable low-rank matrices into attention layers; freezes original weights.
  - **QLoRA**: LoRA + quantized base model — fine-tune large models on consumer GPUs.

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("gpt2")

lora_config = LoraConfig(
    r=8, lora_alpha=16, target_modules=["c_attn"],
    lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: ~0.1-1% of total params
```

---

## 8. Few-shot Prompting

**Definition:** Giving the model a handful of examples directly in the prompt (no weight updates) so it infers the task pattern and applies it to a new input — a form of in-context learning.

- **Zero-shot**: no examples, just an instruction.
- **One-shot**: one example.
- **Few-shot**: multiple (typically 2–10) examples.
- Effective for classification, formatting, and style transfer without any training.

```python
prompt = """
Classify the sentiment as Positive, Negative, or Neutral.

Review: "This laptop is amazing and fast!"
Sentiment: Positive

Review: "The battery died within an hour."
Sentiment: Negative

Review: "It arrived on time."
Sentiment: Neutral

Review: "Absolutely love the camera quality!"
Sentiment:
"""
# Model completes: "Positive"
```

---

## 9. Retrieval Augmented Generation (RAG)

**Definition:** Combines an LLM with an external knowledge retrieval step — instead of relying only on trained-in knowledge, the model fetches relevant documents at query time and generates an answer grounded in them.

**Pipeline:**
1. Chunk documents → embed → store in a vector DB.
2. User query → embed → similarity search → retrieve top-k relevant chunks.
3. Inject retrieved chunks + query into the prompt.
4. LLM generates an answer grounded in that context.

- Reduces hallucination, keeps knowledge current, avoids retraining.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")
docs = ["Python is a programming language.", "Paris is the capital of France."]
doc_vectors = embedder.encode(docs)

query = "What is the capital of France?"
query_vector = embedder.encode(query)

sims = [np.dot(query_vector, d) for d in doc_vectors]
best_doc = docs[np.argmax(sims)]

prompt = f"Context: {best_doc}\nQuestion: {query}\nAnswer:"
# Pass `prompt` to the LLM for a grounded answer
```

---

## 10. Vector Databases

**Definition:** Databases optimized for storing and querying high-dimensional embedding vectors using **Approximate Nearest Neighbor (ANN)** search — the backbone of RAG retrieval at scale.

- Examples: Pinecone, Weaviate, Milvus, Qdrant, Chroma, pgvector.
- Key indexing algorithms: HNSW (Hierarchical Navigable Small World), IVF, product quantization.
- Support metadata filtering alongside vector similarity (hybrid search).

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("my_docs")

collection.add(
    documents=["Python is great for AI.", "Cats are independent pets."],
    ids=["doc1", "doc2"]
)

results = collection.query(query_texts=["Tell me about programming"], n_results=1)
print(results["documents"])  # [['Python is great for AI.']]
```

---

## 11. Model Context Protocol (MCP)

**Definition:** An open standard (introduced by Anthropic) that lets AI models connect to external tools, data sources, and services through a unified interface — like a "USB-C port for AI applications."

- Standardizes how models call **tools** (functions), read **resources** (files/data), and use **prompts** (templates) from external servers.
- Removes the need for custom, one-off integrations per tool per model.
- Architecture: **MCP Host** (the AI app) ↔ **MCP Client** ↔ **MCP Server** (exposes tools/data).

```python
# Simplified MCP server exposing a tool
from mcp.server import Server
import mcp.types as types

server = Server("weather-server")

@server.list_tools()
async def list_tools():
    return [types.Tool(
        name="get_weather",
        description="Get current weather for a city",
        inputSchema={"type": "object", "properties": {"city": {"type": "string"}}}
    )]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        return [types.TextContent(type="text", text=f"Sunny in {arguments['city']}")]
```

---

## 12. Context Engineering

**Definition:** The practice of deliberately curating *everything* in a model's context window (system prompt, retrieved docs, tool outputs, conversation history, memory) to maximize task performance — a broader discipline than prompt engineering.

**Key techniques:**
- Prioritize the most relevant/recent info (context windows are limited and attention degrades over long contexts).
- Compress/summarize old conversation turns instead of keeping raw history.
- Structure context clearly (XML tags, headers) so the model can parse different sources.
- Balance: too little context → poor answers; too much irrelevant context → distraction, higher cost, "lost in the middle" effect.

```python
def build_context(system_prompt, retrieved_docs, chat_history, user_query, max_tokens=4000):
    # Prioritize: system > recent history > top retrieved docs > query
    context = f"{system_prompt}\n\n"
    context += "Relevant info:\n" + "\n".join(retrieved_docs[:3]) + "\n\n"
    context += "Recent conversation:\n" + "\n".join(chat_history[-5:]) + "\n\n"
    context += f"User: {user_query}"
    return context  # Trim/summarize further if over max_tokens
```

---

## 13. Agents

**Definition:** LLM-driven systems that autonomously plan, use tools, observe results, and iterate toward a goal — rather than producing a single one-shot response.

**Common loop (ReAct pattern):** Reason → Act (call a tool) → Observe (result) → repeat until done.

- Components: LLM "brain," tool access (search, code execution, APIs), memory, planning/reflection.
- Multi-agent systems: specialized agents (planner, coder, reviewer) collaborate on complex tasks.

```python
def agent_loop(llm, tools, goal, max_steps=5):
    history = [f"Goal: {goal}"]
    for step in range(max_steps):
        thought_and_action = llm.generate("\n".join(history))
        if "FINAL_ANSWER" in thought_and_action:
            return thought_and_action

        tool_name, tool_input = parse_action(thought_and_action)
        observation = tools[tool_name](tool_input)
        history.append(f"Action: {tool_name}({tool_input})")
        history.append(f"Observation: {observation}")
    return "Max steps reached"
```

---

## 14. Reinforcement Learning (RLHF)

**Definition:** Aligning a model's behavior with human preferences by training it to maximize a reward signal — typically human feedback, used to make models helpful, honest, and harmless.

**RLHF pipeline:**
1. Pretrain base LLM (self-supervised).
2. Supervised Fine-Tuning (SFT) on high-quality demonstrations.
3. Train a **Reward Model** on human-ranked output comparisons.
4. Fine-tune the LLM with RL (commonly **PPO**, or newer methods like **DPO**) to maximize reward model score.

```python
# Simplified reward-model training on preference pairs
import torch.nn as nn

class RewardModel(nn.Module):
    def __init__(self, base_model):
        super().__init__()
        self.base = base_model
        self.reward_head = nn.Linear(base_model.config.hidden_size, 1)

    def forward(self, input_ids):
        hidden = self.base(input_ids).last_hidden_state[:, -1, :]
        return self.reward_head(hidden)  # scalar reward score

def preference_loss(reward_chosen, reward_rejected):
    return -torch.log(torch.sigmoid(reward_chosen - reward_rejected)).mean()
```

---

## 15. Chain of Thought (CoT)

**Definition:** Prompting technique where the model is guided to generate intermediate reasoning steps before the final answer — significantly improves performance on math, logic, and multi-step problems.

- Triggered by phrases like *"Let's think step by step."*
- **Zero-shot CoT**: just add the trigger phrase.
- **Few-shot CoT**: show worked examples with reasoning steps.

```python
prompt = """
Q: A store has 15 apples. They sell 6 and receive a new shipment of 10. How many apples now?
Let's think step by step.
A: Start with 15 apples. Sell 6: 15 - 6 = 9. Receive 10 more: 9 + 10 = 19.
The answer is 19.

Q: A train has 120 passengers. 45 get off, then 30 get on. How many passengers now?
Let's think step by step.
A:
"""
# Model reasons through steps before giving the final number
```

---

## 16. Reasoning Models

**Definition:** Models specifically trained (often via RL) to perform extended internal reasoning — generating long "thinking" traces before answering — improving accuracy on hard problems (math, code, logic).

- Examples: OpenAI's o-series, DeepSeek-R1, Claude with extended thinking.
- Differ from standard CoT prompting: reasoning ability is trained into the model via RL on verifiable reward signals (e.g., correct/incorrect math answers), not just elicited via prompting.
- Trade-off: higher latency and token cost for higher accuracy on complex tasks.

```python
# Conceptual usage — reasoning models expose a "thinking" budget/mode
response = client.messages.create(
    model="reasoning-model",
    max_tokens=2000,
    thinking={"type": "enabled", "budget_tokens": 1000},
    messages=[{"role": "user", "content": "Prove that √2 is irrational."}]
)
# Response includes a reasoning trace + final answer
```

---

## 17. Multi-modal Models

**Definition:** Models that process and generate across multiple data types — text, images, audio, video — within a single unified architecture.

- Typically use a **modality-specific encoder** (e.g., a vision encoder like ViT for images) to project non-text input into the same embedding space as text tokens, then feed everything into a shared Transformer.
- Examples: GPT-4V, Claude (vision), Gemini, LLaVA.
- Use cases: image captioning, visual Q&A, document/chart understanding, audio transcription + reasoning.

```python
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image

processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
model = AutoModelForVision2Seq.from_pretrained("llava-hf/llava-1.5-7b-hf")

image = Image.open("chart.png")
prompt = "USER: <image>\nWhat trend does this chart show? ASSISTANT:"
inputs = processor(text=prompt, images=image, return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=100)
print(processor.decode(output[0], skip_special_tokens=True))
```

---

## 18. Small Language Models (SLMs)

**Definition:** Compact models (roughly <10B parameters) designed to run efficiently on limited hardware (laptops, phones, edge devices) while retaining strong performance on targeted tasks.

- Examples: Phi-3, Llama-3.2-1B/3B, Gemma-2B, Mistral-7B.
- Achieved via better training data quality, distillation, and architecture efficiency rather than just fewer parameters.
- Trade-off: narrower general knowledge/reasoning vs. large models, but much cheaper and faster to run.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# ~2B parameter model — runs on a single consumer GPU or CPU
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b")

inputs = tokenizer("Explain gravity in one sentence:", return_tensors="pt")
output = model.generate(**inputs, max_new_tokens=30)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

---

## 19. Distillation

**Definition:** Training a smaller "student" model to mimic the behavior/outputs of a larger "teacher" model — transfers capability while shrinking size and inference cost.

- **Soft-label distillation**: student learns from the teacher's full probability distribution (logits), not just the final answer — richer training signal than hard labels.
- Common in producing SLMs (e.g., DistilBERT distilled from BERT).

```python
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits, true_labels, T=2.0, alpha=0.5):
    # Soft loss: match teacher's softened probability distribution
    soft_loss = F.kl_div(
        F.log_softmax(student_logits / T, dim=-1),
        F.softmax(teacher_logits / T, dim=-1),
        reduction="batchmean"
    ) * (T ** 2)

    # Hard loss: match ground-truth labels
    hard_loss = F.cross_entropy(student_logits, true_labels)

    return alpha * soft_loss + (1 - alpha) * hard_loss
```

---

## 20. Quantization

**Definition:** Reducing the numerical precision of model weights (e.g., FP32 → INT8/INT4) to shrink model size and speed up inference, with minimal accuracy loss — critical for deploying large models on limited hardware.

- **Post-Training Quantization (PTQ)**: quantize after training is done — fast, no retraining.
- **Quantization-Aware Training (QAT)**: simulate quantization during training for better accuracy retention.
- Common formats: FP16, INT8, INT4, GPTQ, GGUF/GGML (used by llama.cpp).
- Roughly: FP32 → INT8 cuts memory ~4x with small accuracy trade-off.

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    quantization_config=quant_config,
    device_map="auto"
)
# Model now runs in 4-bit precision — ~4x smaller memory footprint
```

---

## Quick Reference Summary

| Concept | One-liner |
|---|---|
| LLM | Predicts next token at massive scale |
| Tokenization | Text → subword units |
| Vectorization | Tokens → semantic number vectors |
| Attention | Weighs relevance between tokens |
| Self-Supervised Learning | Learns from raw data, no labels |
| Transformer | Attention-based architecture, no recurrence |
| Fine-tuning | Specializes a pretrained model (often via LoRA) |
| Few-shot Prompting | Teach via examples, no training |
| RAG | Retrieve external docs, then generate |
| Vector DB | Stores/searches embeddings efficiently |
| MCP | Standard protocol for model ↔ tool/data connections |
| Context Engineering | Curating what goes into the context window |
| Agents | LLM + tools + loop = autonomous action |
| RLHF | Aligns model to human preference via reward signal |
| Chain of Thought | Step-by-step reasoning before answering |
| Reasoning Models | Trained (via RL) to reason deeply, not just prompted |
| Multi-modal | Handles text + image/audio/video together |
| SLM | Small, efficient model for edge/limited hardware |
| Distillation | Small model learns from a large teacher model |
| Quantization | Lower precision weights → smaller, faster model |