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
    import soundfile as sf

    global nome, link, meu_site

    # Criação de lista de saudação
    denada = ['De nada', 'Por nada', 'A seu dispor!', 'Até logo!']
    denada = random.choice(denada)

    sitespadrao = [['whatsapp', 'https://www.whatsapp.com/?lang=pt_br'],
                   ['youtube', 'https://www.youtube.com/'],
                   ['bolsa de valores', 'https://www.b3.com.br/pt_br/']
                   ]

    # Importa arquivos de voz
    filename = 'minha_voz.wav'
    robo = 'fala_robo.mp3'

    global says

    # Função de fala
    def fala(text):
        tts = gTTS(text, lang='pt-BR')
        tts.save('fala_robo.mp3')
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
        sf.write('minha_voz.wav', recording, freq, subtype='PCM_16')
        print('Ok processando...')

    # Criando uma função para abir site predefinidos
    def addsite():
        snome = input('Qual o nome do site?')
        slink = input('Qual o endereço do site?')
        listabase = [snome, slink]
        sitespadrao.append(listabase)

    def get_crypto_price(coin):
        url = f"https://www.google.com/search?q={coin}+hoje"
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        price = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'})
        if price:
            text = price.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
            fala(f'O preço de {coin} é de {text}')
        else:
            fala(f'Desculpe, não foi possível encontrar informações sobre o valor de {coin}.')

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
                wikipedia.set_lang('pt-BR')
                resultado = wikipedia.summary(procurar, 2)
                fala(resultado)

            # Para tocar a musica ou video no youtube
            elif 'toque' in texto or 'tocar' in texto:
                tocar = texto.replace('tocar', '')
                toque = texto.replace('toque', '')
                fala('Ok, tocando musica....')
                resultado = pywhatkit.playonyt(tocar, toque)
                fala(resultado)

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
            elif 'valor hoje' in texto:
                btc = texto.replace('valor hoje', '').strip()
                get_crypto_price(btc)

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

        except:
            print('Ocorreu algum erro, Tente novamente')


janela = Tk()
janela.title('Eu sou a Joye')

label2_l = Label(janela, text='Eu sou a Joye sua assistente virtual em processo de,'
                              'aprendizagem | feito por Dijair Camargo', font='calibri 18')
label2_l.place(x=0, y=0)

label3_l = Label(janela, text='o que posso ajudar', font='calibri 18')
label3_l.place(x=690, y=480)
