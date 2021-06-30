#include <msp430.h> 
#include "sd_card_raw_library.h"
#include "ir_camera_library.h"

/* ----------------------------------------------------
 * BOREALIS Summer 2021 Internship
 * IR Sensor & microSD Card Example
 * @author Dawson Bancroft
 * ----------------------------------------------------
 * LAST EDIT : June 30th, 2021
 * ----------------------------------------------------
 * FUNCTIONALITY :                      ---------------
 * ----------------------------------------------------
 * This program is an example of how to use the
 * sd_card_raw_library and IR_camera_library. This pro-
 * gram uses an MSP430FR2355 microprocessor by TI. In
 * both protocols (SPI for the SD card and I2C for the
 * camera), the data is bit banged so it can translate
 * nicely to any microprocessor. Please note if using
 * a different microprocessor, pins will likely be dif-
 * ferent as well. Please change the definitions in the
 * sd_card_raw_library.h and the i2c_prot.h header fil-
 * es. For this example, my pin setup is below the
 * "NOTES" section.
 * ----------------------------------------------------
 * NOTES :                              ---------------
 * ----------------------------------------------------
 * On the dependency side of things, the IR_camera
 * files depend on the i2c_prot files. Then main
 * depends on both the IR_camera files and the
 * sd_card_raw_library files.
 *
 * ----------------------------------------------------
 * HARDWARE:                            ---------------
 * ----------------------------------------------------
 * Microprocessor :                     TI MSP430FR2355
 * Camera :                            Melexis MLX90640
 * microSD Card:            SanDisk 64 GB Ultra MicroSD
 *
 * ----------------------------------------------------
 * SETUP :                              ---------------
 * ----------------------------------------------------
 *
 * PIN                  FUNCTION
 * ----------------------------------------------------
 * P1.0 ............... SD Card Chip Select
 * P1.1 ............... SD Card Clock
 * P1.2 ............... SD Card Data In
 * P1.3 ............... SD Card Data Out
 * P1.6 ............... SD Card Detect (unused)
 *
 * P4.6 ............... I2C SDA (IR_Camera)
 * P4.7 ............... I2C SCL (IR_Camera)
 * ----------------------------------------------------
 */

//GLOBALS
//-----------------------------------------------------------------------------------------------------------------
long address_cnt  = 0;                                  // CNT for address of microSD
long address_last = 0;                                  // For error flag
unsigned char image[1536];                              // Our Image from IR

int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	                        // Stop Watchdog Timer

	SPIInit();                                          // Initialize SPI Ports
	i2c_init();                                         // Initialize I2C Ports
	
    PM5CTL0 &= ~LOCKLPM5;                               // Turn on digital I/O

    sdCardInit();                                       // Send Initialization Commands to SD Card

    unsigned char dataIn[6];
    sendCommand(0x50, 0x200, 0xFF, dataIn);             // CMD 16 : Set Block Length

    unsigned long k;
    unsigned char buffer[512];

    address_last = 0;                                   // for first time through
    address_error = 1;                                  // ^^
    while(address_error != 0){
        if(address_error != 0){                         // This is to catch any bad block writing.
                address_cnt = address_last;             // If an addressing error occurs (ie end of sd Card or just a weird error on sd side)
                address_error = 0;                      // It will restart at the last good block it had
        }
        address_last = address_cnt;
        IR_init_0(image);
        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);

        IR_init_1(image);
        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);

        IR_init_2(image);
        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);

        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k + 512];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);


        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k + 1024];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);
    }

    // MAIN
    while(1){

        // RETREIVE DATA & IMAGE FROM IR SENSOR
        if(address_error != 0){
            address_cnt = address_last;
            address_error = 0;
        }
        address_last = address_cnt;

        read_IR(image);
        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);

        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k + 512];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);


        for(k = 0; k < 512; k++)
        {
            buffer[k] = image[k + 1024];
        }
        sendData(address_cnt, buffer);
        address_cnt++;
        __delay_cycles(50000);
        sendCommand(0x4D, 0, 0, dataIn);
        sendCommand(0x4D, 0, 0, dataIn);
        __delay_cycles(50000);
    }

	return 0;
}
