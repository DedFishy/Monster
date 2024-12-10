My documentation for these stupid LEDs

All messages appear to be of length 25

# HEX Addresses
`00`
I believe this is the message type:
00 - Data response
01 - Data request
02 - Set command
`01`
Represents whether the light strip is on or off, 1 for on and 0 for off
`02`
Whether Chroma is disabled or enabled. 01 will use normal control, 00 will allow Razer Chroma to use the lights.
`03 04 05`
These three represent the color in RGB format, 00-FF
`06`
This represents the brightness of the LEDs, up to hex digit 64 or integer value 100 (It's a percentage)
`07`
Represents which Chroma zone is currently active
`The rest`
No clue, it's always set to 41 43 30 30 30 57 30 33 36 32 34 38 36 31 39 00 00