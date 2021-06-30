#include <msp430.h>
#include <i2c_prot.h>
#include <ir_camera_library.h>
/*
 * ir_camera_library.c
 *
 *  Created on: June 29, 2021
 *  @author Dawson Bancroft
 */


// 0x0700 : Read RAM Calculation Data
void IR_init_0(unsigned char* data)
{
    int i;
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_WRITE);
    i2c_send_byte(0x07);
    i2c_send_byte(0x00);
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_READ);
    for(i = 0; i < 127; i++)
    {
        data[i] = i2c_receive_byte();
        i2c_send_ack();
    }
    data[127] = i2c_receive_byte();
    i2c_send_nack();
    i2c_stop();
    for(i = 128; i < 1536; i++)
    {
        data[i] = 0;
    }
    __delay_cycles(5000);
}

// 0x2410 : Read EEPROM Calculation Data
void IR_init_1(unsigned char* data)
{
    int i;
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_WRITE);
    i2c_send_byte(0x24);
    i2c_send_byte(0x10);
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_READ);
    for(i = 0; i < 95; i++)
    {
        data[i] = i2c_receive_byte();
        i2c_send_ack();
    }
    data[95] = i2c_receive_byte();
    i2c_send_nack();
    i2c_stop();
    for(i = 96; i < 1536; i++)
    {
        data[i] = 0;
    }
    __delay_cycles(5000);
}

// 0x2440 : Read EEPROM Individual Pixel Calculation Data
void IR_init_2(unsigned char* data)
{
    int i;
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_WRITE);
    i2c_send_byte(0x24);
    i2c_send_byte(0x40);
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_READ);
    for(i = 0; i < 1535; i++)
    {
        data[i] = i2c_receive_byte();
        i2c_send_ack();
    }
    data[1535] = i2c_receive_byte();
    i2c_send_nack();
    i2c_stop();
    __delay_cycles(5000);
}

// 0x0400 : Read RAM for Actual Image Data
void read_IR(unsigned char* data)
{
    int i;
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_WRITE);
    i2c_send_byte(0x04);
    i2c_send_byte(0x00);
    i2c_send_address(IR_CAMERA_ADDRESS, I2C_READ);
    for(i = 0; i < 1535; i++)
    {
        data[i] = i2c_receive_byte();
        i2c_send_ack();
    }
    data[1535] = i2c_receive_byte();
    i2c_send_nack();
    i2c_stop();
    __delay_cycles(5000);
}
