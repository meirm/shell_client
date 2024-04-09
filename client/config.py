""""""
import os
from tools import strToValue
import toml
from client import program_name, __version__
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
basicConfig = dict()
basicConfig["showDisclaimer"] = basicConfig.get("showDisclaimer",True)
basicConfig["verbose"] = basicConfig.get("verbose", False)
basicConfig["debug"] = basicConfig.get("debug", False)

class Config(object):
    def __init__(self):
        self.disclaimer = f"Disclaimer: The advice provided by {program_name} is intended for informational and entertainment purposes only. It should not be used as a substitute for professional advice, and we cannot be held liable for any damages or losses arising from the use of the advice provided by {program_name}."
        self.settingsPath = os.path.join(os.getenv("HOME"), f".{program_name}")
        self.progConfig = dict()
        self.sessionConfig = dict()
        self.has = dict()
        self.has["license"] = False
        self.loadDefaults()
        self.loadProgConfig()
        self.update()
        self.version=__version__
        self.data_path = DATA_PATH

    def loadProgConfig(self):
        if os.path.isfile(os.path.join(self.settingsPath, "config.toml")):
            tomlConfig = toml.load(os.path.join(self.settingsPath,"config.toml"))
            self.progConfig.update(tomlConfig["default"])
        else:
            self.saveConfig()

    def updateParameter(self,key, val):
        val = strToValue(val)
        if key in self.sessionConfig: # order matters
            if self.sessionConfig[key] != val:
                print(f"{key}] = {val}")
                self.sessionConfig[key] = val
        elif key in self.progConfig:
            if self.progConfig[key] != val:
                print(f"{key}] = {val}")
                self.progConfig[key] = val
        


    def saveConfig(self):
        """Save the configuration file"""
        jsonConfig = {'name':f'{program_name}','default':self.progConfig}
        with open(os.path.join(self.settingsPath,"config.toml"), 'w') as f:
            toml.dump(jsonConfig,f)
        self.update()

    def reloadConfig(self):
        """Reload the configuration file"""
        self.update()

    def get_list(self):
        """
        list the previous conversations saved by program_name."""
        conv_array = list()
        # for line in os.listdir(self.conversations_path):
        #     if (not line.startswith("."))  and line.endswith(self.fileExtension) and (os.path.isfile(os.path.join(self.conversations_path,line))):
        #         conv_array.append(line.replace(self.fileExtension,""))
        return sorted(conv_array)

    def loadDefaults(self):
        self.progConfig["showDisclaimer"] = self.progConfig.get("showDisclaimer",True)
        self.progConfig["verbose"] = self.progConfig.get("verbose", False)
        self.progConfig["debug"] = self.progConfig.get("debug", False)

    def printConfig(self):
        """Print the configuration file"""
        print(toml.dumps(self.progConfig))

    def update(self):
        """
Load the configuration file from ~/.program_name/config.toml"""
        self.loadProgConfig()
            # self.progConfig.update(tomlConfig[f"{program_name}"])
