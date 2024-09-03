# Powerfox-Shelly-Automation

This Python script automates the control of a Shelly smart plug based on energy consumption data retrieved from the Powerfox API. The script ensures that the Shelly device is only turned on when there is sufficient excess energy being generated (over 3000 watts), and turns it off otherwise.

## Prerequisites

- Python 3.x
- [requests](https://pypi.org/project/requests/)
- [ShellyPy](https://github.com/StyraHem/ShellyPy)

You can install the necessary Python packages using:

```bash
pip3 install requests ShellyPy
