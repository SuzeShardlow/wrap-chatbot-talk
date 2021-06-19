from flask import Flask

from flask import render_template
from flask import request
from flask import session

import json
import random
import string

# Load temporary participant data from JSON file.
with open("participants.json", "r") as f:
    participant_data = json.load(f)

# Initialize Flask.
app = Flask(__name__)

# Set a secret key for session management reasons.
# Flask internals...
app.secret_key = "factnetwork"

# Returns true if the list of words in "keywords" 
# contains any of the words in the list "message_words".
# Used to determine user intent.
def contains_keywords(keywords, message_words):
    matched_words = set(keywords) & set(message_words)
    return len(matched_words) > 0

# Get the participant's response for a specific intent.  Where
# the participant has > 1 response, choose randomly.  Where the
# participant has no responses, return a default I don't know
# sort of response.
def get_participant_response(participant_record, intent):
    # TODO do this properly
    possible_responses = participant_record[intent]
    num_possible_responses = len(possible_responses)

    if (num_possible_responses == 0):
        return "Sorry I don't know much about that."

    return possible_responses[random.randrange(0, num_possible_responses, 1)]

# Determine how to respond to a message from the user.
def interpret_message(message):
    # The name the bot will reply with.
    bot_name = "Bot"

    # Check that the user actually typed something...
    if (len(message) == 0):
        return "{}: Please ask a question.".format(bot_name)
    
    # Remove punctuation from message to make it easier to match.
    message_no_punctuation = message.translate(str.maketrans("", "", string.punctuation))

    # Make the message all lower case for comparison purposes.
    message_no_punctuation = message_no_punctuation.lower()

    # Make a list of words in the user's message by using the 
    # spaces in the string as a word separator.
    message_words = message_no_punctuation.split()

    # See if we are already talking to a participant.  We will know this
    # by checking to see if participant_name is set in the current session.
    if (session.get("participant_name")):
        # We are talking to a participant, so let's get which one, and update 
        # the name that the bot will reply with as well as get that participant's
        # data from the database.
        participant_name = session["participant_name"]
        bot_name = participant_name
        participant_record = None

        # Also look up the participant in the "database".
        for participant in participant_data["participants"]:
            if (participant["name"] == participant_name):
                participant_record = participant

        # See if the question matches any of the things that we 
        # can ask the currently selected participant.

        # Is this a how old are you intent?
        participant_age_intent_keywords = ["age", "old", "birthday", "teenager"]

        if (contains_keywords(participant_age_intent_keywords, message_words)):
            return "{}: I am {} years old.".format(bot_name, participant_record["age"])

        # Is this a where are you from intent?
        participant_home_intent_keywords = ["home", "town", "city", "where", "located"]

        if (contains_keywords(participant_home_intent_keywords, message_words)):
            return "{}: I am from {}.".format(bot_name, participant_record["city"])

        # Is this a contraception intent?
        participant_contraception_intent_keywords = ["contraception", "condom", "condoms", "pill", "prevention", "coil", "planning"]

        if (contains_keywords(participant_contraception_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "contraception"))

        # Is this a sex intent?
        participant_sex_intent_keywords = ["sex", "intercourse", "oral", "shag", "virgin", "virginity", "romance", "romantic", "love", "kiss", "kissing", "masterbate", "masterbating", "masterbation", "sleep", "slept", "sleeping"]
        if (contains_keywords(participant_sex_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "sex"))

        # Is this a sex-ed intent?
        participant_sex_ed_intent_keywords = ["education", "science", "lessons", "lesson", "periods", "period", "learn", "learning", "teacher", "teachers", "biology", "menstruation"]
        if (contains_keywords(participant_sex_ed_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "sex-ed"))

        # Is this a marriage intent?
        participant_marriage_intent_keywords = ["marriage", "partner", "partnership", "husband", "wife", "marry", "married"]
        if (contains_keywords(participant_marriage_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "marriage"))

        # Is this an AIDS intent?
        participant_aids_intent_keywords = ["aids", "hiv", "needles", "contract"]
        if (contains_keywords(participant_aids_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "aids"))

        # Is this a children intent?
        participant_children_intent_keywords = ["children", "child", "kids", "kid", "baby", "babies", "offspring"]
        if (contains_keywords(participant_children_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "children"))

        # Is this a career intent?
        participant_career_intent_keywords = ["school", "college", "university", "career", "job", "employment", "jobs", "work"]
        if (contains_keywords(participant_career_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "career"))

        # Is this a values intent?
        participant_values_intent_keywords = ["values", "principles", "morals", "moral", "value", "religion", "religious", "faith", "belief", "beliefs", "christian", "catholic", "catholics", "slag", "slags", "politics"]
        if (contains_keywords(participant_values_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "values"))

        # Is this a relationships intent?
        participant_relationships_intent_keywords = ["boyfriend", "girlfriend", "relationship", "relationships", "steady", "daughter", "son"]
        if (contains_keywords(participant_relationships_intent_keywords, message_words)):
            return "{}: {}".format(bot_name, get_participant_response(participant_record, "relationships"))

    # Check if a participant name was mentioned by the user.  Load the 
    # participant names from the sample data for now and make them lower case for comparison.
    all_participants = []

    for participant in participant_data["participants"]:
        all_participants.append(participant["name"].lower())

    names_mentioned = set(message_words) & set(all_participants)

    # It is a I would like to talk to <name> request if the message consists only of 
    # a participant name, or contains a participant name and at least one of the 
    # keywords for the choose participant intent.
    if (len(names_mentioned) > 0):
        # A name has been mentioned, so get the name of the participant.
        chosen_participant = next(iter(names_mentioned))

        # Look for "I'd like to talk to <name>" keywords.
        choose_participant_intent_keywords = ["speak", "talk", "with", "try", "there", "here", "available", "about", "around", "home", "in", "awake", "online", "active", "keyboard", "please", "ask"]

        # If a choose participant keyword matched or the user just typed a
        # participant name, then this is a request to talk to someone by name.
        if (contains_keywords(choose_participant_intent_keywords, message_words)) or (message_no_punctuation == chosen_participant):        
            # Store the participant name in the user's session so that we know the 
            # context of the conversation for subsequent requests.
            session["participant_name"] = chosen_participant.title()

            # Update the bot name
            bot_name = session["participant_name"]

            return "{}: Hello, you're talking to {}.".format(bot_name, session["participant_name"])

    # Look for "who can I talk to" keywords.
    who_intent_keywords = ["who", "name", "names", "person", "people", "talk", "speak"]

    if (contains_keywords(who_intent_keywords, message_words)):
        # This is a who can I talk to request, so get a list of the participants.
        participant_names = ""

        for participant in participant_data["participants"]:
            participant_names = "{}{}, ".format(participant_names, participant["name"])

        # Remove final ,
        participant_names = participant_names[:-2]

        return "{}: You can talk to any of these participants: {}.".format(bot_name, participant_names)

    # Look for hello / welcome / start of conversation keywords.
    welcome_intent_keywords = ["hello", "hi", "hey", "morning", "afternoon", "about"]

    if (contains_keywords(welcome_intent_keywords, message_words)):
        # This is a welcome / start of conversation message and will always come from
        # "Bot" rather than a specific participant.
        return "Bot: Hi, it's the archive of the Women, Risk and Aids Project here.  Ask me which participants you can speak with to explore their experiences."

    # Look for goodbye / end of conversation keywords.
    goodbye_intent_keywords = ["goodbye", "bye", "farewell", "cheerio"]

    if (contains_keywords(goodbye_intent_keywords, message_words)):
        # This is a goodbye / end of conversation message, end the user"s 
        # session.
        session.clear()
        return "{}: Goodbye, thanks for chatting!".format(bot_name)

    # Look for filler words that don"t really merit a reply and 
    # reply with a general platitude.
    filler_intent_keywords = ["great", "cool", "perfect", "thanks", "awesome", "nice"]

    if (contains_keywords(filler_intent_keywords, message_words)):
        return "{}: Thank you.".format(bot_name)

    # Catch all - we were not able to determine the user intent...
    return "{}: Sorry - I don't understand, please ask another question.".format(bot_name)

@app.route("/")
def home():
    # Send the front end web page.
    return render_template("index.html")

@app.route("/message", methods=["POST"])
def process_message():
    return interpret_message(request.form["message"])
