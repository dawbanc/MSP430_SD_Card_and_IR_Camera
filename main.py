import os.path
import matplotlib.cm as cm
import numpy as np
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


def convert_to_twos_comp(binary, length):  # takes length in bits
    tc = (-1) * ((2 ** length) - binary)
    return tc


def cftc(tc, length):  # takes length in bits
    num = (-1) * ((2 ** length) + tc)
    return num


def even_or_odd(num):
    if (num % 2) == 0:
        return "even"
    else:
        return "odd"


print("Running this program will overwrite any previously processed images in the chosen directory.")
print("Do you wish to continue, y / n?")
response = input("")

if (response == "n") or (response == "N"):
    print("stopping code")
    exit()

# possible unknowns to ignore warnings
inputFileName = ""
outputPath = ""
numPics = -1
im_scalar = -1

# USER INPUT                    ----------------------------------------------------------------------------------------
response = "n"
while response == "n" or response == "N":
    checker = False
    numPics = -1
    im_scalar = -1
    while not checker:
        print("Please input text file path and name to convert (recommend copying the absolute path):")
        inputFileName = input("")
        checker = os.path.isfile(inputFileName)
        if not checker:
            print("Sorry, it doesn't look like that file exists, please try again")

    checker = False
    while not checker:
        print("Please input the directory where you want to export the images :")
        outputPath = input("")
        checker = os.path.isdir(outputPath)
        if not checker:
            print("Sorry, it doesn't look like that directory exists, would you like to create it, y / n?")
            response2 = input("")
            if response2 == "y" or response2 == "Y":
                os.mkdir(outputPath)
                checker = os.path.isdir(outputPath)
                print("Directory Created Sucessfully")

    print("How many GBs was the SD card?")
    gbCount = int(input(""))
    fullSDpics = int(((gbCount * 1024 * 1024 * 1024) - 5) / 3) - 1

    while not (1 < numPics < fullSDpics):
        print("How many images would you like to process? A full " + str(gbCount) + "GB SD card would be "
              + str(fullSDpics) +
              " images")
        numPics = int(input(""))
        if not (1 < numPics < fullSDpics):
            print("Sorry the number of images must be between 1 and " + str(fullSDpics))

    while not (0 < im_scalar < 50):
        print("By how much would you like to scale the images (the larger the number the longer " +
              "the process will take, recommended is around 15)")
        im_scalar = int(input(""))
        if not (0 < im_scalar < 50):
            print("Sorry the scaling must be between 1 and 50 (for RAM saving purposes)")

    print("You put " + outputPath + " as the output path and you want "
          + str(numPics) + " images. Is this correct, y / n?")
    response = input("")

# GLOBALS & NUMPY ARRAY DEFS    ----------------------------------------------------------------------------------------
OCC_row = np.zeros(24)
OCC_col = np.zeros(32)
ACC_row = np.zeros(24)
ACC_col = np.zeros(32)

offset_pixel = np.zeros((24, 32))
alpha_pixel = np.zeros((24, 32))
kta_pixel = np.zeros((24, 32))
outlier_pixel = np.zeros((24, 32))

inp = open(inputFileName, "r")
print("Taking in variables")

# VALUES IN IR 0x0700
line = inp.readline()
Ta_Vbe = (convert_line_to_binary(line[10], line[11], line[13], line[14]))

line = inp.readline()
cp_subpage0 = (convert_line_to_binary(line[10], line[11], line[13], line[14]))
gain_700 = (convert_line_to_binary(line[22], line[23], line[25], line[26]))

inp.readline()  # excess data
inp.readline()

line = inp.readline()
Ta_PTAT = (convert_line_to_binary(line[10], line[11], line[13], line[14]))

line = inp.readline()
cp_subpage1 = (convert_line_to_binary(line[10], line[11], line[13], line[14]))
VDDpix = (convert_line_to_binary(line[22], line[23], line[25], line[26]))

inp.readline()  # excess data
inp.readline()

inp.readline()  # zeros
inp.readline()  # *

# VALUES IN IR 0x2410
line = inp.readline()  # first line

