#!/usr/bin/python3 -u
import os, re

class Usb:
  def __init__(self, port="-l 1-1 -p 2"):
    self.port = port
    self.power = False
    self._set("off")

  def _set(self, value):
    print("USB power " + value)
    os.system("uhubctl " + self.port + " -a " + value)

  def start(self):
    if not self.power:
      self._set("on")
      self.power = True

  def stop(self):
    if self.power:
      os.system("aplay -Dplughw:1,0 /home/mattitm/saber.wav")
      self._set("off")
      self.power = False

def main():
  usb = Usb()
  with os.popen('journalctl -fu tidal-connect') as log:
    for line in log:
      if len(re.findall("PlaybackControllerImpl", line)) > 0:
        usb.start()
      elif len(re.findall("asio async_shutdown error", line)) > 0:
        usb.stop()

if __name__ == "__main__":
  main()
