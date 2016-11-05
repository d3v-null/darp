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
alerts {'added': ['5c:0a:5b:97:1e:54', '5c:f9:38:a8:53:ae', 'ec:1a:59:ca:9b:a1', 'd8:50:e6:31:c8:70', 'ec:1a:59:ca:9b:a1']}
```

Roadmap
----

[ ] Make alerts a bit fancier with configurable device "owner"
[ ] Alerts show last seen stamp
