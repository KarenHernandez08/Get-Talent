import datetime

hoy = datetime.datetime.now()
suma = datetime.timedelta( minutes=51)
hoy2 = datetime.datetime.now()+ datetime.timedelta(minutes=5)

print(hoy2-hoy)

if hoy2-hoy > suma :
    print("Mayor a 5 minutos expirado")

if hoy2-hoy < suma : 
    print ("menor a 5 minutos, valido")