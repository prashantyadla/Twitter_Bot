# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.utils import get_supported_interfaces

from ask_sdk_model.intent import Intent
from ask_sdk_model.dialog import delegate_directive
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
import json

from apl.apl_content import apl_main_template, _load_apl_document
import twitter_util
import text_util

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Twitter Bot! Here, you can hear the latest tweets from your favorite Twitter User! Try it by asking \"What is the latest tweet from Justin Bieber\"."
        
        # APL handler
        
        # logger.info(get_supported_interfaces(handler_input).alexa_presentation_apl)
        # handler_input.response_builder.add_directive(
        #         RenderDocumentDirective(
        #             document=_load_apl_document("./apl/welcome.json"),
        #             datasources = apl_main_template()
        #         )
        #     )
        
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    document=_load_apl_document("./apl/welcome.json"),
                    datasources = apl_main_template(speak_output)
                )
            )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ReadLatestNTweetsForUserIntentHandler(AbstractRequestHandler):
    """Handler for Reading Latest Tweet Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ReadLatestNTweetsForUserIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Get any existing attributes from the incoming request
        session_attr = handler_input.attributes_manager.session_attributes
        
        slots = handler_input.request_envelope.request.intent.slots
        num = slots['number']
        name = slots['name']
        
        logger.info(F'num: {num.value}')
        logger.info(F'name: {name.value}')
        speak_output = ""
        
        username = twitter_util.getUserName(name)
        tweets = twitter_util.getLatestTweets(username, num.value).data
        
        # session_attr['1'] = text_util.getSpeakableTweet(tweets[0], username)
        session_attr['2'] = text_util.getSpeakableTweet(tweets[1], username)
        session_attr['3'] = text_util.getSpeakableTweet(tweets[2], username)
        session_attr['4'] = text_util.getSpeakableTweet(tweets[3], username)
        session_attr['5'] = text_util.getSpeakableTweet(tweets[4], username)
        
        # logger.info(session_attr['1'])
        
        datasource_text = text_util.getSpeakableTweet(tweets[0], username)
        
        # speak_output = text_util.getSpeakableTweets(tweets, username) + ". Would you like to hear more tweet?"
        speak_output = text_util.getSpeakableTweet(tweets[0], username) + ". Would you like to hear another tweet from this person?"
        
        logger.info(speak_output)
        
        session_attr["idx"] = 2

        # session_attr['idx'] = 2 if num.value is None else int(num.value)
        session_attr['username'] = username
        
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    document=_load_apl_document("./apl/default.json"),
                    datasources = apl_main_template(datasource_text)
                )
            )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Please let me know how twitter bot can help you")
                .response
        )


class MoreTweetIntentHandler(AbstractRequestHandler):
    """Handler for Reading More Tweet Intent."""
    def can_handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        return (ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input) and "idx" in session_attr)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = "Ok. Let's get some more tweet."+ '<break time="1s"/>'
        
        index = session_attr["idx"]
        logger.info(index)
        session_attr['idx'] = session_attr['idx']+1
        
        if(index <= 5):
            speak_output += session_attr[str(index)]
            datasource_text = session_attr[str(index)]
        
        speak_output += '<break time="1s"/>' +"Would you like to hear another tweet from this person?"
        
        logger.info(speak_output)
        
        # APL handler
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    document=_load_apl_document("./apl/default.json"),
                    datasources = apl_main_template(datasource_text)
                )
            )

        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Please let me know how twitter bot can help you")
                .response
        )
        
        # intent_name = "AMAZON.YesIntent"
        # return (
        #     handler_input.response_builder
        #         .speak(speak_output)
        #         .add_directive(
        #             delegate_directive.DelegateDirective(
        #                 updated_intent = Intent(name=intent_name)
        #             )
        #         )
        #         .response
        # )


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

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ReadLatestNTweetsForUserIntentHandler())
sb.add_request_handler(MoreTweetIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()