from asyncio import sleep
import asyncio
import json
import time
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth import logout

from app.models import Conversation
from app.chat import Chatbot

# Create your views here.

def section(request, section):
    if request.method == 'POST':
        if 'start_session' in request.POST:
            return redirect('login')
        elif 'close_session' in request.POST:
            logout(request)
            return redirect('login')
    else:
        if section == "home":
            conversations = Chatbot.get_instance().load_chat(request.user)

            questions = [
            '¿Cómo puedo buscar información sobre un congresista específico?',
            '¿Cuáles son los datos básicos de cada congresista en el portal del Congreso del Perú?',
            '¿Cómo puedo encontrar el historial de votaciones de un congresista en particular?',
            '¿Puedo ver los discursos o intervenciones de un congresista en el Congreso?',
            '¿Dónde puedo encontrar información sobre los comités y comisiones en los que participa un congresista?',
            '¿Cómo puedo ver las declaraciones juradas de bienes de los congresistas?',
            '¿Hay información sobre la trayectoria profesional y académica de los congresistas en el portal del Congreso del Perú?',
            '¿Puedo ver el registro de asistencias de los congresistas a las sesiones del Congreso?',
            '¿Hay alguna forma de saber si un congresista ha tenido algún tipo de sanción en el pasado?',
            '¿Dónde puedo encontrar información sobre los proyectos de ley presentados por un congresista en particular?',
            ]
            return render(request, 'base.html', {'section':section, 'conversations': conversations, 'questions':questions})
        else:
            return render(request, 'base.html', {'section':section})
    
def home(request):
    return section(request, 'home')
    
def tutorial(request):
    return section(request, 'tutorial')
    
def delete(request):
    if request.method == "POST":
        data = request.POST.get('data')
        ids = json.loads(data)
        Chatbot.get_instance().delete_conversation(user=request.user , ids=ids)
        return JsonResponse({"result":"ok"})    

def message(request):
    if request.method == "POST":
        data = request.POST.get('data')
        message = json.loads(data)
        res = Chatbot.get_instance().response(request.user, message)   
        return JsonResponse(res)

