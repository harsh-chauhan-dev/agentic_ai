# 11 — Parallel Code Review Agent

A multi-agent code review system built with **Google Agent Development Kit (ADK)** that uses `ParallelAgent` to analyze code from multiple independent perspectives at the same time.

---

## 📌 Project Introduction

Code review usually requires checking several things:

- 🐛 Bugs and logical errors
- 🔐 Security vulnerabilities
- ⚡ Performance problems

Doing all of these reviews sequentially can be inefficient.

This project solves that problem by creating **specialized review agents** that independently analyze the same code in parallel.

The project contains three reviewers:

1. 🐛 **Bug Reviewer** — identifies logical and runtime problems.
2. 🔐 **Security Reviewer** — identifies security vulnerabilities.
3. ⚡ **Performance Reviewer** — identifies performance and scalability issues.

After the parallel reviews are completed, a **Final Reviewer** combines their findings into one structured code-review report.

---

## 🤖 What is `ParallelAgent`?

`ParallelAgent` is an ADK workflow agent that executes multiple sub-agents concurrently.

It is useful when several tasks are **independent of each other** and can be performed at the same time.

### Parallel Workflow

```text
                         User Code
                            │
                            ▼
                    ┌────────────────┐
                    │  ParallelAgent │
                    └───────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Bug Reviewer  Security Reviewer  Performance Reviewer
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                    Final Reviewer
                            │
                            ▼
                    Final Code Review
```

Instead of:

```text
Bug Review
    ↓
Security Review
    ↓
Performance Review
    ↓
Final Review
```

the independent reviews can run concurrently:

```text
Bug Review ───────────────┐
                          │
Security Review ──────────┼──→ Final Review
                          │
Performance Review ───────┘
```

### Core Principle

> **Use parallel execution when multiple independent tasks can be performed without depending on each other's results.**

---

## ⚙️ How This Project Works

The system uses a `ParallelAgent` to run multiple specialized code-review tasks at the same time.

### Reviewers

- 🔍 **Bug Reviewer** → analyzes logical errors and potential runtime problems.
- 🛡️ **Security Reviewer** → looks for potential security vulnerabilities and unsafe practices.
- ⚡ **Performance Reviewer** → identifies inefficient operations and possible performance improvements.

These agents work concurrently, which can reduce overall execution time compared with running every reviewer sequentially.

Once the individual agents complete their analysis, their results are passed to a **Final Reviewer**.

The Final Reviewer combines all findings and generates a comprehensive code-review report containing:

- ✅ Potential bugs
- ✅ Security concerns
- ✅ Performance issues
- ✅ Overall assessment
- ✅ Recommended improvements

---

## 🔄 Complete Workflow

The complete workflow combines `ParallelAgent` with sequential orchestration:

```text
                         Root Agent
                              │
                              ▼
                     ┌────────────────┐
                     │  ParallelAgent │
                     └───────┬────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
              Bug        Security     Performance
             Review       Review        Review
                │            │            │
                └────────────┼────────────┘
                             ▼
                     Final Reviewer
                             │
                             ▼
                       Final Report
```

The high-level pattern is:

```text
Sequential
    ↓
Parallel
    ↓
Sequential
```

---

## 🧩 Step-by-Step Execution

### 1. User Provides Code

The user submits a code snippet that needs to be reviewed.

### 2. Parallel Reviewers Start

The `ParallelAgent` sends the task to the specialized reviewers.

Each reviewer has a different responsibility.

### 3. Independent Analysis

The reviewers analyze the code independently:

```text
Bug Reviewer
    → Bugs and logical problems

Security Reviewer
    → Security vulnerabilities

Performance Reviewer
    → Complexity and performance problems
```

They don't need to wait for one another.

### 4. Results Are Collected

Each reviewer produces its own findings.

The results are collected and made available to the final reviewer.

### 5. Final Reviewer Synthesizes

The Final Reviewer combines all findings and creates a single structured report containing:

- 🐛 Bugs
- 🔐 Security issues
- ⚡ Performance issues
- 📊 Overall assessment
- 💡 Recommended changes

---

## 🎯 Why `ParallelAgent`?

The important reason is **independence**.

These tasks can happen independently:

```text
                     Same Code
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
            Bugs      Security   Performance
```

None of the reviewers needs the result of another reviewer before starting.

Therefore, parallel execution is a natural fit.

### Good Use Case

```text
Analyze Code
    ├── Find Bugs
    ├── Find Security Issues
    └── Find Performance Issues
```

### Poor Use Case

If Agent B requires Agent A's result:

```text
Agent A
   ↓
Agent B
   ↓
Agent C
```

then the tasks are dependent and should generally be handled sequentially.

---

## 🧠 Core ADK Concept

This project demonstrates the workflow:

```text
Sequential
    ↓
Parallel
    ↓
Sequential
```

More specifically:

```text
                  SequentialAgent
                         │
                         ▼
                  ParallelAgent
                  ┌──────┼──────┐
                  ▼      ▼      ▼
                  A      B      C
                  └──────┼──────┘
                         ▼
                    Final Agent
```

This demonstrates how different ADK workflow agents can be combined to create structured multi-agent systems.

---

## 🛠️ Technologies

- **Python**
- **Google Agent Development Kit (ADK)**
- **Gemini**
- **Multi-Agent Workflow**
- `ParallelAgent`
- `SequentialAgent`
- `LlmAgent`

---

## 📚 Official Documentation

### Google Agent Development Kit

https://google.github.io/adk-docs/

### Multi-Agent Systems

https://google.github.io/adk-docs/agents/multi-agents/

### Workflow Agents

https://google.github.io/adk-docs/agents/workflow-agents/

### ADK Documentation Index

https://adk.dev/llms.txt

---

## 🚀 Project Goal

The goal of this project is not simply to build a code reviewer.

The main learning objective is to understand **parallel agent orchestration**:

```text
Multiple Specialized Agents
            ↓
   Independent Execution
            ↓
      Shared Results
            ↓
     Final Synthesis
```

This pattern can be applied to many real-world systems, such as:

- 💻 Code review
- 🚨 Incident investigation
- 📄 Document analysis
- 🔐 Security auditing
- 📊 Data analysis
- 🔎 Research systems
- 🧑‍💻 Technical investigation

---

## 📁 Project Structure

```text
11_parallel_code_review/
│
├── __init__.py
├── agent.py
├── .env
├── .gitignore
└── README.md
```

---

## 🔑 Key Takeaway

`ParallelAgent` is not simply about running multiple agents.

The important design principle is:

> **Identify independent tasks, execute them concurrently, then combine their results when the workflow requires a unified answer.**

This project helped me understand how parallel execution can be used as a building block for more efficient and scalable multi-agent workflows.
