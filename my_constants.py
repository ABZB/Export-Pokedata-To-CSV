version = '1.1'

class Pokedata:
    
    def __init__(self):
        #path variables   
        self.personal_path = ''
        self.levelup_path = ''
        self.evolution_path = ''
        self.egg_path = ''
        self.mega_path = ''

        #file/game variables
        self.game = ''
        self.max_species_index = 0

        self.personal = []
        self.levelup = []
        self.evolution = []
        self.egg = []
        self.mega = []
        self.ultra = []
        
        self.tm_name_list = []
        self.special_tutor_name_list = []

        self.bp_tutor_move_name_list = []
        
        self.pokemon_name_list = []
        self.original_pokemon_name_list = []
        self.move_name_list = []
        self.ability_name_list = []
        self.item_name_list = []

        self.write_array = []



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

stat_names = ['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']

level_curve_list = ['Medium-Fast', 'Erratic', 'Fluctuating', 'Medium-Slow', 'Fast', 'Slow']

evolution_description_phrases = ['None', 'gaining a level with high Friendship', 'gaining a level during the day', 'gaining a level during the night', 'gaining a level', 'trading', 'trading while holding a ', 'trade for the opposite Shelmet/Karrablast', 'using a ', 'gaining a level while Attack > Defense', 'gaining a level while Attack = Defense', 'gaining a level while Attack < Defense', 'gaining a level, depending on PID', 'gaining a level, depending on PID', 'gaining a level, also a Shedinja appears', 'gaining a level, also a Shedinja appears', 'gaining a level while having Beauty of at least ', 'being male while using a ', 'being female while using a ', 'gaining a level during the day while holding a ', 'gaining a level during the night while holding a ', 'gaining a level while knowing ', 'gaining a level in the same party as a ', 'gaining a level while being male', 'gaining a level while being female', 'gaining a level in a strong magnetic field', 'gaining a level in a dense forest', 'gaining a level in the freezing cold', 'gaining a level while upside down', 'gaining a level with high Affection and knowing a ', 'gaining a level while in the same party as a ', 'gaining a level in the rain', 'gaining a level during the day', 'gaining a level during the night', 'gaining a level while being female', 'UNUSED', 'gaining a level in ', 'gaining a level during the day in ', 'gaining a level during the night in ', 'gaining a level at Mount Lanakila', 'gaining a level during twilight', 'gaining a level in Ultra Space', 'in Ultra Space, using a ']

evolution_parameter_types = ['', '', '', '', '', '', 'item', '', 'item', '', '', '', '', '', '', '', 'beauty', 'item', 'item', 'item', 'item', 'move', 'pokemon', '', '', '', '', '', '', 'type-move', 'type-Pokemon', '', '', '', '', '', 'game', 'game', 'game', '', '', '', 'item']

pokemon_types = ['Normal', 'Fighting', 'Flying', 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel', 'Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice', 'Dragon', 'Dark', 'Fairy']

pokemon_versions = {32: "Ultra Sun",
                    33: "Ultra Moon"
                    }