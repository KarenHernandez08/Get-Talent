import datetime

hoy = datetime.datetime.now()
suma = datetime.timedelta( minutes=51)
hoy2 = datetime.datetime.now()+ datetime.timedelta(minutes=5)

print(hoy2-hoy)

if hoy2-hoy > suma :
    print("Mayor a 5 minutos expirado")

if hoy2-hoy < suma : 
    print ("menor a 5 minutos, valido")
from datetime import datetime
# Convertimos un string con formato <día>/<mes>/<año> en datetime
una_fecha = '20/04/2019'
fecha_dt = datetime.strptime(una_fecha, '%d/%m/%Y')
fecha_dt = datetime.strptime('2022-07-18 09:46:54.655245', '%Y-%m-%d %H:%M:%S.%f')
print(fecha_dt)

