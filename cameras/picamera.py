import subprocess
import configparser

def fitForType(type):
    return type == 'picamera'

class Camera():
    def __init__(self, config_section_name):
        self.name = config_section_name
        config = configparser.ConfigParser()
        config.read('cameras.ini')

        self.width = config[self.name]['width']
        self.height = config[self.name]['height']
        self.fps = config[self.name]['fps']
        self.extraparams = config[self.name]['extraparams']

    def startSending():
        #nice -n -9 raspivid -w $WIDTH -h $HEIGHT -fps $FPS -b $BITRATE -g $KEYFRAMERATE -t 0 $EXTRAPARAMS -o - | nice -n -9 /home/pi/wifibroadcast-base/tx_rawsock -p 0 -b $VIDEO_BLOCKS -r $VIDEO_FECS -f $VIDEO_BLOCKLENGTH -t $VIDEO_FRAMETYPE -d $VIDEO_WIFI_BITRATE -y 0 $NICS
        return 0