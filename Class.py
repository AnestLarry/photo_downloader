class De_Iterator:
    "Decreasing_Iterator"
    def __init__ (self,key_list):
        self.list=key_list
    
    def get(self):
        if self.list:
            return self.list.pop(0)
        else:
            return False
    
    def check(self):
        if self.list:
            return True
        else:
            return False
    
    def add(self,key_list):
        if self.list:
            self.list.extend(key_list)
            return True
        else:
            self.list=key_list
            return False