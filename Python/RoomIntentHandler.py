import ResponseBuilder
import json
import os

def handleTravel(intent, session):
    direction = intent["slots"]["direction"]["value"]
    connected = session["attributes"]["room"]["connected"]
    directions = connected.keys()

    if direction in directions:
        room_path = os.environ["LAMBDA_TASK_ROOT"] + "/Json/" + connected[direction] + ".json"
        room_data = open(room_path).read()
        session["attributes"]["room"] = json.loads(room_data)
    else:
        title = "Invalid Direction"
        reprompt_text = "What would you like to do?"
        output = "There is no way to go " + direction + ". " + reprompt_text
        return ResponseBuilder.buildResponse(ResponseBuilder.buildSpeechletResponse(title, output, reprompt_text, False), session["attributes"])


def handleInvestigate(intent, session):
    target = intent["slots"]["feature"]["value"]
    features = session["attributes"]["room"]["features"]
    feature_names = features.keys()

    if target in feature_names:
        title = features[target]["name"]
        reprompt_text = "What would you like to do?"
        output = features[target]["description"] + reprompt_text
    else:
        title = "Invalid Target"
        reprompt_text = "What would you like to do?"
        output = "I don't see a(ny) " + target + ". " + reprompt_text
    return ResponseBuilder.buildResponse(ResponseBuilder.buildSpeechletResponse(title, output, reprompt_text, False), session["attributes"])


def handleAttack(intent, session):
    target = intent["slots"]["npc"]["value"]
    npcs = session["attributes"]["room"]["npcs"]
    npc_names = npcs.keys()

    if target in npc_names:
        title = "Combat!?"
        reprompt_text = "What would you like to do?"
        output = npcs[target]["full_name"] + " deftly dodges your pitiful attack. " + reprompt_text
    else:
        title = "Invalid Target"
        reprompt_text = "What would you like to do?"
        output = "I don't see a(ny) " + target + ". " + reprompt_text
    return ResponseBuilder.buildResponse(ResponseBuilder.buildSpeechletResponse(title, output, reprompt_text, False), session["attributes"])


def handleTalk(intent, session):
    target = intent["slots"]["npc"]["value"]
    npcs = session["attributes"]["room"]["npcs"]
    npc_names = npcs.keys()

    if target in npc_names:
        title = npcs[target]["full_name"]
        reprompt_text = "What would you like to do?"
        output = npcs[target]["response"] + reprompt_text
    else:
        title = "Invalid Target"
        reprompt_text = "What would you like to do?"
        output = "I don't see a(ny) " + target + ". " + reprompt_text
    return ResponseBuilder.buildResponse(ResponseBuilder.buildSpeechletResponse(title, output, reprompt_text, False), session["attributes"])


def handleIntent(intent, session):
    intent_name = intent["name"]

    if intent_name == "travel":
        return handleTravel(intent, session)
    elif intent_name == "investigate":
        return handleInvestigate(intent, session)
    elif intent_name == "talk":
        return handleTalk(intent, session)
    else:
        title = "Invalid Action"
        reprompt_text = "What would you like to do?"
        output = "You can't do that right now. " + reprompt_text
        return ResponseBuilder.buildResponse(ResponseBuilder.buildSpeechletResponse(title, output, reprompt_text, False), session["attributes"])