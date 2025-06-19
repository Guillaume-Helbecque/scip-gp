import os
os.chdir("/home/ghelbecq/Bureau/scip-rl/")

from instances.generate_instances import compile_generator, generate_instance
from model.generate_model import extract_data, create_model

n = 5000
type = 9
r = 100000
id = 17

filename = "knapPI_"+str(type)+"_"+str(n)+"_"+str(r)+"_"+str(id)+".txt"

compile_generator()
generate_instance(n, type, r, id)
n, c, p, w = extract_data(filename)
scip = create_model(n, c, p, w)
scip.optimize()
