from cards.BaseCard import BaseCard
import subprocess

def fitForDriver(driver):
    #881[24]au
    return driver in ['rt2800usb','mt7601u','rtl8192cu','rtl88xxau']

class Card(BaseCard):
    pass

    def __init__(self, device, mode):
        super(Card, self).__init__(device, 'realtek')
        self.mode = mode

    def extendedSetup(self):
        print('     Set monitor mode')
        subprocess.check_call(['iw', 'dev', self.name, 'set', 'monitor', 'none'])

        print('     Bring interface up')
        subprocess.check_call(['ifconfig', self.name, 'up'])
        
        print('     Set frequency: ' + self.config['frequency'])
        subprocess.check_call(['iw', 'dev', self.name, 'set', 'freq', self.config['frequency']])

        if self.driver == 'rtl88xxau':
            print('     Set TX Power: ' + self.config['realtek_tx_power'])
            subprocess.check_call(['iw', 'dev', self.name, 'set', 'txpower', 'fixed', self.config['realtek_tx_power']])

        return 0

        