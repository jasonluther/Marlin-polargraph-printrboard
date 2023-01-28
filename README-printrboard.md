## Fork: MarginallyClever + hardware config

This is a fork of a fork: <https://github.com/MarginallyClever/Marlin-polargraph> is a fork (thank you!) of [Marlin](https://github.com/MarlinFirmware/Marlin) for a hanging V plotter robot like the Marginally Clever Robotics Makelangelo at <https://www.marginallyclever.com/> or Sandy Noble's Polargraph at <https://www.polargraph.co.uk/>. 

This personal fork is to keep track of the configuration for my machine, which is built with a printrboard Rev. D board: <https://reprap.org/wiki/Printrboard>. 

### Hardware

The board, motors, limit switches, and power supply are from an old Printrbot simple wooden kit:
 * [Printrboard rev. D](https://reprap.org/wiki/Printrboard)
 * Kysan 1124090 (old Z axis and extruder motors)
 * [Limit switches](https://www.digikey.com/en/products/detail/omron-electronics-inc-emc-div/SS-01GLP/664737
) wired normally-closed
 * 12V 6A power supply ("Model: LY1206")

Other hardware:
 * [Generic hobby servo](https://www.sparkfun.com/products/9065) labeled "9g A0090"
 * Motor & limit switch mounts
 * Pen gondola
 * Belt/chain, pulleys, counterweights
 * Work surface

### Configuration

Following the instructions at <https://www.marginallyclever.com/2021/10/friday-facts-4-how-to-marlin-polargraph/>, these files were updated:

* Marlin/Configuration.h
* [Marlin/Configuration_adv.h](./Marlin/Configuration_adv.h):
  * Set `G0_FEEDRATE` to `3000` mm/min
  * Update lists of settings as needed because we don't have an extruder
* [pins_PRINTRBOARD.h](./src/pins/teensy2/pins_PRINTRBOARD.h):
  * Attach pen lift `SERVO0_PIN` to microcontroller pin 3, which is EXP1 pin 7. 5V is pin 13, ground is pin 14.
* platformio.ini: set `default_envs` to `at90usb1286_dfu` and `board` to `teensy2pp`