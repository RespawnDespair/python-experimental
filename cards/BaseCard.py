import abc
import configparser
import subprocess

def fitForDriver(driver):
        return False

class BaseCard(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, device, driver):
        self.driver = driver.rstrip()
        self.device = device.rstrip()
        self.mac=subprocess.Popen(['cat', '/sys/class/net/{0}/address'.format(device)], stdout = subprocess.PIPE).communicate()[0].rstrip()

        # Because we no longer rename the device this defaults to device name
        #self.name = self.mac.replace(':', '')
        self.name = self.device

        print('   Set MTU 2304')
        subprocess.check_call(['ifconfig', device, 'mtu', '2304'])

        print('   Mac address: {0}'.format(self.mac))
        print('   Rename {0} to {1}'.format(device, self.name))
        
        # Disabled as i feel this only adds confusion
        #subprocess.Popen(['ip', 'link', 'set', self.device, 'name', self.name], stdout = subprocess.PIPE).communicate()[0]
        
        self.config = self.getConfig()
        
        self.datarateconfig=self.getDataRateConfig()

    @abc.abstractmethod
    def extendedSetup(self):
        raise NotImplementedError('users must define extendedSetup to use this base class')
    
    def getDataRateConfig(self):
        config = configparser.ConfigParser()
        config.read('datarates.ini')
        
        return config[self.config['datarate']]


    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('wifi.ini')

        macspecific=self.mac in config
        if macspecific:
            # Take the mac specific overrides
            return config[self.mac]
        else:
            driverspecific=self.driver in config
            if driverspecific:
                # Take the driver specific overrides
                return config[self.driver]
            else:
                return config['common']
