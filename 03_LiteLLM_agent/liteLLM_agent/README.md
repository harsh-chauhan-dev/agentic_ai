# LiteLLM Agent Example

## What is LiteLLM?

LiteLLM is a Python library that provides a unified interface for interacting with multiple Large Language Model (LLM) providers through a consistent API.

It allows you to:

- Use a common interface for different LLM providers
- Switch between models without changing the overall agent architecture
- Connect ADK agents with providers such as Google, OpenAI, and Anthropic
- Experiment with different models for different tasks
- Build multi-model and multi-agent applications

In this example, LiteLLM is used with **Google ADK (Agent Development Kit)** to build a multi-agent coding assistant.

---

## Why Use LiteLLM with ADK?

ADK is designed to work with different LLM providers. LiteLLM makes it easier to connect ADK agents with different models.

The main benefits are:

1. **Provider Flexibility**: Switch between Gemini, OpenAI, Anthropic, and other supported providers.

2. **Model Flexibility**: Different agents can use different models depending on the task.

3. **Specialized Agents**: Create separate agents for explanation, problem solving, and code review.

4. **Easy Model Switching**: Change the underlying model without redesigning the agent architecture.

5. **Model Experimentation**: Test different models and compare their performance.

---

## What This Example Builds

This project builds a **Multi-Model Coding Assistant** using Google ADK and LiteLLM.

The system contains a root `coding_manager` agent and three specialized agents:

```text
                         User
                           │
                           ▼
                    Coding Manager
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
       Gemini Agent    Coding Agent   Review Agent
       Explanation      Solve/Debug     Security
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                         LiteLLM

```

---

## Additional Resources

- [Google ADK LiteLLM Integration Documentation](https://google.github.io/adk-docs/tutorials/agent-team/#step-2-going-multi-model-with-litellm-optional)
- [LiteLLM Documentation](https://docs.litellm.ai/docs/)
- [LiteLLM Supported Providers](https://docs.litellm.ai/docs/providers)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Anthropic Claude Models Overview](https://docs.anthropic.com/en/docs/about-claude/models/all-models)