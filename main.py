# -*- coding: utf-8 -*-

import os
from tkinter import *


def ia():
    # Importando modulos
    import datetime
    import speech_recognition as sr
    import sounddevice as sd
    import wikipedia
    import webbrowser
    import random
    from gtts import gTTS
    from playsound import playsound
    import bs4
    import pywhatkit
    import requests
    import joblib
    import wavio as wv

    # Criação de lista de saudação
    saudacao = ['De nada', 'Por nada', 'A seu dispor!', 'Até logo!']
    saudacao = random.choice(saudacao)

    # Criação de lista para acessar sites predefinidos
    meu_sites = [
                    ['whatsapp', 'https://www.whatsapp.com/?lang=pt_br'],
                    ['youtube', 'https://www.youtube.com/'],
                    ['bolsa de valores', 'https://www.b3.com.br/pt_br/']
                 ]

    # Importa arquivos de voz
    filename = 'minha_voz.wav'
    robo = 'fala_robo.mp3'

    # Função de fala
    def fala(text):
        tts = gTTS(text, lang='pt')
        tts.save('minha_voz.wav')
        tts.save('fala_robo.mp3')
        playsound(robo)
        os.remove(filename)
        os.remove(robo)

    # Criando Função para gravar o audio
    def grava():
        freq = 48000
        duration = 5
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        print('Fale agora!')
        sd.wait()
        wv.write('minha_voz.wav', recording, freq, sampwidth=2)
        print('Ok processando...')

    # Criando uma função para abir site predefinidos
    def addsite():
        snome = input('Qual o nome do site?')
        slink = input('Qual o link do site?')

        # Verifica se o nome do site já existe na lista
        for endereco in meu_sites:
            if endereco[0] == snome:
                print('O site já existe na lista!')
                return

        # Se o nome do site não existir na lista, adiciona o novo site
        lista_site = [snome, slink]
        meu_sites.append(lista_site)

    # Função para pegar as informações os ativos de mercados
    def get_crypto_price():
        url = "https://www.google.com/search?q=" + moeda + "+hoje"
        HTML = requests.get(url)
        soup = bs4.BeautifulSoup(HTML.text, 'html.parser')
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div", attrs={
            'class': 'BNeawe iBp4i AP7Wnd'}).text
        fala(f'O preço de {moeda} é de {text}')

    # Previsão de tempo
    def get_weather():
        api_key = "bdec4d7b671ddc7fa6e8fde913124fc2"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == "404":
            return None
        else:
            description = data["weather"][0]["description"]
            temp = round(data["main"]["temp"] - 273.15, 2)
            return f"Em {city}, está {description} com temperatura de {temp} graus Celsius."

    # Criar um lastro de repetição para o código não parar
    while True:
        grava()

        # Função para ouvir e reconhecer a fala e habilitando o microfone do usuário
        r = sr.Recognizer()
        try:
            with sr.AudioFile(filename) as source:
                audio_data = r.record(source)
                says = r.recognize_google(audio_data, language='pt-BR')
                print('Você disse: ' + says.lower())
                texto = says.lower()

            # Desligar o assistente
            f = open('shutdown.txt')
            fec = f.read()
            if texto in fec:
                fala('Ok desligando....')
                janela.destroy()
                break

            # Para dizer o horário
            elif 'horas' in texto or 'hora' in texto:
                hora = datetime.datetime.now().strftime('%H:%M')
                fala('Agora são' + hora)

            # Para realizar uma pesquisa
            elif 'procure por' in texto:
                procurar = texto.replace('procure por', '')
                wikipedia.set_lang('pt')
                resultado = wikipedia.summary(procurar, 2)
                fala(resultado)

            # Para tocar a musica ou video no youtube
            elif 'toque' in texto or 'tocar' in texto:
                tocar = texto.replace('tocar', '')
                # toque = texto.replace('toque', '')
                fala('Ok, tocando musica....')
                resultado = pywhatkit.playonyt(tocar)
                fala(resultado)

            # Método para abrir site e adicionar sites
            # VERIFICAR ESSA VARIAVEL SE FUNCIONA INCLUIDO COM SUSGESTÃO DO IA-GPT
            elif 'abrir site' in texto:
                site = texto.replace('abrir site', '')
                meu_sites = joblib.load('meu_sites.obj')

                for i in meu_sites:
                    if i[0] in site:
                        webbrowser.open(i[1])
            elif 'adicionar site' in texto:
                addsite()
                joblib.dump(meu_sites, 'meu_sites.obj')

            # informações sobre ativos de mercado
            # VERIFICAR ESSA VARIAVEL SE FUNCIONA INCLUIDO COM SUSGESTÃO DO IA-GPT
            elif 'moeda hoje' in texto:
                moeda = texto.replace('moeda hoje', '').strip()
                resultado = ('moeda', get_crypto_price())
                fala(resultado)

            # Informa a previsão do tempo
            # VERIFICAR ESSA VARIAVEL SE FUNCIONA INCLUIDO COM SUSGESTÃO DO IA-GPT
            elif 'previsão do tempo' in texto or 'clima' in texto:
                city = texto.split()[-1]
                resultado = ('previsão do tempo', get_weather())
                fala(resultado)

            # Apresentação do assistente virtual
            elif 'apresentar-se' in texto or 'sobre você' in texto or 'apresentar' in texto:
                fala('Olá, eu sou a Zoye uma assistente virtual. '
                     'Estou aqui para ajudár em suas tarefas diárias e responder suas perguntas.'
                     'O que posso fazer por você hoje'
                     )

            # Criação de algumas respostas simples
            elif 'bom dia' in texto:
                fala('bom dia!')
            elif 'boa tarde' in texto:
                fala('boa tarde!')
            elif 'boa noite' in texto:
                fala('boa noite!')

        except EXCEPTION:
            print('Ocorreu algum erro, Tente novamente')


# Criação um painel interativo para execução do Assistente virtual
janela = Tk()
janela.title('Eu sou a Joye ')

label_l = Label(janela, text='Zoye - Assistente virtual', font='Arial 35')
label_l.place(x=50, y=100)

botao_l = Button(janela, height=4, width=40, text='Clique aqui para iniciar!', font='Arial 15', command=ia,
                 background='#FFFAFA')
botao_l.place(x=220, y=280)

janela.geometry('950x500+0+0')

janela.mainloop()