alphaPTAT = (convert_hex_to_binary(line[10]))
scale_OCC_row = (convert_hex_to_binary(line[11]))
scale_OCC_col = (convert_hex_to_binary(line[13]))
scale_OCC_rem = (convert_hex_to_binary(line[14]))
pix_os_average = (convert_hex_to_binary(line[16]) << 12) + (convert_hex_to_binary(line[17]) << 8)
pix_os_average += (convert_hex_to_binary(line[19]) << 4) + (convert_hex_to_binary(line[20]))
OCC_row[3] = (convert_hex_to_binary(line[22]))
OCC_row[2] = (convert_hex_to_binary(line[23]))
OCC_row[1] = (convert_hex_to_binary(line[25]))
OCC_row[0] = (convert_hex_to_binary(line[26]))
OCC_row[7] = (convert_hex_to_binary(line[28]))
OCC_row[6] = (convert_hex_to_binary(line[29]))
OCC_row[5] = (convert_hex_to_binary(line[31]))
OCC_row[4] = (convert_hex_to_binary(line[32]))

OCC_row[11] = (convert_hex_to_binary(line[35]))
OCC_row[10] = (convert_hex_to_binary(line[36]))
OCC_row[9] = (convert_hex_to_binary(line[38]))
OCC_row[8] = (convert_hex_to_binary(line[39]))
OCC_row[15] = (convert_hex_to_binary(line[41]))
OCC_row[14] = (convert_hex_to_binary(line[42]))
OCC_row[13] = (convert_hex_to_binary(line[44]))
OCC_row[12] = (convert_hex_to_binary(line[45]))

OCC_row[19] = (convert_hex_to_binary(line[47]))
OCC_row[18] = (convert_hex_to_binary(line[48]))
OCC_row[17] = (convert_hex_to_binary(line[50]))
OCC_row[16] = (convert_hex_to_binary(line[51]))
OCC_row[23] = (convert_hex_to_binary(line[53]))
OCC_row[22] = (convert_hex_to_binary(line[54]))
OCC_row[21] = (convert_hex_to_binary(line[56]))
OCC_row[20] = (convert_hex_to_binary(line[57]))

line = inp.readline()  # second line

OCC_col[3] = (convert_hex_to_binary(line[10]))
OCC_col[2] = (convert_hex_to_binary(line[11]))
OCC_col[1] = (convert_hex_to_binary(line[13]))
OCC_col[0] = (convert_hex_to_binary(line[14]))
OCC_col[7] = (convert_hex_to_binary(line[16]))
OCC_col[6] = (convert_hex_to_binary(line[17]))
OCC_col[5] = (convert_hex_to_binary(line[19]))
OCC_col[4] = (convert_hex_to_binary(line[20]))

OCC_col[11] = (convert_hex_to_binary(line[22]))
OCC_col[10] = (convert_hex_to_binary(line[23]))
OCC_col[9] = (convert_hex_to_binary(line[25]))
OCC_col[8] = (convert_hex_to_binary(line[26]))
OCC_col[15] = (convert_hex_to_binary(line[28]))
OCC_col[14] = (convert_hex_to_binary(line[29]))
OCC_col[13] = (convert_hex_to_binary(line[31]))
OCC_col[12] = (convert_hex_to_binary(line[32]))

OCC_col[19] = (convert_hex_to_binary(line[35]))
OCC_col[18] = (convert_hex_to_binary(line[36]))
OCC_col[17] = (convert_hex_to_binary(line[38]))
OCC_col[16] = (convert_hex_to_binary(line[39]))
OCC_col[23] = (convert_hex_to_binary(line[41]))
OCC_col[22] = (convert_hex_to_binary(line[42]))
OCC_col[21] = (convert_hex_to_binary(line[44]))
OCC_col[20] = (convert_hex_to_binary(line[45]))

OCC_col[27] = (convert_hex_to_binary(line[47]))
OCC_col[26] = (convert_hex_to_binary(line[48]))
OCC_col[25] = (convert_hex_to_binary(line[50]))
OCC_col[24] = (convert_hex_to_binary(line[51]))
OCC_col[31] = (convert_hex_to_binary(line[53]))
OCC_col[30] = (convert_hex_to_binary(line[54]))
OCC_col[29] = (convert_hex_to_binary(line[56]))
OCC_col[28] = (convert_hex_to_binary(line[57]))

line = inp.readline()  # third line

alphaScale = (convert_hex_to_binary(line[10]))
scale_ACC_row = (convert_hex_to_binary(line[11]))
scale_ACC_col = (convert_hex_to_binary(line[13]))
scale_ACC_rem = (convert_hex_to_binary(line[14]))
pix_sens_average = (convert_hex_to_binary(line[16]) << 12) + (convert_hex_to_binary(line[17]) << 8)
pix_sens_average += (convert_hex_to_binary(line[19]) << 4) + (convert_hex_to_binary(line[20]))
ACC_row[3] = (convert_hex_to_binary(line[22]))
ACC_row[2] = (convert_hex_to_binary(line[23]))
ACC_row[1] = (convert_hex_to_binary(line[25]))
ACC_row[0] = (convert_hex_to_binary(line[26]))
ACC_row[7] = (convert_hex_to_binary(line[28]))
ACC_row[6] = (convert_hex_to_binary(line[29]))
ACC_row[5] = (convert_hex_to_binary(line[31]))
ACC_row[4] = (convert_hex_to_binary(line[32]))

