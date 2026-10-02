"""Two AutoGen agents plot the YTD performance of NVDA and TSLA.

One agent writes Python and the other runs it on this machine.

    python financial_analysis.py               # the LLM writes all the code itself
    python financial_analysis.py --with-tools  # the LLM calls helpers from stock_tools.py
"""

import argparse
import datetime
import os
from pathlib import Path

from autogen import AssistantAgent, ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv

from claude_client import ClaudeClient
from stock_tools import get_stock_prices, plot_stock_prices

WORK_DIR = Path(__file__).parent / "coding"


def build_llm_config():
    load_dotenv()  # searches parent folders, so the workspace-root .env works too
    return {
        "config_list": [
            {
                "api_type": "anthropic",
                "model_client_cls": "ClaudeClient",
                "model": os.getenv("CLAUDE_MODEL", "claude-opus-5-5"),
                "api_key": os.environ["ANTHROPIC_API_KEY"],
                "max_tokens": 16000,
            }
        ]
    }


def build_agents(llm_config, with_tools):
    functions = [get_stock_prices, plot_stock_prices] if with_tools else []
    executor = LocalCommandLineCodeExecutor(
        timeout=60,
        work_dir=WORK_DIR,
        functions=functions,
    )

    # Start from AssistantAgent's built-in coding prompt. With tools, append
    # the helper signatures so the LLM knows it can import and call them.
    system_message = AssistantAgent.DEFAULT_SYSTEM_MESSAGE
    if with_tools:
        system_message += executor.format_functions_for_prompt()

    writer = AssistantAgent(
        name="code_writer_agent",
        system_message=system_message,
        llm_config=llm_config,
        code_execution_config=False,
        human_input_mode="NEVER",
    )
    writer.register_model_client(ClaudeClient)

    runner = ConversableAgent(
        name="code_executor_agent",
        llm_config=False,
        code_execution_config={"executor": executor},
        human_input_mode="ALWAYS",
        default_auto_reply="Please continue. If everything is done, reply 'TERMINATE'.",
        # Pressing Enter after the writer says TERMINATE ends the chat
        is_termination_msg=lambda msg: "TERMINATE" in (msg.get("content") or ""),
    )
    return writer, runner


def build_task(with_tools):
    today = datetime.date.today()
    if with_tools:
        filename = "stock_prices_YTD_plot.png"
        task = "Download the stock prices YTD for NVDA and TSLA and create a plot."
    else:
        filename = "ytd_stock_gains.png"
        task = "Create a plot showing stock gain YTD for NVDA and TSLA."
    message = (
        f"Today is {today}. {task} "
        f"Make sure the code is in a markdown code block and save the figure to a file {filename}."
    )
    return message, filename


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--with-tools",
        action="store_true",
        help="give the executor get_stock_prices / plot_stock_prices from stock_tools.py",
    )
    args = parser.parse_args()

    writer, runner = build_agents(build_llm_config(), args.with_tools)
    message, filename = build_task(args.with_tools)

    print("Press Enter to run each code block the writer sends, or type 'exit' to stop.\n")
    runner.initiate_chat(writer, message=message)

    plot = WORK_DIR / filename
    if plot.exists():
        print(f"\nPlot saved to {plot}")
    else:
        print(f"\nNo plot found at {plot}")


if __name__ == "__main__":
    main()
