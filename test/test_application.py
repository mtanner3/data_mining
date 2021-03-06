import unittest

from apfacade import APFacade
from dataset import Dataset
from arm import ARM


class TestApplication(unittest.TestCase):
    def setUp(self):
        test_name = self.id().split('.')[-1]
        ds_name = test_name.split('_')[-1]

        self.dataset = Dataset('datasets/{}.dat'.format(ds_name))
        self.dataset.parse_file()
        self.dataset.encode_data()

        self.device = APFacade(dev_name='//simulator/frio0')
        self.device.setup()

    def tearDown(self):
        self.device = None

    def test_simple(self):
        k = 3
        minsup = 2
        arm = ARM(self.dataset.get_frequent_items(minsup), minsup)
        
        for k in xrange(2, k+1):
            arm.init_iteration(k)
            reports = self.device.execute(arm.fsm, self.dataset.encoded_data)
            arm.process_reports(reports)

        self.assertEquals(arm.items, set([1, 2, 3, 4]))

    def test_contextPasquier99(self):
        k = 4
        minsup = 2
        arm = ARM(self.dataset.get_frequent_items(minsup), minsup)
        
        for k in xrange(2, k+1):
            arm.init_iteration(k)
            reports = self.device.execute(arm.fsm, self.dataset.encoded_data)
            arm.process_reports(reports)

        self.assertEquals(arm.items, set([1, 2, 3, 5]))
        self.assertEquals(arm.itemsets, set([
            (1,), (2,), (3,), (5,), 
            (1, 2), (1, 3), (1, 5), (2, 3), (2, 5), (3, 5), 
            (1, 2, 3), (1, 2, 5), (1, 3, 5), (2, 3, 5), 
            (1, 2, 3, 5),
        ]))

    def test_contextRelim(self):
        k = 2
        minsup = 4
        arm = ARM(self.dataset.get_frequent_items(minsup), minsup)
        
        for k in xrange(2, k+1):
            arm.init_iteration(k)
            reports = self.device.execute(arm.fsm, self.dataset.encoded_data)
            arm.process_reports(reports)

        self.assertEquals(arm.items, set([1, 2, 3, 4]))
        self.assertEquals(arm.itemsets, set([
            (1,), (2,), (3,), (4,),
            (1, 4), (2, 4),
        ]))

    def test_contextItemsetTree(self):
        k = 3
        minsup = 2
        arm = ARM(self.dataset.get_frequent_items(minsup), minsup)
        
        for k in xrange(2, k+1):
            arm.init_iteration(k)
            reports = self.device.execute(arm.fsm, self.dataset.encoded_data)
            arm.process_reports(reports)

        self.assertEquals(arm.items, set([1, 2, 4, 5]))
        self.assertEquals(arm.itemsets, set([
            (1,), (2,), (4,), (5,),
            (1, 2), (1, 4), (2, 4), (2, 5), 
            (1, 2, 4),
        ]))

    def test_contextPFPM(self):
        k = 2
        minsup = 3
        arm = ARM(self.dataset.get_frequent_items(minsup), minsup)
        
        for k in xrange(2, k+1):
            arm.init_iteration(k)
            reports = self.device.execute(arm.fsm, self.dataset.encoded_data)
            arm.process_reports(reports)

        self.assertEquals(arm.items, set([1, 2, 3, 4, 5]))
        self.assertEquals(arm.itemsets, set([
            (1,), (2,), (3,), (4,), (5,),
            (3, 4), (3, 5),
        ]))


# vim: nu:et:ts=4:sw=4:fdm=indent