ACC_row[11] = (convert_hex_to_binary(line[35]))
ACC_row[10] = (convert_hex_to_binary(line[36]))
ACC_row[9] = (convert_hex_to_binary(line[38]))
ACC_row[8] = (convert_hex_to_binary(line[39]))
ACC_row[15] = (convert_hex_to_binary(line[41]))
ACC_row[14] = (convert_hex_to_binary(line[42]))
ACC_row[13] = (convert_hex_to_binary(line[44]))
ACC_row[12] = (convert_hex_to_binary(line[45]))

ACC_row[19] = (convert_hex_to_binary(line[47]))
ACC_row[18] = (convert_hex_to_binary(line[48]))
ACC_row[17] = (convert_hex_to_binary(line[50]))
ACC_row[16] = (convert_hex_to_binary(line[51]))
ACC_row[23] = (convert_hex_to_binary(line[53]))
ACC_row[22] = (convert_hex_to_binary(line[54]))
ACC_row[21] = (convert_hex_to_binary(line[56]))
ACC_row[20] = (convert_hex_to_binary(line[57]))

line = inp.readline()  # fourth line

ACC_col[3] = (convert_hex_to_binary(line[10]))
ACC_col[2] = (convert_hex_to_binary(line[11]))
ACC_col[1] = (convert_hex_to_binary(line[13]))
ACC_col[0] = (convert_hex_to_binary(line[14]))
ACC_col[7] = (convert_hex_to_binary(line[16]))
ACC_col[6] = (convert_hex_to_binary(line[17]))
ACC_col[5] = (convert_hex_to_binary(line[19]))
ACC_col[4] = (convert_hex_to_binary(line[20]))

ACC_col[11] = (convert_hex_to_binary(line[22]))
ACC_col[10] = (convert_hex_to_binary(line[23]))
ACC_col[9] = (convert_hex_to_binary(line[25]))
ACC_col[8] = (convert_hex_to_binary(line[26]))
ACC_col[15] = (convert_hex_to_binary(line[28]))
ACC_col[14] = (convert_hex_to_binary(line[29]))
ACC_col[13] = (convert_hex_to_binary(line[31]))
ACC_col[12] = (convert_hex_to_binary(line[32]))

ACC_col[19] = (convert_hex_to_binary(line[35]))
ACC_col[18] = (convert_hex_to_binary(line[36]))
ACC_col[17] = (convert_hex_to_binary(line[38]))
ACC_col[16] = (convert_hex_to_binary(line[39]))
ACC_col[23] = (convert_hex_to_binary(line[41]))
ACC_col[22] = (convert_hex_to_binary(line[42]))
ACC_col[21] = (convert_hex_to_binary(line[44]))
ACC_col[20] = (convert_hex_to_binary(line[45]))

ACC_col[27] = (convert_hex_to_binary(line[47]))
ACC_col[26] = (convert_hex_to_binary(line[48]))
ACC_col[25] = (convert_hex_to_binary(line[50]))
ACC_col[24] = (convert_hex_to_binary(line[51]))
ACC_col[31] = (convert_hex_to_binary(line[53]))
ACC_col[30] = (convert_hex_to_binary(line[54]))
ACC_col[29] = (convert_hex_to_binary(line[56]))
ACC_col[28] = (convert_hex_to_binary(line[57]))

line = inp.readline()  # fifth line

