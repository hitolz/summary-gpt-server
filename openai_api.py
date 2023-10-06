# -*- coding: utf-8 -*-

import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

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
    return response


def chatcompletion_stream(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=messages,
        stream=True
    )
    return response


def summary(user_input):
    result = completions(system_prompt=[system_message], input_prompt = f"{delimiter}{user_input}{delimiter}")
    print(result)
    return result['choices'][0]['message']['content']


def summary_stream(user_input):
    collected_messages = []
    response =  completions_stream(system_prompt=[system_message], input_prompt = f"{delimiter}{user_input}{delimiter}")
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']  # 提取消息内容
        collected_messages.append(chunk_message)
        if len(chunk_message) > 0:
            yield f"data: {chunk_message['content']} \n\n"