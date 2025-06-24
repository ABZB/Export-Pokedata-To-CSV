from garc_handling import *
from utilities import *
from my_constants import *

def build_total_output_array(pokearray, base_index = 0, target_index = 0, forme_number = 0):

    #iterate over all files
    index = target_index
    least_alt_index = 0xFFFF


    while True:
        temp_array = []
        #don't record index 0
        if(index == 0):
            index += 1
            continue

        #get the local personal file
        personal = pokearray.personal[index]



        #Species/Forme Name
        temp_array.append([index, 'Name',pokearray.pokemon_name_list[index]])

        #check if has any alt formes. target index is 0 in main call
        if(target_index == 0):
            #check for alt formes
            temp_index = from_little_bytes_int(personal[0x1C:0x1E])

            #if it's not 0, handle all of the alt formes now
            if(temp_index != 0):
                for alt_forme_numbers in range(personal[0x20] - 1):
                    pokearray = build_total_output_array(pokearray, index, temp_index + alt_forme_numbers, alt_forme_numbers + 1)
                #this will ultimately find the personal file of the least-indexed alt forme, before it is reached, to handle exiting at the proper time
                if(temp_index < least_alt_index):
                    least_alt_index = temp_index
            
        print('Now compiling ' + str(index) + ': ' + pokearray.pokemon_name_list[index])
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
        temp_array.append([index, 'Type 1', pokemon_types[personal[6]]])
        if(personal[6] ==  personal[7]):
            temp_array.append([index, 'Type 2', ''])
        else:
            temp_array.append([index, 'Type 2', pokemon_types[personal[7]]])
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

        #Egg Groups
        for x in range(2):
            temp_array.append([index, 'Egg Group ' + str(x + 1), egg_group_list[personal[0x16 + x]]])

        #Color
        temp_array.append([index, 'Color', color_list[0xF & personal[0x21]]])

        #Gender Ratio
        gender_report = ''
        match personal[0x12]:
            case 255:
                gender_report = 'Other'
            case 254:
                gender_report = '100% Female'
            case 0:
                gender_report = '100% Male'
            case _:
                per_female = int(100*personal[0x12]/255)
                gender_report = str(100 - per_female) + '% Male/' + str(per_female) + '% Female'
        temp_array.append([index, 'Gender Ratio', gender_report])

        #Friendship
        temp_array.append([index, 'Base Friendship', personal[0x14]])

        #Level Curve
        temp_array.append([index, 'Level Curve', level_curve_list[personal[0x15]]])

        #Base Exp
        temp_array.append([index, 'Base Experience', from_little_bytes_int(personal[0x22:0x24])])

        #Hatch Cycle
        temp_array.append([index, 'Hatch Cycles', personal[0x13]])

        #Height (decimeters)
        temp_array.append([index, 'Height', from_little_bytes_int(personal[0x24:0x26])])

        #Weight (decimeters)
        temp_array.append([index, 'Weight', from_little_bytes_int(personal[0x24:0x26])])
        
        #Special Z-Move
        if(pokearray.game in {'SM', 'USUM'}):
            if(from_little_bytes_int(personal[0x4C:0x4E]) != 0):
                #Z-Crystal
                temp_array.append([index, 'Z-Crystal', pokearray.item_name_list[from_little_bytes_int(personal[0x4C:0x4E])]])

                #Base Move
                temp_array.append([index, 'Base Move', pokearray.move_name_list[from_little_bytes_int(personal[0x4E:0x50])]])

                #Z-Move
                temp_array.append([index, 'Z-Move', pokearray.move_name_list[from_little_bytes_int(personal[0x50:0x52])]])


        #Level up moves
        current_personal = pokearray.levelup[index]
        #each entry in level up is 4 bytes
        for line_offset in range(0, len(current_personal), 4):

            if(current_personal[line_offset + 2] == 0xFF):
                pass
            else:
                temp_array.append([index, 'Level Up', 'Evolve' if current_personal[line_offset + 2] == 0 else current_personal[line_offset + 2], pokearray.move_name_list[from_little_bytes_int(current_personal[line_offset:line_offset + 2])]])
            
        #TM/HM 1-100, HM 1-8
        bit_count = 0
        for offset in range(14):
            byte_value = personal[0x28 + offset]

            #iterate through the bits of current byte
            for bit_position in range(8):
                #check if this bit is 1
                if(byte_value & (1 << bit_position) == (1 << bit_position)):
                    #Index, TM/HM, [TM][HM] XXX, move name
                    try:
                        temp_array.append([index, 'TM/HM', pokearray.tm_name_list[bit_count][0], pokearray.tm_name_list[bit_count][1]])
                    except:
                        pass
                bit_count += 1

        #Special Tutors
        bit_count = 0

        #iterate through the bits of current byte
        for bit_position in range(8):
            #check if this bit is 1
            if(personal[0x35] & (1 << bit_position) == (1 << bit_position)):
                #Index, TM/HM, Tutor Name, move name
                temp_array.append([index, 'Move Tutor', pokearray.special_tutor_name_list[bit_count][0], pokearray.special_tutor_name_list[bit_count][1]])
            bit_count += 1

        #finally the BP move tutors. Depends on ORAS or USUM

        if(pokearray.game == 'ORAS'):
            bit_count = 0
            #ORAS jumps around a little
            for offset in [0X40, 0X41, 0X44, 0X45, 0X46, 0X48, 0X49, 0X4C, 0X4D]:
                byte_value = personal[0x40 + offset]

                #iterate through the bits of current byte
                for bit_position in range(8):
                    #check if this bit is 1
                    if(byte_value & (1 << bit_position) == (1 << bit_position)):
                        #Index, Move Tutor, Tutor #, move name
                        temp_array.append([index, 'Move Tutor', 1 if bit_count <= 15 else 2 if bit_count <= 31 else 3 if bit_count <= 48 else 4, pokearray.bp_tutor_move_name_list[bit_count]])
                    bit_count += 1

        #todo for USUM open shop.cro, grab the relocation patch values for the 4 tutors and the table of lengths, and use that instead of hardcoded table

        elif(pokearray.game == 'USUM'):
            bit_count = 0
            for offset in range(9):
                byte_value = personal[0x40 + offset]

                #iterate through the bits of current byte
                for bit_position in range(8):
                    #check if this bit is 1
                    if(byte_value & (1 << bit_position) == (1 << bit_position)):
                        #Index, TM/HM, [TM][HM] XXX, move name
                        temp_array.append([index, 'Move Tutor', 'Big Wave Beach' if bit_count <= 15 else 'Heahea Beach' if bit_count <= 31 else "Ula'ula Beach" if bit_count <= 48 else 'Battle Tree', pokearray.bp_tutor_move_name_list[bit_count]])
                    bit_count += 1




        #Egg Moves
        #if is a base forme, same as index
        egg_index = 0
        if(base_index == 0):
            egg_index = index
        #XY/ORAS have all formes share the same egg move file
        elif(pokearray.game in {'XY', 'ORAS'}):
            egg_index = base_index
        #otherwise we need to get the first two bytes of the base forme's egg move file, this is the pointer to the first alt forme's file. add (forme number - 1) to that to get correct file, IF IT EXISTS
        else:
            temp_value = from_little_bytes_int(pokearray.egg[base_index][0:2])

            if(temp_value == base_index or temp_value == 0):
                pass
            else:
                egg_index = temp_value + forme_number - 1

                #if the pointer in the new file is wrong, no eggs
                if(from_little_bytes_int(pokearray.egg[egg_index][0:2]) != temp_value):
                    egg_index = 0


        #if length is 4 or less, than it has no actual egg moves

        if(len(pokearray.egg[egg_index]) <= 4 or egg_index == 0):
            pass
        else:
            #each move is 2 bytes. in XY/ORAS first two bytes are count of egg moves. In SM/USUM before those bytes are the pointer to the alt forme egg move file
            for x in range((2 if pokearray.game in {'XY', 'ORAS'} else 4), len(pokearray.egg[egg_index]), 2):
                temp_array.append([index, 'Egg Move', '', pokearray.move_name_list[from_little_bytes_int(pokearray.egg[egg_index][x:x + 2])]])




        #Evolve From

        #0x0 - Evolution type
        #0x1 - unused
        #0x2 - other parameter low byte
        #0x3 - other parameter high byte
        #0x4 - target species low byte
        #0x5 - target species high byte
        
        #Gen 7 only
        #0x6 - Target forme (FF is preserve current)
        #0x7 - Level (0 is "NA")

        #set values depending on generation
        line_length = 6 if pokearray.game in ('XY', 'ORAS') else 8
        for index_number, file in enumerate(pokearray.evolution):
            for offset in range(0, 8*line_length, line_length):
                evolve_to_index = from_little_bytes_int(file[offset + 4:offset + 6])
                
                method = file[offset]

                
                evolve_from_index = index_number
                found_one = False
                #exit this for loop if we have an empty entry
                if(evolve_to_index == 0):
                    break
                #evolves to us given match in species in following cases:
                #Target is forme 1, has evo method 34
                #gen 7 and byte 6 matches target forme
                #target and source have same forme and either is gen 6 or byte 0x6 is -1
                #Shedinja is special, the listed Pokemon in the GARC is only Ninjask, Shedinja is generated automatically
                elif((evolve_to_index == index) or (evolve_to_index == base_index) or (max(index, base_index) == 292 and method in {0xE, 0xF})):
                    if(forme_number == 1 and method == 0x22):
                        found_one = True
                    if(pokearray.game in {'SM', 'USUM'}):
                        #get target forme byte
                        if(forme_number == file[offset + 0x6]):
                            found_one = True
                    #get source forme
                    temp_pointer = from_little_bytes_int(pokearray.personal[index_number][0x1C:0x1E])
                    source_forme = 0
                    
                    if(index_number >= temp_pointer and temp_pointer != 0):
                        source_forme = index_number - temp_pointer + 1
                        #find the base forme's index
                        for x in range(1, temp_pointer, 1):
                            if(from_little_bytes_int(pokearray.personal[x][0x1C:0x1E]) == temp_pointer):
                                evolve_from_index = x
                                break


                    if(source_forme == forme_number):
                        if(pokearray.game in {'XY', 'ORAS'}):
                            found_one = True
                        elif(0xFF == file[offset + 0x6]):
                                found_one = True
                if(found_one):
                    pass
                else:
                    continue
                #write evolves from line
                #index, "Evolves From", source name, long description

                parameter_phrase = ''
                level_phrase = ''
                parameter_index = from_little_bytes_int(file[offset + 2:offset + 4])


                match evolution_parameter_types[method]:
                    case '':
                        pass
                    case 'item':
                        parameter_phrase = pokearray.item_name_list[parameter_index]
                    case 'move':
                        parameter_phrase = pokearray.move_name_list[parameter_index]
                    case 'pokemon':
                        parameter_phrase = pokearray.pokemon_name_list[parameter_index]
                    case 'beauty':
                        parameter_phrase = str(parameter_index)
                    case _:
                        parameter_phrase = pokemon_types[parameter_index] + '-Type Move' if evolution_parameter_types[method] == 'type-move' else '-Type Pokemon'


                if(pokearray.game in {'XY', 'ORAS'} and evolution_parameter_types[method] == '' and parameter_index != 0):
                    level_phrase = ', while at least Level ' + str(parameter_index)
                elif(pokearray.game in {'SM', 'USUM'}):
                    if(file[offset + 7] != 0):
                        level_phrase = ', while at least Level ' + str(file[offset + 7])


                output_phrase = 'Evolves from ' + pokearray.pokemon_name_list[index_number] + ' by ' + evolution_description_phrases[method] + parameter_phrase + level_phrase

                temp_array.append([index, 'Evolves From', pokearray.pokemon_name_list[index_number], output_phrase])

        #Evolve to
        file = pokearray.evolution[index]
        for offset in range(0, 8*line_length, line_length):
            evolve_to_index = from_little_bytes_int(file[offset + 4:offset + 6])
                

            #exit this for loop if we have an empty entry
            if(evolve_to_index == 0):
                break
            #write evolves from line
            #index, "Evolves From", source name, long description

            parameter_phrase = ''
            level_phrase = ''
            parameter_index = from_little_bytes_int(file[offset + 2:offset + 4])

            
            method = file[offset]

            #get real Personal number 
            #first get target forme number
            target_forme = 0
            #in gen 6, it's either 1 for meowstic special method, or matches current forme
            if(method == 0x22):
                target_forme = 1
            elif(pokearray.game in {'XY', 'ORAS'}):
                target_forme = forme_number
            elif(file[offset + 0x6] == 0xFF):
                target_forme = forme_number
            else:
                target_forme = file[offset + 0x6]

            #get evolve-to forme pointer
            if(target_forme != 0):
                evo_target_index = from_little_bytes_int(pokearray.personal[evolve_to_index][0x1C:0x1E]) + target_forme - 1
            else:
                evo_target_index = evolve_to_index

            match evolution_parameter_types[method]:
                case '':
                    pass
                case 'item':
                    parameter_phrase = pokearray.item_name_list[parameter_index]
                case 'move':
                    parameter_phrase = pokearray.move_name_list[parameter_index]
                case 'pokemon':
                    parameter_phrase = pokearray.pokemon_name_list[parameter_index]
                case 'beauty':
                    parameter_phrase = str(parameter_index)
                case _:
                    parameter_phrase = pokemon_types[parameter_index] + '-Type Move' if evolution_parameter_types[method] == 'type-move' else '-Type Pokemon'


            if(pokearray.game in {'XY', 'ORAS'} and evolution_parameter_types[method] == '' and parameter_index != 0):
                level_phrase = ', while at least Level ' + str(parameter_index)
            elif(pokearray.game in {'SM', 'USUM'}):
                if(file[offset + 7] != 0):
                    level_phrase = ', while at least Level ' + str(file[offset + 7])


            output_phrase = 'Evolves to ' + pokearray.pokemon_name_list[evo_target_index] + ' by ' + evolution_description_phrases[method] + parameter_phrase + level_phrase

            temp_array.append([index, 'Evolves To', pokearray.pokemon_name_list[evo_target_index], output_phrase])

        #put the fully built pokemon output thing into its place
        pokearray.write_array[index] = temp_array

        #Check if in a subcall for alt forme or if added final non-alt forme (alt formes of that base forme were branched to above)
        if(base_index != 0 or (index == least_alt_index - 1)):
            return(pokearray)
        #otherwise increment index by 1 and do next loop
        else:
            index += 1

