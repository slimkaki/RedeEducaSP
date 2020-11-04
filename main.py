# Microdados - Atribuição de Aulas dos Servidores da Educação Municipal:
# http://dados.prefeitura.sp.gov.br/pt_PT/dataset/microdados-servidores-atribuicao

# Ideb e Prova Brasil na Rede Municipal de Ensino (2005-2015):
# http://dados.prefeitura.sp.gov.br/pt_PT/dataset/ideb-e-prova-brasil-na-rede-municipal-de-ensino

"""
TO-DO:
    - apagar escolas que não tão em algum csv
    - somente 



IDEB:
Bater o codigo da escola com o 
Para cada ano:
    Pagina excel anos iniciais: notas (2 + 3 + 4 + 5 ano)/4
    Pagina excel anos finais: notas (2 + 3 + 4 + 5 ano)/4
     
"""
from csv import reader

class Educa(object):
    def __init__(self):

        self.data = {"atribuicao2010.csv": 2010, "atribuicao2011.csv": 2011 , "atribuicao2012.csv": 2012,
                    "atribuicao2013.csv": 2013, "atribuicao2014.csv": 2014, "atribuicao2015.csv": 2015}#, 
                    #"atribuicao2016.csv": 2016, "atribuicao2017.csv": 2017, "atribuicao2018.csv": 2018, 
                    #"atribuicaocomaulas2019.csv": 2019}

        self.professores = {}
        self.connections = {} 
        self.escolas = []
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
            "id prof 1": {id_escola
            "id prof 2": {
                2016: [...]
            }
        }
        """

    def getIndexes(self, indexes):

        
        for i in range(len(indexes)):
            if  "CD_SERV" in  indexes[i]:
                professor_index = i 
            elif indexes[i] == "CD_UNIDADE":
                escola_index = i

        return professor_index, escola_index


    def getSchools(self):

        for tabela in self.data:

            escolas_atuais = []

            if self.data[tabela] == 2010:
                with open(tabela) as file:
                    indexes = file.readline()
                    indexes = indexes.split(";")
                    prof_index, escola_index = self.getIndexes(indexes)

                    for i, row in enumerate(reader(file), 2):
                        row = row[0].replace(";;", ";null;").split(";")

                        id_escola = row[escola_index]
                        if id_escola not in self.escolas:
                            self.escolas.append(id_escola)
            else:
                with open(tabela) as file:
                    indexes = file.readline()
                    indexes = indexes.split(";")
                    prof_index, escola_index = self.getIndexes(indexes)

                    for i, row in enumerate(reader(file), 2):
                        row = row[0].replace(";", ",").split(",")
                        id_escola = row[escola_index]
                        
                        if id_escola not in escolas_atuais:
                            escolas_atuais.append(id_escola)

                    for escola in self.escolas:
                        if escola not in escolas_atuais:
                            self.escolas.remove(escola)



    
    def getCSV(self, tabela, ano):


        with open(tabela) as file:
            indexes = file.readline()
            indexes = indexes.split(";")
            professor_index, escola_index = self.getIndexes(indexes)

            
            for i, row in enumerate(reader(file), 2):
                # row = row[0].replace(";", ",").split(",")
                row = row[0].replace(";;", ";null;").split(";")
                
                id_professor  = row[professor_index]
                id_escola = row[escola_index]


                #Se não está na lista de escolas, não precisa adicionar
                if id_escola not in self.escolas:
                    continue

                #Se o professor não está na professores, cria o objeto
                elif id_professor not in self.professores:  
                    self.professores[id_professor] = { 
                        int(ano) : id_escola
                    }

                #Se o professor está na professores mas o ano especifico não, adiciona o ano.
                elif ano not in self.professores[id_professor]:
                    self.professores[id_professor][ano] = id_escola

                #Remove os professores que trabalham em mais de uma escola (por simplicidade)
                elif id_escola not in self.professores[id_professor][ano]:
                    self.professores.pop(id_professor)

    def getAllCSV(self):
        for d in self.data.keys():
            self.getCSV(d, self.data[d])

    def makeConnections(self):
        escolas = []
        with open('escolas.gml', 'w') as file:
            
            file.write('graph [\n')
            file.write('  directed 1\n')


            for professor in self.professores:
                for ano in self.professores[professor]:
                    if self.professores[professor][ano] not in escolas:
                        file.write('  node [\n')
                        file.write('    id "{}"\n'.format(self.professores[professor][ano]))
                        file.write('  ] \n')
            
            file.write(']\n')




                                        
                            
        
            

    def start(self):
        self.getSchools()
        self.getAllCSV()
        self.makeConnections()


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

if __name__ == '__main__':
    ed = Educa()
    ed.start()
    ed.makeConnections()
    #print(ed.professores)
    print("elle boba")
#EU ODEIO O LEONARDO     