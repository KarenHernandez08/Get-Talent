from datetime import datetime
# Convertimos un string con formato <día>/<mes>/<año> en datetime
una_fecha = '20/04/2019'
fecha_dt = datetime.strptime(una_fecha, '%d/%m/%Y')
fecha_dt = datetime.strptime('2022-07-18 09:46:54.655245', '%Y-%m-%d %H:%M:%S.%f')
print(fecha_dt)

