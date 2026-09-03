from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent


# ============================================================
# 1. Bug Reviewer
# ============================================================

bug_reviewer = LlmAgent(
    name="bug_reviewer",
    model="gemini-3.5-flash",
    description="Reviews code for bugs and logical problems.",
    instruction="""
    You are a senior software engineer specializing in debugging.

    Review the code provided by the user.

    Focus ONLY on:
    - Logical bugs
    - Runtime errors
    - Incorrect assumptions
    - Edge cases
    - Incorrect input handling

    For every issue:
    1. Explain the problem.
    2. Explain why it can cause incorrect behavior.
    3. Suggest a fix.

    If you find no bugs, clearly say so.

    Do not review security or performance.
    """,
    output_key="bug_review",
)


# ============================================================
# 2. Security Reviewer
# ============================================================

security_reviewer = LlmAgent(
    name="security_reviewer",
    model="gemini-3.5-flash",
    description="Reviews code for security vulnerabilities.",
    instruction="""
    You are a senior application security engineer.

    Review the code provided by the user.

    Focus ONLY on:
    - Injection vulnerabilities
    - Authentication problems
    - Authorization problems
    - Sensitive data exposure
    - Unsafe input handling
    - Insecure dependencies or patterns
    - Other realistic security risks

    For every issue:
    1. Identify the vulnerability.
    2. Explain the risk.
    3. Suggest a safer approach.

    If you find no security problems, clearly say so.

    Do not review general code quality or performance.
    """,
    output_key="security_review",
)


# ============================================================
# 3. Performance Reviewer
# ============================================================

performance_reviewer = LlmAgent(
    name="performance_reviewer",
    model="gemini-3.5-flash",
    description="Reviews code for performance and scalability problems.",
    instruction="""
    You are a senior performance engineer.

    Review the code provided by the user.

    Focus ONLY on:
    - Time complexity
    - Space complexity
    - Unnecessary loops
    - Expensive operations
    - Memory usage
    - Scalability problems
    - Database or network performance issues when applicable

    For every issue:
    1. Identify the problem.
    2. Explain its performance impact.
    3. Suggest an improvement.

    Include Big-O complexity when possible.

    If there are no significant performance problems, clearly say so.

    Do not review security or general code style.
    """,
    output_key="performance_review",
)


# ============================================================
# 4. Parallel Review Team
# ============================================================

parallel_reviewers = ParallelAgent(
    name="parallel_code_reviewers",
    description="Runs independent code reviews in parallel.",
    sub_agents=[
        bug_reviewer,
        security_reviewer,
        performance_reviewer,
    ],
)


# ============================================================
# 5. Final Review Agent
# ============================================================

final_reviewer = LlmAgent(
    name="final_reviewer",
    model="gemini-3.5-flash",
    description="Combines all code review results into one report.",
    instruction="""
    You are the lead code reviewer.

    Multiple specialized reviewers have analyzed the user's code.

    BUG REVIEW:
    {bug_review}

    SECURITY REVIEW:
    {security_review}

    PERFORMANCE REVIEW:
    {performance_review}

    Combine their findings into one professional code review.

    Use this structure:

    # Code Review

    ## 🐛 Bugs
    Summarize important bugs and logical issues.

    ## 🔐 Security
    Summarize security vulnerabilities.

    ## ⚡ Performance
    Summarize performance and scalability issues.

    ## 📊 Overall Assessment
    Give a short assessment of the code.

    ## 🔧 Recommended Changes
    Give the most important fixes in priority order.

    Use severity levels where appropriate:

    - 🔴 Critical
    - 🟠 High
    - 🟡 Medium
    - 🟢 Low

    Do not invent issues that were not identified by the reviewers.
    """,
)


# ============================================================
# 6. Complete Workflow
# ============================================================

root_agent = SequentialAgent(
    name="code_review_workflow",
    description="Runs parallel code reviews and produces a final report.",
    sub_agents=[
        parallel_reviewers,
        final_reviewer,
    ],
)