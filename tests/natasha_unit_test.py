import unittest
from tools.NatashaTextProcessing import NatashaProcessing
import warnings


class TestNatasha(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=DeprecationWarning) #для более чистого вывода без предупреждений
        self.name_pattern = "<b>{0}</b>, наверняка отличный человек, раз вы о нем говорите.\n\n" \
                                               "<i>Но может лучше закажите у нас цветы?</i>"
        self.loc_pattern = "<b>{0}</b>. Говорят там красиво, я хотел бы там побывать\n\n" \
                                               "Но вы же сюда пришли не слушать мечты робота, " \
                                               "<i>а купить прекрасные цветы, верно?</i>"
        self.org_pattern = "Зачем вам <b>{0}</b>? Лучше загляните в раздел \"Скидки\"."

    def test_name(self):
        name_for_test = "Марина"
        self.name_pattern = self.name_pattern.format(name_for_test)
        res = NatashaProcessing.get_fact_answer(name_for_test).text
        self.assertEqual(res, self.name_pattern)

    def test_lock(self):
        loc_for_test = "Россия"
        self.loc_pattern = self.loc_pattern.format(loc_for_test)
        res = NatashaProcessing.get_fact_answer(self.loc_pattern).text
        self.assertEqual(res, self.loc_pattern)

    def test_org(self):
        org_for_test = "Газпром"
        self.org_pattern = self.org_pattern.format(org_for_test)
        res = NatashaProcessing.get_fact_answer(self.org_pattern).text
        self.assertEqual(res, self.org_pattern)

if __name__ == "__main__":
    unittest.main()
