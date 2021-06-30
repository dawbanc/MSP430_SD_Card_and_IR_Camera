/*
 * i2c_prot.h
 *
 *  Created on: June 29, 2021
 *  @author Dawson Bancroft
 */
#ifndef IR_CAMERA_I2C_PROT_H_
#define IR_CAMERA_I2C_PROT_H_

// IF USING DIFFERENT PINS OR A DIFFERENT MICROCONTROLLER CHANGE THE NEXT 6 LINES
#include <msp430.h>

#define I2C_PORT_DIR            P4DIR
#define I2C_PORT_OUT            P4OUT
#define I2C_PORT_IN             P4IN
#define I2C_SDA                 BIT6
#define I2C_SCL                 BIT7
// ANYTHING AFTER THIS SHOULD BE FINE

#define I2C_DELAY               5
#define I2C_WRITE               0
#define I2C_READ                1
#define I2C_SLAVE_ACK           'Y'
#define I2C_SLAVE_NACK          'N'

// FUNCTION DEF
int i2c_init(void);
void i2c_pulse_clock(void);
void i2c_start(void);
void i2c_stop(void);
void i2c_send_ack(void);
void i2c_send_nack(void);
char i2c_receive_ack_or_nack(void);
char i2c_send_byte(char data);
char i2c_receive_byte(void);
void i2c_send_address(char address, int rW);

#endif /* IR_CAMERA_I2C_PROT_H_ */
