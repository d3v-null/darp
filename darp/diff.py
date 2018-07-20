class ScanDiff(object):
    def __init__(self, old_scan, new_scan):
        self.old_scan = old_scan
        self.new_scan = new_scan

    @property
    def new_macs(self):
        return [scan.get('mac') for scan in self.new_scan]

    @property
    def old_macs(self):
        return [scan.get('mac') for scan in self.old_scan]

    def mac_difference(self):
        new_macs = set(self.new_macs)
        old_macs = set(self.old_macs)
        return list(new_macs - old_macs), list(old_macs - new_macs)
