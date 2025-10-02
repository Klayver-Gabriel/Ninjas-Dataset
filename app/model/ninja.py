class Ninja:
    def __init__(self,element,name,village,salario,rank):
        self.rank = rank
        self.element = element
        self.name = name
        self.village = village
        self.salario = salario
        pass
    def setName(self,name: str):
        self.name = name
        pass
    def getName(self):
        return self.name
    
    def setRank(self,grade : int):
        if grade == 1:
            return self.rank == "Gennin"

        if grade == 2:
            return self.rank == "Chunnin"

        if grade == 3:
            return self.rank == "Jounnin"
        else:
            return self.rank == "Renegado"
            pass
    def getRank(self):
        return self.rank
    
    def setVillage(self,village : str):
        return self.village == village
        pass
    def getVillage(self):
        return self.village
    
    def setElement(self,element:str):
        self.element = element
        pass
    def getElement(self):
        return self.element
    def setSalario(self,salario: int):
        self.salario = salario
        pass
    def getSalario(self):
        return self.salario
    
        

                




