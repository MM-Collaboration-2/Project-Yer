class Object():
    regex = '.*?'
    type: str = 'object'
    def __init__(self, data=0):
        self.data: int = data
                                        
    def __repr__(self):
        return str(self.data)
