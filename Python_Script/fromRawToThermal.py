import sys

import numpy as np
import matplotlib.cm as cm
from PIL import Image
from PIL import ImageDraw

# FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------


def file_check(filename):
    try:
        open(filename, "r")
        return 1
    except IOError:
        print("Error: File not found")
        return 0


def convert_hex_to_binary(value):
    if value == '0':
        return 0b0000
    elif value == '1':
        return 0b0001
    elif value == '2':
        return 0b0010
    elif value == '3':
        return 0b0011
    elif value == '4':
        return 0b0100
    elif value == '5':
        return 0b0101
    elif value == '6':
        return 0b0110
    elif value == '7':
        return 0b0111
    elif value == '8':
        return 0b1000
    elif value == '9':
        return 0b1001
    elif value == 'a':
        return 0b1010
    elif value == 'b':
        return 0b1011
    elif value == 'c':
        return 0b1100
    elif value == 'd':
        return 0b1101
    elif value == 'e':
        return 0b1110
    elif value == 'f':
        return 0b1111
    else:
        return "error"


def convert_line_to_binary(first, second, third, fourth):
    new = (convert_hex_to_binary(first) << 12) + (convert_hex_to_binary(second) << 8)
    new += (convert_hex_to_binary(third) << 4) + (convert_hex_to_binary(fourth))
    return new


def convert_to_twos_comp(binary, length):   # takes length in bits
    tc = (-1) * ((2 ** length) - binary)
    return tc


def cftc(tc, length):     # takes length in bits
    num = (-1) * ((2 ** length) + tc)
    return num


def even_or_odd(num):
    if (num % 2) == 0:
        return "even"
    else:
        return "odd"


# MAIN
# ----------------------------------------------------------------------------------------------------------------------
if len(sys.argv) == 2:
    capacity = sys.argv[1]
else:
    capacity = 16                   # capacity default value
numBytes = capacity * 1000000000
numLines = numBytes/32

num_pics = 10       # number of pictures you want
im_scalar = 10      # uses PIL's built-in interpolation

OCC_row = np.zeros(24)
OCC_col = np.zeros(32)
ACC_row = np.zeros(24)
ACC_col = np.zeros(32)

offset_pixel = np.zeros((24, 32))
alpha_pixel = np.zeros((24, 32))
kta_pixel = np.zeros((24, 32))
outlier_pixel = np.zeros((24, 32))

P_OCC_row = np.zeros(24)
P_OCC_col = np.zeros(32)
P_ACC_row = np.zeros(24)
P_ACC_col = np.zeros(32)

P_offset_pixel = np.zeros((24, 32))
P_alpha_pixel = np.zeros((24, 32))
P_kta_pixel = np.zeros((24, 32))
P_outlier_pixel = np.zeros((24, 32))

