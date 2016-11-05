class ScanDiff(object):
    def __init__(self, old_scan, new_scan):
        self.old_scan = old_scan
        self.new_scan = new_scan

    def mac_difference(self):
        added = []
        removed = []
        new_macs = [scan.get('mac') for scan in self.new_scan]
        if not self.old_scan:
            added = new_macs
        else:
            old_macs = [scan.get('mac') for scan in self.old_scan]
            for mac in new_macs:
                if mac not in old_macs:
                    added.append(mac)
            for mac in old_macs:
                if mac not in new_macs:
                    removed.append(mac)
        return added, removed
