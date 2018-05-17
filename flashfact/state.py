# singleton pattern to store application state


debug = False # set to true to debug setting overrides 


class AppState:
    class __State:
            
        def __str__(self):
            return repr(self) + self.val
            
        def get(self, attr, default):
            value = getattr( AppState.instance, attr, default) 
            if debug and value != default:
                    print("appstate overrides %s of %s with %s" % (attr , default, value))
            return getattr( AppState.instance, attr, default)
        
        def set(self, attr, value): 
            setattr(AppState.instance, attr, value)
            
            
            
    instance = None
    def __init__(self):
        if not AppState.instance:
            AppState.instance = AppState.__State()
        
            
    def __setattr__(self, name, val):
        setattr(self.instance, name, val)
        
    def __getattr__(self, name):
        return getattr(self.instance, name)
        
    def save(self):
        '''save state into ~/.<appname>rc'''
        open()