def build_summary_output_array(pokearray):

    for index, personal in enumerate(pokearray.personal):
        temp_array = []
        if(index == 0):
            continue

        #index
        temp_array.append(index)

        #Species/Forme Name
        temp_array.append(pokearray.pokemon_name_list[index])

        #Types
        temp_array.append(pokemon_types[personal[6]])
        if(personal[6] ==  personal[7]):
            temp_array.append('')
        else:
            temp_array.append(pokemon_types[personal[7]])


        #Stats
        temp_array.append(personal[0])
        temp_array.append(personal[1])
        temp_array.append(personal[2])
        temp_array.append(personal[4])
        temp_array.append(personal[5])
        temp_array.append(personal[3])

        temp_array.append('')

        #BST
        bst = 0
        for x in range(6):
            bst += personal[x]

        abst = bst - min(personal[1], personal[4])
        temp_array.append(bst)
        temp_array.append(abst)


        temp_array.append('')

        #Abilities
        for x in range(3):
            temp_array.append(pokearray.ability_name_list[personal[0x18 + x]])

        
        #Special Z-Move
        if(pokearray.game in {'SM', 'USUM'}):
            if(from_little_bytes_int(personal[0x4C:0x4E]) != 0):

                
                #Z-Move
                temp_array.append(pokearray.move_name_list[from_little_bytes_int(personal[0x50:0x52])])

                #Z-Crystal
                temp_array.append(pokearray.item_name_list[from_little_bytes_int(personal[0x4C:0x4E])])

                #Base Move
                temp_array.append(pokearray.move_name_list[from_little_bytes_int(personal[0x4E:0x50])])


        #put the fully built pokemon output thing into its place
        pokearray.write_array.append(temp_array)

    return(pokearray)


