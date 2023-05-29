import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
from gpiozero import MCP3008, OutputDevice
from time import sleep
import serial
import glob
import subprocess










pump_pin = 26
dht_pin = 19
mcp = MCP3008(channel = 0)
pump = OutputDevice(pump_pin)

def pump_on():
      pump.on()
      print("Currently pumping water")
      
def pump_off():
      pump.off()
      print("Pumping has stopped")

def read_temp():
      global humidity
      global temperature
      humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht_pin)
      if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.2f}C, Humidity: {humidity:.2f}%")
      else:
            print("Failed to retrieve data from DHT11 sensor!")

def soilmoist():
      global moisture
      moisture = mcp.value
      print("Soil Moisture: ", moisture)
      if soilmoist is None:
            print("Bad")
          

try:
      while True:
            soilmoist()
            read_temp()
            if soilmoist is None:
                  print("Error")
            elif moisture < 0.2 or temperature > 32:
                  pump_on()
                  sleep(3)
                  pump_off()
                  sleep(3)
            sleep(3600)
            
except KeyboardInterrupt:
      print("Exiting")
      GPIO.cleanup()