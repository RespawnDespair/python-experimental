from cards.BaseCard import BaseCard
import subprocess

def fitForDriver(driver):
        return driver == 'ath9k_htc'

class Card(BaseCard):
    pass

    def __init__(self, device, mode):
        super(Card, self).__init__(device, 'ath9k_htc')
        self.mode = mode

    def extendedSetup(self):
        print('     Bring interface up')
        subprocess.check_call(['ifconfig', self.name, 'up'])

        if self.mode == 'AIR':
            print('     Change bitrate: ' + self.datarateconfig['video_wifi_bitrate'])
            if self.datarateconfig['video_wifi_bitrate'] != '19.5':
                subprocess.check_call(['iw', 'dev', self.name, 'set', 'bitrates', 'legacy-2.4', self.datarateconfig['video_wifi_bitrate']])
        elif self.mode == 'GND':
            print('     Change bitrate: ' + self.datarateconfig['video_wifi_bitrate'])
            if self.datarateconfig['video_wifi_bitrate'] != '19.5':
                subprocess.check_call(['iw', 'dev', self.name, 'set', 'bitrates', 'legacy-2.4', self.datarateconfig['uplink_wifi_bitrate']])

        print('     Bring interface down')
        subprocess.check_call(['ifconfig', self.name, 'down'])

        print('     Set monitor mode')
        subprocess.check_call(['iw', 'dev', self.name, 'set', 'monitor', 'none'])

        print('     Bring interface up')
        subprocess.check_call(['ifconfig', self.name, 'up'])
        
        print('     Set frequency: ' + self.config['frequency'])
        subprocess.check_call(['iw', 'dev', self.name, 'set', 'freq', self.config['frequency']])

        return 0

        