from garc_handling import *
from utilities import *
from my_constants import *
from pokemon_data_handling import *
from move_data_handling import *

def get_default_custom_csv(base_name, reference_directory, game = '', dual_bool = False):

    temp_default = []
    temp_custom = []

    temp_default_second = []
    temp_custom_second = []

    #get default
    with open(os.path.join(reference_directory, 'default_' + base_name + (('_' + game) if game !='' else '') + '.csv'), newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)
        if(dual_bool):
            for line in temp:
                if(line[1] != '' or line[0] == '0'):
                    if(line[0][0:2].upper() in {'TM', "HM"}):
                        temp_default.append(line)
                    else:
                        temp_default_second.append(line)
        else:
            for line in temp:
                if(line[1] != '' or line[0] == '0'):
                    temp_default.append(line[1])
    #try to get custom
    try:
        with open(os.path.join(reference_directory, 'custom_' + base_name + '.csv'), newline = '', encoding='utf-8-sig') as csvfile:
            reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
            #load csv into an array      
            temp = list(reader_head)
            if(dual_bool):
                if(line[1] != '' or line[0] == '0'):
                    if(line[0][0:2].upper() in {'TM', "HM"}):
                        temp_custom.append(line)
                    else:
                        temp_custom_second.append(line)
            else:
                for line in temp:
                    if(line[1] != '' or line[0] == '0'):
                        temp_custom.append(line[1])
    #if fail load default
    except:
        print('Loading default_',base_name)
        temp_custom = []




    #return default if custom is very small or they're the same, otherwise custom
    if(dual_bool):
        return(temp_default, temp_default_second if (temp_default == temp_custom or len(temp_custom) <= 10) else temp_custom, temp_custom_second)
    else:
        return(temp_default if (temp_default == temp_custom or len(temp_custom) <= 10) else temp_custom)

