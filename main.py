"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import Python.ResponseBuilder as ResponseBuilder
import Python.EncounterIntentHandler as EncounterHandler
import Python.RoomIntentHandler as RoomHandler

attributes = {}

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = attributes
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Virtual DM. " \
                    "You are currently in room " \
                    + str(attributes["room"]) + \
                    ". Where would you like to go?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Where would you like to go?"
    should_end_session = False
    return ResponseBuilder.build_response(ResponseBuilder.build_speechlet_response(card_title, speech_output,
        reprompt_text, should_end_session), attributes)
        

def get_travel_response(target):
    room = attributes["room"]
    
    if target.lower() == "north":
        attributes["room"] = (room+5) % 8
    elif target.lower() == "south":
        attributes["room"] = (room+3) % 8
    elif target.lower() == "west":
        attributes["room"] = (room-room%3) + (room+2)%3
    elif target.lower() == "east":
        attributes["room"] = (room-room%3) + (room+1)%3
    else:
        card_title = "Moving"
        speech_output = "I didn't understand that. " \
                        "You are currently in room " \
                        + str(attributes["room"]) + \
                        ". Where would you like to go?"
        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        reprompt_text = "Where would you like to go?"
        should_end_session = False
        return ResponseBuilder.build_response(ResponseBuilder.build_speechlet_response(card_title,
            speech_output, None, should_end_session), attributes)
    
    card_title = "Moving"        
    speech_output = "You are currently in room " \
                    + str(attributes["room"]) + \
                    ". Where would you like to go?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Where would you like to go?"
    should_end_session = False
    return ResponseBuilder.build_response(ResponseBuilder.build_speechlet_response(card_title,
        speech_output, None, should_end_session), attributes)
    

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return ResponseBuilder.build_response(ResponseBuilder.build_speechlet_response(
        card_title, speech_output, None, should_end_session), attributes)


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
          
    # Set the initial game state
    attributes["room"] = 4
    


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "TravelIntent":
        return get_travel_response(intent["slots"]["direction"]["value"])
    elif intent_name == "AMAZON.RepeatIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    else:
        attributes = event["session"]["attributes"]

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
