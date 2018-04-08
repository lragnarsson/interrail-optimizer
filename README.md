# Interrail Optimizer

Small program to optimize an interrail trip.

Currently, the input is
  - city wishlists from different travellers
  - total travel duration in days
  - average time spent in each city
  - start/end city
  
and the output is the top scoring trips as an ordered list of cities.

Enter input in a trip .json file.

Other parameters should also be possible to use in a cost function to model
a destinations desirability other than amount of travellers who want to go there.