def main():
    pokearray = Pokedata()
    
    reference_directory = os.path.join(os.getcwd(),'config and data')

    tutor_table_raw = []

    #get generation
    while True:
        temp = input('Enter Game, (XY, ORAS, SM, USUM)\n').upper()
        if(temp in {'XY', 'ORAS', 'SM', 'USUM'}):
            pokearray.game = temp
            break
        else:
            print(temp, 'is not valid\n\n')
        
    
    pokemon_list_path = os.path.join(reference_directory, 'default_pokemon_list_' + pokearray.game + '.csv')
    
    custom_pokemon_list_path = os.path.join(reference_directory, 'custom_pokemon_list.csv')



    #get default Pokemon names
    with open(pokemon_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != '' or line[0] == '0'):
                pokearray.original_pokemon_name_list.append(line[1])
            else:
                break

    #load custom Pokemon names
    try:
        with open(custom_pokemon_list_path, newline = '', encoding='utf-8-sig') as csvfile:
            reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
            #load csv into an array      
            temp = list(reader_head)

            for line in temp:
                if(line[1] != '' or line[0] == '0'):
                    pokearray.pokemon_name_list.append(line[1])
                else:
                    break
    except:
        pokearray.pokemon_name_list = []
    print('Loaded Pokemon Name List')

    #check if no custom names
    if(len(pokearray.pokemon_name_list) <= 10 or pokearray.original_pokemon_name_list == pokearray.pokemon_name_list):
        #no custom names
        print('No new names detected')
        pokearray.pokemon_name_list = pokearray.original_pokemon_name_list
        pokearray.new_list = [False]*len(pokearray.pokemon_name_list)
    else:
        print('New names detected')
        #see what names are new or not
        for name in pokearray.pokemon_name_list:
            if(name in pokearray.original_pokemon_name_list):
                pokearray.new_list.append(False)
            else:
                pokearray.new_list.append(True)

    #load move names
    pokearray.move_name_list = get_default_custom_csv('move_list', reference_directory).copy()
    print('Loaded Move Name List')

    #load ability names
    pokearray.ability_name_list = get_default_custom_csv('ability_list', reference_directory).copy()
    print('Loaded Ability Name List')

    #load item names
    pokearray.item_name_list = get_default_custom_csv('item_list', reference_directory).copy()
    print('Loaded Item Name List')

    #load TM/HM/Special Tutor names
    pokearray.tm_name_list, pokearray.special_tutor_name_list, _ = get_default_custom_csv('tm_hm_special_tutor_list', reference_directory, pokearray.game, dual_bool = True)
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
    pokearray.egg_path = os.path.join(romfs_path, get_GARC_path('Egg', pokearray.game))
    pokearray.move_path = os.path.join(romfs_path, get_GARC_path('Move', pokearray.game))

    print('Now loading GARCs...')

    #load garcs
    load_GARC(pokearray, pokearray.personal_path, 'Personal')
    load_GARC(pokearray, pokearray.evolution_path, 'Evolution')
    load_GARC(pokearray, pokearray.levelup_path, 'Levelup')
    load_GARC(pokearray, pokearray.egg_path, 'Egg')
    load_GARC(pokearray, pokearray.move_path, 'Move')
    print('GARCs Loaded')

    #in SM/USUM, moves are all in a single file, not each in their own when extracted
    if(pokearray.game == 'XY'):
        pokearray.move = pokearray.move_raw
    else:
        #this includes the empty 0th move
        move_count = from_little_bytes_int(pokearray.move_raw[0][2:4])

        #get the offsets of 0th move and 1st move
        zeroth_address = from_little_bytes_int(pokearray.move_raw[0][4:8])
        first_address = from_little_bytes_int(pokearray.move_raw[0][8:0xC])

        #and from them the length of each block
        move_data_length = first_address - zeroth_address

        #put each block in its own sublist
        for block in range(move_count):
            pokearray.move.append(pokearray.move_raw[0][block*move_data_length + zeroth_address : block*move_data_length + zeroth_address + move_data_length])


    if(pokearray.game in {'ORAS', 'USUM'}):
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


        #get tutor table
        tutor_table_raw = convert_bytes_to_ntuples(binary_file_read_to_flag(code_file_path, offset = tutor_table_offset), 2)
        
        #every two bytes is a move
        for x in tutor_table_raw:
            pokearray.bp_tutor_move_name_list.append(pokearray.move_name_list[x])


            
    pokemon_dump_bool = False
    pokemon_summary_bool = False
    move_dump_bool = False

    #Query what to generate
    while True:
        temp = input('Generate full Pokemon Data dump file? (y/n)\n').lower()
        if(temp in {'y', 'n'}):
            if(temp == 'y'):
                pokemon_dump_bool = True
            break
        else:
            print(temp, 'is not valid\n\n')

    while True:
        temp = input('Generate small Pokemon Data summary table? (y/n)\n').lower()
        if(temp in {'y', 'n'}):
            if(temp == 'y'):
                pokemon_summary_bool = True
            break
        else:
            print(temp, 'is not valid\n\n')

    while True:
        temp = input('Generate Move Data dump file? (y/n)\n').lower()
        if(temp in {'y', 'n'}):
            if(temp == 'y'):
                move_dump_bool = True
            break
        else:
            print(temp, 'is not valid\n\n')





    if(pokemon_dump_bool):
        pokearray.write_array = [[]]*len(pokearray.personal)
        pokearray.evolution_chain_to = [[]]*len(pokearray.personal)
        pokearray.evolution_chain_from = [[]]*len(pokearray.personal)

        pokearray = build_total_output_array(pokearray)

        while True:
            try:
                with open(asksaveasfilename(title='Save Full Pokemon Dump File', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
                    writer_head = csv.writer(csvfile, dialect='excel', delimiter=',')

                    #write the header line
                    writer_head.writerow (['Personal Index', 'Field', 'Data 1', 'Data 2'])

                    for entry in pokearray.write_array:
                        for row in entry:
                            writer_head.writerow(row)
                        writer_head.writerow(['', '', '', ''])
                break
            except Exception as e:
                print(e)

    if(pokemon_summary_bool):
        pokearray.write_array = []

        pokearray = build_summary_output_array(pokearray)

        while True:
            try:
                with open(asksaveasfilename(title='Save Exported Pokemon Summary File', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
                    writer_head = csv.writer(csvfile, dialect='excel', delimiter=',')

                    #write the header line
                    if(pokearray.game in {'XY', 'ORAS'}):
                        header_row = ['Personal Index', 'Name', 'Type 1', 'Type 2', 'HP', 'ATK', 'DEF', 'SpA', 'SpD', 'SPE', '', 'BST', 'ABST', '', 'Ability 1', 'Ability 2', 'Ability 3']
                    else:
                        header_row = ['Personal Index', 'Name', 'Type 1', 'Type 2', 'HP', 'ATK', 'DEF', 'SpA', 'SpD', 'SPE', '', 'BST', 'ABST', '', 'Ability 1', 'Ability 2', 'Ability 3', 'Special Z-Move', 'Z-Crystal', 'Base Move']

                    writer_head.writerow(header_row)

                    for row in pokearray.write_array:
                            writer_head.writerow(row)
                break
            except Exception as e:
                print(e)

    if(move_dump_bool):
        pokearray.write_array = []

        pokearray = build_move_output_array(pokearray)

        while True:
            try:
                with open(asksaveasfilename(title='Save Exported Move Dump File', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
                    writer_head = csv.writer(csvfile, dialect='excel', delimiter=',')

                    #write the header line
                    writer_head.writerow (['Move Index', 'Field', 'Data 1', 'Data 2'])

                    for entry in pokearray.write_array:
                        for row in entry:
                            writer_head.writerow(row)
                        writer_head.writerow(['', '', '', ''])
                break
            except Exception as e:
                print(e)



main()