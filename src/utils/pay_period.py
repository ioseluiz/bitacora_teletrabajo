import datetime

def calcular_periodo_pago(fecha_consulta=None):
    if fecha_consulta is None:
        fecha_consulta = datetime.date.today()
        
    # Ancla maestra: El fin del periodo 202601 (Sábado)
    ancla = datetime.date(2026, 1, 24)
    
    # Normalizamos cualquier fecha al sábado en que termina su catorcena
    delta_dias = (fecha_consulta - ancla).days
    dias_para_cierre = (14 - (delta_dias % 14)) % 14
    fin_periodo_actual = fecha_consulta + datetime.timedelta(days=dias_para_cierre)
    
    def obtener_primer_cierre_del_ano(ano):
        enero_1 = datetime.date(ano, 1, 1)
        delta = (enero_1 - ancla).days
        primer_sabado = enero_1 + datetime.timedelta(days=(14 - (delta % 14)) % 14)
        
        if primer_sabado.day < 14:
            return primer_sabado + datetime.timedelta(days=14)
        return primer_sabado

    primer_cierre_este_ano = obtener_primer_cierre_del_ano(fin_periodo_actual.year)
    
    if fin_periodo_actual < primer_cierre_este_ano:
        ano_fiscal = fin_periodo_actual.year - 1
        inicio_fiscal = obtener_primer_cierre_del_ano(ano_fiscal)
    else:
        ano_fiscal = fin_periodo_actual.year
        inicio_fiscal = primer_cierre_este_ano

    dias_transcurridos = (fin_periodo_actual - inicio_fiscal).days
    numero_periodo = (dias_transcurridos // 14) + 1
    
    return f"{ano_fiscal}{numero_periodo:02d}", fin_periodo_actual
