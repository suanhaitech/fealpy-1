
import numpy as np

class ProvidesSymmetricTangentOperatorIntegrator:
    def __init__(self):
        pass

    def assembly_cell_matrix(self, space, index=np.s_[:], cellmeasure=None, out=None):
        self.space = space[0]
        self.mesh = space[0].mesh


    def assembly_cell_matrix_fast(self, space0, _, index=np.s_[:], cellmeasure=None):
        pass


    def assembly_cell_matrix_ref(self, space0, _, index=np.s_[:], cellmeasure=None):
        pass
