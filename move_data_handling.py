from utilities import *
from my_constants import *

def build_move_output_array(pokearray):

    for move_index, move_block in enumerate(pokearray.move):
        temp_array = []

        #move name
        try:
            temp_array.append([move_index, 'Name', pokearray.move_name_list[move_index]])
        except Exception as e:
            print(e)
            break
        #Category
        temp_array.append([move_index, 'Category', move_categories[move_block[2]]])

        #Type
        temp_array.append([move_index, 'Type', pokemon_types[move_block[0]]])

        #Targeting
        temp_array.append([move_index, 'Targeting', move_targeting[move_block[0x14]]])

        #Base power
        temp_array.append([move_index, 'Base Power', '' if move_block[3] == 0 else move_block[3]])

        #Accuracy
        temp_array.append([move_index, 'Accuracy', str(move_block[4]) + '%' if move_block[4] <= 100 else 'Cannot Miss'])

        #PP
        temp_array.append([move_index, 'PP', move_block[5]])

        #Priority
        if(move_block[6] != 0):
            temp_array.append([move_index, 'Priority', '+' + str(move_block[6]) if move_block[6] <= 156 else str(move_block[6] - 256)])


        #Min Hits & Max Hits
        min_hits = move_block[7] & 0xF
        max_hits = (move_block[7] >> 4) & 0xF

        if(max_hits != 0):
            temp_array.append([move_index, 'Min Hits', min_hits])
            temp_array.append([move_index, 'Max Hits', max_hits])

        #Status
        if(move_block[8] != 0):
            temp_array.append([move_index, 'Status', status_conditions[move_block[8]]])

            #Chance to inflict Status
            temp_array.append([move_index, 'Status %', '' if move_block[8] == 0 else (str(move_block[8] if move_block[2] != 0 else 100) + '%')])

            #Min & Max Effect turns
            min_turns = move_block[0XC] & 0xF
            max_turns = move_block[0xD] & 0xF

            if(max_turns != 0):
                temp_array.append([move_index, 'Min Turns', min_hits])
                temp_array.append([move_index, 'Max Turns', max_hits])

        #Crit stage
        temp_array.append([move_index, 'Crit Stage', move_block[0xE]])

        #Flinch %
        if(move_block[0xF] != 0):
            temp_array.append([move_index, 'Flinch %', str(move_block[0xF]) + '%'])

        #Drain/Recoil %
        if(move_block[0x12] > 156):
            temp_array.append([move_index, 'Recoil', str(move_block[0x12] - 256) + '%'])
        elif(move_block[0x12] > 0):
            temp_array.append([move_index, 'Drain', str(move_block[0x12]) + '%'])

        #Heal %
        if(move_block[0x14] > 156):
            temp_array.append([move_index, 'Damage', str(move_block[0x12] - 256) + '%'])
        elif(move_block[0x13] > 0):
            temp_array.append([move_index, 'Heal', str(move_block[0x12]) + '%'])

        #Stats to raise
        for x in range(3):
            if(move_block[0x15 + x] == 0):
                break
            temp_stage = -1
            if(move_block[0x18 + x] > 6):
                temp_stage = str(move_block[0x18 + x] - 256)
            elif(move_block[0x18 + x] != 0):
                temp_stage = '+' + str(move_block[0x18 + x])
                
            temp_array.append([move_index, 'Altered Stat ' + str(x + 1), stat_names[move_block[0x15 + x]], temp_stage])

        #Chance of Stat change (first one is only one that matters)
        if(move_block[0x15 + x] != 0):
            temp_array.append([move_index, 'Stat Change %', '' if move_block[0x1B] == 0 else (str(move_block[0x1B] if move_block[2] != 0 else 100) + '%')])
        

        #Flags

        #in gen 7, flag is 6 bytes later to make room for Z-moves (4 bytes) and Refresh Afflictions (2 bytes)
        flag_offset = (0x1E if pokearray.game in {'XY', 'ORAS'} else 0x24)

        bit_count = 0
        for bit_flag_byte in range(0x4):
            byte_flag = move_block[bit_flag_byte + flag_offset]

            for bit in range(8):
                if((bit_count == 3 and (byte_flag >> bit) & 0x1 == 0) or (bit_count != 3 and (byte_flag >> bit) & 0x1 == 1)):
                    temp_array.append([move_index, 'Flag', flag_array[bit_count]])
                bit_count += 1
            
        #Z-moves
        if(pokearray.game in {'SM', 'USUM'}):
            temp_array.append([move_index, 'Z-Move', 'Z-' + pokearray.move_name_list[move_index] if from_little_bytes_int(move_block[0x1E:0x20]) == 0 else pokearray.move_name_list[from_little_bytes_int(move_block[0x1E:0x20])]])
            temp_array.append([move_index, 'Z-Move BP', '' if move_block[0x20] == 0 else move_block[0x20]])
            if(move_block[0x21] != 0):
                temp_array.append([move_index, 'Z-Move Additional Effect', z_move_effects[move_block[0x21]]])


        pokearray.write_array.append(temp_array)

    return(pokearray)
