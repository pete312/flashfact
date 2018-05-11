# singleton pattern to store application state


class AppState:
    class __State:
            
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self):
        if not AppState.instance:
            AppState.instance = AppState.__State()
        
            
    def __setattr__(self, name, val):
        setattr(self.instance, name, val)
        
    def __getattr__(self, name):
        return getattr(self.instance, name)
        
    