from datetime import datetime

ENCARGO_PERMANENTE = 0.36
TAXA = 0.09

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
     'end': 1564610974, 'start': 1564610674
     },
    {'source': '41-885633788', 'destination': '41-886383097',
     'end': 1564506121, 'start': 1564504821
     },
    {'source': '48-996383697', 'destination': '41-886383097',
     'end': 1564630198, 'start': 1564629838
     },
    {'source': '48-999999999', 'destination': '41-885633788',
     'end': 1564697158, 'start': 1564696258
     },
    {'source': '41-833333333', 'destination': '41-885633788',
     'end': 1564707276, 'start': 1564704317
     },
    {'source': '41-886383097', 'destination': '48-996384099',
     'end': 1564505621, 'start': 1564504821
     },
    {'source': '48-999999999', 'destination': '48-996383697',
     'end': 1564505721, 'start': 1564504821
     },
    {'source': '41-885633788', 'destination': '48-996384099',
     'end': 1564505721, 'start': 1564504821
     },
    {'source': '48-996355555', 'destination': '48-996383697',
     'end': 1564505821, 'start': 1564504821
     },
    {'source': '48-999999999', 'destination': '41-886383097',
     'end': 1564610750, 'start': 1564610150
     },
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564505021, 'start': 1564504821
     },
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564627800, 'start': 1564626000
     }
]


def calculando_valor(start, end):

    # Calcula a quantidade de segundos que a ligaçao durou.
    tempo_segundos = end - start
    # Transforma os segundos em minutos.
    tempo_minuto = (tempo_segundos // 60)

    horario_inicio = datetime.fromtimestamp(start).hour
    horario_final = datetime.fromtimestamp(end).hour
    '''
    Analisa se a ligação foi feita de dia ou de noite.
    E calcula a taxa.
    '''
    if 6 < horario_inicio <= 22 and 6 < horario_final <= 22:
        valor = (tempo_minuto * 0.09) + ENCARGO_PERMANENTE
    elif (22 < horario_inicio and 22 < horario_final) or \
         (0 <= horario_inicio <= 6 and 0 <= horario_final <= 6):
        valor = ENCARGO_PERMANENTE
    elif horario_inicio == 22 and horario_final > 22:
        minutos_final = datetime.fromtimestamp(end).minute
        diferenca = tempo_minuto - minutos_final
        valor = ENCARGO_PERMANENTE + (diferenca * TAXA + ENCARGO_PERMANENTE)
    elif horario_inicio == 6 and horario_final > 6:
        minutos_inicio = datetime.fromtimestamp(start).minute
        diferenca = tempo_minuto - minutos_inicio
        valor = ENCARGO_PERMANENTE + (diferenca * TAXA + ENCARGO_PERMANENTE)
    return round(valor, 2)


def classify_by_phone_number(records):
    conta = []
    for r in range(len(records)):
        value = calculando_valor(records[r]['start'], records[r]['end'])
        # Verifica se a lista conta está vazia.
        if not conta:
            conta.append({'source': records[r]['source'], 'total': value})
        else:
            contador = 0
            '''
            Verifica se o telefone já está na lista conta.
            Se sim, ele acrescenta o valor dessa ligação ao
            telefone já existente na lista conta.
            '''
            for e in range(len(conta)):
                if records[r]['source'] == conta[e]['source']:
                    conta[e]['total'] += value
                    conta[e]['total'] = round(conta[e]['total'], ndigits=2)
                else:
                    contador = contador + 1
                    '''
                    Verifica se o telefone não está na lista conta.
                    Se não está ele adiciona o telefone a lista conta.
                    '''
                    if contador == len(conta):
                        conta.append({'source': records[r]['source'],
                                      'total': value})
    return sorted(conta, key=lambda i: i['total'], reverse=True)
