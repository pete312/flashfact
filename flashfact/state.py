# singleton pattern to store application state

import configparser
import os

debug = False # set to true to debug setting overrides 
default_config_filename = os.getenv("HOME", '/tmp') + "/.flashfactrc"




class AppState:
    class __State:
        def __init__(self, filename=None):
            self.config = configparser.ConfigParser()
            if filename is None:
                filename = default_config_filename
            if os.path.exists(filename):
                self.config.read_file(open(filename))
                self.conversion = {"<class 'str'>": str,
                                "<class 'bool'>": self.config.getboolean,
                                "<class 'int'>": self.config.getint,
                                "<class 'int'>": self.config.getfloat,
                                    }
                if self.config.has_section('appstate'):
                    for k,v in self.config['appstate'].items():
                        
                        setattr(self, k , self.convert('appstate', k, self.config['meta'][k]))
            self.filename = filename
            
        
        def convert(self, section, option, typeof ):
            if typeof == "<class 'str'>":
                return self.config.get(section, option)
                
            elif typeof == "<class 'int'>":
                return self.config.getint(section, option)
   
            elif typeof == "<class 'bool'>":
                return self.config.getboolean(section, option)
            elif typeof == "<class 'float'>":
                return self.config.getfloat(section, option)
            
            
        
        def __str__(self):
            return repr(self) + self.val
            
        def get(self, attr, default):
            value = getattr( self, attr, default) 
            if debug and value != default:
                print("appstate overrides %s of %s with %s" % (attr , default, value))
            return getattr( AppState.instance, attr, default)
        
        def set(self, attr, value): 
            print("here with ", type(values))
            setattr(self, attr, value)
            
        def save_state(self, varlist=[] ):
            self.config['appstate'] = {}
            self.config['meta'] = {}
            setting = {}
            
            for k in vars(self):
                val = self.get(k, None)
                if type(val) in [str, int, float, bool, list, tuple]:
                    self.config['appstate'][k] = str(val)
                    self.config['meta'][k] = str(type(val))
            
            with open(self.filename, 'w') as fh:
                self.config.write(fh)
        
        def load_state(self):
            if os.path.exists(self.filename):
                self.config.read_file(open(self.filename))
                for k,v in self.config['appstate'].items():
                    setattr(self, k , v)
                    
        def dump_state(self):
            for k in vars(self):
                val = self.get(k, None)
                if type(val) in [str, int, float, bool, list, tuple]:
                    print("val of %s is type %s with val %s" %(k, type(val), val))
                    
    instance = None
    def __init__(self):
        if not AppState.instance:
            AppState.instance = AppState.__State()
        
            
    def __setattr__(self, name, val):
        setattr(self.instance, name, val)
        
    def __getattr__(self, name):
        return getattr(self.instance, name)
        
        
        
if __name__ == "__main__":
    appstate = AppState()
    
    print(vars(appstate))