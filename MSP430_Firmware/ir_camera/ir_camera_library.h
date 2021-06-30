/*
 * ir_camera_library.h
 *
 *  Created on: June 29, 2021
 *  @author Dawson Bancroft
 */

#ifndef IR_CAMERA_IR_CAMERA_LIBRARY_H_
#define IR_CAMERA_IR_CAMERA_LIBRARY_H_

#include <msp430.h>
#include <i2c_prot.h>

#define IR_CAMERA_ADDRESS               0x33

// FUNCTION DEFS
void IR_init_0(unsigned char* data);
void IR_init_1(unsigned char* data);
void IR_init_2(unsigned char* data);
void read_IR(unsigned char* data);

#endif /* IR_CAMERA_IR_CAMERA_LIBRARY_H_ */
