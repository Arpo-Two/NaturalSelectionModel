# NaturalSelectionModel
A simple model for testing natural selection effects. A simple GUI made in pygame allow you to adjust things like population size, food available and mutation rate It also builds graphs to analyse and give population statistics 
Environment rules:
Food spawns randomly inside the given screens bounds
Individuals also spawn randomly each new round
If and individual gets no food at the end of the round, it dies. If it manages to get one food, it stays alive. And if it gets 2, it stops seeking for more and is able to reproduce
A child has the exact same speed of the parent
At each new round, each individual's speed is mutated
Each individual has an ammount of energy that allows it to move while there's energy left
Energy is directly proporcional to the square of the speed
The individual's color show it's speed, red means slower and green means faster
