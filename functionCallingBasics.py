import pathlib
import textwrap
import time

import google.generativeai as genai


from IPython import display
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def multiply(a:float, b:float):
    """returns a * b."""
    print('THing')
    return a*b

genai.configure(api_key="AIzaSyCUfDONUArVKNY5utYlcfJSul9iFCwVy3Q")
model = genai.GenerativeModel('gemini-1.0-pro', tools=[multiply])

chat = model.start_chat(enable_automatic_function_calling=False)
response = chat.send_message('I have 57 cats, each owns 44 mittens, how many mittens is that in total?')
print(response.text)
