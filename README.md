# razerMambaSuspend
A simple Linux program that locks your computer (or executes any given command) when you dock your Razer Mamba mouse (in it's charging base).

<img src="https://user-images.githubusercontent.com/25673263/34489878-2ecf1a26-efde-11e7-9153-d95760882859.png" data-canonical-src="https://assets.razerzone.com/eeimages/products/22332/razer-mamba-gallery-02.png" width="200" />

You cannot really use a modern computer without a mouse, so why not take advantage of the docking action?

## Requirements
* A linux computer (tested in Ubuntu 17.10 w/ Gnome 3.26, Wayland display server)
* The [openrazer](https://openrazer.github.io/) driver installed.
* A Razer Mamba 2015 mouse (will likely work with other rechargeable razer wireless mice such as the Naga Epic Chroma & Ouroboros). Tested with the Razer Mamba 2015 (16 000 dpi).

This will most likely work in any linux distro with DBUS support. Change the "onChargingCommand" to an appropiate sleep/lock command if your distro doesn't use systemd (or GNOME if locking instead of suspending).

## Usage
1. Clone/download this program: `git clone http://github.com/rgon/razerMambaSuspend/` and change to it's directory `cd razerMambaSuspend`.
2. Let the program know your mouse's Serial Number and [set it](#configuration) in the `config.json` file.
3. Make the script executable `chmod +x main.py`.
4. Finally, just execute the script `./main.py`.

## Automatically running the script at startup
To be done.

## Configuration
All user-modifiable parameters are stored in the `config.json` file that must be located in the program's root directory.
The "deviceSerial" variable should be filled with your mouse's serial number.
```json
{
    "deviceSerial": "PM1**********26",

    "onChargingCommand": "systemctl sleep",
    "chargingScanInterval": 1
}
```
If you want to lock your computer when docking your mose, modify the "onChargingCommand" line as follows (only for GNOME-based DEs):
```json
    "onChargingCommand": "gnome-screensaver-command -l",
```
The "chargingScanInterval" decides how often the program will check if the mouse is charging. The default value is 1s.
