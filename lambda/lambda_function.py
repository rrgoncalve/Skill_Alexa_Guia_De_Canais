# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests
import json
from requests.exceptions import HTTPError
from datetime import datetime, timedelta



from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

id_canal_data=""
aux=""


def programacao(id_canal,prox_):
    currentdate = datetime.now()#Data atual com hora
    dateStart = currentdate.strftime("%Y-%m-%d")#data inicial
    timeStart = "T00:00:00Z"
    dateEnd = currentdate.strftime("%Y-%m-%d")#Data final
    timeEnd = "T23:59:00Z"

    res1=""

    #Url para resgatar a programação
    urll = "https://programacao.netcombo.com.br/gatekeeper/exibicao/select?q=id_revel:1_"+str(id_canal)+'&callback=callbackShows&json.wrf=callbackShows&wt=json&rows=100000&sort=id_canal%20asc,dh_inicio%20asc&fl=dh_fim%20dh_inicio%20st_titulo%20titulo%20id_programa%20id_canal&fq=dh_inicio:%5B'+str(dateStart) + str(timeStart) + '%20TO%20' + str(dateEnd) + str(timeEnd) + '%5D&callback=callbackShowsRequest%20method:GET'      
    responses = requests.get(urll)
    status = responses.status_code


    if (status != 204 and responses.headers["content-type"].strip().startswith("application/json")):
        try:
            res1=responses.text
        except ValueError:            
            print('Bad Data from Server. Response content is not valid JSON')

    elif (status != 204):
        try:
            res1=responses.text
        except ValueError:
            print('Bad Data From Server. Reponse content is not valid text')
            
    obj = json.loads(res1[14:-1])
    
    
    
    for i in obj['response']['docs']:
        #data_replase = str(i['dh_fim'])[0:10]+" "+str(i['dh_fim'])[11:-1]+":00"
        #data_hora = datetime.strptime(data_replase, '%Y-%m-%d %H:%M:%S')- timedelta(hours=3)

        #data_atual=str(currentdate)[0:-7]
        
        data_ = str(i['dh_fim'])[0:10]        
        data_replase = data_+" "+str(i['dh_fim'])[11:-1]+":00"        
        data_hora = datetime.strptime(data_replase, '%Y-%m-%d %H:%M:%S')- timedelta(hours=-3)
        data_hora = data_+" "+ str(data_hora)[11:-2]+"00"
        data_atual=str(currentdate)[0:-7]
        
        if prox_==0:
            if data_hora > data_atual:
                global aux
                aux=data_hora
                return i['titulo'] 
        else:
            if data_hora > aux:
                return i['titulo']
           
            
       

    pass



class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = "Quer saber o que está passando na TV neste momento? Basta perguntar me dizer o nome do canal!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CanalNameIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CanalNameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots_ = handler_input.request_envelope.request.intent.slots
        
        try:
            canal = slots_["canalname"].value
        except ValueError:
            canal = ""
            
        #try:    
           # incremento=slots_["incrementoname"].value
        #except ValueError:
            #incremento=""

        pesquisa=canal#+" "+incremento
        
        url = "https://programacao.netcombo.com.br/gatekeeper/canal/select?q=id_cidade:1&callback=callbackChannels&json.wrf=callbackChannels&wt=json&rows=10&start=0&sort=cn_canal%20asc&fl=id_canal%20st_canal%20cn_canal%20nome%20url_imagem&fq=st_canal:"+pesquisa+"&_=1577582659100&callback=callbackChannels"
        print(url)
        
        response = requests.get(url)
        status = response.status_code
        res=""
        
        if (status != 204 and response.headers["content-type"].strip().startswith("application/json")):
            try:
                res=response.text
            except ValueError:
                #print('Dados inválidos do servidor. O conteúdo da resposta não é um JSON válido')
                res="-1"
        elif (status != 204):
            try:
                res=response.text
            except ValueError:
                #print('Dados inválidos do servidor. O conteúdo da resposta não é um texto válido')
                res="-1"
            
        #speak_output = "Você pode dizer olá para mim! Como posso ajudar?"
        if res=="-1":
            speak_output = "Canal não encontrado!"
        else:    
            pythonObj = json.loads(res[17:-1])
            id_canal_ = pythonObj['response']['docs'][0]['id_canal']
            nome_canal =pythonObj['response']['docs'][0]['nome']
            url_imagem =pythonObj['response']['docs'][0]['url_imagem']
            global id_canal_data
            id_canal_data=id_canal_
            a = programacao(id_canal_,0)
            speak_output = "Está passando agora no canal " + nome_canal +", "+ a #+ str(datetime.now())#Data atual com hora
            
            
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CanalCompostoIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CanalCompostoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots_ = handler_input.request_envelope.request.intent.slots
        
        try:
            canal = slots_["canal"].value
        except ValueError:
            canal = ""
            
        try:    
            incremento=slots_["incremento"].value
        except ValueError:
            incremento=""

        pesquisa=canal+"_"+incremento
        
        url = "https://programacao.netcombo.com.br/gatekeeper/canal/select?q=id_cidade:1&callback=callbackChannels&json.wrf=callbackChannels&wt=json&rows=10&start=0&sort=cn_canal%20asc&fl=id_canal%20st_canal%20cn_canal%20nome%20url_imagem&fq=st_canal:"+pesquisa+"&_=1577582659100&callback=callbackChannels"
        print(url)
        
        response = requests.get(url)
        status = response.status_code
        res=""
        
        if (status != 204 and response.headers["content-type"].strip().startswith("application/json")):
            try:
                res=response.text
            except ValueError:
                #print('Dados inválidos do servidor. O conteúdo da resposta não é um JSON válido')
                res="-1"
        elif (status != 204):
            try:
                res=response.text
            except ValueError:
                #print('Dados inválidos do servidor. O conteúdo da resposta não é um texto válido')
                res="-1"
            
        #speak_output = "Você pode dizer olá para mim! Como posso ajudar?"
        if res=="-1":
            speak_output = "Canal não encontrado!"
        else:    
            pythonObj = json.loads(res[17:-1])
            id_canal_ = pythonObj['response']['docs'][0]['id_canal']
            nome_canal =pythonObj['response']['docs'][0]['nome']
            url_imagem =pythonObj['response']['docs'][0]['url_imagem']
            global id_canal_data
            id_canal_data=id_canal_
            a = programacao(id_canal_,0)
            speak_output = "Está passando agora no canal " + nome_canal +", "+ a #+ str(datetime.now())#Data atual com hora
            
            
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ProximoProgramaIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ProximoProgramaIntent")(handler_input)

    def handle(self, handler_input):

        global id_canal_data
        a = programacao(id_canal_data,1)
        speak_output = "Vai passar, "+ a #+ str(datetime.now())#Data atual com hora

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
        speak_output = "Você pode dizer o canal para mim! Como posso ajudar?"

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
        speak_output = "Até mais!"

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
        speech = "Hum, não tenho certeza. Você pode dizer o nome do canal ou Ajuda. O que você gostaria de fazer?"
        reprompt = "Eu não peguei isso. Com o que posso ajudar?"

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
        speak_output = "Você acabou de acionar " + intent_name + "."

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

        speak_output = "Desculpe, tive problemas para fazer o que você pediu. Por favor, tente novamente."

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
sb.add_request_handler(CanalNameIntentHandler())
sb.add_request_handler(CanalCompostoIntentHandler())
sb.add_request_handler(ProximoProgramaIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()