gain = (convert_hex_to_binary(line[10]) << 12) + (convert_hex_to_binary(line[11]) << 8)
gain += (convert_hex_to_binary(line[13]) << 4) + (convert_hex_to_binary(line[14]))
ptat_25 = (convert_hex_to_binary(line[16]) << 12) + (convert_hex_to_binary(line[17]) << 8)
ptat_25 += (convert_hex_to_binary(line[19]) << 4) + (convert_hex_to_binary(line[20]))
whole_line = convert_line_to_binary(line[22], line[23], line[25], line[26])
kv_ptat = ((whole_line & 0b1111110000000000) << 10)
kt_ptat = (whole_line & 0b1111111111)
kv_vdd = (convert_hex_to_binary(line[28]) << 8) + (convert_hex_to_binary(line[29]))
vdd_25 = (convert_hex_to_binary(line[31]) << 8) + (convert_hex_to_binary(line[32]))
kv_avg_odd_row_odd_col = (convert_hex_to_binary(line[35]))
kv_avg_eve_row_odd_col = (convert_hex_to_binary(line[36]))
kv_avg_odd_row_eve_col = (convert_hex_to_binary(line[38]))
kv_avg_eve_row_eve_col = (convert_hex_to_binary(line[39]))
whole_line = convert_line_to_binary(line[41], line[42], line[44], line[45])
IL_Chess_C3 = ((whole_line & 0b1111100000000000) >> 11)
IL_Chess_C2 = ((whole_line & 0b11111000000) >> 6)
IL_Chess_C1 = (whole_line & 0b111111)
kta_avg_odd_row_odd_col = ((convert_hex_to_binary(line[47]) << 4) + (convert_hex_to_binary(line[48])))
kta_avg_eve_row_odd_col = ((convert_hex_to_binary(line[50]) << 4) + (convert_hex_to_binary(line[51])))
kta_avg_odd_row_eve_col = ((convert_hex_to_binary(line[53]) << 4) + (convert_hex_to_binary(line[54])))
kta_avg_eve_row_eve_col = ((convert_hex_to_binary(line[56]) << 4) + (convert_hex_to_binary(line[57])))

line = inp.readline()  # sixth line

whole_line = convert_line_to_binary(line[10], line[11], line[13], line[14])
res_control_calib = ((whole_line & 0b11000000000000) >> 12)
kv_scale = ((whole_line & 0b111100000000) >> 8)
kta_scale_1 = ((whole_line & 0b11110000) >> 4)
kta_scale_2 = (whole_line & 0b1111)
whole_line = convert_line_to_binary(line[16], line[17], line[19], line[20])
alpha_CP_subpage1_div_Csubpage0_2tothe7 = ((whole_line & 0b1111110000000000) << 10)
alpha_CP_subpage0 = (whole_line & 0b1111111111)
whole_line = convert_line_to_binary(line[22], line[23], line[25], line[26])
offset_CP_subpage1_sub_CP_subpage0 = ((whole_line & 0b1111110000000000) << 10)
offset_CP_subpage0 = (whole_line & 0b1111111111)
kv_CP = ((convert_hex_to_binary(line[28]) << 4) + (convert_hex_to_binary(line[29])))
kta_CP = ((convert_hex_to_binary(line[31]) << 4) + (convert_hex_to_binary(line[32])))
ksta_2tothe13 = ((convert_hex_to_binary(line[35]) << 4) + (convert_hex_to_binary(line[36])))
TGC_plusOminus4 = ((convert_hex_to_binary(line[38]) << 4) + (convert_hex_to_binary(line[39])))
Ks_to_range_2 = ((convert_hex_to_binary(line[41]) << 4) + (convert_hex_to_binary(line[42])))
Ks_to_range_1 = ((convert_hex_to_binary(line[44]) << 4) + (convert_hex_to_binary(line[45])))
Ks_to_range_4 = ((convert_hex_to_binary(line[47]) << 4) + (convert_hex_to_binary(line[48])))
Ks_to_range_3 = ((convert_hex_to_binary(line[50]) << 4) + (convert_hex_to_binary(line[51])))
temp_step = (convert_hex_to_binary(line[53]) & 0b0011)
CT4 = (convert_hex_to_binary(line[54]))
CT3 = (convert_hex_to_binary(line[56]))
KsTo_Scale_offset = (convert_hex_to_binary(line[57]))

inp.readline()  # zeros
inp.readline()  # *

