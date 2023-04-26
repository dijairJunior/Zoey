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
    # from googlesearch import search

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

    def abrir_site(site):
        # Carrega a lista de sites predefinidos
        meu_sites = joblib.load('meu_sites.obj')

        # Procura na lista pelo site desejado
        for i in meu_sites:
            if i[0] == site:
                # Abre o site no navegador padrão
                webbrowser.open(i[1])
                return f'Abrindo {site}...'

        # Se não encontrar o site, retorna uma mensagem de erro
        return f'O site {site} não foi encontrado.'

    # Função para pegar as informações os ativos de mercados
    def get_crypto_price(moeda=None):
        url = "https://www.google.com/search?q=" + moeda + "+hoje"
        HTML = requests.get(url)
        moeda = 'Bitcoin'
        soup = bs4.BeautifulSoup(HTML.text, 'html.parser')
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div", attrs={
            'class': 'BNeawe iBp4i AP7Wnd'}).text
        fala(f'O preço de {moeda} é de {text}')

    # Previsão de tempo
    def get_weather(city=None):
        api_key = "bdec4d7b671ddc7fa6e8fde913124fc2"
        url = f"https://api.openweathermap.org/data/2.5/weather?q=" \
              f"{city}&appid={api_key}&units=metric"
        city = "São Paulo"
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
                resultado = wikipedia.summary(procurar, 1)
                fala(resultado)

            # Para tocar a musica ou video no youtube
            elif 'toque' in texto or 'tocar' in texto:
                tocar = texto.replace('tocar', '')
                resultado = pywhatkit.playonyt(tocar)
                fala('Ok, tocando música....')

            # Método para abrir site e adicionar sites
            elif 'abrir site' in texto:
                site = texto.replace('abrir site ', '')
                resultado = abrir_site(site)
                fala(resultado)

                for i in meu_sites:
                    if i[0] in site:
                        webbrowser.open(i[1])
            elif 'adicionar site' in texto:
                addsite()
                joblib.dump(meu_sites, 'meusites.obj')

            # informações sobre ativos de mercado
            elif 'moeda hoje' in texto:
                moeda = texto.replace('moeda hoje', '').strip()
                if moeda:
                    resultado = ('moeda', get_crypto_price(moeda))
                else:
                    moeda = "Bitcoin"
                    resultado = ('moeda', get_crypto_price(moeda))
                fala(resultado)

            # Informa a previsão do tempo
            elif 'previsão do tempo' in texto or 'clima' in texto:
                city = texto.split()[-1]
                if city:
                    resultado = ('previsão do tempo', get_weather(city))
                else:
                    city = "São Paulo"  # valor padrão
                    resultado = ('previsão do tempo', get_weather(city))
                fala(resultado)

            # Apresentação do assistente virtual
            elif 'Zoye apresente-se' in texto or 'sobre você' in texto or 'apresentar' in texto:
                fala('Olá sou a Zoye uma assistente virtual em construção, fui criada pelo meu criador Dijair.'
                     'Estou aqui para tentar lhe ajudar em suas tarefas diárias e responder suas perguntas,'
                     'minhas respostas são limitadas porque ainda estou aprendendo,'
                     'meu código fonte não ainda está completo tenha paciência'
                     )

            # Criação de algumas respostas simples
            elif 'bom dia' in texto:
                fala('bom dia!')
            elif 'boa tarde' in texto:
                fala('boa tarde!')
            elif 'boa noite' in texto:
                fala('boa noite!')

        except:
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
