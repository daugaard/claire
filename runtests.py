import unittest
from tests import ModelsTest


suite = unittest.TestLoader().loadTestsFromTestCase(ModelsTest)
unittest.TextTestRunner(verbosity=2).run(suite)
