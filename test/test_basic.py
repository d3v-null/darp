""" Darp tests """

import unittest

import darp
from darp.arp_scan import ArpScan
from darp.db import DBWrapper

class ArpScanTestCase(unittest.TestCase):
    """ Test case for ArpScan class """

    def setUp(self):
        pass

    def test_parse(self):
        """ Tests the parse function of the ArpScan class """
        example_arp_scan_out = "\n".join([
            "Interface: en0, datalink type: EN10MB (Ethernet)",
            "Starting arp-scan 1.9 with 256 hosts (http://www.nta-monitor.com/tools/arp-scan/)",
            "10.1.1.1	aa:bb:cc:dd:ee:ff	(Unknown)",
            "10.1.1.10	bb:cc:dd:ee:ff:aa	Apple, Inc",
            "",
            "524 packets received by filter, 0 packets dropped by kernel",
            "Ending arp-scan 1.9: 256 hosts scanned in 1.776 seconds (144.14 hosts/sec). "\
            + "2 responded",
        ])
        test_parsed = ArpScan.parse(example_arp_scan_out)
        expected_parsed = {
            'devices': [
                {'address': '10.1.1.1',
                'mac': 'aa:bb:cc:dd:ee:ff',
                'name': '(Unknown)'},
                {'address': '10.1.1.10',
                'mac': 'bb:cc:dd:ee:ff:aa',
                'name': 'Apple, Inc'}
            ],
            'interface': 'en0'
        }
        self.assertEquals(test_parsed, expected_parsed)

class DBWrapperTestCase(unittest.TestCase):
    """ Test case for DBWrapper class """
    def setUp(self):
        self.dbwrapper = DBWrapper("darp_db_test.json")
        self.dbwrapper.purge()
        self.stamp = '2016-11-5_11-53-00'
        self.dbwrapper.insert_sighting(
            name="(Unknown)",
            address="10.1.1.1",
            mac="aa:bb:cc:dd:ee:ff",
            stamp=self.stamp
        )

    def testLastSighting(self):
        stamp = self.dbwrapper.last_sighting("aa:bb:cc:dd:ee:ff").get('stamp')
        expected_stamp = self.stamp
        self.assertEqual(stamp, expected_stamp)

        stamp = self.dbwrapper.last_sighting("ff:ff:ff:ff:ff:ff")
        expected_stamp = None
        self.assertEqual(stamp, expected_stamp)



if __name__ == '__main__':
    unittest.main()
