from network import WLAN, STA_IF
from time import sleep_ms

def map(value, in_min, in_max, out_min, out_max):
    scaled_value = int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    return scaled_value

def clamp(value: int, maxValue: int) -> int:
	value %= maxValue+1
	if value < 0:
		velue = maxValue
	return value

def wifi_connect(rede: str, senha: str) -> object:
    wifi = WLAN(STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        wifi.connect(rede, senha)
        tentativas = 0
        while not wifi.isconnected() and tentativas < 8:
            sleep_ms(1000)
            tentativas += 1

    if not wifi.isconnected():
        raise
    return wifi