def main():
    pokearray = Pokedata()
    
    reference_directory = os.path.join(os.getcwd(),'config and data')
    move_list_path = os.path.join(reference_directory, 'move_list.csv')
    ability_list_path = os.path.join(reference_directory, 'ability_list.csv')
    item_list_path = os.path.join(reference_directory, 'item_list.csv')
    tm_list_path = os.path.join(reference_directory, 'tm_hm_special_tutor_list.csv')

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



    #get default names
    with open(pokemon_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != '' or line[0] == '0'):
                pokearray.original_pokemon_name_list.append(line[1])
            else:
                break

    #load custom names
    with open(custom_pokemon_list_path, newline = '', encoding='utf-8-sig') as csvfile:
        reader_head = csv.reader(csvfile, dialect='excel', delimiter=',')
        
        #load csv into an array      
        temp = list(reader_head)

        for line in temp:
            if(line[1] != '' or line[0] == '0'):
                pokearray.pokemon_name_list.append(line[1])
            else:
                break

    print('Loaded Pokemon Name List')

    #check if no custom names
    if(len(pokearray.original_pokemon_name_list) <= 10 or pokearray.original_pokemon_name_list == pokearray.pokemon_name_list):
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
                if(line[0][0:2].upper() in {'TM', "HM"}):
                    pokearray.tm_name_list.append(line)
                else:
                    pokearray.special_tutor_name_list.append(line)
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

    print('Now loading GARCs...')

    #load garcs
    load_GARC(pokearray, pokearray.personal_path, 'Personal')
    load_GARC(pokearray, pokearray.evolution_path, 'Evolution')
    load_GARC(pokearray, pokearray.levelup_path, 'Levelup')
    load_GARC(pokearray, pokearray.egg_path, 'Egg')


    print('GARCs Loaded')

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


            
    dump_bool = False
    summary_bool = False

    #Query what to generate
    while True:
        temp = input('Generate full dump file? (y/n)\n').lower()
        if(temp in {'y', 'n'}):
            if(temp == 'y'):
                dump_bool = True
            break
        else:
            print(temp, 'is not valid\n\n')

    while True:
        temp = input('Generate small summary table? (y/n)\n').lower()
        if(temp in {'y', 'n'}):
            if(temp == 'y'):
                summary_bool = True
            break
        else:
            print(temp, 'is not valid\n\n')





    if(dump_bool):
        pokearray.write_array = [[]]*(len(pokearray.personal))

        pokearray = build_total_output_array(pokearray)

        while True:
            try:
                with open(asksaveasfilename(title='Save Full Dump File', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
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

    if(summary_bool):
        pokearray.write_array = []

        pokearray = build_summary_output_array(pokearray)

        while True:
            try:
                with open(asksaveasfilename(title='Save Exported Data', defaultextension='.csv',filetypes= [('CSV','.csv')]), 'w', newline = '', encoding='utf-8-sig') as csvfile:
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



main()