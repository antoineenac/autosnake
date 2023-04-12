# autosnake
a snake game that plays itself the best it can

Before all, I apologize to all non french speaker for the use of a combination of french and english name in my code, and english speakers for all the bad spelling that will follow. Sorry!

The project is divided like this :

  - Serpent.py define the snake class. It contains a basic representation of the snake (list of coordinates, ...). 
  
  - Environnement.py define the environnement of the game, as well as a primitive interface to see what is happening. You can play by yourself the game by 
    defining an environnement with the size of your map, the places of the obstacles (in a list of coordinates [[x1,y1],...]) and the place where you start, 
    and by using the "boucle" function. At each step, you have to play "z" to go up, "q" to go left, "s" to go down and "d" to go right (the game was created 
    whith an azerty keyboard...). The key "k" stop the game.
  
  - AlgoGen.py gives a basic implementation of a genetic algorithm in order to get a "good" solution. The algorithm works like this :
          - Generation of a base population : vector of random deplacements
          - Each element of the population get "truncated" : we cut the vector where it gives a wrong deplacement (hit an obstacle for instance)
          - for each element of the population, we compute a score that represent the quality of the sequence of deplacement. For now, the score is 
            (lenght of the snake, 1/lenght of the sequence of deplacement), and we use lexicographic order. Thus, we give higher score when the snake successfuly
            eat objectives (called croquettes in the game), and also higher score when it do so with the minimal number of step.
          - We select the best element of the population, that is to say those with best score. This will be the base of our next population.
          - For each element in this selection, we create mutation. To do so, we randomly select a index (higher the index higher the probability), and truncate 
            the element at this index. Then, we add random deplacement a the end of this truncated vector, and add this vector to the population. We do this a fixed number of time in order to have a "big enough" population.
           - We have created a new population with higher score than the previous one. We can repeat this operation a few time (10 to 50) to have a "good" solution
            for a given environnement. The algorithm seems to converge and give good solution, but it takes quite a lot of time.
            
   - GenerationBDD.py runs the genetic algorithm with random environnements (fixed sized), in order to gather data to use for supervized learning. This data 
     is either representation of the state by a vector (defined in Environnement.py, function get_q_etat) for simple neural network (or maybe deepQlearning in the future), or a graphic representation of the environnement for CNNs or LSTMS. 
 
The files that are not mentionned here are not finished yet. I also use thise repo to transfer my work between two computers.
I am currently working on the simple neural network, and the next steps will certainly be deep learning with CNNs or LSTMS. I am aware that this type of problem
is usually solved using reinforcement learning, but I wanted to explore the possibility to do otherwise first.

You can use, modify, or do whatever you want with this code.
Have fun!
