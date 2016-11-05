```
    ___    ___    ____  ____
   /   |  /   |  / __ \/ __ \
  / /| | / /| | / /_/ / /_/ /
 / /_| |/ ___ |/ _, _/ ____/
/______/_/  |_/_/ |_/_/      
```

A simple Python utility for detecting changes in devices connected to the local network using arp-scan (short for delta-arp).
Useful for finding out which of your housemates are home

Requirements
----

arp-scan: https://github.com/royhills/arp-scan

Install
----

Clone this repository and cd into it

```bash
git clone https://github.com/derwentx/darp
cd darp/

```

install install/test the python package

```bash
sudo python setup.py install
python test/test_basic.py
```

Play around with the scanner

```bash
python -m arp_scan
```
```python
alerts {'added': ['aa:bb:cc:dd:ee:ff']}
```

Roadmap
----

- [ ] Make alerts a bit fancier with configurable device "owner"
- [ ] Alerts show last seen stamp
