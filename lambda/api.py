import logging

import requests
import json
from requests.exceptions import HTTPError
from datetime import datetime, timedelta


id_canal_data=""
aux=""
option=[]


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

def getCanalList(num_option):
    
    for index, item in enumerate(option) : # "item in vet" e' um iterador, item comeca em vet[0], depois vet[1] e assim por diante
        if(index==int(num_option)-1):
            id_canal_ = item['id_canal']
            nome_canal= item['nome']
            global id_canal_data
            id_canal_data=id_canal_
            programa=programacao(id_canal_,0)
            #url_imagem =item['url_imagem']
            #print("Opção "+str(index)+ " "+id_canal_ + " " +nome_canal)
            
            
    return nome_canal+", "+programa

def getCanalName(dados_pesquisa):
    option.clear()
    url = "https://programacao.netcombo.com.br/gatekeeper/canal/select?q=id_cidade:1&callback=callbackChannels&json.wrf=callbackChannels&wt=json&rows=10&start=0&sort=cn_canal%20asc&fl=id_canal%20st_canal%20cn_canal%20nome%20url_imagem&fq=nome:"+str(dados_pesquisa)+"&_=1577582659100&callback=callbackChannels"
    
    response = requests.get(url)
    status = response.status_code
    res=""
    speak_output=" "
        
        
    if (status != 204 and response.headers["content-type"].strip().startswith("application/json")):
        try:
            res=response.text
        except ValueError:
            res="-1"
    elif (status != 204):
        try:
            res=response.text
        except ValueError:
            res="-1"

    if res=="-1":
        speak_output = "Canal não encontrado!"
    else:
        qtd_request=0
        pythonObj = json.loads(res[17:-1])
            
            
        if len(pythonObj['response']['docs'])>=2:
            
            speak_output="Encontrei algumas opções, qual delas você quer saber a programação:\n Você deve dizer por exemplo Opção 1. \n"
            for i in pythonObj['response']['docs']:
                id_canal_ = i['id_canal']
                nome_canal =i['nome']
                url_imagem =i['url_imagem']
                option.append(i)
                qtd_request=qtd_request+1
                speak_output = speak_output + "Opção "+str(qtd_request)+ " "+nome_canal+";\n"
            return speak_output
            
        else:
            id_canal_ = pythonObj['response']['docs'][0]['id_canal']
            nome_canal =pythonObj['response']['docs'][0]['nome']
            url_imagem =pythonObj['response']['docs'][0]['url_imagem']
            global id_canal_data
            id_canal_data=id_canal_
            a = programacao(id_canal_,0)
            speak_output = "Está passando agora no canal " + nome_canal +", "+ a
            return speak_output    
    