# Interrail Optimizer

Small program to optimize an interrail trip.

Currently, the user can enter two city names,
and if train stations can be found in those cities,
an approximate travel duration is calculated.

The goal is to input 
  - city wishlists from different travellers
  - total travel duration in days
  - average time spent in each city
  - start and end city
  
and get a suggested trip as an ordered list of cities.

Other parameters should also be possible to use in a cost function to model
a destinations desirability other than amount of travellers who want to go there.