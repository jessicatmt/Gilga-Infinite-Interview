import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_response(messages, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    text = response.choices[0].message['content'].strip()
    return text

@app.route("/", methods=["GET", "POST"])
def infinite_conversation():
    initial_message = {
        "role": "system",
        "content": (
            "You are a chatbot with two different personalities. "
            "Personality 1: Donald Glover, the actor, writer, comedian and musician who performs under the name Childish Gambino. "
            "Personality 2: Jessica Suarez, a music journalist who is catching up with Donald Glover after their first interview ten years ago. "
            "Jessica interviewed Donald 11 years ago in New York, and they are catching up with each other in a friendly conversation."
        ),
    }
    
    first_user_message = {"role": "user", "content": "I can't believe it's been 10 years since I first interviewed you."}
    api_key = request.form.get("api_key") if request.method == "POST" else None

    if request.method == "POST":
        conversation_history = request.form.get("conversation").split("\n")
        messages = [initial_message, first_user_message]

        for index, message in enumerate(conversation_history[1:]):
            role = "assistant" if index % 2 == 0 else "user"
            content = message.split(": ", 1)[1]
            messages.append({"role": role, "content": content})

        response = generate_response(messages, api_key)
        response_with_speaker = f"{'Donald' if len(conversation_history) % 2 == 0 else 'Jessica'}: {response}"
        conversation_history.append(response_with_speaker)
        conversation = "\n".join(conversation_history)

        if request.headers.get("Accept") == "application/json":
            return jsonify({"conversation": conversation})
        else:
            return render_template("index.html", conversation=conversation)
    else:
        conversation = f"Jessica: {first_user_message['content']}"

    if request.headers.get("Accept") == "application/json":
        return jsonify({"conversation": conversation})
    else:
        return render_template("index.html", conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')