# MSP430_SD_Card_and_IR_Camera
On the first version of a working way to pull data from an IR camera connected to an MSP430FR2355 and put that data onto a microSD card.

## Current Things to Change :

1. C Code needs to become its own .c and .h file
2. Python Code needs cleaned
3. Python Needs to be able to take input from user on command line for easier file finding and number of images

## Current Issues : Average temperature printed on images is incorrect

## Notes on setup and use: There should be 4 documents that are 100% necessary to be at least viewed before figuring on how these programs work.

The first one is this text file so good job! This file will have the complete process of how to use the IR camera and all the pinouts.

The secound document is the MSP430FR2355's firmware. This one will give the ability for the MSP to talk to the SD card and the IR camera. The camera is connected via I2C and uses a header written by Cameron Blegen & Larson Brandstetter. The main file was written by Dawson Bancroft and is eventually going to be overlayed on the program that runs on the LOng RAnge radio Device (LoRaD). So as of right now, both the main.c and the I2Cdefs.h are necessary to download.

The next one is the Word documents. This is a short and sweet walkthough of how to convert the information from the microSD card to a txt file. This is convienent for two reasons: 1. Windows OS doesn't like to deal with raw data 2. The size of the file is dramatically increased For this part you will need a Linux computer to run just two commands. It takes about 10 minutes for a 16GB SD card and about 30 - 40 minutes for a 64GB SD card to process. This is just because it is copying all of the information from the microSD to a file. I do recommend deleting the .raw files once you have verified the .txt file looks correct as they take up the size of your SD card.

Finally, the last step is to use the Python script to convert that raw data into images. This was made specifically for the MLX90640 so if you wish to get other data, I recommend just writing your own. It simply reads each line from the input.txt file created earlier and will then calculate the temperature and convert it with a heatmap. Then will put the desired amount of images in the outputImages directory.
