from flask import Flask
import os
import openai
from flask import request
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)

@app.route('/analyze', methods=['GET'])
def analyze():
  openai.api_key = os.getenv("OPENAI_API_KEY")
  json_data = request.json
  msg = json_data["msg"]
  is_harmful_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Is the following message harmful, yes or no? Then explain why. " + str(msg),
    temperature=0.1,
    max_tokens=64,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  stripped_harmful_response = " ".join(is_harmful_response["choices"][0]["text"].split())
  is_harmful = True if is_harmful_response["choices"][0]["text"].find("is harmful") >= 0 else False
  return {"harmful_evaluation": is_harmful, "harmful_gpt_reason": stripped_harmful_response}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)