# DATA FOR IMAGE CALCULATION
# VALUES IN IR 0x2440
for row in range(24):
    for col in range(4):
        line = inp.readline()
        whole_line = convert_line_to_binary(line[10], line[11], line[13], line[14])
        offset_pixel[row, 0 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 0 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 0 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 0 + (col * 8)] = (whole_line & 0b0001)

        whole_line = convert_line_to_binary(line[16], line[17], line[19], line[20])
        offset_pixel[row, 1 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 1 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 1 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 1 + (col * 8)] = (whole_line & 0b0001)

        whole_line = convert_line_to_binary(line[22], line[23], line[25], line[26])
        offset_pixel[row, 2 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 2 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 2 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 2 + (col * 8)] = (whole_line & 0b0001)

        whole_line = convert_line_to_binary(line[28], line[29], line[31], line[32])
        offset_pixel[row, 3 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 3 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 3 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 3 + (col * 8)] = (whole_line & 0b0001)

        whole_line = convert_line_to_binary(line[35], line[36], line[38], line[39])
        offset_pixel[row, 4 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 4 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 4 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 4 + (col * 8)] = (whole_line & 0b0001)

        whole_line = convert_line_to_binary(line[41], line[42], line[44], line[45])
        offset_pixel[row, 5 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 5 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 5 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 5 + (col * 8)] = (whole_line & 0b0001)

        whole_line = convert_line_to_binary(line[47], line[48], line[50], line[51])
        offset_pixel[row, 6 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 6 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 6 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 6 + (col * 8)] = (whole_line & 0b0001)

        whole_line = convert_line_to_binary(line[53], line[54], line[56], line[57])
        offset_pixel[row, 7 + (col * 8)] = ((whole_line & 0b1111110000000000) >> 10)
        alpha_pixel[row, 7 + (col * 8)] = ((whole_line & 0b1111110000) >> 4)
        kta_pixel[row, 7 + (col * 8)] = ((whole_line & 0b1110) >> 1)
        outlier_pixel[row, 7 + (col * 8)] = (whole_line & 0b0001)

