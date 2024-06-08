from model.model import Model

mymodel = Model()
mymodel.buildGraph(120*60*1000)
print(mymodel.getGraphDetails())

mymodel.getSetAlbum(mymodel.getNodeI(1), )
