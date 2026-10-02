"""ag2 model client for current Claude models.

ag2 0.x's built-in AnthropicClient always sends `temperature` (default 1.0).
Current Claude models such as Opus 5.5 reject sampling parameters, so this
subclass drops it. Everything else is ag2's own Anthropic client.

Use it by putting `"model_client_cls": "ClaudeClient"` in the llm_config and
calling `agent.register_model_client(ClaudeClient)` on each agent that uses it.
"""

from autogen.oai.anthropic import AnthropicClient


class ClaudeClient(AnthropicClient):
    def __init__(self, config, **kwargs):
        super().__init__(**config)

    def load_config(self, params):
        anthropic_params = super().load_config(params)
        anthropic_params.pop("temperature", None)
        return anthropic_params
