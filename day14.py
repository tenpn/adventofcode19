import math
from pathlib import Path

# 999 ABC
# returns (Item, Quantity)
def parse_ingredient(ingredient_str):
    split_str = ingredient_str.split()
    return (split_str[1].lower(), int(split_str[0]))

# 999 ABC(, 999 ABC)+ => 999 ABC
# returns ({IngredientItem:Quantity,}, (ResultItem, Quantity))
def parse_recipe(recipe_str):
    splits = recipe_str.split(" => ")
    ingredients = {ingredient:quantity for (ingredient,quantity) in [parse_ingredient(ing_str) for ing_str in splits[0].split(", ")]}
    return (ingredients, parse_ingredient(splits[1]))

# {Result: (Result Quantity, {Ingredient:Quantity,}),}
def parse_recipes(recipes_str):
    return {result:(res_quan, ingredients) for (ingredients, (result, res_quan))
            in [parse_recipe(recipe_str) for recipe_str in recipes_str.splitlines()] }

# returns how much fuel to produce 1 ore
def calculate_ore(recipes):
    print(">")
    
    total_ore = 0
    needs = {"fuel":1}
    spares = {}
    
    while len(needs) > 0:
        current_item = next(iter(needs))
        current_needed = needs.pop(current_item)
        print("expanding", current_item, current_needed, needs)
        assert current_item in recipes, "no recipe for item " + current_item
        (recipe_production, recipe) = recipes[current_item]
        print("recipe produces", recipe_production)

        if current_item in spares:
            current_needed -= spares.pop(current_item)
            print("used spares to reduce need to", current_needed, spares)

        if current_needed <= 0:
            continue

        recipe_coeff = math.ceil(max(current_needed, recipe_production)/recipe_production)
        new_spares = recipe_coeff*recipe_production - current_needed
        if new_spares > 0:
            spares[current_item] = new_spares
            print("added spares", new_spares, spares)

        for (r_ingredient, r_quantity) in recipe.items():
            r_quantity *= recipe_coeff
            if r_ingredient == "ore":
                total_ore += r_quantity
                print("found ore", r_quantity, ">", total_ore)
            else:
                needs[r_ingredient] = r_quantity + (needs[r_ingredient] if r_ingredient in needs else 0)
                print("need", r_ingredient, r_quantity, needs)
    
    return total_ore

def test(actual, expected, msg):
    print("<",msg)
    assert actual == expected, "%s expected %s got %s"%(msg, str(expected), str(actual))

def tests():
    test(parse_ingredient("1 foo"), ("foo", 1), "simple ingredient")
    test(parse_recipe("1 foo => 9 blah"), ({"foo":1}, ("blah", 9)), "simple recipe")
    test(parse_recipe("1 foo, 12 fish => 9 blah"), ({"foo":1, "fish":12}, ("blah", 9)), "compound recipe")
    test(parse_recipes("1 foo => 9 blah\n3 fish => 12 bump"), {"blah": (9,{"foo":1}), "bump": (12,{"fish":3})}, "recipes dict")

    test(calculate_ore({"fuel":(1, {"ore":1})}), 1, "simplest path")
    test(calculate_ore({"fuel":(1, {"ore":10})}), 10, "simple path with multiples")
    test(calculate_ore({"fuel":(10, {"ore":1})}), 1, "simple overproduction")
    test(calculate_ore({"fuel":(1, {"mid":1}),
                        "mid":(1, {"ore":1})}), 1, "nested path")
    test(calculate_ore({"fuel":(1, {"mid":3}),
                        "mid":(1, {"ore":1})}), 3, "stockpiling")
    test(calculate_ore({"fuel":(1, {"mid":3}),
                        "mid":(3, {"ore":1})}), 1, "match-quantities")
    test(calculate_ore({"fuel":(1, {"mid":1}),
                        "mid":(3, {"ore":1})}), 1, "ballooning")
    test(calculate_ore({"fuel":(1, {"mid": 1, "ore": 1}),
                        "mid": (1, {"ore": 1})}), 2, "combo")
    test(calculate_ore({"a":(1, {"ore":1}),
                        "d":(1, {"a":1}),
                        "fuel":(1,{"d":1, "a":1})}), 2, "quantities are stacked")
    test(calculate_ore({"a":(3, {"ore":1}),
                        "d":(1, {"a":1}),
                        "fuel":(1,{"a":1, "d":1})}), 1, "reusable spares aren't lost")
    test(calculate_ore({"a":(3, {"ore":1}),
                        "d":(1, {"a":1}),
                        "e":(1, {"a":1}),
                        "fuel":(1,{"a":1, "e":1, "d":1})}), 1, "reusable spares are shared")

    test1_recipes = parse_recipes("""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""")
    test(calculate_ore(test1_recipes), 31, "test1 data")

    test(calculate_ore(parse_recipes("""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""")), 165, "test2 data")
    test(calculate_ore(parse_recipes("""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""")), 13312, "test3 data")
    test(calculate_ore(parse_recipes("""2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""")), 180697, "test4 data")
    test(calculate_ore(parse_recipes("""171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""")), 2210736, "test5 data")
    print("tests pass")

tests()

puzzle_input = Path("day14.txt").read_text()
puzzle_recipes = parse_recipes(puzzle_input)
print(calculate_ore(puzzle_recipes))
