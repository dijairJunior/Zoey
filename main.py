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

    global snome, slink, meu_site

    # Criação de lista de saudação
    saudacao = ['De nada', 'Por nada', 'A seu dispor!', 'Até logo!']
    saudacao = random.choice(saudacao)

    # Criação de lista para acessar sites predefinidos
    sitespadrao = [['whatsapp', 'https://www.whatsapp.com/?lang=pt_br'],
                   ['youtube', 'https://www.youtube.com/'],
                   ['bolsa de valores', 'https://www.b3.com.br/pt_br/']
                   ]

    # Importa arquivos de voz
    filename = 'minha_voz.wav'
    robo = 'fala_robo.mp3'

    # Variavel global
    global says

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
        slink = input('Qual o endereço do site?')
        listabase = [snome, slink]
        sitespadrao.append(listabase)

    # Função para pegar as informações os ativos de mercados
    def get_crypto_price(moeda):
        url = "https://www.google.com/search?q=" + moeda + "+hoje"
        HTML = requests.get(url)
        soup = bs4.BeautifulSoup(HTML.text, 'html.parser')
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div", attrs={
            'class': 'BNeawe iBp4i AP7Wnd'}).text
        fala(f'O preço de {moeda} é de {text}')

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

            # Método para abrir site e adicionar sites
            elif 'abrir site' in texto:
                site = texto.replace('abrir site', '')
                meu_site = joblib.dump(meu_site, 'meus_sites.obj')

                for i in meu_site:
                    if i[0] in site:
                        webbrowser.open(i[1])

            elif 'adicionar sites' in texto:
                addsite()
                joblib.dump(sitespadrao, 'nome.obj')

            # informações sobre ativos de mercado
            elif 'moeda hoje' in texto:
                moeda = texto.replace('moeda hoje', '').strip()
                get_crypto_price(moeda)

            # Apresentação do assistente virtual
            elif 'apresentar-se' in texto or 'sobre você' in texto or 'apresentar' in texto:
                fala(
                    'Olá, eu sou ChatGPT, um assistente virtual desenvolvido pela OpenAI.,'
                    ' Estou aqui para ajudá-lo a encontrar,'
                    ' respostas para suas perguntas e auxiliá-lo em tarefas simples ou complexas.,'
                    ' Estou equipado com tecnologia de linguagem natural avançada ,'
                    'para fornecer respostas precisas e relevantes,'
                    ' para suas consultas. Sinta-se à vontade para me perguntar ,'
                    'qualquer coisa - estou sempre pronto para ajudá-lo!')

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
