#!/usr/bin/python3

"""
Einstein's riddle
The situation
  There are 5 houses in five different colors.
  In each house lives a person with a different nationality.
  These five owners drink a certain type of beverage, smoke a certain brand of cigar and keep a certain pet.
  No owners have the same pet, smoke the same brand of cigar or drink the same beverage.
  The question is: Who owns the fish?
Hints
  The Brit lives in the red house
  the Swede keeps dogs as pets
  The Dane drinks tea
  The green house is on the left of the white house
  The green house's owner drinks coffee
  The person who smokes Pall Mall rears birds
  The owner of the yellow house smokes Dunhill
  The man living in the center house drinks milk
  The Norwegian lives in the first house
  The man who smokes blends lives next to the one who keeps cats
  The man who keeps horses lives next to the man who smokes Dunhill
  The owner who smokes BlueMaster drinks beer
  The German smokes Prince
  The Norwegian lives next to the blue house
  The man who smokes blend has a neighbor who drinks water
"""

from ortools.sat.python import cp_model


def solve_fish():
  model = cp_model.CpModel()

  # House colors
  white = model.NewIntVar(1, 5, 'white')
  red = model.NewIntVar(1, 5, 'red')
  green = model.NewIntVar(1, 5, 'green')
  yellow = model.NewIntVar(1, 5, 'yellow')
  blue = model.NewIntVar(1, 5, 'blue')

  # Nationalities
  brit = model.NewIntVar(1, 5, 'brit')
  swede = model.NewIntVar(1, 5, 'swede')
  dane = model.NewIntVar(1, 5, 'dane')
  norwegian = model.NewIntVar(1, 5, 'norwegian')
  german = model.NewIntVar(1, 5, 'german')

  # Pets
  dog = model.NewIntVar(1, 5, 'dog')
  bird = model.NewIntVar(1, 5, 'bird')
  cat = model.NewIntVar(1, 5, 'cat')
  fish = model.NewIntVar(1, 5, 'fish')
  horse = model.NewIntVar(1, 5, 'horse')

  # Drinks
  tea = model.NewIntVar(1, 5, 'tea')
  coffee = model.NewIntVar(1, 5, 'coffee')
  milk = model.NewIntVar(1, 5, 'milk')
  water = model.NewIntVar(1, 5, 'water')
  beer = model.NewIntVar(1, 5, 'beer')

  # Smokes
  pall_mall= model.NewIntVar(1, 5, 'pal mall')
  dunhill = model.NewIntVar(1, 5, 'dunhill')
  blends = model.NewIntVar(1, 5, 'blends')
  bluemaster = model.NewIntVar(1, 5, 'bluemaster')
  prince=model.NewIntVar(1, 5, 'prince')

  # Add features to the main model
  model.AddAllDifferent([white, red, green, yellow, blue])
  model.AddAllDifferent([brit, swede, dane, norwegian, german])
  model.AddAllDifferent([dog, bird, cat, fish, horse])
  model.AddAllDifferent([tea, coffee, milk, water, beer])
  model.AddAllDifferent([pall_mall, dunhill, prince, blends, bluemaster])

  # Add relationships
  model.Add(brit == red)
  model.Add(swede == dog)
  model.Add(dane == tea)
  model.Add(white == green + 1)
  model.Add(coffee == green)
  model.Add(pall_mall == bird)
  model.Add(dunhill == yellow)
  model.Add(milk == 3)
  model.Add(norwegian == 1)
  
  # model.Add(kools == yellow)  
  diff_cat_blends = model.NewIntVar(-4, 4, 'diff_cat_blends')
  model.Add(diff_cat_blends == cat - blends)
  model.AddAbsEquality(1, diff_cat_blends)
  
  diff_horse_dunhill = model.NewIntVar(-4, 4, 'diff_horse_dunhill')
  model.Add(diff_horse_dunhill == horse - dunhill)
  model.AddAbsEquality(1, diff_horse_dunhill)

  model.Add(bluemaster == beer)
  model.Add(german == prince)

  diff_norwegian_blue = model.NewIntVar(-4, 4, 'diff_norwegian_blue')
  model.Add(diff_norwegian_blue == norwegian - blue)
  model.AddAbsEquality(1, diff_norwegian_blue)

  diff_blends_water = model.NewIntVar(-4, 4, 'diff_blends_water')
  model.Add(diff_blends_water == blends - water)
  model.AddAbsEquality(1, diff_blends_water)

  # Use model to find solution
  solver = cp_model.CpSolver()
  status = solver.Solve(model)

  if status == cp_model.FEASIBLE:
    people = [brit, swede, dane, norwegian, german]
    water_drinker = [
        p for p in people if solver.Value(p) == solver.Value(water)
    ][0]
    fish_owner = [
        p for p in people if solver.Value(p) == solver.Value(fish)
    ][0]
    print('The', fish_owner.Name(), 'owns the fish')
  else:
    print('No solutions were found.')


solve_fish()

"""Output
$ python3 einstein_fish_sat.py 

The german owns the fish
"""