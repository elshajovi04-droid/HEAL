from flask import Flask, request, jsonify, send_from_directory
import nltk
import random

app = Flask(__name__)

# =========================
# Conversation Memory
# =========================

conversation_history = []
recent_replies = []


# =========================
# Emotion Keywords
# =========================

EMOTIONS = {

    "sad": [
        "sad", "cry", "crying", "upset",
        "hurt", "low", "lonely"
    ],

    "tired": [
        "tired", "exhausted", "sleepy",
        "drained", "fatigued"
    ],

    "happy": [
        "happy", "excited", "great",
        "amazing", "glad"
    ],

    "angry": [
        "angry", "mad", "frustrated",
        "annoyed", "irritated"
    ],

    "stressed": [
        "stressed", "stress",
        "overwhelmed", "pressure",
        "worried"
    ]
}


# =========================
# Reply Selection
# =========================

def choose_reply(replies):

    available = [
        reply for reply in replies
        if reply not in recent_replies
    ]

    if not available:
        available = replies

    reply = random.choice(available)

    recent_replies.append(reply)

    if len(recent_replies) > 6:
        recent_replies.pop(0)

    return reply


# =========================
# Emotion Detection
# =========================

def detect_emotion(message):

    words = nltk.wordpunct_tokenize(message.lower())

    scores = {}

    for emotion, keywords in EMOTIONS.items():

        scores[emotion] = sum(
            1 for word in keywords
            if word in words
        )

    best_emotion = "neutral"
    best_score = 0

    for emotion, score in scores.items():

        if score > best_score:
            best_score = score
            best_emotion = emotion

    return best_emotion


# =========================
# Conversation Type
# =========================

def detect_intent(message):

    text = message.lower().strip()


    # Listen
    if (
        "just listen" in text
        or "listen to me" in text
        or "i just want to talk" in text
        or "just want to talk" in text
        or "don't give advice" in text
        or "dont give advice" in text
    ):
        return "listen"


    # Advice
    if (
        "what should i do" in text
        or "what can i do" in text
        or "give me advice" in text
        or "i need advice" in text
        or "suggest something" in text
    ):
        return "advice"


    # Study / Academic
    if any(word in text for word in [
        "exam",
        "test",
        "assignment",
        "homework",
        "study",
        "studying",
        "college",
        "class",
        "lab",
        "marks",
        "subject",
        "syllabus"
    ]):
        return "study"


    # Casual greeting
    if text in [
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "hey buddy",
        "hi buddy",
        "hello buddy"
    ]:
        return "greeting"


    # Movie / entertainment
    if any(word in text for word in [
        "movie",
        "film",
        "song",
        "music",
        "series",
        "youtube"
    ]):
        return "casual"


    # Question
    if (
        text.startswith("what ")
        or text.startswith("why ")
        or text.startswith("how ")
        or text.startswith("when ")
        or text.startswith("where ")
        or text.startswith("who ")
    ):
        return "question"


    return "general"


# =========================
# HEAL Personality
# =========================

