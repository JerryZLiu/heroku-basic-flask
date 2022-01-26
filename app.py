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

@app.route('/analyze', methods=['POST'])
def analyze():
  openai.api_key = os.getenv("OPENAI_API_KEY")
  json_data = request.json
  msg = json_data["msg"]
  is_sexist_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Classify the following texts into  'sexist', or 'not sexist'.\n'That girl still need a good ass whooping, stupid ass bitch!!': sexist.\n'She is heavily relying on him to turn the other cheek...tough talking demon infested woman': sexist.\n'Women are more likely to be diagnosed with breast cancer': not sexist\n'She's kind of mean': not sexist\n " + str(msg) + ":",
    temperature=0.0,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  is_sexist = False if is_sexist_response["choices"][0]["text"].find("not sexist") >= 0 else True

  is_racist_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Classify the following texts into  'racist', or 'not racist'.\n'I hate chinese people': racist.\n'White people are bad at ping pong': racist.\n'I hate Chinese food': not racist\n'I have many friends who are indian and white': not racist\n " + str(msg) + ":",
    temperature=0.0,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  is_racist = False if is_racist_response["choices"][0]["text"].find("not racist") >= 0 else True

  is_spam_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Classify the following texts into  'spam', or 'not spam'.\n'Here's a link where you can get free bitcoin': spam\n'I can give you some free ethereum': spam\n'Let's play some fortnite together': not spam\n'I love using ethereum for transactions': not spam\n " + str(msg) + ":",
    temperature=0.0,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  is_spam = False if is_spam_response["choices"][0]["text"].find("not spam") >= 0 else True
  return {"is_sexist": is_sexist,
  "is_sexist_response": is_sexist_response["choices"][0]["text"],
  "is_racist": is_racist, 
  "is_racist_response": is_racist_response["choices"][0]["text"],
  "is_spam": is_spam,
  "is_spam_response": is_spam_response["choices"][0]["text"]
  }

@app.route('/analyzev2', methods=['POST'])
def analyzev2():
  openai.api_key = os.getenv("OPENAI_API_KEY")
  json_data = request.json
  msg = json_data["msg"]
  is_sexist_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Classify the following text into 'sexist' or 'not sexist'.\n" + str(msg) + ":",
    temperature=0.0,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  is_sexist = False if is_sexist_response["choices"][0]["text"].find("not sexist") >= 0 else True

  is_racist_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Classify the following text into 'racist' or 'not racist'.\n" + str(msg) + ":",
    temperature=0.0,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  is_racist = False if is_racist_response["choices"][0]["text"].find("not racist") >= 0 else True

  is_spam_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Classify the following texts into  'spam', or 'not spam'.\n" + str(msg) + ":",
    temperature=0.0,
    max_tokens=20,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  is_spam = False if is_spam_response["choices"][0]["text"].find("not spam") >= 0 else True

  harmful_response = openai.Completion.create(
    engine="text-davinci-001",
    prompt="Why is the following message harmful?\n" + str(msg) + ":",
    temperature=0.0,
    max_tokens=50,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  if is_racist or is_sexist or is_spam:
    response = "This may be harmful content. Reasoning: " + harmful_response["choices"][0]["text"]
  else: 
    response = "There doesn't appear to be any harmful content."

  return {
    "response": response,
    "is_sexist": is_sexist,
  "is_sexist_response": is_sexist_response["choices"][0]["text"],
  "is_racist": is_racist, 
  "is_racist_response": is_racist_response["choices"][0]["text"],
  "is_spam": is_spam,
  "is_spam_response": is_spam_response["choices"][0]["text"]
  }

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug=True, use_reloader=True)

