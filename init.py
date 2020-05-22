import main
import csv
import server

def sa(state): #state abbreviation
    print('selected state:', state)
    state = state.lower()

    if state == 'acre':
        state = 'AC'
    elif state == 'alagoas':
        state = 'AL'
    elif state == 'amapá':
        state = 'AP'
    elif state == 'amazonas':
        state = 'AM'
    elif state == 'bahia':
        state = 'BA'
    elif state == 'ceará':
        state = 'CE'
    elif state == 'distrito federal':
        state = 'DF'
    elif state == 'espirito santo':
        state = 'ES'
    elif state == 'goiás':
        state = 'GO'
    elif state == 'maranhão':
        state = 'MA'
    elif state == 'mato grosso':
        state = 'MT'
    elif state == 'mato grosso do sul':
        state = 'MS'
    elif state == 'minas gerais':
        state = 'MG'
    elif state == 'pará':
        state = 'PA'
    elif state == 'paraíba':
        state = 'PB'
    elif state == 'paraná':
        state = 'PR'
    elif state == 'pernambuco':
        state = 'PE'
    elif state == 'piauí':
        state = 'PI'
    elif state == 'rio de janeiro':
        state = 'RJ'
    elif state == 'rio grande do norte':
        state = 'RN'
    elif state == 'rio grande do sul':
        state = 'RS'
    elif state == 'rondônia':
        state = 'RO'
    elif state == 'roraima':
        state = 'RR'
    elif state == 'santa catarina':
        state = 'SC'
    elif state == 'são paulo':
        state = 'SP'
    elif state == 'sergipe':
        state = 'SE'
    elif state == 'tocantins':
        state = 'TO'

    return state
    
    
# init server (needs ESP8266 client)
local = server.local
state = sa(local[3])
local.insert(3, state)
del local[-1]


#local = ['-15.085800', '-57.526000', 'Barra do Bugres', 'MT']
# transformar em credencial:
usr = 'ericopiantkoski@gmail.com'
pas='01c7od42'

obj = main.SA(float(local[0]), float(local[1]), local[2], local[3])

#print(obj.dirBDMEP())
#obj.dirBDMEP()
obj.wsBDMEP(usr, pas)
#obj.bdmeptxttolist()
#lista = obj.averageinsolation(list)
#obj.im(lista)

print(obj.red())
