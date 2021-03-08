import cbpro
import configparser 


def get_curr():
    _curr = []
    
    for section in config.sections():
        if '-usd' in section:
            _curr.append(section)
    return _curr

conf_file = '/home/mike/bin/dcabot/dcabot/etc/dcabot.conf'
config = configparser.ConfigParser()
config.read(conf_file)
print(get_curr())
