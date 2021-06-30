# MSP430_SD_Card_and_IR_Camera
On the first version of a working way to pull data from an IR camera connected to an MSP430FR2355 and put that data onto a microSD card.

### Current Things to Change :

1. ~~C Code needs to become its own .c and .h file~~
2. Python Code needs cleaned
3. Python needs to be able to take input from user on command line for easier file finding and number of images
4. Bash script to automate the SD card to raw to text file process
5. Add the Card Detect pin for redundancy

### Current Issues : 
1. Average temperature printed on images is incorrect

### Notes on setup and use: There should be 4 documents that are 100% necessary to be at least viewed before figuring on how these programs work.

The first one is this text file so good job! This file will have the complete process of how to use the IR camera and all the pinouts.

The secound document is the MSP430FR2355's firmware. This one will give the ability for the MSP to talk to the SD card and the IR camera. The camera is connected via I2C. The microSD card is connected via SPI. If using the TI MSP430FR2355, the pin setup is as follows and can also be found in the main.c file of the MSP430 firmware folder. Do note that the Card Detect is not currently used as it is not necessary in normal operation. However, it can be added as an input (and might in later versions) in the main.c file.
##### MSP430FR2355 Pin Diagram
 PIN                  FUNCTION
 ----------------------------------------------------
 P1.0 ............... SD Card Chip Select
 P1.1 ............... SD Card Clock
 P1.2 ............... SD Card Data In
 P1.3 ............... SD Card Data Out
 P1.6 ............... SD Card Detect (unused)
 
 P4.6 ............... I2C SDA (IR_Camera)
 P4.7 ............... I2C SCL (IR_Camera)

The next one is the Word documents. This is a short and sweet walkthough of how to convert the information from the microSD card to a txt file. This is convienent for two reasons: 1. Windows OS doesn't like to deal with raw data 2. The size of the file is dramatically increased For this part you will need a Linux computer to run just two commands. It takes about 10 minutes for a 16GB SD card and about 30 - 40 minutes for a 64GB SD card to process. This is just because it is copying all of the information from the microSD to a file. I do recommend deleting the .raw files once you have verified the .txt file looks correct as they take up the size of your SD card. A bash script is in process to replace this process.

Finally, the last step is to use the Python script to convert that raw data into images. This was made specifically for the MLX90640 so if you wish to get other data, I recommend just writing your own. It simply reads each line from the input.txt file created earlier and will then calculate the temperature then converts it to an image with a heatmap. Then will put the desired amount of images in the outputImages directory.
