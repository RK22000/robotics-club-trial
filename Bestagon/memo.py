# import pandas as pd
import honeycomb
from bee import *
from bee0 import Bee
memo_file = 'memo.csv'
# try:
#     memo = pd.read_csv(memo_file)
# except FileNotFoundError:
#     memo = pd.DataFrame(columns=['Bee_type', 'Density', 'Ideal_Travel_length', 'Travel_length', 'Virtual_exploration'])

last_entry = None
def memo_bee(bee: BeePrime):
    # check if bee is done
    if bee.goals or bee.status_failed: return
    ideal_bee = Bee()
    ideal_bee.blocks = honeycomb.blocks
    while not ideal_bee.status_failed and ideal_bee.goals:
        ideal_bee.step()
    ideal_bee.blocks = set()
    ideal_bee.draw(epath='green')
    entry = [bee.type, honeycomb.block_density, len(ideal_bee.explored), len(bee.explored), bee.mentally_explored_total]
    # global last_entry
    # if entry == last_entry:
    #     return
    # memo.loc[len(memo.index)] = entry
    # last_entry = entry
    # memo.to_csv(memo_file, index=False)

