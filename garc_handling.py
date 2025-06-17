import csv
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from utilities import *
from functools import reduce

def binary_file_to_array(file_path, offset = 0, read_length = 0):

    with open(file_path, "r+b") as f:

        #get location of last byte in file
        f.seek(0, os.SEEK_END)
        file_end = f.tell()

        #go to the specified offset
        f.seek(offset, 0)

        #in this case, reading whole file from offset
        if(read_length == 0):
            read_length = file_end - offset

        return(list(f.read(read_length)))

def binary_file_read_to_flag(file_path, offset = 0):

    with open(file_path, "r+b") as f:
        x = 0
        while True:
            #go to the start offset plus x
            f.seek(offset + x, 0)

            
            #get the three bytes starting from location
            halfword = f.read(3)

            #if next byte is not 0xFF, go to next byte
            if(halfword[1] != 0xFF):
                x += 1
                continue
            #if next next byte is not 0xFF (i.e. we have 0xFFZZ where ZZ != FF), skip two forward
            elif(halfword[2] != 0xFF):
                x += 2
                continue

            #if we did not trigger the above, found the end-flag. i.e. we have three bytes, first is last data byte, then 0xFF, and offset + x points to that last data byte. Length of data is then x+1
            return(binary_file_to_array(file_path, offset = offset, read_length = x+1))



def deconstruct_GARC(bindata, poke_edit_data):
        #header:
        # 0x4 Header length (4 bytes)
        # 0x10 Data start (4 bytes)
        # 0x14 total file length (4 bytes)

        #then depends on version
        
        # V4
        # 0x18 largest file size (unpadded)

        # V6

        # 0x18 largest file size (with padding if it exists)
        # 0x1C largest file size (without padding, virtually always equal to the above for our purposes)
        # 0x20 Padding value (usually 0x4)

        #counting from end of whatever version you're in (so 0x4 = 0x1C in v4, 0x24 in v6)

        # 0x8 FAT0 header length (counting from 0x4)
        # 0xC, number of files (2 bytes)
        # from 0x10, 4 bytes per file, each one is 0x10 times file number (start from 0)
        

        #from end of above, 0x4 - header length
        # 0x8 - file count, then 
        # then for each file, 0x01 00 00 00, then offset start, offset end, and file length, offset counting first byte of first file as 0x0

        #finally, last magic word, then header length (0xC), then length of actual data (same as final offset end from previous section

        #get Fat0 offset
        FAT0_offset = 0
        if(poke_edit_data.game in {"XY", "ORAS"}):
           FAT0_offset = 0x1C
        else:
           FAT0_offset = 0x24
        
        
        FATB_offset = FAT0_offset + from_little_bytes_int(bindata[FAT0_offset + 0x4:FAT0_offset + 0x8])

        file_count = from_little_bytes_int(bindata[FAT0_offset + 0x8:FAT0_offset + 0xA])

        data_absolute_offset = from_little_bytes_int(bindata[0x10:0x14])


        output_array = []

        #0xC is start of the actual file location/length data.
        FATB_offset += 0xC

        #iterate over the files, pulling the length from the FATB data, each file gets its own array in temp
        for _ in range(file_count):
            
            #move data pointer to start of next file
            data_offset = data_absolute_offset + from_little_bytes_int(bindata[FATB_offset + 0x4:FATB_offset + 0x8])
            #print(data_offset)
            #get length of current file
            file_length = from_little_bytes_int(bindata[FATB_offset + 0xC:FATB_offset + 0x10])

            #append the file to a new entry in output array
            output_array.append(bindata[data_offset:data_offset + file_length])
            

            #the offset end is different than start + length because length is padded to multiple of 4.

            #move to next file in FATB data
            FATB_offset += 0x10

        return(output_array)


#loads list of filenames in extracted GARC if it exists, otherwise return empty array
def load_GARC(poke_edit_data, garc_path, target):

    if(os.path.exists(garc_path)):

        try:
            file_array = deconstruct_GARC(binary_file_to_array(garc_path), poke_edit_data)

            match target:
                case "Personal":
                    #delete compilation file
                    file_array.pop()
                    poke_edit_data.personal = file_array

                case "Levelup":
                    poke_edit_data.levelup = file_array

                case "Evolution":
                    poke_edit_data.evolution = file_array


        except Exception as e:
            print(e)
            return(poke_edit_data)

    else:
        print("Garc folder not found, unreadable, or empty")
    return(poke_edit_data)

def get_GARC_path(target, gameassert):
    
    targetpath = ''
    #Evolution table has a fixed length per personal file, 0x30 in gen VI, 0x40 in gen VII
    #Similarly, the Personal file itself is 0x50 in gen VI, 0x54 in gen VII (additional bytes for "is regional forme" and Species-specific Z move)
    match gameassert:
        case "XY":
            match target:
                case "Personal":
                    targetpath = '2/1/8'
                case "Levelup":
                    targetpath = '2/1/4'
                case "Evolution":
                    targetpath = '2/1/5'
        case "ORAS":
            match target:
                case "Personal":
                    targetpath = '1/9/5'
                case"Levelup":
                    targetpath = '1/9/1'
                case"Evolution":
                    targetpath = '1/9/2'
        case "SM":
            match target:
                case"Personal":
                    targetpath = '0/1/7'
                case"Levelup":
                    targetpath = '0/1/3'
                case"Evolution":
                    targetpath = '0/1/4'
        case "USUM":
            match target:
                case"Personal":
                    targetpath = '0/1/7'
                case"Levelup":
                    targetpath = '0/1/3'
                case"Evolution":
                    targetpath = '0/1/4'
        case "Select Game":
               print("Error: Game not set")
               return
    
    return(targetpath)           
