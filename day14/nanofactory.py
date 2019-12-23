import sys
import re
import math
from copy import copy
from collections import defaultdict

chemical_amount = re.compile(r'(\d+)\s+(\w+)')
reaction = re.compile(r'(.*)\s+=>\s+(.*)')

def parse_ingredient(ingredient):
    ingred_match = chemical_amount.findall(ingredient)
    assert(ingred_match != None)
    amount = int(ingred_match[0][0])
    name = ingred_match[0][1]
    return amount, name

def parse_ingredients(ingredients):
    return [parse_ingredient(ingredient) for ingredient in ingredients.split(',')]

def get_reactions_for_ingredient(all_reactions, ingredient_name, amount):
    reactions = []
    for ingred, outgred in all_reactions:
        for x in outgred:
            if x[1] == ingredient_name:
                if x[0] >= amount:
                    scale = 1
                else:
                    scale = int(math.ceil(amount / x[0]))
                reactions.append((ingred,outgred,scale,scale*x[0]-amount))
    return reactions

def resolve_ingredient(all_reactions, target_name, target_amount, spare_ingredients):
    total = 0

    # if this is ore, then this can't be further reduced
    # just return the amount of ore required

    #print(f"INPUT: {spare_ingredients} {target_name}:{target_amount}")
    extracted_val = min(spare_ingredients[target_name], target_amount)
    spare_ingredients[target_name] -= extracted_val
    target_amount -= extracted_val
    #print(f"new target_amount {target_amount}")
    if target_amount == 0:
        #print(f"Have spares for item {target_name}")
        return 0, spare_ingredients
    if target_name == 'ORE':
        return target_amount, spare_ingredients


    # for other ingredients, iterate through all reactions that produce this ingredient
    # as one of the outputs then select the reaction that requires the minimum ore
    reactions = get_reactions_for_ingredient(all_reactions, target_name, target_amount)
    best_total = -1
    best_reaction_for_target = None
    best_spares = None

    for ingred, outgred, scale, spare in reactions:
        total = 0
        spares = copy(spare_ingredients)
        for x in ingred:
            # add any leftovers to our list of spares
            tval, spares = resolve_ingredient(all_reactions, x[1], x[0]*scale, spares)
            total += tval
        for x in outgred:
            #print(f"Adding spare {x[1]} with {x[0]*scale - target_amount}")
            spares[x[1]] = x[0]*scale - target_amount
        if best_total > total or best_total==-1:
            best_total = total
            best_reaction_for_target = (ingred,outgred,scale)
            best_spares = spares
    #print(f"best_reaction_for_target for {target_name}:{target_amount} is {best_reaction_for_target} {best_total}")
    return best_total, best_spares

def reaction_supports(ingredient_amount, ingredient_name, remaining_consumables):
    return remaining_consumables[ingredient_name] >= ingredient_amount

def get_possible_reactions(all_reactions, all_consumables):
    possible_reactions = []
    for ingred, outgred in all_reactions:
        remaining_consumables = copy(all_consumables)
        allSupported = True
        for amount, name in ingred:
            allSupported = allSupported and reaction_supports(amount, name, remaining_consumables)
            remaining_consumables[name] -= amount
        if allSupported:
            possible_reactions.append((ingred,outgred))
    return possible_reactions

TOTAL_ORE = int(1e12)
def search(reactions):
    next_target_fuel = 1
    prev_fuel = 0
    factor = 2
    delta_ore = 0
    ore_required = 0
    while (next_target_fuel - prev_fuel) >= 1 or ore_required > TOTAL_ORE:
        print(f"Attempting search for {next_target_fuel}")
        ore_required, spares = resolve_ingredient(reactions, 'FUEL', next_target_fuel, defaultdict(int))
        prev_fuel = next_target_fuel
        ore_required_high, spares = resolve_ingredient(reactions, 'FUEL', next_target_fuel+1, defaultdict(int))
        ore_required_low, spares = resolve_ingredient(reactions, 'FUEL', next_target_fuel-1, defaultdict(int))
        print(f"high {ore_required_high} low {ore_required_low} {ore_required}")
        next_target_fuel = next_target_fuel - (ore_required - TOTAL_ORE)/((ore_required_high - ore_required_low)/2)
        next_target_fuel = int(next_target_fuel)
    return next_target_fuel

    

def main():
    lines = open(sys.argv[1]).readlines()
    source_ore = int(sys.argv[2])
    reactions = []
    for line in lines:
        match = reaction.findall(line.rstrip('\n'))
        assert(match != None)
        inputMatch = match[0][0]
        outputMatch = match[0][1]
        input_ingredients = parse_ingredients(inputMatch)
        output_ingredients = parse_ingredients(outputMatch)
        reactions.append((input_ingredients, output_ingredients))
    #print(f"reactions: {reactions}")
    best_total, best_spares = resolve_ingredient(reactions, 'FUEL', 1, defaultdict(int))

    print(f"best reactions for 1T ORE produces {search(reactions)}")


if __name__ == "__main__":
    main()
