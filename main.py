class Educa(object):
    def __init__(self):

        self.data = {"atribuicao2010.csv": 2010, "atribuicao2011.csv": 2011 , "atribuicao2012.csv": 2012,
                    "atribuicao2013.csv": 2013, "atribuicao2014.csv": 2014, "atribuicao2015.csv": 2015}#, 
                    #"atribuicao2016.csv": 2016, "atribuicao2017.csv": 2017, "atribuicao2018.csv": 2018, 
                    #"atribuicaocomaulas2019.csv": 2019} 
        self.professores = {}
        self.connections = {}
        """
    connections  =  {
                    "a" : [{
                        target: "b",
                        weight: 343
        
                    },
                    {
                        target: "d",
                        weight: 23
                    }],: invalid syntax

                    "b": [{
                        target: "b"
                        weight: 3
                    }]




    }
        {source: id escola init
          
        target: id escola final
                
        weight: 2 
        }
    ]





        {
            "id prof 1": {
                2019: ["id escola 1", "id escola 2"],
                2018: ["id escola 2"]
                }, 
            "id prof 2": {
                2016: [...]
            }
        }
        """
    
    def getCSV(self, tabela, ano):
        from csv import reader

        with open(tabela) as file:
            indexes = file.readline()
            indexes = indexes.split(";")
            for i in range(len(indexes)):
                if  "CD_SERV" in  indexes[i]:
                    professor_index = i 
                elif indexes[i] == "CD_UNIDADE":
                    escola_index = i
            
            for i, row in enumerate(reader(file), 2):
                row = row[0].replace(";", ",").split(",")
                id_professor  = row[professor_index]
                id_escola = row[escola_index]

                if id_professor not in self.professores:
                    self.professores[id_professor] = { 
                        int(ano) : [id_escola]
                    }
                
                elif ano not in self.professores[id_professor].keys():
                    self.professores[id_professor][ano] = [id_escola]

                elif id_escola not in self.professores[id_professor][ano]:
                    self.professores[id_professor][ano].append(id_escola)

                                                                                                                                                                                                             

    def getAllCSV(self):
        for d in self.data.keys():
            self.getCSV(d, self.data[d])

    def makeConnections(self):
        #REFAZER ISSO AQUI EH O CODIGO MAIS NOJENTO Q JA FIZ!!!!!!!!!!!!!!!IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII!IIi!i!i!i!i!i!ii!i!iAJKSDUJH
        #for professor in self.professores:
        #    for ano in self.professores[professor]:
        #        for escola in self.professores[professor][ano]:
        #            if (ano+1 in self.professores[professor]) and (professor not in self.professores[professor][ano+1]):
        #                for escola_nova in self.professores[professor][ano+1]:
        #                    for objeto in self.connections:
        #                        if escola_nova in self.connections[escola]():
        #                
                    
                                        
                            
        
            

    def start(self):
        self.getAllCSV()
        #self.makeConnections()


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

if __name__ == '__main__':
    ed = Educa()
    ed.start()
    ed.makeConnections()
    print("leonardo babaca")
#EU ODEIO O LEONARDO    