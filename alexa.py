# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
from datetime import datetime
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "What would you like to know?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HeartRateIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("HeartRateIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In HeartRateIntentHandler")
        url = "https://comp590-a2.herokuapp.com/heartrate/last"
        response = requests.get(url).json()
        print(response)
        speak_output = "Your heart rate is " + str(response["heart rate"]) + " and this was recorded " + response["time offset"] + " ago"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
                
        )

# class FitbitAndSensorDataIntentHandler(AbstractRequestHandler):
#     '''handler for opening project'''
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("FitbitAndSensorData")(handler_input)
#     def handle(self, handler_input):
#         speak_output = "Welcome to Fitbit and Sensor. You can ask me about your health vitals or your environment."
#         return(handler_input.response_builder.speak(speak_output).ask("What would you like to know?").response)

# class HeartRateIntentHandler(AbstractRequestHandler):
#     '''Handler for heart rate '''
#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("HeartRateIntent")(handler_input)
#     def handle(self, handler):
#         logger.info("In HeartRateIntentHandler")
#         url = "https://comp590-a2.herokuapp.com/heartrate/last"
#         response = requests.get(url).json()
#         print(response)
#         if response.status_code == 200:
#             ret = response.text
#         else:
#             ret = "Error occurred"
#         speech = ret + " Would you like to hear another one?"
#         handler_input.response_builder.speak(speech).ask(speech)
#         return handler_input.response_builder.response

class StepCountIntentHandler(AbstractRequestHandler):
    '''Handler for step count'''
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("StepCountIntent")(handler_input)
    def handle(self, handler_input):
        logger.info("In HeartRateIntentHandler")
        url = "https://comp590-a2.herokuapp.com/steps/last"
        response = requests.get(url).json()
        print(response)
        speak_output = "Your step count was recorded " + response["offset"] + " ago, and the count was " + str(response["step-count"]) + " steps"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class PoseIntentHandler(AbstractRequestHandler):
    '''Handler for pose'''
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PoseIntent")(handler_input)
    def handle(self, handler_input):
        logger.info("In PoseIntentHandler")
        url = "https://comp590-a2.herokuapp.com/sensors/pose"
        response = requests.get(url).json()
        print(response)
        
        # time 
        timestamp = response["timestamp"]
        timestamp_datetime = datetime.fromtimestamp(timestamp)
        time_now = datetime.now()
        time_diff_base = time_now - timestamp_datetime
        time_diff_minutes = time_diff_base.total_seconds() / 60
        hours = 0
        while time_diff_minutes > 60:
            hours += 1
            time_diff_minutes -= 60
        time_diff_minutes_rounded = round(time_diff_minutes, 2)
        
        
        #speak_output = "test"
        speak_output = "You were seen " + response["pose"] + " , " + str(hours) + " hours and " + str(time_diff_minutes_rounded) + " minutes ago"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ClimateIntentHandler(AbstractRequestHandler):
    '''Handler for climate'''
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ClimateIntent")(handler_input)
    def handle(self, handler_input):
        logger.info("In ClimateIntentHandler")
        url = "https://comp590-a2.herokuapp.com/sensors/env"
        response = requests.get(url).json()
        print(response)
        speak_output = "Right now, the indoor tempterature is " + str(response["temp"]) + " , and the humidity is " + str(response["humidity"])

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class ActivityIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ActivityIntent")(handler_input)
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        activity_slot = slots["ACTIVITY_DATE"]
        o_date = str(activity_slot.value)
        date = "2022" + o_date[4:]
        if activity_slot.value:
            url = "https://comp590-a2.herokuapp.com/activity/" + date
        else:
            url = "https://comp590-a2.herokuapp.com/activity/today" 
        response = requests.get(url).json()
        light = response["lightly-active"]
        sedentary = response["sedentary"]
        active = response["very-active"]
        if light > sedentary and light > active:
            most = "lightly-active"
        elif sedentary > light and sedentary > active:
            most = "sedentary"
        elif active > light and active > sedentary:
            most = "active"
        speak_output = "On this day, you had " + str(response["lightly-active"]) + " minutes of light activity, " + str(response["sedentary"]) + " minutes sedentary, and " + str(response["very-active"]) + " minutes very active. You spent most of the day being " + most
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
         )
class SleepIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SleepIntent")(handler_input)
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        activity_slot = slots["SLEEP_DATE"]
        o_date = str(activity_slot.value)
        date = "2022" + o_date[4:]
        if activity_slot.value:
            url = "https://comp590-a2.herokuapp.com/sleep/" + date
        else:
            url = "https://comp590-a2.herokuapp.com/sleep/today" 
        response = requests.get(url)
        if response == "No data available for this day.":
            speak_output = "There is no data available for this day"
        else:
            sleep_data = response.json()
            deep = sleep_data["deep"]
            rem = sleep_data["rem"]
            light = sleep_data["light"]
            wake = sleep_data["wake"]
            total_min = deep + rem + light + wake
            speak_output = "On this day, you slept for " + str(total_min) + " minutes."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
         )
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

# sb.add_request_handler(FitbitAndSensorDataIntentHandler())
sb.add_request_handler(HeartRateIntentHandler())
sb.add_request_handler(StepCountIntentHandler())
sb.add_request_handler(ClimateIntentHandler())
sb.add_request_handler(PoseIntentHandler())
sb.add_request_handler(ClimateIntentHandler())
sb.add_request_handler(ActivityIntentHandler())
sb.add_request_handler(SleepIntentHandler())

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()