import google.generativeai as genai
from rich import print

genai.configure(api_key="AIzaSyCUfDONUArVKNY5utYlcfJSul9iFCwVy3Q")

model = genai.GenerativeModel('gemini-pro')

res = model.generate_content("""I need to find bus routes that runs from Bến xe buýt Sài Gòn to THẠNH LỘC.
Given the keys are:
'_RouteId': id of route,
'_RouteVarId': id of the direction of the route,
'_RouteVarName': name of the direction of the route,
'_RouteVarShortName': the shorter name of the direction of the route,
'_RouteNo': A public number represent the route,
'_StartStop': The name of the starting stop,
'_EndStop': The name of the ending stop,
'_Distance': The distance of the direction of the route
'_Outbound': None,
'_RunningTime': The running time of the direction of the route
Return ONLY 2 Python arrays in one array, the first one contains the necessary keys, the second contains the value to search for of those keys. I really need it to be only 2 PYTHON ARRAYS.""")

print(res)