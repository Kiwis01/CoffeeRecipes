
import os
from flask import Flask, render_template, url_for, request
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, dotenv_values

#secret key load
load_dotenv('.env')

#Langchain initialization
os.environ["OPENAI_API_KEY"] = os.getenv("APIKEY")
loader = TextLoader('prompt.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

#flask setup for css file
app = Flask(__name__, static_url_path='/static', static_folder='static')

#format output
def format_recipe(recipe):
    recipe_lines = recipe.split("\n")
    name =[]
    # Start formatting ingredients
    ingredients = []
    ingredients_flag = False
    for line in recipe_lines:
        if "Instructions:" in line:
            break
        if ingredients_flag and line.strip() != "":
            ingredients.append(line.strip())
        if "Ingredients:" in line:
            ingredients_flag = True
        elif ingredients_flag == False:
            name.append(line.strip())
    
    # Start formatting instructions
    instructions = []
    instructions_flag = False
    for line in recipe_lines:
        if instructions_flag and line.strip() != "":
            instructions.append(line.strip())
        if "Instructions:" in line:
            instructions_flag = True 
    return name, ingredients, instructions

#website setup
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/recipe',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    recipe = "Make a recipe for {}".format(output["name"])
    recipe_text = index.query(recipe, llm=ChatOpenAI())
    print(recipe_text)
    name, ingredients, instructions = format_recipe(recipe_text)
    return render_template('index.html', name = name,  ingredients="\n".join(ingredients), instructions="\n".join(instructions))
    
if __name__ == "__main__":
    app.run(debug=True)