def generate_reply(emotion, intent, text):

    message = text.lower().strip()


    # =========================
    # I'm Fine
    # =========================

    if (
        message == "fine"
        or "i'm fine" in message
        or "im fine" in message
        or "i am fine" in message
    ):

        return (
            "Okay, I hear you. I hope you're okay. "
            "If you feel like talking about anything later, I'm here."
        )


    # =========================
    # Listen Mode
    # =========================

    if intent == "listen":

        return choose_reply([

            "Yeah, I'm listening. Take your time.",

            "Of course. You don't have to make it sound perfect. Just tell me what's on your mind.",

            "I'm listening. You can start wherever you want.",

            "Go ahead. I'm here, and I won't jump straight into advice."
        ])


    # =========================
    # Advice Mode
    # =========================

    if intent == "advice":

        return choose_reply([

            "Sure. Tell me what happened first, and we'll think through it properly.",

            "Okay. Give me a little context before we decide what to do.",

            "Yeah, tell me what's going on. Then we can look at your options.",

            "I'm listening. Let's understand the situation first before jumping to a solution."
        ])


    # =========================
    # Greeting
    # =========================

    if intent == "greeting":

        return choose_reply([

            "Heyy! What's up?",

            "Hey buddy 😄 How's your day going?",

            "Hey! I'm here. What's happening?",

            "Hii 😄 What are you up to?"
        ])


    # =========================
    # Study / College
    # =========================

    if intent == "study":

        if emotion == "stressed":

            return choose_reply([

                "Okay, don't panic yet. Tell me what you have to finish and how much time you have.",

                "Sounds like you've got a lot on your plate. Let's break it into smaller parts instead of looking at everything at once.",

                "Alright, let's make this manageable. What's the most urgent thing right now?"
            ])


        if emotion == "tired":

            return choose_reply([

                "Sounds like college has taken a lot out of you. What were you working on today?",

                "You sound pretty drained. What subject or work was keeping you busy?",

                "That's understandable after a long day. What do you still have left to finish?"
            ])


        return choose_reply([

            "Oh okay. What subject are you working on?",

            "Got it. What's the assignment or topic?",

            "College stuff ah? 😄 What are you working on right now?"
        ])


    # =========================
    # Casual Conversation
    # =========================

    if intent == "casual":

        return choose_reply([

            "Oh nice 😄 What did you watch or listen to?",

            "Interesting 👀 Tell me more about it.",

            "Okayyy 😄 Was it actually good?",

            "Nice! What did you like about it?"
        ])


    # =========================
    # Emotion + Mature Responses
    # =========================

    if emotion == "sad":

        return choose_reply([

            "Sounds like something's bothering you. Want to tell me what happened?",

            "You seem a little low today. What happened?",

            "That doesn't sound like a great day. Do you want to talk about what happened?",

            "I'm listening. What made you feel this way?"
        ])


    if emotion == "tired":

        return choose_reply([

            "You sound tired today. What made the day so exhausting?",

            "Sounds like today was a long one. What happened?",

            "You've had a tiring day, huh? What kept you so busy?",

            "Okay, you're tired. 😭 What happened today?"
        ])


    if emotion == "happy":

        return choose_reply([

            "Oh nice 😄 What's making you feel this good?",

            "That's good to hear! What happened?",

            "Yess 😂 Tell me what happened.",

            "Okay, something clearly went well today. What is it?"
        ])


    if emotion == "angry":

        return choose_reply([

            "Okay, something clearly annoyed you. What happened?",

            "That sounds frustrating. What exactly happened?",

            "Yeah, I can tell you're annoyed. Want to tell me what caused it?",

            "Alright, what happened? I'm listening."
        ])


    if emotion == "stressed":

        return choose_reply([

            "Sounds like you've got a lot going on. What's stressing you out the most?",

            "Okay, let's not look at everything at once. What's the biggest problem right now?",

            "You seem pretty overwhelmed. What are you dealing with?",

            "Alright, tell me what's piling up on your mind."
        ])


    # =========================
    # Context Awareness
    # =========================

    if len(conversation_history) >= 2:

        previous = conversation_history[-2]

        previous_emotion = previous["emotion"]

        if previous_emotion != "neutral":

            return choose_reply([

                f"You mentioned feeling {previous_emotion} earlier. How are things now?",

                "We were talking about what was bothering you earlier. Did anything change?",

                "You mentioned something was going on earlier. Want to continue?"
            ])


    # =========================
    # Question Mode
    # =========================

    if intent == "question":

        return choose_reply([

            "Hmm, good question. Tell me a little more about what you're trying to figure out.",

            "Let's look at it properly. What's the context?",

            "Interesting question. What made you think about that?"
        ])


    # =========================
    # General Conversation
    # =========================

    return choose_reply([

        "Hmm, tell me more.",

        "Ohh okay. What happened next?",

        "I get you. And then?",

        "Interesting. What are you thinking about it?",

        "Okay, I'm following. Tell me more.",

        "Got it 😄 What's on your mind?"
    ])


# =========================
# Human Support Boundary
# =========================

def needs_human_support(text):

    message = text.lower()

    phrases = [

        "need someone",
        "talk to someone",
        "need help from someone",
        "want someone to talk",
        "counsellor",
        "counselor",
        "trusted person"
    ]

    return any(
        phrase in message
        for phrase in phrases
    )


# =========================
# Frontend Routes
# =========================

@app.route("/")
def home():

    return send_from_directory(".", "index.html")


@app.route("/style.css")
def style():

    return send_from_directory(".", "style.css")


@app.route("/script.js")
def script():

    return send_from_directory(".", "script.js")


# =========================
# Chat Route
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json() or {}

    user_message = data.get("message", "").strip()


    if not user_message:

        return jsonify({

            "reply": "Tell me what's on your mind.",

            "emotion": "neutral",

            "intent": "general"
        })


    # Analyze
    emotion = detect_emotion(user_message)

    intent = detect_intent(user_message)


    # Save conversation
    conversation_history.append({

        "message": user_message,

        "emotion": emotion,

        "intent": intent
    })


    # Keep recent context
    if len(conversation_history) > 10:

        conversation_history.pop(0)


    # Generate reply
    reply = generate_reply(

        emotion,

        intent,

        user_message
    )


    # Human support
    if needs_human_support(user_message):

        reply += (
            " And if things feel difficult to handle, "
            "talking to someone you trust or a counsellor "
            "can be helpful too."
        )


    return jsonify({

        "reply": reply,

        "emotion": emotion,

        "intent": intent
    })


# =========================
# Run HEAL
# =========================

if __name__ == "__main__":

    app.run(debug=True,host="0.0.0.0")