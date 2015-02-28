#!/usr/bin/env python

import numpy as np
import pandas as pd
import pandas.compat as compat

import sklearn.datasets as datasets
import sklearn.mixture as mixture

import expandas as expd
import expandas.util.testing as tm


class TestMixture(tm.TestCase):

    def test_objectmapper(self):
        df = expd.ModelFrame([])
        self.assertIs(df.mixture.GMM, mixture.GMM)
        self.assertIs(df.mixture.DPGMM, mixture.DPGMM)
        self.assertIs(df.mixture.VBGMM, mixture.VBGMM)

    def test_Classifications(self):
        iris = datasets.load_iris()
        df = expd.ModelFrame(iris)

        models = ['GMM', 'DPGMM', 'VBGMM']
        for model in models:
            mod1 = getattr(df.mixture, model)(random_state=self.random_state)
            mod2 = getattr(mixture, model)(random_state=self.random_state)

            df.fit(mod1)
            mod2.fit(iris.data)

            result = df.predict(mod1)
            expected = mod2.predict(iris.data)

            self.assertTrue(isinstance(result, expd.ModelSeries))
            self.assert_numpy_array_almost_equal(result.values, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
