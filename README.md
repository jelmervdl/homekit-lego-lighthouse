HomeKit integration for [LEGO Lighthouse 21335-1][(https://www.bricklink.com/v2/catalog/catalogitem.page?S=21335-1)

Requirements:
- [Raspberry Pi A+ form factor](https://www.raspberrypi.com/products/raspberry-pi-3-model-a-plus/)
- [Raspberry PI Build HAT](https://www.raspberrypi.com/products/build-hat/)
- Python 3

Installation:
- Copy over files to Pi, e.g into `~/lighthouse/`
- Install requirements, e.g. `pip install -r requirements.txt`
- Copy systemd config file, e.g. `cd contrib && cp --parents .config/systemd/user/lighthouse.service`
- Enable systemd unit, e.g. `systemctl --user enable lighthouse`
- Start it: `systemctl --user start lighthouse`
- Look up the connect code: `systemctl --user status lighthouse`
- Use that to add it to your HomeKit environment (use the alternative way link once the barcode scanner pops up)
