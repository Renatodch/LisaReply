import subprocess
import sys
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from openai.error import RateLimitError
from app.botMessages import botMessages, indicators
from app.models import Conversation
from llama_index import  ListIndex,GPTVectorStoreIndex, VectorStoreIndex, ServiceContext, SimpleDirectoryReader,LLMPredictor, PromptHelper
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine

from langchain import OpenAI
import openai
import os

from app.keys import API_KEY


model_id = 'gpt-3.5-turbo'

class Chatbot:
    __instance = None
    index = None
    query_engine = None
    def __init__(self):
        if Chatbot.__instance is not None:
            raise Exception("Singleton ya existe")
        else:
            print("######### INICIALIZANDO CHATBOT ############")
            Chatbot.__instance = self

        self.init_msg = {'role': 'system', 'content': botMessages["chatPurpose"]}
        openai.api_key = API_KEY
        os.environ['OPENAI_API_KEY'] = API_KEY
        self.update_index() # when boot

    @staticmethod
    def get_instance():
        if Chatbot.__instance is None:
            Chatbot()
        return Chatbot.__instance


    def response(self, user, message):
        conversations = [self.init_msg]
        for msg in Chatbot.get_instance().load_chat(user):
            conversations.append({'role':'user','content':msg.request})
            conversations.append({'role':'assistant','content':msg.response})

        conversations.append(self.init_msg) #asegura contexto
        conversations.append(message) 
        try:
            response = openai.ChatCompletion.create(
                model= model_id,
                messages=conversations,
            )
            conversations.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
            conversations[-1]['content'] = self.support_response(conversations)
            print(conversations[-1])
        except RateLimitError:
            conversations.append({'role':'assistant', 'content':botMessages["chatErrorFrecuency"]})
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(f"Caught exception: {exc_type}: {exc_value}")
            conversations.append({'role':'assistant', 'content':botMessages["chatError"]})

        chat_id = self.save_conversation(user, conversations)

        return {"id":chat_id,"data":conversations}

    def support_response(self, conversations):
        req = conversations[-2]['content']
        res = conversations[-1]['content']
        print("##### 1er RES ######")
        response = res.lower();
        print(response)
        msg = res
        if any(indicator in response for indicator in indicators):
            res = self.query_engine.query(req)
            msg = res.response
            print("##### 2do RES ######")
            print(res.response)
        return msg 
    
    def save_conversation(self, user, conversations):
        chat_id = "0"
        if(user.is_authenticated and "+3RR0R" not in conversations[-1]['content']):
            chat = Conversation(user=user, request=conversations[-2]['content'], response=conversations[-1]['content'])
            chat.save()
            chat_id = chat.id 
        return chat_id

    def load_chat(self, user):
        if(user.is_authenticated):
            return Conversation.objects.filter(user=user)
        else:
            return []
    
    def delete_conversation(self, user, ids):
        if(user.is_authenticated):    
            for id in ids:
                conversation = get_object_or_404(Conversation, pk=id)
                conversation.delete()
    
    def update_index(self):
        print("Creating query engine")
        try:
            docs = SimpleDirectoryReader(input_files=["./data/data_prepared.txt"]).load_data()
            self.index = GPTVectorStoreIndex.from_documents(docs)
            self.query_engine = self.index.as_query_engine()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(f"Caught exception: {exc_type}: {exc_value}")
   
