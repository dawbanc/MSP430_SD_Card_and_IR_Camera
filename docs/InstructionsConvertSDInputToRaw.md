    1. Get Ubuntu on either a flash drive or a computer.
    2. Insert SD card to computer via built-in reader or USB.
    3. Open disks and make sure the card is detected by Ubuntu.Take note of the device name. In this case, /dev/mmcblk0

![Disks Example](docs/image/docs_dd_sd_card_location.png?raw=true)

    4. Then use the dd command which will mostly likely will require superuser permissions. This is a VERY POWERFUL and VERY DANGEROUS command. If this part is not done correctly, you may delete everything from your harddrive. Please TRIPLE check the command before running it. This command can be ran from anywhere. The “if” argument is the name of the SD card device name found in the Disks application. The “of” argument can be changed from “/tmp/sdCardRead.raw” to any path and file name but keep the .raw. ie: “/home/<username>/desktop/myFile.raw” is a pretty good place to start.
    
![dd Usage](docs/image/docs_dd_usage.png?raw=true)
    
    5. The next commands are easiest if the terminal is open in the directory where the file is saved. In this case “/tmp” and my example “/home/<username>/desktop.” So navigate to the desired directory.
    6. Then run the command “hexdump -v -C <filename>.raw  >  <outputfilename>.txt where “<filename>” and “<outputfilename>” are replaced with correctly named files. Another option is to open the file in vim by running the command “LESSOPEN= less <filename>.raw”, but only works good if you are in the ascii range of values that make sense.
    
![hexdump Usage](docs/image/docs_hexdump_usage.png?raw=true)