fileThere = file_check("input.txt")  # open file
if fileThere:
    inp = open("input.txt", "r")
    # out = open("hexOut.txt", "w")

    # VALUES IN IR 0x0700
    line = inp.readline()
    P_Ta_Vbe = (convert_line_to_binary(line[10], line[11], line[13], line[14]))

    line = inp.readline()
    P_cp_subpage0 = (convert_line_to_binary(line[10], line[11], line[13], line[14]))
    P_gain_700 = (convert_line_to_binary(line[22], line[23], line[25], line[26]))

    line = inp.readline()  # excess data
    line = inp.readline()

    line = inp.readline()
    P_Ta_PTAT = (convert_line_to_binary(line[10], line[11], line[13], line[14]))

    line = inp.readline()
    P_cp_subpage1 = (convert_line_to_binary(line[10], line[11], line[13], line[14]))
    P_VDDpix = (convert_line_to_binary(line[22], line[23], line[25], line[26]))

    line = inp.readline()  # excess data
    line = inp.readline()

    line = inp.readline()  # zeros
    line = inp.readline()  # *

    # VALUES IN IR 0x2410
    line = inp.readline()  # first line

    P_alphaPTAT = (convert_hex_to_binary(line[10]))
    P_scale_OCC_row = (convert_hex_to_binary(line[11]))
    P_scale_OCC_col = (convert_hex_to_binary(line[13]))
    P_scale_OCC_rem = (convert_hex_to_binary(line[14]))
    P_pix_os_average = (convert_hex_to_binary(line[16]) << 12) + (convert_hex_to_binary(line[17]) << 8)
    P_pix_os_average += (convert_hex_to_binary(line[19]) << 4) + (convert_hex_to_binary(line[20]))
    P_OCC_row[3] = (convert_hex_to_binary(line[22]))
    P_OCC_row[2] = (convert_hex_to_binary(line[23]))
    P_OCC_row[1] = (convert_hex_to_binary(line[25]))
    P_OCC_row[0] = (convert_hex_to_binary(line[26]))
    P_OCC_row[7] = (convert_hex_to_binary(line[28]))
    P_OCC_row[6] = (convert_hex_to_binary(line[29]))
    P_OCC_row[5] = (convert_hex_to_binary(line[31]))
    P_OCC_row[4] = (convert_hex_to_binary(line[32]))

    P_OCC_row[11] = (convert_hex_to_binary(line[35]))
    P_OCC_row[10] = (convert_hex_to_binary(line[36]))
    P_OCC_row[9] = (convert_hex_to_binary(line[38]))
    P_OCC_row[8] = (convert_hex_to_binary(line[39]))
    P_OCC_row[15] = (convert_hex_to_binary(line[41]))
    P_OCC_row[14] = (convert_hex_to_binary(line[42]))
    P_OCC_row[13] = (convert_hex_to_binary(line[44]))
    P_OCC_row[12] = (convert_hex_to_binary(line[45]))

    P_OCC_row[19] = (convert_hex_to_binary(line[47]))
    P_OCC_row[18] = (convert_hex_to_binary(line[48]))
    P_OCC_row[17] = (convert_hex_to_binary(line[50]))
    P_OCC_row[16] = (convert_hex_to_binary(line[51]))
    P_OCC_row[23] = (convert_hex_to_binary(line[53]))
    P_OCC_row[22] = (convert_hex_to_binary(line[54]))
    P_OCC_row[21] = (convert_hex_to_binary(line[56]))
    P_OCC_row[20] = (convert_hex_to_binary(line[57]))

    line = inp.readline()  # second line

    P_OCC_col[3] = (convert_hex_to_binary(line[10]))
    P_OCC_col[2] = (convert_hex_to_binary(line[11]))
    P_OCC_col[1] = (convert_hex_to_binary(line[13]))
    P_OCC_col[0] = (convert_hex_to_binary(line[14]))
    P_OCC_col[7] = (convert_hex_to_binary(line[16]))
    P_OCC_col[6] = (convert_hex_to_binary(line[17]))
    P_OCC_col[5] = (convert_hex_to_binary(line[19]))
    P_OCC_col[4] = (convert_hex_to_binary(line[20]))

    P_OCC_col[11] = (convert_hex_to_binary(line[22]))
    P_OCC_col[10] = (convert_hex_to_binary(line[23]))
    P_OCC_col[9] = (convert_hex_to_binary(line[25]))
    P_OCC_col[8] = (convert_hex_to_binary(line[26]))
    P_OCC_col[15] = (convert_hex_to_binary(line[28]))
    P_OCC_col[14] = (convert_hex_to_binary(line[29]))
    P_OCC_col[13] = (convert_hex_to_binary(line[31]))
    P_OCC_col[12] = (convert_hex_to_binary(line[32]))

    P_OCC_col[19] = (convert_hex_to_binary(line[35]))
    P_OCC_col[18] = (convert_hex_to_binary(line[36]))
    P_OCC_col[17] = (convert_hex_to_binary(line[38]))
    P_OCC_col[16] = (convert_hex_to_binary(line[39]))
    P_OCC_col[23] = (convert_hex_to_binary(line[41]))
    P_OCC_col[22] = (convert_hex_to_binary(line[42]))
    P_OCC_col[21] = (convert_hex_to_binary(line[44]))
    P_OCC_col[20] = (convert_hex_to_binary(line[45]))

    P_OCC_col[27] = (convert_hex_to_binary(line[47]))
    P_OCC_col[26] = (convert_hex_to_binary(line[48]))
    P_OCC_col[25] = (convert_hex_to_binary(line[50]))
    P_OCC_col[24] = (convert_hex_to_binary(line[51]))
    P_OCC_col[31] = (convert_hex_to_binary(line[53]))
    P_OCC_col[30] = (convert_hex_to_binary(line[54]))
    P_OCC_col[29] = (convert_hex_to_binary(line[56]))
    P_OCC_col[28] = (convert_hex_to_binary(line[57]))

    line = inp.readline()  # third line

    P_alphaScale = (convert_hex_to_binary(line[10]))
    P_scale_ACC_row = (convert_hex_to_binary(line[11]))
    P_scale_ACC_col = (convert_hex_to_binary(line[13]))
    P_scale_ACC_rem = (convert_hex_to_binary(line[14]))
    P_pix_sens_average = (convert_hex_to_binary(line[16]) << 12) + (convert_hex_to_binary(line[17]) << 8)
    P_pix_sens_average += (convert_hex_to_binary(line[19]) << 4) + (convert_hex_to_binary(line[20]))
    P_ACC_row[3] = (convert_hex_to_binary(line[22]))
    P_ACC_row[2] = (convert_hex_to_binary(line[23]))
    P_ACC_row[1] = (convert_hex_to_binary(line[25]))
    P_ACC_row[0] = (convert_hex_to_binary(line[26]))
    P_ACC_row[7] = (convert_hex_to_binary(line[28]))
    P_ACC_row[6] = (convert_hex_to_binary(line[29]))
    P_ACC_row[5] = (convert_hex_to_binary(line[31]))
    P_ACC_row[4] = (convert_hex_to_binary(line[32]))

    P_ACC_row[11] = (convert_hex_to_binary(line[35]))
    P_ACC_row[10] = (convert_hex_to_binary(line[36]))
    P_ACC_row[9] = (convert_hex_to_binary(line[38]))
    P_ACC_row[8] = (convert_hex_to_binary(line[39]))
    P_ACC_row[15] = (convert_hex_to_binary(line[41]))
    P_ACC_row[14] = (convert_hex_to_binary(line[42]))
    P_ACC_row[13] = (convert_hex_to_binary(line[44]))
    P_ACC_row[12] = (convert_hex_to_binary(line[45]))

    P_ACC_row[19] = (convert_hex_to_binary(line[47]))
    P_ACC_row[18] = (convert_hex_to_binary(line[48]))
    P_ACC_row[17] = (convert_hex_to_binary(line[50]))
    P_ACC_row[16] = (convert_hex_to_binary(line[51]))
    P_ACC_row[23] = (convert_hex_to_binary(line[53]))
    P_ACC_row[22] = (convert_hex_to_binary(line[54]))
    P_ACC_row[21] = (convert_hex_to_binary(line[56]))
    P_ACC_row[20] = (convert_hex_to_binary(line[57]))

    line = inp.readline()  # fourth line

    P_ACC_col[3] = (convert_hex_to_binary(line[10]))
    P_ACC_col[2] = (convert_hex_to_binary(line[11]))
    P_ACC_col[1] = (convert_hex_to_binary(line[13]))
    P_ACC_col[0] = (convert_hex_to_binary(line[14]))
    P_ACC_col[7] = (convert_hex_to_binary(line[16]))
    P_ACC_col[6] = (convert_hex_to_binary(line[17]))
    P_ACC_col[5] = (convert_hex_to_binary(line[19]))
    P_ACC_col[4] = (convert_hex_to_binary(line[20]))

    P_ACC_col[11] = (convert_hex_to_binary(line[22]))
    P_ACC_col[10] = (convert_hex_to_binary(line[23]))
    P_ACC_col[9] = (convert_hex_to_binary(line[25]))
    P_ACC_col[8] = (convert_hex_to_binary(line[26]))
    P_ACC_col[15] = (convert_hex_to_binary(line[28]))
    P_ACC_col[14] = (convert_hex_to_binary(line[29]))
    P_ACC_col[13] = (convert_hex_to_binary(line[31]))
    P_ACC_col[12] = (convert_hex_to_binary(line[32]))

    P_ACC_col[19] = (convert_hex_to_binary(line[35]))
    P_ACC_col[18] = (convert_hex_to_binary(line[36]))
    P_ACC_col[17] = (convert_hex_to_binary(line[38]))
    P_ACC_col[16] = (convert_hex_to_binary(line[39]))
    P_ACC_col[23] = (convert_hex_to_binary(line[41]))
    P_ACC_col[22] = (convert_hex_to_binary(line[42]))
    P_ACC_col[21] = (convert_hex_to_binary(line[44]))
    P_ACC_col[20] = (convert_hex_to_binary(line[45]))

    P_ACC_col[27] = (convert_hex_to_binary(line[47]))
    P_ACC_col[26] = (convert_hex_to_binary(line[48]))
    P_ACC_col[25] = (convert_hex_to_binary(line[50]))
    P_ACC_col[24] = (convert_hex_to_binary(line[51]))
    P_ACC_col[31] = (convert_hex_to_binary(line[53]))
    P_ACC_col[30] = (convert_hex_to_binary(line[54]))
    P_ACC_col[29] = (convert_hex_to_binary(line[56]))
    P_ACC_col[28] = (convert_hex_to_binary(line[57]))

    line = inp.readline()  # fifth line

    P_gain = (convert_hex_to_binary(line[10]) << 12) + (convert_hex_to_binary(line[11]) << 8)
    P_gain += (convert_hex_to_binary(line[13]) << 4) + (convert_hex_to_binary(line[14]))
    P_ptat_25 = (convert_hex_to_binary(line[16]) << 12) + (convert_hex_to_binary(line[17]) << 8)
    P_ptat_25 += (convert_hex_to_binary(line[19]) << 4) + (convert_hex_to_binary(line[20]))
    whole_line = convert_line_to_binary(line[22], line[23], line[25], line[26])
    P_kv_ptat = (((whole_line & 0b1111110000000000) << 10))
    P_kt_ptat = ((whole_line & 0b1111111111))
    P_kv_vdd = (convert_hex_to_binary(line[28]) << 8) + (convert_hex_to_binary(line[29]))
    P_vdd_25 = (convert_hex_to_binary(line[31]) << 8) + (convert_hex_to_binary(line[32]))
    P_kv_avg_odd_row_odd_col = (convert_hex_to_binary(line[35]))
    P_kv_avg_eve_row_odd_col = (convert_hex_to_binary(line[36]))
    P_kv_avg_odd_row_eve_col = (convert_hex_to_binary(line[38]))
    P_kv_avg_eve_row_eve_col = (convert_hex_to_binary(line[39]))
    whole_line = convert_line_to_binary(line[41], line[42], line[44], line[45])
    P_IL_Chess_C3 = ((whole_line & 0b1111100000000000) >> 11)
    P_IL_Chess_C2 = ((whole_line & 0b11111000000) >> 6)
    P_IL_Chess_C1 = ((whole_line & 0b111111))
    P_kta_avg_odd_row_odd_col = ((convert_hex_to_binary(line[47]) << 4) + (convert_hex_to_binary(line[48])))
    P_kta_avg_eve_row_odd_col = ((convert_hex_to_binary(line[50]) << 4) + (convert_hex_to_binary(line[51])))
    P_kta_avg_odd_row_eve_col = ((convert_hex_to_binary(line[53]) << 4) + (convert_hex_to_binary(line[54])))
    P_kta_avg_eve_row_eve_col = ((convert_hex_to_binary(line[56]) << 4) + (convert_hex_to_binary(line[57])))

    line = inp.readline()  # sixth line

    whole_line = convert_line_to_binary(line[10], line[11], line[13], line[14])
    P_res_control_calib = ((whole_line & 0b11000000000000) >> 12)
    P_kv_scale = ((whole_line & 0b111100000000) >> 8)
    P_kta_scale_1 = ((whole_line & 0b11110000) >> 4)
    P_kta_scale_2 = ((whole_line & 0b1111))
    whole_line = convert_line_to_binary(line[16], line[17], line[19], line[20])
    P_alpha_CP_subpage1_div_CP_subpage0_2tothe7 = ((whole_line & 0b1111110000000000) << 10)
    P_alpha_CP_subpage0 = ((whole_line & 0b1111111111))
    whole_line = convert_line_to_binary(line[22], line[23], line[25], line[26])
    P_offset_CP_subpage1_sub_CP_subpage0 = ((whole_line & 0b1111110000000000) << 10)
    P_offset_CP_subpage0 = ((whole_line & 0b1111111111))
    P_kv_CP = ((convert_hex_to_binary(line[28]) << 4) + (convert_hex_to_binary(line[29])))
    P_kta_CP = ((convert_hex_to_binary(line[31]) << 4) + (convert_hex_to_binary(line[32])))
    P_ksta_2tothe13 = ((convert_hex_to_binary(line[35]) << 4) + (convert_hex_to_binary(line[36])))
    P_TGC_plusOminus4 = ((convert_hex_to_binary(line[38]) << 4) + (convert_hex_to_binary(line[39])))
    P_Ks_to_range_2 = ((convert_hex_to_binary(line[41]) << 4) + (convert_hex_to_binary(line[42])))
    P_Ks_to_range_1 = ((convert_hex_to_binary(line[44]) << 4) + (convert_hex_to_binary(line[45])))
    P_Ks_to_range_4 = ((convert_hex_to_binary(line[47]) << 4) + (convert_hex_to_binary(line[48])))
    P_Ks_to_range_3 = ((convert_hex_to_binary(line[50]) << 4) + (convert_hex_to_binary(line[51])))
    P_temp_step = (convert_hex_to_binary(line[53]) & 0b0011)
    P_CT4 = (convert_hex_to_binary(line[54]))
    P_CT3 = (convert_hex_to_binary(line[56]))
    P_KsTo_Scale_offset = (convert_hex_to_binary(line[57]))

    line = inp.readline()  # zeros
    line = inp.readline()  # *
    if line[0] != "*":
        print("PARSING ERROR")

    # DATA FOR IMAGE CALCULATION
    # VALUES IN IR 0x2440
    for row in range(24):
        for col in range(4):
            line = inp.readline()
            whole_line = convert_line_to_binary(line[10], line[11], line[13], line[14])
            P_offset_pixel[row, 0 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 0 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 0 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 0 + (col * 8)] = (whole_line & 0b0001)

            whole_line = convert_line_to_binary(line[16], line[17], line[19], line[20])
            P_offset_pixel[row, 1 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 1 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 1 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 1 + (col * 8)] = (whole_line & 0b0001)

            whole_line = convert_line_to_binary(line[22], line[23], line[25], line[26])
            P_offset_pixel[row, 2 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 2 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 2 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 2 + (col * 8)] = (whole_line & 0b0001)

            whole_line = convert_line_to_binary(line[28], line[29], line[31], line[32])
            P_offset_pixel[row, 3 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 3 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 3 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 3 + (col * 8)] = (whole_line & 0b0001)

            whole_line = convert_line_to_binary(line[35], line[36], line[38], line[39])
            P_offset_pixel[row, 4 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 4 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 4 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 4 + (col * 8)] = (whole_line & 0b0001)

            whole_line = convert_line_to_binary(line[41], line[42], line[44], line[45])
            P_offset_pixel[row, 5 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 5 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 5 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 5 + (col * 8)] = (whole_line & 0b0001)

            whole_line = convert_line_to_binary(line[47], line[48], line[50], line[51])
            P_offset_pixel[row, 6 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 6 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 6 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 6 + (col * 8)] = (whole_line & 0b0001)

            whole_line = convert_line_to_binary(line[53], line[54], line[56], line[57])
            P_offset_pixel[row, 7 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
            P_alpha_pixel[row, 7 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
            P_kta_pixel[row, 7 + (col * 8)] = ((whole_line & 0b1110) >> 1)
            P_outlier_pixel[row, 7 + (col * 8)] = (whole_line & 0b0001)

    for i in range(num_pics):

        avg = 0

        Ta_Vbe = P_Ta_Vbe
        cp_subpage0 = P_cp_subpage0
        Ta_PTAT = P_Ta_PTAT
        cp_subpage1 = P_cp_subpage1

        ir_image = np.zeros((24, 32))
        pix_gain = np.zeros((24, 32))
        pix_os_ref = np.zeros((24, 32))
        kv_ij = np.zeros((24, 32))
        kta_ij = np.zeros((24, 32))
        pix_os = np.zeros((24, 32))
        alpha_comp_ij = np.zeros((24, 32))
        alpha_ij = np.zeros((24, 32))
        Sx = np.zeros((24, 32))
        To = np.zeros((24, 32))
        To_ext = np.zeros((24, 32))

        offset_pixel = np.copy(P_offset_pixel)
        alpha_pixel = np.copy(P_alpha_pixel)
        kta_pixel = np.copy(P_kta_pixel)
        outlier_pixel = np.copy(P_outlier_pixel)

        OCC_row = np.copy(P_OCC_row)
        OCC_col = np.copy(P_OCC_col)
        ACC_row = np.copy(P_ACC_row)
        ACC_col = np.copy(P_ACC_col)

        kv_vdd = P_kv_vdd
        vdd_25 = P_vdd_25
        VDDpix = P_VDDpix
        kv_ptat = P_kv_ptat
        kt_ptat = P_kt_ptat
        ptat_25 = P_ptat_25
        Ta_PTAT = P_Ta_PTAT
        Ta_Vbe = P_Ta_Vbe
        alphaPTAT = P_alphaPTAT
        alphaScale = P_alphaScale
        gain = P_gain
        gain_700 = P_gain_700
        scale_OCC_row = P_scale_OCC_row
        scale_OCC_col = P_scale_OCC_col
        scale_OCC_rem = P_scale_OCC_rem
        scale_ACC_row = P_scale_ACC_row
        scale_ACC_col = P_scale_ACC_col
        scale_ACC_rem = P_scale_ACC_rem
        kv_avg_eve_row_eve_col = P_kv_avg_eve_row_eve_col
        kv_avg_eve_row_odd_col = P_kv_avg_eve_row_odd_col
        kv_avg_odd_row_eve_col = P_kv_avg_odd_row_eve_col
        kv_avg_odd_row_odd_col = P_kv_avg_odd_row_odd_col
        kta_avg_eve_row_eve_col = P_kta_avg_eve_row_eve_col
        kta_avg_eve_row_odd_col = P_kta_avg_eve_row_odd_col
        kta_avg_odd_row_eve_col = P_kta_avg_odd_row_eve_col
        kta_avg_odd_row_odd_col = P_kta_avg_odd_row_odd_col
        kv_scale = P_kv_scale
        kta_scale_1 = P_kta_scale_1
        kta_scale_2 = P_kta_scale_2
        pix_os_average = P_pix_os_average
        pix_sens_average = P_pix_sens_average

        res_control_calib = P_res_control_calib
        alpha_CP_subpage1_div_CP_subpage0_2tothe7 = P_alpha_CP_subpage1_div_CP_subpage0_2tothe7
        alpha_CP_subpage0 = P_alpha_CP_subpage0
        offset_CP_subpage1_sub_CP_subpage0 = P_offset_CP_subpage1_sub_CP_subpage0
        offset_CP_subpage0 = P_offset_CP_subpage0
        kv_CP = P_kv_CP
        kta_CP = P_kta_CP
        ksta_2tothe13 = P_ksta_2tothe13
        TGC_plusOminus4 = P_TGC_plusOminus4
        Ks_to_range_2 = P_Ks_to_range_2
        Ks_to_range_1 = P_Ks_to_range_1
        Ks_to_range_4 = P_Ks_to_range_4
        Ks_to_range_3 = P_Ks_to_range_3
        temp_step = P_temp_step
        CT4 = P_CT4
        CT3 = P_CT3
        KsTo_Scale_offset = P_KsTo_Scale_offset

        # ACTUAL IMAGE DATA
        # VALUES IN IR 0x0400
        for row in range(24):
            for col in range(4):
                line = inp.readline()

                whole_line = convert_line_to_binary(line[10], line[11], line[13], line[14])
                ir_image[row, 0 + (8 * col)] = whole_line

                whole_line = convert_line_to_binary(line[16], line[17], line[19], line[20])
                ir_image[row, 1 + (8 * col)] = whole_line

                whole_line = convert_line_to_binary(line[22], line[23], line[25], line[26])
                ir_image[row, 2 + (8 * col)] = whole_line

                whole_line = convert_line_to_binary(line[28], line[29], line[31], line[32])
                ir_image[row, 3 + (8 * col)] = whole_line

                whole_line = convert_line_to_binary(line[35], line[36], line[38], line[39])
                ir_image[row, 4 + (8 * col)] = whole_line

                whole_line = convert_line_to_binary(line[41], line[42], line[44], line[45])
                ir_image[row, 5 + (8 * col)] = whole_line

                whole_line = convert_line_to_binary(line[47], line[48], line[50], line[51])
                ir_image[row, 6 + (8 * col)] = whole_line

                whole_line = convert_line_to_binary(line[53], line[54], line[56], line[57])
                ir_image[row, 7 + (8 * col)] = whole_line

        # CALCULATIONS

        #   11.2.2.2 Supply Voltage Value Calc (cfap)
        if kv_vdd > 127:
            kv_vdd = kv_vdd - 256
        kv_vdd = kv_vdd * (2 ** 5)
        vdd_25 = (vdd_25 - 256) * (2 ** 5) - (2 ** 13)
        #       VDD calc
        if VDDpix > 32767:
            VDDpix = VDDpix - 65536
        vdd = ((1 + VDDpix - (vdd_25))/kv_vdd) + 3.3

        #   11.2.2.3 Ambient Temperature Calc (cfap)
        if kv_ptat > 31:
            kv_ptat = kv_ptat - 64
        kv_ptat = kv_ptat/(2 ** 12)

        if kt_ptat > 511:
            kt_ptat = kt_ptat - 1024
        kt_ptat = kt_ptat/(2 ** 3)

        deltaV = (VDDpix - vdd_25) / kv_vdd

        if ptat_25 > 32767:
            ptat_25 = ptat_25 - 65536

        if Ta_PTAT > 32767:
            Ta_PTAT = Ta_PTAT - 65536

        if Ta_Vbe > 32767:
            Ta_Vbe = Ta_Vbe - 65536

        alphaPTAT = (alphaPTAT/(2 ** 2)) + 8

        V_ptat_art = (Ta_PTAT/(Ta_PTAT + alphaPTAT + Ta_Vbe)) * (2 ** 18)

        Ta = (((V_ptat_art/(1 + (kv_ptat * deltaV))) - ptat_25) / kt_ptat) + 25

        for row in range(24):
            for col in range(32):
                row_spec = even_or_odd(row)
                col_spec = even_or_odd(col)

                # 11.2.2.4 Gain Parameter Calculation (cfap)
                if gain > 32767:
                    gain = gain - 65536

                if gain_700 > 32767:
                    gain_700 = gain_700 - 65536

                k_gain = gain / gain_700

                # 11.2.2.5.1 Gain Compensation
                if ir_image[row, col] > 32767:
                    ir_image[row, col] = ir_image[row, col] - 65536
                pix_gain[row, col] = ir_image[row, col] * k_gain

                # 11.2.2.5.2 Offset Calculation
                if pix_os_average > 32767:
                    pix_os_average = pix_os_average - 65536

                if OCC_row[row] > 7:
                    OCC_row[row] = OCC_row[row] - 16

                if OCC_col[col] > 7:
                    OCC_col[col] = OCC_col[col] - 16

                if offset_pixel[row, col] > 31:
                    offset_pixel[row, col] = offset_pixel[row, col] - 64

                pix_os_ref[row, col] = pix_os_average + (OCC_row[row] * (2 ** scale_OCC_row))
                pix_os_ref[row, col] += (OCC_col[col] * (2 ** scale_OCC_col))
                pix_os_ref[row, col] += (offset_pixel[row, col] * (2 ** scale_OCC_rem))

                # 11.2.2.5.3 IR Data Compensation
                if kta_pixel[row, col] > 3:
                    kta_pixel[row, col] = kta_pixel[row, col] - 8

                if row_spec == "even":
                    if col_spec == "even":
                        kv = kv_avg_eve_row_eve_col
                        kta = kta_avg_eve_row_eve_col
                    else:
                        kv = kv_avg_eve_row_odd_col
                        kta = kta_avg_eve_row_odd_col
                else:
                    if col_spec == "even":
                        kv = kv_avg_odd_row_eve_col
                        kta = kta_avg_odd_row_eve_col
                    else:
                        kv = kv_avg_odd_row_odd_col
                        kta = kta_avg_odd_row_odd_col

                if kv > 7:
                    kv = kv - 8

                if kta > 127:
                    kta = kta - 256

                kta_ij[row, col] = (kta + (kta_pixel[row, col] / 2) * (2 ** kta_scale_2)) / (2 ** (kta_scale_1 + 8))

                kv_ij[row, col] = kv / (2 ** kv_scale)

                Inside = pix_os_ref[row, col] * (1 + kta_ij[row, col] * (Ta - 25))
                Inside = Inside * (1 + kv_ij[row, col] * (vdd - 3.3))
                pix_os[row, col] = pix_gain[row, col] - Inside

                # 11.2.2.5.4 IR Data Emissivity Compensation
                E = 1  # EMISSIVITY COEFFICIENT
                V_ir_E_comp = pix_os[row, col] / E

                # 11.2.2.6.1 Compensating the GAIN of CP Pixel
                if cp_subpage0 > 32767:
                    cp_subpage0 = cp_subpage0 - 65536

                pix_gain_cp_SP0 = k_gain * cp_subpage0

                if cp_subpage1 > 32767:
                    cp_subpage1 = cp_subpage1 - 65536

                pix_gain_cp_SP1 = k_gain * cp_subpage1

                # 11.2.2.6.2 Compensating Offset, Ta, and Vdd of CP Pixel
                if offset_CP_subpage0 > 511:
                    offset_CP_subpage0 = offset_CP_subpage0 - 1024

                Off_CP_SP0 = offset_CP_subpage0

                if offset_CP_subpage1_sub_CP_subpage0 > 31:
                    offset_CP_subpage1_sub_CP_subpage0 = offset_CP_subpage1_sub_CP_subpage0 - 64

                Off_CP_SP1 = Off_CP_SP0 + offset_CP_subpage1_sub_CP_subpage0

                if kta_CP > 127:
                    kta_CP -= 256

                K_TA_CP = kta_CP / (2 ** (kta_scale_1 + 8))

                if kv_CP > 127:
                    kv_CP -= 256

                K_V_CP = kv_CP / (2 ** kv_scale)

                pix_os_CP_SP0 = pix_gain_cp_SP0 - Off_CP_SP0 * (1 + K_TA_CP * (Ta - 25)) * (1 + K_V_CP * (vdd - 3.3))
                pix_os_CP_SP1 = pix_gain_cp_SP1 - Off_CP_SP1 * (1 + K_TA_CP * (Ta - 25)) * (1 + K_V_CP * (vdd - 3.3))

                # 11.2.2.7 IR Data Gradient Compensation
                pix_num = (row * 32) + col

                Pattern = (int((pix_num - 1) / 32) - int((int(pix_num - 1) / 32) / 2) * 2)
                Pattern = Pattern ^ ((pix_num - 1) - int((pix_num - 1) / 2) * 2)

                if TGC_plusOminus4 > 127:
                    TGC_plusOminus4 -= 256

                TGC = TGC_plusOminus4 / (2 ** 5)

                V_ir_comp = V_ir_E_comp - TGC * ((1 - Pattern) * pix_os_CP_SP0 + Pattern * pix_os_CP_SP1)

                # 11.2.2.8 Normalizing to Sensitivity
                alphaCP_subpage0 = alpha_CP_subpage0 / (2 ** (alphaScale + 27))

                CP_P1_P0_ratio = alpha_CP_subpage1_div_CP_subpage0_2tothe7
                if CP_P1_P0_ratio > 31:
                    CP_P1_P0_ratio -= 64

                alphaCP_subpage1 = alphaCP_subpage0 * (1 + (CP_P1_P0_ratio / (2 ** 7)))

                k_sTa = ksta_2tothe13

                if k_sTa > 127:
                    k_sTa -= 256

                if ACC_row[row] > 7:
                    ACC_row[row] -= 16

                if ACC_col[col] > 7:
                    ACC_col[col] -= 16

                if alpha_pixel[row, col] > 31:
                    alpha_pixel[row, col] -= 64

                alpha_ij[row, col] = pix_sens_average + ACC_row[row] * (2 ** scale_ACC_row)
                alpha_ij[row, col] += ACC_col[col] * (2 ** scale_ACC_col)
                alpha_ij[row, col] += alpha_pixel[row, col] * (2 ** scale_ACC_rem)
                alpha_ij[row, col] = alpha_ij[row, col] / (2 ** alphaScale + 30)

                alpha_comp_ij[row, col] = (TGC * ((1 - Pattern) * alphaCP_subpage0 + Pattern * alphaCP_subpage1))
                alpha_comp_ij[row, col] = (alpha_ij[row, col] - alpha_comp_ij[row, col])
                alpha_comp_ij[row, col] = alpha_comp_ij[row, col] * (1 + k_sTa * (Ta - 25))

                # 11.2.2.9 Calculating To For Basic Temperature Range (0°C ... CT3°C)
                K_sTo2_EE = Ks_to_range_2
                if K_sTo2_EE > 127:
                    K_sTo2_EE -= 256

                K_sTo2 = K_sTo2_EE / (2 ** (KsTo_Scale_offset + 8))

                Tr = Ta - 8

                TaK4 = ((Ta + 273.15) ** 4)
                TrK4 = ((Tr + 273.15) ** 4)

                Ta_min_r = (TrK4 - ((TrK4 - TaK4) / E))

                Sx[row, col] = (alpha_comp_ij[row, col] ** 3) * V_ir_comp
                Sx[row, col] += (alpha_comp_ij[row, col] ** 4) * Ta_min_r
                Sx[row, col] = (Sx[row, col] ** .25) * K_sTo2

                Inside2 = (V_ir_comp / (alpha_comp_ij[row, col] * (1 - K_sTo2 * 273.15) + Sx[row, col]))
                Inside2 += Ta_min_r
                Inside2 = (Inside2 ** .25) + 11  # calibration
                To[row, col] = Inside2

                # 11.2.2.9.1 Calculating For Extended Temperature Ranges
                Step = temp_step * 10
                ct3 = CT3 * Step
                ct4 = (CT4 * Step) + ct3

                Ks_To1_EE = Ks_to_range_1
                if Ks_To1_EE > 127:
                    Ks_To1_EE -= 256
                Ks_To1 = Ks_To1_EE / (2 ** (KsTo_Scale_offset + 8))

                Ks_To3_EE = Ks_to_range_3
                if Ks_To3_EE > 127:
                    Ks_To3_EE -= 256
                Ks_To3 = Ks_To3_EE / (2 ** (KsTo_Scale_offset + 8))

                Ks_To4_EE = Ks_to_range_4
                if Ks_To4_EE > 127:
                    Ks_To4_EE -= 256
                Ks_To4 = Ks_To4_EE / (2 ** (KsTo_Scale_offset + 8))

                Alpha_corr_range1 = 1 / (1 + Ks_To1 * (0 - (-40)))
                Alpha_corr_range2 = 1
                Alpha_corr_range3 = 1 + K_sTo2 * (ct3 - 0)
                Alpha_corr_range4 = (1 + K_sTo2 * (ct3 -0)) * (1 + Ks_To3 * (ct4 - ct3))

                if To.any() < 0:
                    KS = Ks_To1
                    ALPHA = Alpha_corr_range1
                    CT = -40
                elif 0 < To.any() < ct3:
                    KS = K_sTo2
                    ALPHA = Alpha_corr_range2
                    CT = 0
                elif ct3 < To.any() < ct4:
                    KS = Ks_To3
                    ALPHA = Alpha_corr_range3
                    CT = ct3
                elif ct4 < To.any():
                    KS = Ks_To4
                    ALPHA = Alpha_corr_range4
                    CT = ct4
                else:
                    KS = K_sTo2
                    ALPHA = Alpha_corr_range2
                    CT = 0

                Inside = alpha_comp_ij[row, col] * ALPHA * (1 + KS * (To[row, col] - CT))
                Inside = V_ir_comp / Inside
                Inside += Ta_min_r
                Inside = (Inside ** .25) - 273.15
                To_ext[row, col] = Inside

        # Find Average Temp
        avg = np.average(To)

        # IMAGE MAKING
        words = "Avg. Temp = {0:.2f}°C".format(avg)
        image = (To - np.min(To)) / np.ptp(To)
        im = Image.fromarray(np.uint8(cm.jet(image)*255))
        im = im.resize((round(im.size[0]*im_scalar), round(im.size[1]*im_scalar)))
        image_edit = ImageDraw.Draw(im)
        image_edit.text((5, 5), words, (0, 0, 0))
        #  im.show()   # shows the image in default image viewer
        im.save("C:/Users/dMaN1/PycharmProjects/fromRawToThermal/outputImages/IR_Image_{:>05}.png".format(i))
        #  im.close()

    inp.close()                     # close input  file when done
