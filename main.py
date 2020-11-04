# Microdados - Atribuição de Aulas dos Servidores da Educação Municipal:
# http://dados.prefeitura.sp.gov.br/pt_PT/dataset/microdados-servidores-atribuicao

# Índice de Desenvolvimento da Educação Paulistana (IDEP) (2018-2019):
# http://dados.prefeitura.sp.gov.br/pt_PT/dataset/idep

"""
IDEB:
Bater o codigo da escola com o 
Para cada ano:
    Pagina excel anos iniciais: notas (2 + 3 + 4 + 5 ano)/4
    Pagina excel anos finais: notas (2 + 3 + 4 + 5 ano)/4
"""
from csv import reader
import json 


class EducacaoData(object):
    def __init__(self):

        self.data = {"atribuicao2010.csv": 2010, "atribuicao2011.csv": 2011 , "atribuicao2012.csv": 2012,
                    "atribuicao2013.csv": 2013, "atribuicao2014.csv": 2014, "atribuicao2015.csv": 2015}#, 
                    #"atribuicao2016.csv": 2016, "atribuicao2017.csv": 2017, "atribuicao2018.csv": 2018, 
                    #"atribuicaocomaulas2019.csv": 2019}
        self.data_idep = ["idepanosiniciaisescolas2019FAIXA_1.csv", 
        "idepanosiniciaisescolas2019FAIXA_2.csv", 
        "idepanosiniciaisescolas2019FAIXA_3.csv", 
        "idepanosiniciaisescolas2019FAIXA_4.csv", 
        "idepanosiniciaisescolas2019FAIXA_5.csv",
        "idepanosiniciaisescolas2019FAIXA_6.csv",
            "idepanosfinaisescolas2019FAIXA_1.csv", 
            "idepanosfinaisescolas2019FAIXA_2.csv", 
            "idepanosfinaisescolas2019FAIXA_3.csv", 
            "idepanosfinaisescolas2019FAIXA_4.csv", 
            "idepanosfinaisescolas2019FAIXA_5.csv",
            "idepanosfinaisescolas2019FAIXA_6.csv"]


        self.professores = {}
        self.connections = {} 
        self.escolas = []
        self.idep = {}
        self.totalTeachers = {}
        self.totalTeachersValues = {}
    

    def getDesempenho(self, tabela):
        
        with open(tabela) as file:
            file.readline()
            file.readline()


            for i, row in enumerate(reader(file), 2):
                #Estamos zerando a nota de escolas que tem * na nota
                desempenho_2018 = float(row[7].replace(",", ".").replace('"',"").replace("*","0"))
                desempenho_2019 = float(row[8].replace(",", ".").replace('"',"").replace("*","0"))
                id_escola = row[0]
                id_escola = id_escola.lstrip("0")
    
                if id_escola not in self.escolas:
                    continue

                if id_escola not in self.idep:
                    self.idep[id_escola] = (desempenho_2018+desempenho_2019)/4
                else:
                    self.idep[id_escola] += (desempenho_2018+desempenho_2019)/4                
                
                
    def getAllDesempenho(self):
        for d in self.data_idep:
            self.getDesempenho(d)

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

    def getTotalOfTeachers(self, tabela, ano):
        """
        self.totalTeachers = {
                                "escola1" : {
                                            2010: [prof1, prof2, prof3],
                                            2011: [prof2, prof3, prof4, prof5],
                                            ...
                                            },  
                                "escola2" : {
                                        2010: [prof1, prof2, prof3, prof4, prof5],
                                            ...
                                            },
                                ...
                            }
        """
    
        with open(tabela) as file:

            indexes = file.readline()
            indexes = indexes.split(";")
            professor_index, escola_index = self.getIndexes(indexes)

            for i, row in enumerate(reader(file), 2):
                # row = row[0].replace(";", ",").split(",")
                row = row[0].replace(";;", ";null;").split(";")
                id_professor  = row[professor_index]
                id_escola = row[escola_index]

                if id_escola not in self.totalTeachers:
                    self.totalTeachers[id_escola]={
                        ano : [id_professor]
                    }
                elif ano not in self.totalTeachers[id_escola]:
                    self.totalTeachers[id_escola][ano] = [id_professor]
                elif id_professor not in self.totalTeachers[id_escola][ano]:
                    self.totalTeachers[id_escola][ano].append(id_professor)

        
    
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
                if id_escola not in self.idep:
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
            self.getTotalOfTeachers(d, self.data[d])

        for escola in self.totalTeachers:
            for ano in self.totalTeachers[escola]:
                if escola not in self.totalTeachersValues:
                    self.totalTeachersValues[escola] = len(self.totalTeachers[escola][ano])
                else:
                    self.totalTeachersValues[escola] += len(self.totalTeachers[escola][ano])
            
            self.totalTeachersValues[escola] = self.totalTeachersValues[escola]/(len(self.data))

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
                        file.write('    professores "{}"\n'.format(self.totalTeachersValues[self.professores[professor][ano]]))
                        file.write('  ] \n')
                        escolas.append(self.professores[professor][ano])
            
            weights = {}
            for professor in self.professores:
                for ano in self.professores[professor]:
                    #se o professor mudou de escola:
                    if (ano + 1 in self.professores[professor]) and (self.professores[professor][ano] != self.professores[professor][ano+1]):
                        #soma os pesos das mudancas entre escolas
                        id_edge = str(self.professores[professor][ano]) + "/" + str(self.professores[professor][ano+1])
                        if (id_edge not in weights):
                            weights[id_edge] = 1
                        else:
                            weights[id_edge] += 1
            
            for edge in weights:
                ids = edge.split("/")
                source, target = ids[0], ids[1]
                weight = weights[edge]
                file.write('  edge [\n')
                file.write('    source "{}"\n'.format(source))
                file.write('    target "{}"\n'.format(target))
                file.write('    weight "{}"\n'.format(weight))
                file.write('  ]\n')
                                                
            file.write(']\n')
    

    def start(self):
        self.getSchools()
        self.getAllDesempenho()
        self.getAllCSV()
        self.makeConnections()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

if __name__ == '__main__':
    ed = EducacaoData()
    ed.start()
    json_object = json.dumps(ed.idep, indent = 4) 

    with open("uwu.json", "w") as outfile: 
        outfile.write(json_object) 
#EU ODEIO O LEONARDO