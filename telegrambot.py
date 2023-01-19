import telepot
import time
import datetime
import os
import socket
import logging


from picamera import PiCamera
from dotenv import load_dotenv

path=os.getenv("HOME")

# Load .env file using:
load_dotenv()

logging.basicConfig(filename='./telegrambot.log', encoding='utf-8', level=logging.INFO)

# Handling message from Telegram
def handleMessage(msg):

 username = msg["from"]["username"]

 epoch_time = msg["date"]
 time_formatted = time.strftime('%Y-%m-%d', time.localtime(epoch_time))
 hour = int(time.strftime("%H"))+1
 minutes = time.strftime("%M")
 seconds = time.strftime("%S")

 clock = str(hour)+":"+minutes+":"+seconds
 fullDate = time_formatted +" "+clock

 chat_id = msg['chat']['id'];
 command = msg['text'];
 date = msg["date"]
 date_time = datetime.datetime.fromtimestamp( msg["date"] )

 print ("["+fullDate+"] @" + username + " says -> "+ command)
 logging.info("["+fullDate+"] @" + username + " says -> "+ command)

 if (chat_id == int(os.getenv("CHAT_ID"))):

  if (command == '/photo'):

   camera = PiCamera();
   #camera.resolution = (640, 480)
   camera.resolution = (1920, 1080)
   camera.framerate = 25

   print ("Taking picture…");
   logging.info("["+fullDate+"] Taking a picture")

   # Initialize the camera
   camera.start_preview()
   time.sleep(5)
   camera.capture(path + '/pic.jpg',resize=camera.resolution)
   #time.sleep(1)
   camera.stop_preview()
   camera.close()
   # Seding picture
   bot.sendPhoto(chat_id, open(path + '/pic.jpg', 'rb'))
   print ('Photo sended')
   logging.info("["+fullDate+"] Photo sended")

  elif (command == '/video'):

   camera = PiCamera();
   #camera.resolution = (640, 480)
   camera.resolution = (1920, 1080)
   camera.framerate = 25

   print ('Recording video…')
   logging.info("["+fullDate+"] Recording a video")
   filename = "./video_" + (time.strftime("%y%b%d_%H%M%S"))
   camera.start_recording(filename + '.h264')
   time.sleep(5)
   camera.stop_recording()
   camera.close()
   command = "MP4Box -add " + filename + '.h264' + " " + filename + '.mp4'
   call([command], shell=True)
   bot.sendVideo(chat_id, open(filename + '.mp4', 'rb'))
   print ('Video sended')
   logging.info("["+fullDate+"] Video sended")
   # borrar original
   command = "rm -rf " + filename + '.h264'
   call([command], shell=True)
   print ('Original Video deleted')
   #borrar mp4
   command = "rm -rf " + filename + '.mp4'
   call([command], shell=True)
   print ('MP4 Video deleted')

  elif (command == '/hello'):
   bot.sendMessage(chat_id, 'Hey!')
  elif (command == '/chatid'):
   bot.sendMessage(chat_id, 'Our chat id is ' + str(chat_id))
  elif (command == '/ip'):
   hostname=socket.gethostname()   
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))
   bot.sendMessage(chat_id, 'My local IP is ' + s.getsockname()[0])
  else:
   bot.sendMessage(chat_id, "Command not found..")
 else:
  bot.sendMessage(chat_id, "Command not found..")
  print ('###¡INTRUSO!### ->Command ' + command + ' from @' + username);
  logging.warning('['+fullDate+'] ###¡INTRUSO!### ->Command ' + command + ' from @' + username)

bot = telepot.Bot(os.getenv("BOT_TOKEN"));
bot.message_loop(handleMessage);
print ("Listening to bot messages….");
while 1:
  time.sleep(10);
