import houndify
import sys
import base64
import time

clientId = "-Xd2lHXxgmsGSKNzqRsjzw=="
clientKey = "QGJCqsi2oYO7CI-LiaunEfjQIAhKlh42Suh0OOk_ecz_0S1e75dqdUJ-_CWliTnU7pRCoZeKdKRippkqkHHTvA=="
userId = "test_user"
client = houndify.StreamingHoundClient(clientId, clientKey, userId, sampleRate=8000)

#import pyodbc
import config
import subprocess
from subprocess import call

connection_string = """Driver={ODBC Driver 17 for SQL Server};
Server=tcp:treehacks2020.database.windows.net,1433;
Database=treehacks2020;Uid=cahogan;
Pwd=hackathon2020!;Encrypt=yes;TrustServerCertificate=no;Connection_Timeout=30;"""

conversation_over = False
user_id = "0"
card_scan_func = None
rotor_move_func = None

def setup_chat_vars(card_scan_func_in, rotor_move_func_in):
    global card_scan_func, rotor_move_func
    card_scan_func = card_scan_func_in
    rotor_move_func = rotor_move_func_in

def preprocess_transcript(response):
    global conversation_over
    if "Result" in response['AllResults'][0]:
        print(response['AllResults'][0]['Result'])
        if "move_motor" in response['AllResults'][0]['Result']:
            print("MOVING ROTOR HERE")
            rotor_move_func()
        if "end_convo" in response['AllResults'][0]['Result']:
            print("ITS OVER")
            conversation_over = True
        if 'silent_response' in response['AllResults'][0]['Result']:
            print("QUIET TIME")
            print(response['AllResults'][0]['Result']["silent_response"])
            tclient = houndify.TextHoundClient(clientId, clientKey, "test_user", requestInfo)
            rep = tclient.query(user_id + response['AllResults'][0]['Result']["silent_response"] + response['AllResults'][0]["SpokenResponse"])
            print("LMFAO")
            if "Result" in rep['AllResults'][0]:
                print(rep['AllResults'][0]['Result'])
                if "move_motor" in rep['AllResults'][0]['Result']:
                    print("MOVING ROTOR HERE")
                    rotor_move_func()
                if "end_convo" in rep['AllResults'][0]['Result']:
                    print("ITS OVER")
                    conversation_over = True
            #if "AllResults" in rep:
            response = rep
    say_aloud(response)

class MedleyListener(houndify.HoundListener):
  #  an abstract base class that defines the callbacks
  #  that can be received while streaming speech to the server

  def onPartialTranscript(self, transcript):
    print("Partial transcript: " + transcript)

  def onFinalResponse(self, response):
#    print("Final response: " + str(response))
    preprocess_transcript(response)

  def onError(self, err):
    print("Error " + str(err))

requestInfo = {
  'Latitude': 37.4275,
  'Longitude': -122.1697,
  'ResponseAudioVoice': "Sarah",
  'ResponseAudioShortOrLong': "Short"
}

def say_aloud(response):
    if 'ResponseAudioBytes' in response['AllResults'][0]:
        base64_message = response['AllResults'][0]['ResponseAudioBytes']
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        with open('myfile.wav', mode='wb') as f:
            f.write(message_bytes)
        call(["aplay", "myfile.wav"])

    #print(response) #['AllResults'][0]['Result'])
    #print(response['AllResults'][0]['SpokenResponse'])


def listen_for_response(should_prepend, prepend_str):
    client = houndify.StreamingHoundClient(clientId, clientKey, "test_user", requestInfo)
    client.start(MedleyListener())
    if should_prepend:
        samples = prepend_str
    process = subprocess.Popen(['arecord', '-d', '7', '-t', 'raw', '-c', '1', '-r', '16000', '-f', 'S16_LE'], stdout=subprocess.PIPE)
    while True:
        samples = process.stdout.readline()
        if process.poll() is not None or len(samples) == 0 or client.fill(samples):
            break
    client.finish()

def scan_user_card():
    return "0" # placeholder, caitlin user

def start_chat(): # call this when button pressed
    global user_id, conversation_over
    tclient = houndify.TextHoundClient(clientId, clientKey, "test_user", requestInfo)
    greeting = tclient.query("000nouser_say_hi")
    say_aloud(greeting)
    user_id = str(card_scan_func())
# TODO ADD TIME OUT HERE
    welcome = tclient.query(user_id + "welcome_user_specific")
    say_aloud(welcome)

    while(conversation_over != True):
        listen_for_response(False, user_id)

    goodbye = tclient.query(user_id + "bye_user_specific")
    conversation_over = False
    say_aloud(goodbye)
