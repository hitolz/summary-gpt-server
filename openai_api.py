# -*- coding: utf-8 -*-

import openai
import json
import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

delimiter = "##^^&&##"

system_message = f"""
你是一个知识渊博的文学家，负责根据用户输入的内容，对内容进行总结、提炼。
你要告诉我这篇文章主要讲了什么内容，从哪些方面讲起的。
不要超过200字。
文章内容将使用{delimiter}字符分隔。
"""


def build_message(system_prompt, input_prompt, context_input):
    message = []
    if system_prompt is not None and len(system_prompt) > 0:
        for system_p in system_prompt:
            message.append({"role": "system", "content": system_p})
    if context_input is not None and len(context_input) > 0:
        for context_message in context_input:
            message.append(context_message)
    if input_prompt is not None and len(input_prompt) > 0:
        message.append({"role": "user", "content": input_prompt})
    return message


def completions(messages=[], system_prompt=[], input_prompt="", context_input=[], temperature=0.0):
    if len(messages) == 0:
        messages = build_message(system_prompt, input_prompt, context_input)
    data = {
        "messages": messages,
        "temperature": temperature
    }
    headers = {
        "Content-type": "application/json",
        "api-key": openai.api_key
    }
    response = chatcompletion(messages)
    return response


def chatcompletion(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
    )

    return response


def completions_stream(messages=[], system_prompt=[], input_prompt="", context_input=[], temperature=0.0):
    if len(messages) == 0:
        messages = build_message(system_prompt, input_prompt, context_input)
    data = {
        "messages": messages,
        "temperature": temperature
    }
    headers = {
        "Content-type": "application/json",
        "api-key": openai.api_key
    }
    response = chatcompletion_stream(messages)
    num_tokens = num_tokens_from_messages(messages)
    return response,num_tokens


def chatcompletion_stream(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
        stream=True
    )
    return response


def summary(user_input):
    result = completions(system_prompt=[system_message], input_prompt=f"{delimiter}{user_input}{delimiter}")
    print(result)
    return result['choices'][0]['message']['content']


def summary_stream(user_input):
    collected_messages = []
    response,num_tokens = completions_stream(system_prompt=[system_message], input_prompt=f"{delimiter}{user_input}{delimiter}")
    print(num_tokens)
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']  # 提取消息内容
        collected_messages.append(chunk_message)
        if len(chunk_message) > 0:
            yield f"data: {chunk_message['content']} \n\n"


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
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