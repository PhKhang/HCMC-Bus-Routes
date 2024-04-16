import google.generativeai as genai
import vertexai.preview
from rich import print

genai.configure(api_key="AIzaSyCUfDONUArVKNY5utYlcfJSul9iFCwVy3Q")

from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)

model = genai.GenerativeModel('gemini-1.0-pro')

def qr(key, value):
    print(key, value)
    
getRouteVarPath = FunctionDeclaration(
    name="qr",
    description="Query route by key: value pair",
    parameters={
    "type": "object",
    "properties": {
        "key": {
            "type": "string",
            "description": ''' The keys are:
'_RouteId': id of route,
'_RouteVarId': id of the direction of the route,
'_RouteVarName': name of the direction of the route,
'_RouteVarShortName': the shorter name of the direction of the route,
'_RouteNo': A public number represent the route,
'_StartStop': The name of the starting stop,
'_EndStop': The name of the ending stop,
'_Distance': The distance of the direction of the route
'_Outbound': None,
'''
        },
        "value": {
            "type": "string",
            "description": "The value to search for the key, it must be a string"
        }
    },
         "required": [
            "key",
            "value",
      ]
  },
)


tool = Tool(
    function_declarations = [
        getRouteVarPath
    ]
)


prompt = """I need to find bus routes that runs from Bến xe buýt Sài Gòn to THẠNH LỘC."""

response = model.generate_content(
    prompt,
    tools=[tool],
)