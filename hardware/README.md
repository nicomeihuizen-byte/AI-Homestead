# Hardware

- `wiring/`: pinout and wiring diagrams for the Pico node
- `enclosure/`: radiation shield STL and mounting notes

## Radiation shield

Print in **ASA or PETG, not PLA.** Tested over 90 days outdoors, PLA showed notable strength loss
within 30 days and a sharp decline by 90; ASA showed no visible deformation. Paint it white with
a UV-stable acrylic either way. Source STL: https://www.printables.com/model/73421

Mount the BME280 **inside the shield, on a short I2C tail, separated from the main enclosure**;
keeping it away from the electronics' own waste heat matters as much as the shield does. Keep the
I2C run under ~1 m, or drop to 50 kHz with 2.2 kOhm pull-ups.

## Enclosure

IP66 ABS box **inside** the wooden birdbox. Wood is hygroscopic and will sit at ambient RH
permanently; the birdbox is the decorative rain-and-sun shell, not the seal. The air gap between
the two buffers thermal swings nicely.

Every gland and the ePTFE vent go on the **underside**. Drip loop every cable before it enters.
Indicating desiccant inside, baked out annually. Conformal-coat the boards.

## Panel

60-75 deg from horizontal, due south. Much steeper than the annual optimum (~36 deg): you are
deliberately trading summer surplus for winter capture, and the steep angle sheds snow, leaves
and grime.
