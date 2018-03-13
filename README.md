# Void-IntroToIM-FinalProject
Final Project for Introduction to Interactive Media (Fall 2017)


Concept 

At first, I was pretty much clueless as to what to do for the final project. The idea to do a game came to mind while the others in class were pitching their own ideas. However, since this is Interactive Media, and not Computer Science, I wanted to showcase my hardware knowledge and build some level of interaction between my game and the outside world that doesn’t involve a keyboard. And, so I decided to build an external controller too, a simple joystick in a box. My initial idea was to create a button as well, but since Michael asked us to produce a simple take on our original idea, I decided to scrap the idea of including a button. 

The inspiration behind my game was essentially my childhood memories. Having grown up in the Gameboy Color/Advance generation, I was exposed to games from franchises such as Pokemon, The Legend of Zelda,  Dragon Ball, Dragon Quest and Final Fantasy. These games had very simple graphics, sounds and storylines, unlike the current generation of high spec AAA rating games. However, it was these retro games that left a lasting impact on my mind, and it only felt right to pay homage to the games that made my childhood so memorable.

The structure of the game is simple. Your character, the hero, is on the moon and he fights off space bats and lizards that have invaded the moon. He ultimately discovers a dragon, a.k.a the final boss of the game, and his goal is to eliminate the dragon. 

Implementation

I implemented the game using PyProcessing, which is Processing that executes native Python code. The reason why I chose this over standard Processing that runs on Java is because I was more confident of my programming skills in Python as opposed to Java. Ultimately, this turned out to be a major inhibitor which I’ll explain later. 

The controls of the game were simple, the player moves the characters left, right or up, and if the player comes into contact with any foe with his dagger facing the right direction, the player would inflict damage onto the foe. Otherwise, the player would lose some health instead. In order to create the necessary software aspects of the game, I used the following :
1) PyProcessing IDE – To program the actual game logic
2) Arduino IDE – To program the hardware aspect of the project to receive input
3) Adobe Photoshop – To crop and resize images
4) Character Generator to create Hero Sprite – Can be found here 
5) Sithjester’s RXMP Resources for the enemy sprites – Can be found here.

I used Object Oriented Programming to implement the vast majority of functions, considering how versatile it is to duplicate elements of the same type with slightly different characteristics. Since I had learnt OOP in Intro to CS, and had implemented a game of similar nature, it didnt prove to be too difficult to come up with the logic for the game.
