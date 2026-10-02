# AutoGen: Coding and Financial Analysis

Two [AutoGen](https://github.com/ag2ai/ag2) agents work together on a stock analysis task. One writes Python and the other runs it. The task is to plot the year-to-date performance of NVDA and TSLA.

New to it? Open [walkthrough.html](walkthrough.html) in a browser for an 8-slide visual guide to how the agents work and how to run them.

## What it covers

- Running code locally with `LocalCommandLineCodeExecutor`
- A **code writer** agent (`AssistantAgent`, backed by Claude Opus 5.5) and a **code executor** agent that runs the code it writes
- Giving the executor **user-defined functions** (`get_stock_prices`, `plot_stock_prices` in [stock_tools.py](stock_tools.py)) so the LLM calls ready-made helpers instead of writing everything itself

## Files

| File | What it does |
|------|--------------|
| [financial_analysis.py](financial_analysis.py) | Builds the two agents and starts the chat |
| [stock_tools.py](stock_tools.py) | Helpers the executor can hand to the LLM |
| [claude_client.py](claude_client.py) | ag2's Anthropic client, minus the `temperature` param that current Claude models reject |
| [walkthrough.html](walkthrough.html) | Slide-deck walkthrough of the lesson |

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your Anthropic API key

python financial_analysis.py               # the LLM writes all the code itself
python financial_analysis.py --with-tools  # the LLM calls the helpers in stock_tools.py
```

Set `CLAUDE_MODEL` in `.env` to use a model other than `claude-opus-5-5`.

The executor agent asks for your input at every turn. Press Enter to run the generated code, or type `exit` to stop. The generated code and plots are saved to `coding/`.

Keep the venv active while it runs. The executor calls `python` from your PATH.

> ⚠️ The generated code runs directly on your machine with no sandbox. Read it before you press Enter.
