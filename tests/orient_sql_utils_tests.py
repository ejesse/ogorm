from models.base import Model
from models.orient_sql_utils import is_model, get_model_extensions
from tests import OgormTest


class Foo:
    pass


class ImAModel(Model):
    pass


class IAMToo(Model):
    pass


class AndMeThree(IAMToo):
    pass


class AndMeFour(ImAModel, AndMeThree):
    pass

class TestUtils(OgormTest):
    
    def test_is_model(self):
        
        self.assertFalse(is_model(Foo))
        self.assertFalse(is_model(Foo()))
        self.assertTrue(is_model(ImAModel))
        self.assertTrue(is_model(ImAModel()))
        self.assertTrue(is_model(IAMToo))
        self.assertTrue(is_model(IAMToo()))
        self.assertTrue(is_model(AndMeThree))
        self.assertTrue(is_model(AndMeThree()))
        
    def test_get_model_extensions(self):
        self.assertLessEqual(get_model_extensions(ImAModel), [])
        self.assertRaises(ValueError, get_model_extensions, Foo)
        self.assertEqual(get_model_extensions(AndMeThree),['tests___dot___orient_sql_utils_tests___dot___IAMToo'])
        self.assertEqual(get_model_extensions(AndMeFour),['tests___dot___orient_sql_utils_tests___dot___ImAModel','tests___dot___orient_sql_utils_tests___dot___AndMeThree'])



