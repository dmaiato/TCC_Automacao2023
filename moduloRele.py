def moduloRele(PinIn, PinOut):
    divisor = ADC(Pin(PinIn))
    divisor.atten(ADC.ATTN_11DB)
    rele = Pin(PinOut, Pin.OUT)
    tensao = 0
    for i in range(20):
        tensao += adc.read()
    media = tensao/20
    if media < 1550:
        tensaoBaixa()
    elif media > 1700:
        tensaoAlta()
    elif media >= 1550 and media <= 1700:
        rele.on()
        