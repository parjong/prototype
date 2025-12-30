#!/usr/bin/env -S uv run --python 3.11 --script
#
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "ollama",
#     "rich",
# ]
# ///
"""
Single tool, single turn example.
Run with: uv run tool.py
"""

import json

from rich import print

from ollama import chat

model = 'functiongemma:270m'


def get_current_time() -> str:
  """
  Get the current Seoul time

  Returns:
    A string describing the current Seoul time in 24-hour format (HH:MM)
  """
  return json.dumps({'time': '17:40:00'})

def convert_time(source_timezone, time, target_timezone) -> str:
  """
  Convert time between timezones

  Args:
    source_timezone: Source IANA timezone name (e.g., 'America/New_York', 'Europe/London')
    time: Time to convert in 24-hour format (HH:MM)
    target_timezone: Target IANA timezone name (e.g., 'Asia/Tokyo', 'America/San_Francisco')

  Returns:
    A string describing the time in target timezone in 24-hour format (HH:MM)
  """
  return json.dumps({'time': '01:40:00'})


messages = [{'role': 'user', 'content': 'What is the current time of New York?'}]
print('Prompt:', messages[0]['content'])

response = chat(model, messages=messages, tools=[get_current_time, convert_time])
print(response)

if response.message.tool_calls:
  tool = response.message.tool_calls[0]
  print(f'Calling: {tool.function.name}({tool.function.arguments})')

  result = get_current_time(**tool.function.arguments)
  print(f'Result: {result}')

  messages.append(response.message)
  messages.append({'role': 'tool', 'content': result}) # tool result

  final = chat(model, messages=messages)
  print('Response:', final.message.content)
else:
  print('Response:', response.message.content)

