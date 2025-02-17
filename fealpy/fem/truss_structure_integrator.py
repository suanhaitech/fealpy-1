import numpy as np
from typing import Tuple, Optional, Union

class TrussStructureIntegrator:
    def __init__(self, E: float, A: float, q :int = 3):
        """
        TrussStructureIntegrator 类的初始化

        参数:
        E -- 杨氏模量
        A -- 单元横截面积
        q -- 积分公式的等级，默认值为3
        """
        self.E = E  # 杨氏模量
        self.A = A  # 单元横截面积
        self.q = q # 积分公式

    def assembly_cell_matrix(self, space: Tuple, 
                            index: Optional[Union[int, slice]] = np.s_[:],
                            cellmeasure: Optional[np.ndarray] = None, 
                            out: Optional[np.ndarray] = None):
        """
        组装单元网格的刚度矩阵

        参数:
        space -- 空间维度的元组
        index -- 单元网格的索引，默认为全部单元
        cellmeasure -- 单元的度量，默认为 None，表示使用默认度量
        out -- 输出的数组，默认为 None，表示创建新数组

        返回值:
        组装好的单元网格刚度矩阵
        """
        assert isinstance(space, tuple) 
        space0 = space[0]
        mesh = space0.mesh
        GD = mesh.geo_dimension()

        assert  len(space) == GD

        if cellmeasure is None:
            cellmeasure = mesh.entity_measure('cell', index=index)

        NC = len(cellmeasure)

        c = self.E*self.A
        tan = mesh.cell_unit_tangent(index=index)
        R = np.einsum('ik, im->ikm', tan, tan)
        R *= c/cellmeasure[:, None, None]

        ldof = 2 # 一个单元两个自由度, @TODO 高次元的情形？本科毕业论文
        if out is None:
            K = np.zeros((NC, GD*ldof, GD*ldof), dtype=np.float64)
        else:
            assert out.shape == (NC, GD*ldof, GD*ldof)
            K = out

        if space0.doforder == 'sdofs':
            for i in range(GD):
                for j in range(i, GD):
                    if i == j:
                        K[:, i::ldof, i::ldof] += R[i, i] 
                    else:
                        K[:, i::ldof, j::ldof] -= R[i, j] 
                        K[:, j::ldof, i::ldof] -= R[j, i] 
        elif space0.doforder == 'vdims':
            for i in range(ldof):
                for j in range(i, ldof):
                    if i == j:
                        K[:, i*GD:(i+1)*GD, i*GD:(i+1)*GD] += R
                    else:
                        K[:, i*GD:(i+1)*GD, j*GD:(j+1)*GD] -= R
                        K[:, j*GD:(j+1)*GD, i*GD:(i+1)*GD] -= R

        if out is None:
            return K
