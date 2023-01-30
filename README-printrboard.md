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

Following the instructions at <https://www.marginallyclever.com/2021/10/friday-facts-4-how-to-marlin-polargraph/>, these files were updated. As of this writing, the machine isn't working fully, so things will change. 

* Marlin/Configuration.h
  * Comment out `SHOW_BOOTSCREEN` because we don't have a display
  * Set `MOTHERBOARD` to `BOARD_PRINTRBOARD`
  * Set `POLARGRAPH_MAX_BELT_LEN` to `890.0`, measured from the pulley to the pen when the belt is at its longest (when the limit switches are triggered)
  * In `@section endstops`, set `USE_XMAX_PLUG`, `USE_YMAX_PLUG`, and `USE_ZMAX_PLUG` because our limit switches determine when the gondola is at the maximum X and Y values. Later, set direction of endstops when homing:
    `#define X_HOME_DIR 1`
    `#define Y_HOME_DIR 1`
  * Set `DEFAULT_AXIS_STEPS_PER_UNIT` to `{ 46, 46, 46 }`. It has three values because we don't have an extruder. The actual value is calculated using values from the motor, driver, and pulley.
  * Set `DEFAULT_MAX_FEEDRATE` to `{ 2000, 2000, 2000 }`. Again, use three values because we don't have an extruder, and guess at some reasonable values. 
  * Set `DEFAULT_MAX_ACCELERATION` to `{ 2000, 2000, 2000 }`Again, use three values because we don't have an extruder, and guess at some reasonable values. 
  * Based on my motor and board wiring:
    `#define INVERT_X_DIR false`
    `#define INVERT_Y_DIR true`
  * Printable area:
    `#define X_BED_SIZE 620.0`
    `#define Y_BED_SIZE 760.0`
  * Home position: 
    * Enable `BED_CENTER_AT_0_0`. 
    * Set `MANUAL_X_HOME_POS` to `0`, which puts X=0 centered between the motors. 
    * `MANUAL_Y_HOME_POS` is calculated using the method described at <https://www.marginallyclever.com/2021/10/friday-facts-4-how-to-marlin-polargraph/>, which uses the Pythagorean theorem with a triangle formed by the belt and half of the bed size. That means the pen must be within the bed area in the home position! 
    `#define MANUAL_Y_HOME_POS (Y_MAX_POS-( sqrt(sq(POLARGRAPH_MAX_BELT_LEN)-sq(X_BED_SIZE/2))))`  
    * Note that I've used floating point values in this formula so that I don't have to manually recalculate it if I adjust machine sizes. I haven't checked to see whether it's a performance problem if something is being forced to use floating point math instead of integer math. 
    * With the bed size configured this way, it's easy to move the gondola to bad positions or to send one of the gondola arms into the motor pulley. 
    The value is calculated manually because X_BED_SIZE^2 causes an integer overflow error.
  * Enable `NUM_SERVOS` and set to `1`, enable `DEACTIVATE_SERVOS_AFTER_MOVE`
  * Enable `EEPROM_SETTINGS` to save changes to configuration on the machine
  * Settings related to polar machines generally: 
    * Set `CUSTOM_MACHINE_NAME` to `"Polargraph"`
    * Set `EXTRUDERS` to `0` because we aren't making a 3D printer
    * `#define POLARGRAPH`, which requires that you also `#define CLASSIC_JERK`
    * Set travel limits:
       `#define X_MIN_POS (-X_BED_SIZE/2.0)`
       `#define Y_MIN_POS (-Y_BED_SIZE/2.0)`
       `#define Z_MIN_POS 0`
       `#define X_MAX_POS (X_BED_SIZE/2.0)`
       `#define Y_MAX_POS (Y_BED_SIZE/2.0)`
       `#define Z_MAX_POS 0`
    * Disable `MIN_SOFTWARE_ENDSTOPS`


* [Marlin/Configuration_adv.h](./Marlin/Configuration_adv.h):
  * Set `G0_FEEDRATE` to `3000` mm/min
  * Update lists of settings as needed because we don't have an extruder
* [pins_PRINTRBOARD.h](./src/pins/teensy2/pins_PRINTRBOARD.h):
  * Attach pen lift `SERVO0_PIN` to microcontroller pin 3, which is EXP1 pin 7. 5V is pin 13, ground is pin 14.
* platformio.ini: set `default_envs` to `at90usb1286_dfu` and `board` to `teensy2pp`

### Building the software

Install the PlatformIO extension. To build the firmware, select the PlatformIO icon on the left panel. Under _PROJECT TASKS > Default > General_, click _Build All_. If there are no errors, proceed to load the firmware. 

The firmware should be located in `./.pio/build/at90usb1286_dfu/firmware.hex`. 

### Loading the firmware

The printrboard rev. D requires two pins on the board to be connected together while the board is reset to enter bootloader mode. 

From Ubuntu Linux, you can see when the device is in bootloader mode with `lsusb`:
 * Normal mode: `Bus 003 Device 029: ID 16c0:0483 Van Ooijen Technische Informatica Teensyduino Serial`
 * Bootloader: `Bus 003 Device 030: ID 03eb:2ffb Atmel Corp. at90usb AVR DFU bootloader`

Install the programmer with `sudo apt install dfu-programmer` or `brew install dfu-programmer`.

Upload the firmware (`sudo` is not necessary on Mac OS):
```sh
# sudo dfu-programmer at90usb1286 erase
# sudo dfu-programmer at90usb1286 flash firmware.hex
```

Then remove the jumper and reset the board. It doesn't hurt to completely power cycle the board. 

