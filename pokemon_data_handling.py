from utilities import *
from my_constants import *

def make_eggs_list(pokearray, underlying_source_index = 0, ):
    pokearray.egg_array = [[] for _ in range(len(pokearray.personal))]

    #build stage 1
    for index, pokemon_data in enumerate(pokearray.write_array):

        #Egg Moves. 
        #if is a base forme, same as index
        egg_index = 0
        if(index <= pokearray.max_species_index):
            egg_index = index
        #XY/ORAS have all formes share the same egg move file
        elif(pokearray.game in {'XY', 'ORAS'}):
            #this gets the base species index from
            egg_index = int(pokemon_data[1][2])
        #otherwise we need to get the first two bytes of the base forme's egg move file, this is the pointer to the first alt forme's file. add (forme number - 1) to that to get correct file, IF IT EXISTS
        else:
            temp_value = from_little_bytes_int(pokearray.egg[int(pokemon_data[1][2])][0:2])

            if(temp_value == int(pokemon_data[1][2]) or temp_value == 0):
                pass
            else:
                egg_index = temp_value + int(pokemon_data[2][2]) - 1

                #if the pointer in the new file is wrong, no eggs
                if(from_little_bytes_int(pokearray.egg[egg_index][0:2]) != temp_value):
                    egg_index = 0


        #if length is 4 or less, than it has no actual egg moves

        if(len(pokearray.egg[egg_index]) <= 4 or egg_index == 0):
            pass
        else:
            #each move is 2 bytes. in XY/ORAS first two bytes are count of egg moves. In SM/USUM before those bytes are the pointer to the alt forme egg move file
            temp_egg = []
            for x in range((2 if pokearray.game in {'XY', 'ORAS'} else 4), len(pokearray.egg[egg_index]), 2):
                temp_egg.append([index, 'Egg Move', '', pokearray.move_name_list[from_little_bytes_int(pokearray.egg[egg_index][x:x + 2])]])

            pokearray.egg_array[index] = temp_egg

    #remove duplicates from the evolution chain lists (happens from having multiple evo methods)

    for x in pokearray.evolution_chain_to:
        x = list(set(x))

    for x in pokearray.evolution_chain_from:
        x = list(set(x))


    #build list of Pokemon that actually evolve at all
    iter_table = []
    for x, evo_to_table in enumerate(pokearray.evolution_chain_to):
        if(len(evo_to_table) != 0):
            iter_table.append(x)

    last_value = 0
    no_remove_bool = False
    while True:
        to_remove = []

        print(len(iter_table),'Pokemon that evolve')

        for current_index in iter_table:
            no_remove_bool = False
            #if no egg moves, go to next pokemon
            if(len(pokearray.egg_array[current_index]) == 0):
                continue
            #if this Pokemon has any Pokemon it evolves from that haven't been finished yet, if so go to next
            if(len(pokearray.evolution_chain_from[current_index]) != 0):
                no_remove_bool = True

            print(current_index,'evolves to', pokearray.evolution_chain_to[current_index])

            #iterate over all Pokemon it evolves into
            for target_index in pokearray.evolution_chain_to[current_index]:
                temp = []
                #for each egg move it has
                for move_line in pokearray.egg_array[current_index]:
                    #print(move_line)
                    #check to see if evolved form already has it
                    temp_bool = True
                    for other_move_line in pokearray.egg_array[target_index]:
                        if(move_line[2] == other_move_line[2]):
                            temp_bool = False
                            break
                    #if it doesn't, append it
                    if(temp_bool):
                        
                        temp.append([target_index, move_line[1], move_line[2], move_line[3]])
                for x in temp:
                    pokearray.egg_array[target_index].append(x)

                #remove the current Pokemon from list of Pokemon target evolves from
                if(no_remove_bool is False):
                    try:
                        pokearray.evolution_chain_from[target_index].remove(current_index)
                    except:
                        pass
                    #remove target pokemon from list of Pokemon current pokemon evolves to
                    pokearray.evolution_chain_to[current_index].remove(target_index)
            if(no_remove_bool is False):
                #build list of the pokemon we did
                try:
                    to_remove.append(current_index)
                except:
                    pass
        #remove the completed elements
        for x in to_remove:
            try:
                iter_table.remove(x)
            except:
                pass

        if(len(iter_table) == 0):
            if(len(pokearray.evolution_chain_from) == len(pokearray.evolution_chain_to)):
                break
            else:
                print('error', len(pokearray.evolution_chain_from), len(pokearray.evolution_chain_to))
        elif(len(iter_table) == last_value):
            print('infinite loop detected, breaking')
            break
        else:
            last_value = len(iter_table)
        
    #now we need to eliminate duplicates
    for egg_move_list in pokearray.egg_array:
        tupled_lst = set(map(tuple, egg_move_list))
        egg_move_list = map(list, tupled_lst)


    #and finally append
    for index, entry in enumerate(pokearray.write_array):
        #write array does not record pokemon 0, so it ends up off-by-one
        entry.extend(pokearray.egg_array[index])

    return(pokearray)

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
        temp_array.append([index, 'Name', pokearray.pokemon_name_list[index]])


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
            temp_array.append([index, 'Base Index', index])
        else:
            temp_array.append([index, 'Base Index', base_index])
        
        temp_array.append([index, 'Forme Index', forme_number])


        temp_array.append([index, 'Is New', str(pokearray.new_list[index])])
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

        temp_from = []
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

                #build array of indices this index evolves to
                temp_from.append(index_number)
                

                temp_array.append([index, 'Evolves From', pokearray.pokemon_name_list[index_number], output_phrase])
        pokearray.evolution_chain_from[index] = temp_from
        #Evolve to
        file = pokearray.evolution[index]
        temp_to = []
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

            #build array of indices this index evolves to
            temp_to.append(evo_target_index)

            temp_array.append([index, 'Evolves To', pokearray.pokemon_name_list[evo_target_index], output_phrase])
        pokearray.evolution_chain_to[index] = temp_to

        #put the fully built pokemon output thing into its place
        pokearray.write_array[index] = temp_array

        #Check if in a subcall for alt forme
        if(base_index != 0):
            return(pokearray)
        #added final non-alt forme (alt formes of that base forme were branched to above)
        elif(index == least_alt_index - 1):
            pokearray.max_species_index = index
            break
        #otherwise increment index by 1 and do next loop
        else:
            index += 1

    make_eggs_list(pokearray)

    return(pokearray)

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