for i in range(numPics):

    ir_image = np.zeros((24, 32))
    C_pix_gain = np.zeros((24, 32))
    C_pix_os_ref = np.zeros((24, 32))
    C_kv_ij = np.zeros((24, 32))
    C_kta_ij = np.zeros((24, 32))
    C_pix_os = np.zeros((24, 32))
    C_alpha_comp_ij = np.zeros((24, 32))
    C_alpha_ij = np.zeros((24, 32))
    C_Sx = np.zeros((24, 32))
    C_To = np.zeros((24, 32))
    C_To_ext = np.zeros((24, 32))
    C_To_avg = 0

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

    #   11.2.2.2 Supply Voltage Value Calc (Common for all Pixels)
    C_kv_vdd = kv_vdd
    if C_kv_vdd > 127:
        C_kv_vdd -= 256
    C_kv_vdd *= (2 ** 5)
    C_vdd_25 = vdd_25
    C_vdd_25 = (C_vdd_25 - 256) * (2 ** 5) - (2 ** 13)
    #       VDD Calc
    C_VDDpix = VDDpix
    if C_VDDpix > 32767:
        C_VDDpix -= 65536
    C_vdd = ((1 + C_VDDpix - C_vdd_25) / C_kv_vdd) + 4.3  # changed

    #   11.2.2.3 Ambient Temperature Calc (Common for all Pixels)
    C_kv_ptat = kv_ptat
    if C_kv_ptat > 31:
        C_kv_ptat -= 64
    C_kv_ptat = C_kv_ptat / (2 ** 12)

    C_kt_ptat = kt_ptat
    if C_kt_ptat > 511:
        C_kt_ptat -= 1024
    C_kt_ptat = C_kt_ptat / (2 ** 3)

    C_deltaV = (C_VDDpix - C_vdd_25) / C_kv_vdd

    C_ptat_25 = ptat_25
    if C_ptat_25 > 32767:
        C_ptat_25 -= 65536

    C_Ta_PTAT = Ta_PTAT
    if C_Ta_PTAT > 32767:
        C_Ta_PTAT -= 65536

    C_Ta_Vbe = Ta_Vbe
    if C_Ta_Vbe > 32767:
        C_Ta_Vbe -= 65536

    C_alphaPTAT = alphaPTAT
    C_alphaPTAT = (C_alphaPTAT / (2 ** 2)) + 8

    C_V_ptat_art = (C_Ta_PTAT / (C_Ta_PTAT + C_alphaPTAT + C_Ta_Vbe)) * (2 ** 18)

    C_Ta = (((C_V_ptat_art / (1 + (C_kv_ptat * C_deltaV))) - C_ptat_25) / C_kt_ptat) + 273.15

    for row in range(24):
        for col in range(32):
            row_spec = even_or_odd(row)
            col_spec = even_or_odd(col)

            # 11.2.2.4 Gain Parameter Calculation (Common for all Pixels)
            C_gain = gain
            if C_gain > 32767:
                C_gain -= 65536

            C_gain_700 = gain_700
            if C_gain_700 > 32767:
                C_gain_700 -= 65536

            C_k_gain = C_gain / C_gain_700

            # 11.2.2.5.1 Gain Compensation
            C_pixel = ir_image[row, col]
            if C_pixel > 32767:
                C_pixel -= 65536
            C_pix_gain[row, col] = C_pixel * C_k_gain

            # 11.2.2.5.2 Offset Calculation
            C_pix_os_average = pix_os_average
            if C_pix_os_average > 32767:
                C_pix_os_average -= 65536

            C_OCC_row_value = OCC_row[row]
            if C_OCC_row_value > 7:
                C_OCC_row_value -= 16

            C_OCC_col_value = OCC_col[col]
            if C_OCC_col_value > 7:
                C_OCC_col_value -= 16

            C_offset_pixel_value = offset_pixel[row, col]
            if C_offset_pixel_value > 31:
                C_offset_pixel_value -= 64

            C_scale_OCC_row = scale_OCC_row
            C_scale_OCC_col = scale_OCC_col
            C_scale_OCC_rem = scale_OCC_rem
            C_pix_os_ref[row, col] = C_pix_os_average + (C_OCC_row_value * (2 ** C_scale_OCC_row))
            C_pix_os_ref[row, col] += (C_OCC_col_value * (2 ** C_scale_OCC_col))
            C_pix_os_ref[row, col] += (C_offset_pixel_value * (2 ** C_scale_OCC_rem))

            # 11.2.2.5.3 IR Data Compensation
            C_kta_pixel_value = kta_pixel[row, col]
            if C_kta_pixel_value > 3:
                C_kta_pixel_value -= 8

            C_kv_avg_eve_row_eve_col = kv_avg_eve_row_eve_col
            C_kv_avg_eve_row_odd_col = kv_avg_eve_row_odd_col
            C_kv_avg_odd_row_eve_col = kv_avg_odd_row_eve_col
            C_kv_avg_odd_row_odd_col = kv_avg_odd_row_odd_col
            C_kta_avg_eve_row_eve_col = kta_avg_eve_row_eve_col
            C_kta_avg_eve_row_odd_col = kta_avg_eve_row_odd_col
            C_kta_avg_odd_row_eve_col = kta_avg_odd_row_eve_col
            C_kta_avg_odd_row_odd_col = kta_avg_odd_row_odd_col
            if row_spec == "even":
                if col_spec == "even":
                    C_kv = C_kv_avg_eve_row_eve_col
                    C_kta = C_kta_avg_eve_row_eve_col
                else:
                    C_kv = C_kv_avg_eve_row_odd_col
                    C_kta = C_kta_avg_eve_row_odd_col
            else:
                if col_spec == "even":
                    C_kv = C_kv_avg_odd_row_eve_col
                    C_kta = C_kta_avg_odd_row_eve_col
                else:
                    C_kv = C_kv_avg_odd_row_odd_col
                    C_kta = C_kta_avg_odd_row_odd_col

            if C_kv > 7:
                C_kv -= 16

            if C_kta > 127:
                C_kta -= 256

            C_kta_scale_2 = kta_scale_2
            C_kta_scale_1 = kta_scale_1
            C_kv_scale = kv_scale
            C_kta_ij[row, col] = (C_kta + (C_kta_pixel_value / 2) * (2 ** C_kta_scale_2)) / (2 ** (C_kta_scale_1 + 8))
            C_kv_ij[row, col] = C_kv / (2 ** C_kv_scale)

            Inside = C_pix_os_ref[row, col] * (1 + C_kta_ij[row, col] * (C_Ta - 25))
            Inside = Inside * (1 + C_kv_ij[row, col] * (C_vdd - 3.3))
            C_pix_os[row, col] = C_pix_gain[row, col] - Inside

            # 11.2.2.5.4 IR Data Emissivity Compensation
            E = 1  # EMISSIVITY COEFFECIENT
            C_V_ir_E_Comp = C_pix_os[row, col] / E

            # 11.2.2.6.1 Compensating the GAIN of CP Pixel
            C_cp_subpage0 = cp_subpage0
            C_cp_subpage1 = cp_subpage1

            if C_cp_subpage0 > 32767:
                C_cp_subpage0 -= 65536

            C_pix_gain_cp_SP0 = C_k_gain * C_cp_subpage0

            if C_cp_subpage1 > 32767:
                C_cp_subpage1 -= 65536

            C_pix_gain_cp_SP1 = C_k_gain * C_cp_subpage1

            # 11.2.2.6.2 Compensating Offset, Ta, and Vdd of CP Pixel
            C_offset_CP_subpage0 = offset_CP_subpage0
            if C_offset_CP_subpage0 > 511:
                C_offset_CP_subpage0 -= 1024

            C_Off_CP_SP0 = C_offset_CP_subpage0

            C_offset_CP_subpage1 = offset_CP_subpage1_sub_CP_subpage0
            if C_offset_CP_subpage1 > 31:
                C_offset_CP_subpage1 -= 64

            C_Off_CP_SP1 = C_Off_CP_SP0 + C_offset_CP_subpage1

            C_kta_CP = kta_CP
            if C_kta_CP > 127:
                C_kta_CP -= 256

            C_K_TA_CP = C_kta_CP / (2 ** (C_kta_scale_1 + 8))

            C_kv_CP = kv_CP
            if C_kv_CP > 127:
                C_kv_CP -= 256

            C_K_V_CP = C_kv_CP / (2 ** C_kv_scale)

            Inside = C_Off_CP_SP0 * (1 + C_K_TA_CP * (C_Ta - 25)) * (1 + C_K_V_CP * (C_vdd - 3.3))
            C_pix_os_CP_SP0 = C_pix_gain_cp_SP0 - Inside
            Inside = C_Off_CP_SP1 * (1 + C_K_TA_CP * (C_Ta - 25)) * (1 + C_K_V_CP * (C_vdd - 3.3))
            C_pix_os_CP_SP1 = C_pix_gain_cp_SP1 - Inside

            # 11.2.2.7 IR Data Gradient Compensation
            C_pix_num = (row * 32) + col

            C_Pattern = (int((C_pix_num - 1) / 32) - int((int(C_pix_num - 1) / 32) / 2) * 2)
            C_Pattern = C_Pattern ^ ((C_pix_num - 1) - int((C_pix_num - 1) / 2) * 2)

            C_TGC_plus0minus4 = TGC_plusOminus4
            if C_TGC_plus0minus4 > 127:
                C_TGC_plus0minus4 -= 256

            C_TGC = C_TGC_plus0minus4 / (2 ** 5)

            C_V_ir_comp = C_V_ir_E_Comp - C_TGC * (((1 - C_Pattern) * C_pix_os_CP_SP0) + (C_Pattern * C_pix_os_CP_SP1))

            # 11.2.2.8 Normalizing to Sensitivity
            C_alphaScale = alphaScale
            C_alpha_CP_subpage0 = alpha_CP_subpage0
            C_alpha_CP_subpage0 = C_alpha_CP_subpage0 / (2 ** (C_alphaScale + 27))

            C_CP_P1_P0_ratio = alpha_CP_subpage1_div_Csubpage0_2tothe7
            if C_CP_P1_P0_ratio > 31:
                C_CP_P1_P0_ratio -= 64

            C_alphaCP_subpage1 = C_alpha_CP_subpage0 * (1 + (C_CP_P1_P0_ratio / (2 ** 7)))

            C_K_sTa = ksta_2tothe13
            if C_K_sTa > 127:
                C_K_sTa -= 256

            C_ACC_row_value = ACC_row[row]
            C_ACC_col_value = ACC_col[col]
            C_ACC_alp_value = alpha_pixel[row, col]
            C_scale_ACC_row = scale_ACC_row
            C_scale_ACC_col = scale_ACC_col
            C_scale_ACC_rem = scale_ACC_rem

            if C_ACC_row_value > 7:
                C_ACC_row_value -= 16
            if C_ACC_col_value > 7:
                C_ACC_col_value -= 16
            if C_ACC_alp_value > 31:
                C_ACC_alp_value -= 64

            C_pix_sens_avg = pix_sens_average
            C_alpha_ij[row, col] = C_pix_sens_avg + C_ACC_row_value * (2 ** C_scale_ACC_row)
            C_alpha_ij[row, col] += C_ACC_col_value * (2 ** C_scale_ACC_col)
            C_alpha_ij[row, col] += C_ACC_alp_value * (2 ** C_scale_ACC_rem)
            C_alpha_ij[row, col] = C_alpha_ij[row, col] / (2 ** C_alphaScale + 30)

            Inside = (C_TGC * ((1 - C_Pattern) * C_alpha_CP_subpage0 + C_Pattern * C_alphaCP_subpage1))
            C_alpha_comp_ij[row, col] = (C_alpha_ij[row, col] - Inside)
            C_alpha_comp_ij[row, col] = C_alpha_comp_ij[row, col] * (1 + C_K_sTa * (C_Ta - 25))

            # 11.2.2.9 Calculating To for Basic Temperature Range (0°C ... CT3°C)
            C_K_sTo2_EE = Ks_to_range_2
            if C_K_sTo2_EE > 127:
                C_K_sTo2_EE -= 256

            C_KsTo_Scale_offset = KsTo_Scale_offset
            C_K_sTo2 = C_K_sTo2_EE / (2 ** (C_KsTo_Scale_offset + 8))

            C_Tr = C_Ta - 8

            C_TaK4 = ((C_Ta + 273.15) ** 4)
            C_TrK4 = ((C_Tr + 273.15) ** 4)

            C_Ta_min_r = (C_TrK4 - ((C_TrK4 - C_TaK4) / E))

            Inside = (C_alpha_comp_ij[row, col] ** 3) * C_V_ir_comp
            Inside += (C_alpha_comp_ij[row, col] ** 4) * C_Ta_min_r
            C_Sx[row, col] = (Inside ** .25) * C_K_sTo2

            Inside = (C_V_ir_comp / (C_alpha_comp_ij[row, col] * (1 - C_K_sTo2 * 273.15) + C_Sx[row, col]))
            Inside += C_Ta_min_r
            Inside = (Inside ** .25) - 273.15  # calibration
            C_To[row, col] = Inside

            # 11.2.2.9.1 Calculating for Extended Temperature Ranges
            C_Step = temp_step * 10
            C_CT3 = CT3 * C_Step
            C_CT4 = (CT4 * C_Step) + C_CT3

            C_Ks_To1_EE = Ks_to_range_1
            if C_Ks_To1_EE > 127:
                C_Ks_To1_EE -= 256
            C_Ks_To1 = C_Ks_To1_EE / (2 ** (C_KsTo_Scale_offset + 8))

            C_Ks_To3_EE = Ks_to_range_3
            if C_Ks_To3_EE > 127:
                C_Ks_To3_EE -= 256
            C_Ks_To3 = C_Ks_To3_EE / (2 ** (C_KsTo_Scale_offset + 8))

            C_Ks_To4_EE = Ks_to_range_4
            if C_Ks_To4_EE > 127:
                C_Ks_To4_EE -= 256
            C_Ks_To4 = C_Ks_To4_EE / (2 ** (C_KsTo_Scale_offset + 8))

            C_Alpha_corr_range1 = 1 / (1 + C_Ks_To1 * (0 - (-40)))
            C_Alpha_corr_range2 = 1
            C_Alpha_corr_range3 = 1 + C_K_sTo2 * (C_CT3 - 0)
            C_Alpha_corr_range4 = C_Alpha_corr_range3 * (1 + C_Ks_To3 * (C_CT4 - C_CT3))

            if C_To[row, col] < 0:
                C_KS = C_Ks_To1
                C_ALPHA = C_Alpha_corr_range1
                C_CT = -40
            elif 0 < C_To[row, col] < C_CT3:
                C_KS = C_K_sTo2
                C_ALPHA = C_Alpha_corr_range2
                C_CT = 0
            elif C_CT3 < C_To[row, col] < C_CT4:
                C_KS = C_Ks_To3
                C_ALPHA = C_Alpha_corr_range3
                C_CT = C_CT3
            elif C_CT4 < C_To[row, col]:
                C_KS = C_Ks_To4
                C_ALPHA = C_Alpha_corr_range4
                C_CT = CT4
            else:
                C_KS = C_K_sTo2
                C_ALPHA = C_Alpha_corr_range2
                C_CT = 0

            Inside = C_alpha_comp_ij[row, col] * C_ALPHA * (1 + C_KS * (C_To[row, col] - C_CT))
            Inside = C_V_ir_comp / Inside
            Inside += C_Ta_min_r
            Inside = (Inside ** .25) - 273.15
            C_To_ext[row, col] = Inside

    # Calculate average of Image
    C_avg = np.average(C_To)
    C_min = np.min(C_To)
    C_max = np.max(C_To)

    # IMAGE MAKING
    words = "Avg. Temp = {0:.2f}°C".format(C_avg) + " Min. Temp = {0:.2f}°C".format(C_min) \
            + " Max. Temp = {0:.2f}°C".format(C_max)
    image = (C_To - np.min(C_To)) / np.ptp(C_To)
    im = Image.fromarray(np.uint8(cm.jet(image) * 255))
    im = im.resize((round(im.size[0] * im_scalar), round(im.size[1] * im_scalar)))
    image_edit = ImageDraw.Draw(im)
    image_edit.text((5, 5), words, (0, 0, 0))
    im.save(outputPath + r"\IR_Image_{:>05}.png".format(i))

    percent = i / numPics * 100
    print("Progress : {:}%".format(percent))

print("Progress : 100%")
inp.close()  # close file when done
