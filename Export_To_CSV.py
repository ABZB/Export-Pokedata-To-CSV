from signal import pause
from garc_handling import *
from utilities import *
from my_constants import *

def build_output_array(pokearray, base_index = 0, target_index = 0):
    
    #iterate over all files
    index = target_index
    least_alt_index = 0xFFFF

    while True:
        temp_array = []
        #don't record index 0
        if(index == 0):
            continue

        #get the local personal file
        personal = pokearray.personal[index]

        #Species/Forme Name
        temp_array.append([index, 'Name',pokearray.pokemon_name_list])

        #check if has any alt formes. target index is 0 in main call
        if(target_index == 0):
            #check for alt formes
            temp_index = from_little_bytes_int(personal[0x1C:0x1E])
            
            #if it's not 0, handle all of the alt formes now
            if(temp_index != 0):
                for forme_number in range(personal[0x20] - 1):
                    pokearray = build_output_array(pokearray, index, temp_index + forme_number)
                #this will ultimately find the personal file of the least-indexed alt forme, before it is reached, to handle exiting at the proper time
                if(temp_index < least_alt_index):
                    least_alt_index = temp_index

        #Base Index
        if(base_index == 0):
            temp_array.append([index, 'Base Index',index])
        else:
            temp_array.append([index, 'Base Index',base_index])

        #Stats
        temp_array.append([index, stat_names[0], personal[0]])
        temp_array.append([index, stat_names[1], personal[1]])
        temp_array.append([index, stat_names[2], personal[2]])
        temp_array.append([index, stat_names[3], personal[4]])
        temp_array.append([index, stat_names[4], personal[5]])
        temp_array.append([index, stat_names[5], personal[3]])

        #Types
        temp_array.append([index, 'Type 1', personal[6]])
        temp_array.append([index, 'Type 2', personal[7]])
        temp_array.append([index, 'Catch Rate', personal[8]])

        #EVs
        temp_array.append([index, stat_names[0] + ' EV', personal[0xa] & 3])
        temp_array.append([index, stat_names[1] + ' EV', (personal[0xa] >> 2) & 3])
        temp_array.append([index, stat_names[2] + ' EV', (personal[0xa] >> 4) & 3])
        temp_array.append([index, stat_names[3] + ' EV', personal[0xb] & 3])
        temp_array.append([index, stat_names[4] + ' EV', (personal[0xb] >> 2) & 3])
        temp_array.append([index, stat_names[5] + ' EV', (personal[0xa] >> 6) & 3])

        #Items
        temp_array.append([index, 'Item 50%', pokearray.item_name_list[from_little_bytes_int(personal[0x0C:0x0E])]])
        temp_array.append([index, 'Item 5%', pokearray.item_name_list[from_little_bytes_int(personal[0x0E:0x10])]])
        temp_array.append([index, 'Item 1%', pokearray.item_name_list[from_little_bytes_int(personal[0x10:0x12])]])

        #Abilities
        for x in range(3):
            temp_array.append([index, 'Ability ' + str(x + 1), pokearray.ability_name_list[personal[0x18 + x]]])


        #put the fully built pokemon output thing into its place
        pokearray.write_array[index] = temp_array

        #Check if in a subcall for alt forme or if added final non-alt forme (alt formes of that base forme were branched to above)
        if(base_index != 0 or (index == least_alt_index - 1)):
            return(pokearray)
        #otherwise increment index by 1 and do next loop
        else:
            index += 1

