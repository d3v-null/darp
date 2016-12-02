```
    ___    ___    ____  ____
   /   |  /   |  / __ \/ __ \
  / /| | / /| | / /_/ / /_/ /
 / /_| |/ ___ |/ _, _/ ____/
/______/_/  |_/_/ |_/_/      
```

A simple Python utility for detecting changes in devices connected to the local network using arp-scan (short for delta-arp).
Useful for finding out which of your housemates are home
Darp: Enabling musicians with crippling anxiety since 2016

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

Play around with the scanner. if there has been an update, then something like this will print

```bash
python -m darp --set-owners '{"12:34:56:78:9a:bc":"Housemate A"}'
```
```python
 -> added
owner        mac                name      
-----------  -----------------  ----------
Housemate A  12:34:56:78:9a:bc  Apple, Inc
 -> removed
owner        mac                name
------       -----------------  -----------------------------------
Housemate B  bc:12:34:56:78:9a  SAMSUNG ELECTRO-MECHANICS CO., LTD.
-> static
owner        mac                name
------       -----------------  -----------------------------------
Housemate C  9a:bc:12:34:56:78  Azurewave Technologies, Inc.
```

This means that housemate A has recently connected to the network, housemate B has recently left, and housemate C has stayed on the network

Roadmap
----

- [x] Make alerts a bit fancier with configurable device "owner"
- [ ] Alerts show last seen stamp
- [ ] handle duplicates in scan better
- [ ] use nmap to determine hostnames, instead of manufacturer name
