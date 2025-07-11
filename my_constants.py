version = '1.1'

class Pokedata:
    
    def __init__(self):
        #path variables   
        self.personal_path = ''
        self.levelup_path = ''
        self.evolution_path = ''
        self.egg_path = ''
        self.mega_path = ''

        self.move_path = ''

        #file/game variables
        self.game = ''
        self.max_species_index = 0

        self.personal = []
        self.levelup = []
        self.evolution = []
        self.egg = []
        self.mega = []
        self.ultra = []

        self.move = []
        self.move_raw = []
        
        self.tm_name_list = []
        self.special_tutor_name_list = []

        self.bp_tutor_move_name_list = []
        
        self.pokemon_name_list = []
        self.original_pokemon_name_list = []
        self.new_list = []

        self.move_name_list = []
        self.ability_name_list = []
        self.item_name_list = []

        self.write_array = []

        self.evolution_chain_to = []

        self.evolution_chain_from = []

        self.egg_array = []


type_list = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel','Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy']
egg_group_list = ['','Monster','Water 1 (Amphibious)','Bug','Flying','Field','Fairy','Grass','Humanoid','Water 3 (Aquatic Invertebrate)','Mineral','Amorphous','Water 2 (Piscine)','Ditto','Dragon','Undiscovered',]
color_list = {0x0: 'Red',
              0x1: 'Blue',
              0x2: 'Yellow',
              0x3: 'Green',
              0x4: 'Black',
              0x5: 'Brown',
              0x6: 'Purple',
              0x7: 'Gray',
              0x8: 'White',
              0x9: 'Pink',}

stat_names = ['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed', 'Accuracy', 'Evasion', 'All']

level_curve_list = ['Medium-Fast', 'Erratic', 'Fluctuating', 'Medium-Slow', 'Fast', 'Slow']

evolution_description_phrases = ['None', 'gaining a level with high Friendship', 'gaining a level during the day', 'gaining a level during the night', 'gaining a level', 'trading', 'trading while holding a ', 'trade for the opposite Shelmet/Karrablast', 'using a ', 'gaining a level while Attack > Defense', 'gaining a level while Attack = Defense', 'gaining a level while Attack < Defense', 'gaining a level, depending on PID', 'gaining a level, depending on PID', 'gaining a level, also a Shedinja appears', 'gaining a level, also a Shedinja appears', 'gaining a level while having Beauty of at least ', 'being male while using a ', 'being female while using a ', 'gaining a level during the day while holding a ', 'gaining a level during the night while holding a ', 'gaining a level while knowing ', 'gaining a level in the same party as a ', 'gaining a level while being male', 'gaining a level while being female', 'gaining a level in a strong magnetic field', 'gaining a level in a dense forest', 'gaining a level in the freezing cold', 'gaining a level while upside down', 'gaining a level with high Affection and knowing a ', 'gaining a level while in the same party as a ', 'gaining a level in the rain', 'gaining a level during the day', 'gaining a level during the night', 'gaining a level while being female', 'UNUSED', 'gaining a level in ', 'gaining a level during the day in ', 'gaining a level during the night in ', 'gaining a level at Mount Lanakila', 'gaining a level during twilight', 'gaining a level in Ultra Space', 'in Ultra Space, using a ']

evolution_parameter_types = ['', '', '', '', '', '', 'item', '', 'item', '', '', '', '', '', '', '', 'beauty', 'item', 'item', 'item', 'item', 'move', 'pokemon', '', '', '', '', '', '', 'type-move', 'type-Pokemon', '', '', '', '', '', 'game', 'game', 'game', '', '', '', 'item']

pokemon_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']

pokemon_versions = {32: "Ultra Sun",
                    33: "Ultra Moon"
                    }

move_categories = ['Status', 'Physical', 'Special']

move_targeting = ['Single Adjacent', 'Any Ally (including self)', 'Any Ally (excluding self)', 'Single Foe', 'All Adjacent', 'All Foes', 'All Allies (including self)', 'Self', 'All (including self)', 'Random Foe', 'Entire Field', 'Opponent Field', 'User Field', 'Self (counter moves)']

z_move_effects = ['', '+1 ATK', '+2 ATK', '+3 ATK', '+1 DEF', '+2 DEF', '+3 DEF', '+1 SPATK', '+2 SPATK', '+3 SPATK', '+1 SPDEF', '+2 SPDEF', '+3 SPDEF', '+1 SPE', '+2 SPE', '+3 SPE', '+1 ACC', '+2 ACC', '+3 ACC', '+1 EVA', '+2 EVA', '+3 EVA', '+1 to all (except ACC/EVA)', '+2 to all (except ACC/EVA)', '+3 to all (except ACC/EVA)', '+2 CRIT', 'Reset user lowered stats', 'Recover user HP', 'Recovers HP of Pokémon switching in', 'Makes user center of attention', 'Recovers HP if the user is a Ghost type, +1 ATK otherwise']

status_conditions = ['None', 'Paralyze', 'Sleep', 'Freeze', 'Burn', 'Poison', 'Confusion', 'Attract', 'Capture', 'Nightmare', 'Curse', 'Taunt', 'Torment', 'Disable', 'Yawn', 'Heal Block', 'Protected', 'Detected', 'Leech Seed', 'Embargo', 'Perish Song', 'Ingrain', 'Cannot Switch', 'Encore', 'Mute', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Grounded', 'Telekinesis', 'Unknown', 'Unknown', 'Aqua Ring', 'Unknown', 'Unknown', 'Unknown', 'Unknown']

flag_array = ['Contact', 'Charge', 'Recharge', 'Ignores Protect', 'Magic Bounce/Coat', 'Snatchable', 'Mirror Moveable', 'Punch', 'Sound', 'Gravity Disables', 'Defrosts User', 'Any Target Triple', 'Healing', 'Ignores Substitute', 'Fails Sky Battle', 'Animates Ally', 'Dance', 'Slicing', 'Biting', 'Bulletproof', 'Mega Launcher', 'Wind', 'Light']