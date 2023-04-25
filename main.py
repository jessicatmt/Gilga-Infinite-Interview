import openai
import json
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Infinite Conversation</title>
    <style>
        body {
            background-color: #DF9B2A;
            font-family: 'SentientBold', Georgia, serif;
        }
        p {
            font-family: Arial, sans-serif;
        }
        textarea {
            background-color: #F5A92B;
            border: 1px solid #1D1D1C;
            box-shadow: none;
            color: #1D1D1C;
            font-family: Arial, sans-serif;
        }
        input[type="submit"] {
            background-color: transparent;
            border: 1px solid #1D1D1C;
            color: #1D1D1C;
            cursor: pointer;
            font-family: Arial, sans-serif;
            padding: 5px 10px;
        }
        input[type="submit"]:hover {
            background-color: #1D1D1C;
            color: #DF9B2A;
        }
    </style>
    <script>
        function generateResponse(event) {
            event.preventDefault();
            const textarea = document.getElementById('conversation');
            const apiKey = document.getElementById('api_key').value;
            const formData = new FormData(event.target);
            formData.append('api_key', apiKey);
            textarea.value += '\\n';
            fetch('/', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                textarea.value = data.conversation;
                textarea.scrollTop = textarea.scrollHeight;
            });
        }
    </script>
</head>
<body>
    <h1>Donald Glover Neverending Conversation</h1>
    <p>I interviewed Donald Glover back in 2011. I decided to see what it would be like to interview the AI version of Donald.<br></p>
  
<p>Please use your own OpenAI API key.<br> OpenAI API keys are free. Generate one at <a href="https://platform.openai.com/">OpenAI's website</a>.</p>
 <form onsubmit="generateResponse(event)">
       <p> <label for="api_key">API key:</label>
        <input type="password" id="api_key" name="api_key" required>
        </p>
        <textarea id="conversation" name="conversation" rows="10" cols="80" readonly>{{ conversation }}</textarea><br>
        <input type="submit" value="Generate Next Response">
    </form>
</body>
</html>
"""


def generate_response(prompt, chatbot, speaker, api_key):
  openai.api_key = api_key
  response = openai.Completion.create(
    engine=chatbot,
    prompt=f"{prompt}\n{speaker}:",
    max_tokens=150,
    n=1,
    temperature=0.8,
  )
  text = response.choices[0].text.strip()
  return text


@app.route("/", methods=["GET", "POST"])
def infinite_conversation():
  initial_question = (
    "You are a chatbot with two different personalities. "
    "Personality 1: Donald Glover, the actor, writer, comedian and musician who performs under the name Childish Gambino. "
    "Personality 2: Jessica Suarez, a music journalist who is catching up with Donald Glover after their first interview ten years ago. "
    "\n\nJessica: Hey Donald. I can't believe it's been 10 years since we talked."
  )
  api_key = request.form.get("api_key") if request.method == "POST" else None

  if request.method == "POST":
    conversation_history = request.form.get("conversation").split("\n")
    speaker1_history = [
      conv for i, conv in enumerate(conversation_history) if i % 2 == 0
    ]
    speaker2_history = [
      conv for i, conv in enumerate(conversation_history) if i % 2 != 0
    ]
    speaker1 = "Donald"
    speaker2 = "Jessica"
    prompt1 = f"{initial_question}\n" + "\n".join(speaker1_history)
    prompt2 = f"{initial_question}\n" + "\n".join(speaker2_history)
    response1 = generate_response(prompt1, "text-davinci-002", speaker1,
                                  api_key)
    response2 = generate_response(prompt2, "text-davinci-002", speaker2,
                                  api_key)

    response_with_speaker1 = f"{speaker1}: {response1}"
    response_with_speaker2 = f"{speaker2}: {response2}"
    conversation_history.append(response_with_speaker1)
    conversation_history.append(response_with_speaker2)
    conversation = "\n".join(conversation_history)
  else:
    conversation = initial_question
    conversation_history = [conversation]

  if request.headers.get("Accept") == "application/json":
    return jsonify({"conversation": conversation})
  else:
    return render_template_string(template, conversation=conversation)


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
