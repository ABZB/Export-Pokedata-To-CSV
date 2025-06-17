version = '3.1'

class Pokedata:
    
    def __init__(self):
        #path variables   
        self.personal_path = ''
        self.levelup_path = ''
        self.evolution_path = ''
        self.egg_path = ''

        #file/game variables
        self.game = ''
        self.max_species_index = 0

        self.personal = []
        self.levelup = []
        self.evolution = []
        self.egg = []
        
        self.tm_name_list = []
        self.hm_name_list = []
        self.special_tutor_name_list = []

        self.bp_tutor_move_name_list = []
        
        self.pokemon_name_list = []
        self.move_name_list = []
        self.ability_name_list = []
        self.item_name_list = []

        self.write_array = []



type_list = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel','Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy']
egg_group_list = ['','Monster','Water 1 (Amphibious)','Bug','Flying','Field','Fairy','Grass','Humanoid','Water 3 (Aquatic Invertebrate)','Mineral','Amorphous','Water 2 (Piscine)','Ditto','Dragon','Undiscovered',]
color_list = ['Red','Blue','Yellow','Green','Black','Brown','Purple','Gray','White','Pink']

stat_names = ['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']

level_curve_list = ['Medium-Fast', 'Erratic', 'Fluctuating', 'Medium-Slow', 'Fast', 'Slow']