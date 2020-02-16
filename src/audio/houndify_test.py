import houndify
import sys
import base64


clientId = "-Xd2lHXxgmsGSKNzqRsjzw=="
clientKey = "QGJCqsi2oYO7CI-LiaunEfjQIAhKlh42Suh0OOk_ecz_0S1e75dqdUJ-_CWliTnU7pRCoZeKdKRippkqkHHTvA=="
userId = "test_user"
client = houndify.StreamingHoundClient(clientId, clientKey, userId, sampleRate=8000)

#import pyodbc
import config
import traceback
#import pandas as pd
import subprocess
from subprocess import call


connection_string = """Driver={ODBC Driver 17 for SQL Server};
Server=tcp:treehacks2020.database.windows.net,1433;
Database=treehacks2020;Uid=cahogan;
Pwd=hackathon2020!;Encrypt=yes;TrustServerCertificate=no;Connection_Timeout=30;"""
# 'DRIVER=' + driver + \
#                     ';SERVER=' + config.DATABASE_CONFIG['server'] + \
#                     ';PORT=1433' + \
#                     ';DATABASE=' + config.DATABASE_CONFIG['database'] + \
#                     ';UID=' + config.DATABASE_CONFIG['username'] + \
#                     ';PWD=' + config.DATABASE_CONFIG['password']

requestInfo = {
  ## Pretend we're at SoundHound HQ.  Set other fields as appropriate
  'Latitude': 37.4275,
  'Longitude': -122.1697,
  'ResponseAudioVoice': "Sarah",
  'ResponseAudioShortOrLong': "Short"
}

# def read_data_to_df(query):
#     try:
#         print("connecting db" )#+ config.DATABASE_CONFIG['database'])
#         sql_conn = pyodbc.connect(connection_string)
#         # execute query and save data in pandas df
#         df = pd.read_sql(query, sql_conn)
#         print(df)
#         return df
#     except Exception as error:
#         print("error message: {}".format(error))
#         # I found that traceback prints much more detailed error message
#         traceback.print_exc()
#
#
# def write2db(df):
#     # prepare SQLAlchemy engine
#     # Doc: https://docs.sqlalchemy.org/en/latest/dialects/mssql.html#module-sqlalchemy.dialects.mssql.pyodbc
#     # same connection string as before
#     params = urllib.parse.quote_plus(connection_string)
#     engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
#     # df columns names need to match the table column names in DB
#
#     # check #rows in table before write operation
#     sql_conn = pyodbc.connect(connection_string)
#     cursor = sql_conn.cursor()
#     query = '''
#                 SELECT count(*)
#                 FROM table_name
#             '''
#     cursor.execute(query)
#     rows_before = cursor.fetchone()
#
#     # write results to Azure DB table
#     topn.to_sql('table_name', con = engine, if_exists = 'append', index = False)
#     # check #rows in table after write operation
#     cursor.execute(query)
#     rows_after = cursor.fetchone()
#     # print(rows_after)
#     print("Inserted ")#"{} rows into table {}".format(rows_after[0] - rows_before[0], 'table_name'))
#     return

#def processResponse(response, user_id):

def controlFlow(user_id, response):
    #getSounds
    #getResponse
    base64_message = response['AllResults'][0]['ResponseAudioBytes']
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    with open('myfile.wav', mode='wb') as f:
        f.write(message_bytes)
        #response['AllResults'][0]['ResponseAudioBytes'])
    print(response['AllResults'][0]['Result'])
    print(response['AllResults'][0]['SpokenResponse'])
    call(["aplay", "myfile.wav"])
#    follow_up = processResponse(response, user_id)
#    if follow_up != "":
#        contextAwareLoop(follow_up, user_id)
#    writeRecordToDatabase()



class MyListener(houndify.HoundListener):
  def onPartialTranscript(self, transcript):
    print("Partial transcript: " + transcript)
  def onFinalResponse(self, response):
    print("Final response: " + str(response))
    controlFlow('000', response)
  def onError(self, err):
    print("Error: " + str(err))


client = houndify.StreamingHoundClient(clientId, clientKey, "test_user", requestInfo)
client.start(MyListener())
process = subprocess.Popen(['arecord', '-t', 'raw', '-c', '1', '-r', '16000', '-f', 'S16_LE'], stdout=subprocess.PIPE)
while True:
    samples = process.stdout.readline()
    if process.poll() is not None or len(samples) == 0 or client.fill(samples):
        break
client.finish()


#controlFlow("test_user")
#
# class MyListener(houndify.HoundListener):
#   def onPartialTranscript(self, transcript):
#     print("Partial transcript: " + transcript)
#   def onFinalResponse(self, response):
#     print("Final response: " + str(response))
#   def onError(self, err):
#     print("Error: " + str(err))
#
#
# client = houndify.StreamingHoundClient(clientId, clientKey, "test_user")
# client.setLocation(37.388309, -121.973968)
#
# client.start(MyListener())
#
# while True:
#     print("listening", flush=True)
#     samples = sys.stdin.buffer.read(512)
#     print("done listening", flush=True)
#     if len(samples) == 0: break
#     if client.fill(samples): break
#
# client.finish()


print("done")
