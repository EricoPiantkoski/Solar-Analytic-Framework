import main
import csv

local = ['-15.085800', '-57.526000', 'Barra do Bugres', 'MT']
usr = 'ericopiantkoski@gmail.com'
pas='01c7od42'

obj = main.SA(float(local[0]), float(local[1]), local[2], local[3])

#print(obj.dirBDMEP())
#s = obj.dirBDMEP()
#obj.wsBDMEP(usr, pas)
#list = obj.bdmeptxttolist()
#lista = obj.averageinsolation(list)
#obj.im(lista)

print(obj.red())
