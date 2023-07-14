from object import Object


class Void(Object):
    regex: str = ''
    type: str = 'void'

    def __inif__(self, data: str=''):
        self.data: str = str(data)
    
    def __repr__(self):
        return 'void#' + str(self.data)
