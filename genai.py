import google.generativeai as genai
import json

genai.configure(api_key="AIzaSyB9j50TUQK-6R_qSlrcw8zdC13nneFpjGg")

def food_suggestion(weather, place):
    
    # model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(f"its {weather} in {place}, recommend some food items to eat at {place}, Give the output in json format, that include name,description.")
    response = response.text[7:response.text.index("```",1)]
    return json.loads(response)