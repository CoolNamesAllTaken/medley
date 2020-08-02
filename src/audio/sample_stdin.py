#!/usr/bin/env python3
import houndify
import sys
import subprocess


CLIENT_ID = "-Xd2lHXxgmsGSKNzqRsjzw=="
CLIENT_KEY = "QGJCqsi2oYO7CI-LiaunEfjQIAhKlh42Suh0OOk_ecz_0S1e75dqdUJ-_CWliTnU7pRCoZeKdKRippkqkHHTvA=="
BUFFER_SIZE = 512

#
# Simplest HoundListener; just print out what we receive.
# You can use these callbacks to interact with your UI.
#
class MyListener(houndify.HoundListener):
  def onPartialTranscript(self, transcript):
    print("Partial transcript: " + transcript)
  def onFinalResponse(self, response):
    print("Final response: " + str(response))
  def onError(self, err):
    print("Error: " + str(err))


client = houndify.StreamingHoundClient(CLIENT_ID, CLIENT_KEY, "test_user")
client.setLocation(37.388309, -121.973968)

client.start(MyListener())
process = subprocess.Popen(['arecord', '-t', 'raw', '-c', '1', '-r', '16000', '-f', 'S16_LE'], stdout=subprocess.PIPE)
while True:
    samples = process.stdout.readline()
    if process.poll() is not None or len(samples) == 0 or client.fill(samples):
        break
    #if output:
    #    print (output.strip())
# retval = process.poll()
# 
# while True:
#     print("listening", flush=True)
#     samples = sys.stdin.buffer.read(512)
#     print("done listening", flush=True)
#     if len(samples) == 0: break
#     if client.fill(samples): break

client.finish()

## Uncomment the lines below to see an example of using a custom
## grammar for matching.  Use the file 'turnthelightson.wav' to try it.
# clientMatches = [ {
#   "Expression" : '([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].("turn"|"switch"|(1/100 "flip"))."on".["the"].("light"|"lights").[1/20 "for"."me"].[1/20 "please"])|([1/100 ("can"|"could"|"will"|"would")."you"].[1/10 "please"].[100 ("turn"|"switch"|(1/100 "flip"))].["the"].("light"|"lights")."on".[1/20 "for"."me"].[1/20 "please"])|((("i".("want"|"like"))|((("i".["would"])|("i\'d")).("like"|"want"))).["the"].("light"|"lights").["turned"|"switched"|("to"."go")|(1/100"flipped")]."on".[1/20"please"])"',
#   "Result" : { "Intent" : "TURN_LIGHT_ON" },
#   "SpokenResponse" : "Ok, I\'m turning the lights on.",
#   "SpokenResponseLong" : "Ok, I\'m turning the lights on.",
#   "WrittenResponse" : "Ok, I\'m turning the lights on.",
#   "WrittenResponseLong" : "Ok, I\'m turning the lights on."
# } ]
# client.setHoundRequestInfo('ClientMatches', clientMatches)

#client.start(MyListener())

#while True:
 # samples = call(["arecord "])
  #if len(samples) == 0: break
  #if client.fill(samples): break
#  
#client.finish()