def main():
    pokearray = Pokedata()
    action_choice = ''
    
    reference_directory = os.path.join(os.getcwd(),'config and data')
    pokemon_list_path = os.path.join(reference_directory, 'pokemon_list_' + pokearray.game + '.csv')
    move_list_path = os.path.join(reference_directory, 'move_list.csv')
    ability_list_path = os.path.join(reference_directory, 'ability_list.csv')
    item_list_path = os.path.join(reference_directory, 'item_list.csv')
    tm_list_path = os.path.join(reference_directory, 'tm_hm_special_tutor_list.csv')

    tutor_table_offset = 0
    tutor_table_raw = []


    #get generation
    while True:
        temp = input('Enter Generation, (XY, ORAS, SM, USUM)\n').upper()
        if(temp in {'XY', 'ORAS', 'SM', 'USUM'}):
            pokearray.game = temp
            break
        else:
            print(temp, 'is not valid\n\n')
        


    #load pokemon names
    with open(pokemon_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != '' or line[0] == '0'):
                pokearray.pokemon_name_list.append(line[1])
            else:
                break

    print('Loaded Pokemon Name List')

    #load move names
    with open(move_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != ''):
                pokearray.move_name_list.append(line[1])
            else:
                break
    print('Loaded Move Name List')

    #load ability names
    with open(ability_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != ''):
                pokearray.ability_name_list.append(line[1])
            else:
                break
    print('Loaded Ability Name List')

    #load item names
    with open(item_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != ''):
                pokearray.item_name_list.append(line[1])
            else:
                break
    print('Loaded Item Name List')









    #load TM/HM/Special Tutor names
    with open(tm_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != ''):
                if(line[0][0:2].upper() == 'TM'):
                    pokearray.tm_name_list.append(line)
                elif(line[0][0:2].upper() == 'HM'):
                    pokearray.hm_name_list.append(line)
                elif(line[0][0:2].upper() == 'SP'):
                    pokearray.special_tutor_name_list.append(line)
            else:
                break
    print('Loaded TM/HM/Special Tutor Move Name Lists')

    
    #Get ROM paths
    
    #path to folder
    rom_path = askdirectory(title='Choose the extracted ROM folder')

    #determine if using "ExtractedRomFS" or "romfs"
    romfs_path = ''

    if(os.path.isdir(os.path.join(rom_path, 'ExtractedRomFS'))):
        romfs_path = os.path.join(rom_path, 'ExtractedRomFS/a')
    elif(os.path.isdir(os.path.join(rom_path, 'romfs'))):
        romfs_path = os.path.join(rom_path, 'romfs/a')
    else:
        print('Error: no subfolder named ExtractedRomFS or romfs')  
        return


    pokearray.personal_path = os.path.join(romfs_path, get_GARC_path('Personal', pokearray.game))
    pokearray.evolution_path = os.path.join(romfs_path, get_GARC_path('Evolution', pokearray.game))
    pokearray.levelup_path = os.path.join(romfs_path, get_GARC_path('Levelup', pokearray.game))

    print('Now loading GARCs...')

    #load garcs
    load_GARC(pokearray, pokearray.personal_path, 'Personal')
    load_GARC(pokearray, pokearray.evolution_path, 'Evolution')
    load_GARC(pokearray, pokearray.levelup_path, 'Levelup')


    print('GARCs Loaded')

    print('Now loading BP Move Tutor Table')
    
    #load data from config file
    with open(os.path.join(reference_directory, 'offsets.csv'), newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        #move tutor line
        match pokearray.game:
            case 'XY':
                tutor_table_offset = temp[1][1]
            case 'ORAS':
                tutor_table_offset = temp[1][2]
            case 'SM':
                tutor_table_offset = temp[1][3]
            case 'USUM':
                tutor_table_offset = temp[1][4]



    #determine if using "ExtractedExeFS" or "exefs"
    exefs_path = ''

    if(os.path.isdir(os.path.join(rom_path, 'ExtractedExeFS'))):
        exefs_path = os.path.join(rom_path, 'ExtractedExeFS')
    elif(os.path.isdir(os.path.join(rom_path, 'exefs'))):
        exefs_path = os.path.join(rom_path, 'exefs')
    else:
        print('Error: no subfolder named ExtractedExeFS or exefs')  
        return

    #look for code.bin or .code.bin

    code_file_path = ''


    if(os.path.exists(os.path.join(exefs_path, 'code.bin'))):
        code_file_path = os.path.join(exefs_path, 'code.bin')
    elif(os.path.exists(os.path.join(exefs_path, '.code.bin'))):
        code_file_path = os.path.join(exefs_path, '.code.bin')
    else:
        print('Error: no subfolder named ExtractedExeFS or exefs')  
        return



    #get entire file starting with offset
    tutor_table_raw = binary_file_read_to_flag(code_file_path, offset = 0)

    #every two bytes is a move
    for line in range(len(tutor_table_raw)//2):
        pokearray.bp_tutor_move_name_list.append(pokearray.move_name_list[from_little_bytes_int(line)])
        
    pokearray.write_array = []*(len(pokearray.personal))


    pokearray.write_array = build_output_array(pokearray)

    
    with open(asksaveasfilename(title='Save Exported Data', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
        writer_head = csv.writer(csvfile, dialect='excel', delimiter=',')

        #write the header line
        writer_head.writerow (['Personal Index', 'Field', 'Data 1', 'Data 2', 'Data 3', 'Data 4'])





main()