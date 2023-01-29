from header import wled_lightning
import time

def main():
    light1 = wled_lightning("192.168.1.250")
    while True:
        light1.send_request()
        time.sleep(3600)
    
main()