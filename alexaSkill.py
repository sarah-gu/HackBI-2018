import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hey there!"
        
        handler_input.response_builder.speak(speech_text).set_card(
                                                                   SimpleCard("TTS", speech_text)).set_should_end_session(
                                                                                                                          False)
        return handler_input.response_builder.response


class TTSIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TTSIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        person = str(handler_input.request_envelope.request.intent.slots["Person"].value).lower()
        
        #text = {"sarah" : "This is Sarah", "sanjana" : "This is Sanjana"}
        #speech_text = text[person]
        
        file_path = {"sanjana" : "./sanjana.txt", "sarah" : "./sarah.txt"}
        file = open(file_path[person], 'r')
        speech_text = str(file.readline())
        
        handler_input.response_builder.speak(speech_text).set_card(
                                                                   SimpleCard("TTS", speech_text)).set_should_end_session(
                                                                                                                          True)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Tell me to read someone's file."
        
        handler_input.response_builder.speak(speech_text).ask(
                                                              speech_text).set_card(SimpleCard(
                                                                                               "TTS", speech_text))
        return handler_input.response_builder.response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"
        
        handler_input.response_builder.speak(speech_text).set_card(
                                                                   SimpleCard("TTS", speech_text))
        return handler_input.response_builder.response

class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
        This handler will not be triggered except in that locale,
        so it is safe to deploy on any locale.
        """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
                       "Sorry, I can't help you with that.")
                       reprompt = "Tell me whose file to read."
                       handler_input.response_builder.speak(speech_text).ask(reprompt)
                       return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
        respond with custom message.
        """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True
    
    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        
        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TTSIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
