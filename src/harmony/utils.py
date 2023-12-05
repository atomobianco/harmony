import tiktoken


def parse_file(file_name):
    """Parse file and return a string"""
    with open(file_name, "r") as f:
        return f.read()


def calculate_cost(usage, model):
    pricing = {
        "gpt-3.5-turbo": {
            "prompt": 0.0010,
            "completion": 0.0020,
        },
        "gpt-3.5-turbo-1106": {
            "prompt": 0.0010,
            "completion": 0.0020,
        },
        "gpt-3.5-turbo-0613": {
            "prompt": 0.0015,
            "completion": 0.0020,
        },
        "gpt-3.5-turbo-16k-0613": {
            "prompt": 0.0030,
            "completion": 0.0040,
        },
        "gpt-4": {
            "prompt": 0.03,
            "completion": 0.06,
        },
        "gpt-4-0613": {
            "prompt": 0.03,
            "completion": 0.06,
        },
        "gpt-4-32k": {
            "prompt": 0.06,
            "completion": 0.12,
        },
        "gpt-4-32k-0613": {
            "prompt": 0.06,
            "completion": 0.12,
        },
        "gpt-4-1106-preview": {
            "prompt": 0.01,
            "completion": 0.03,
        },
    }
    try:
        model_pricing = pricing[model]
    except KeyError:
        raise ValueError("Invalid model specified")
    prompt_cost = usage.prompt_tokens * model_pricing["prompt"] / 1000
    completion_cost = usage.completion_tokens * model_pricing["completion"] / 1000
    total_cost = prompt_cost + completion_cost
    return total_cost


def num_tokens_from_messages(messages, model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4-1106-preview",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-1106")
    elif "gpt-4-32k" in model:
        return num_tokens_from_messages(messages, model="gpt-4-32k-0613")
    elif "gpt-4" in model:
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_text() is not implemented for model {model}. See """
            f"""https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are """
            f"""converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
