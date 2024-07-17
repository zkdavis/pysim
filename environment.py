from pysim.parsing import File, Folder 
#need to rethink this
pysimDir = Folder("/".join(__file__.split('/')[:-1]))
simulationDir = Folder("/anvil/scratch/x-kgootkin/sims/")
dHybridRtemplate = Folder(pysimDir.path + "/templates/dHybridR/")
figDir = Folder("/home/x-kgootkin/figures/")
frameDir = Folder("/home/x-kgootkin/frames/")
videoDir = Folder("/home/x-kgootkin/videos/")