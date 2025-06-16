version = '3.1'

class Pokedata:
    
    def __init__(self):
        #path variables   
        self.personal_path = ''
        self.levelup_path = ''
        self.evolution_path = ''
        self.model_path = ''
        self.csv_pokemon_list_path = ''

        #file/game variables
        self.game = ''
        self.max_species_index = 0
        self.personal = []

        self.levelup = []

        self.evolution = []

        self.model = []
        self.model_header = []

        self.modelless_exists = True
        self.model_folder_prefix = ''

        self.run_model_later = False

        self.sorted = False

        #on startup, initialize to empty
        #when load, initialize to full and current to full
        #when search, search in current for speed
        self.base_species_list =  ['Bulbasaur']
        self.master_formes_list = ['Bulbasaur']
        self.model_source_list = ['Bulbasaur']

        self.master_list_csv = []
        
        self.extracted_extension = '.bin'


xy_master_list_csv = []

oras_master_list_csv = []

sm_master_list_csv = []

usum_master_list_csv = []