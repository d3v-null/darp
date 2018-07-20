# -*- coding: utf-8 -*-
""" Provides ArpScan class, A wrapper for the arp-scan CLI utility"""

# import sys
import subprocess
import re

class ArpScan(object):
    """ Wrapper for the ArpScan CLI utility """
    default_args = {
        'localnet': True,
        'retry': 5,
        'timeout': 3000
    }

    option_properties = {
        'localnet':{
            'type':bool
        },
        'retry':{
            'type':int
        },
        'timeout':{
            'type':int
        },
        'interval':{
            'type':int
        },
        'bandwidth':{
            'type':int
        },
        'backoff':{
            'type':float
        },
        'random':{
            'type':bool
        },
        'interface':{
            'type':str
        }
    }

    re_interface = r'Interface: (?P<interface>[^\s,]*),?'
    re_device = r'(?P<address>[0-9.]*)\s(?P<mac>[0-9a-f:]{17})(?:\s(?P<name>\S[\S\s]*\S))'

    def __init__(self, **kwargs):
        """ Creates ArpScan object and performs scan, parsing and storing results """

        scan_args = dict(self.default_args.items())
        scan_args.update(**kwargs)
        arp_scan_options = ['arp-scan']
        for option_name, properties in self.option_properties.items():
            if not option_name in scan_args:
                continue
            option_type = properties.get('type', bool)
            option_value = scan_args[option_name]
            assert \
                isinstance(option_value, option_type), \
                "value of option %s is of type %s when it should be %s" \
                    % (option_name, type(option_value), option_type)
            if option_type == bool:
                if option_value:
                    arp_scan_options.append("--%s" % option_name)
            elif option_type in [int, float]:
                arp_scan_options.append("--%s=%s" % (option_name, option_value))
            elif option_type == str:
                arp_scan_options.append("--%s='%s'" % (option_name, option_value))

        subp = subprocess.Popen(arp_scan_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = subp.communicate()
        returncode = subp.returncode

        if returncode != 0:
            raise UserWarning("nonzero return code (%d). stderr: %s" % (returncode, stderr))

        self.results = self.parse(stdout)
        # print self.results

        # return self.parse(stdout)

    @classmethod
    def parse(cls, out):
        """ Parses the output of running arp-scan, results in dict """
        results = {}
        for line in out.split('\n'):
            if re.match(cls.re_interface, line):
                matchdict = re.match(cls.re_interface, line).groupdict()
                interface = matchdict.get('interface')
                results['interface'] = interface
            elif re.match(cls.re_device, line):
                matchdict = re.match(cls.re_device, line).groupdict()
                address = matchdict.get('address')
                mac = matchdict.get('mac')
                name = matchdict.get('name')
                if 'devices' not in results:
                    results['devices'] = []
                results['devices'].append({
                    'address':address,
                    'mac':mac,
                    'name':name
                })
        return results


def main():
    """ Main method of arp_scan package """
    ArpScan()

if __name__ == '__main__':
    main()
