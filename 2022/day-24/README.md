Based on [an existing solution by James Crawford](https://jactl.io/blog/2023/05/08/advent-of-code-2022-day24.html) written in [jactl](https://jactl.io/)

Before this, my initial understanding was that 

- We have a matrix within which any given grid coordinate may be considered 'ground' (free space) or 'blizzard'. 
- Blizzards move minute by minute in a constant direction, when they hit a wall, their next position is in the same diction at the opposite wall.
- Multiple blizzards may occupy the same position and not interact with one another.
- We have a defined entry point and a defined exit point.
- We can move 1 space move up, down, left, or right, or wait in place.
- We may not occupy the same space as a blizzard, only 'ground' positions.
- it is not clear to me what happens when a blizzard hits the entry or exit space.
- My suggested approach would be to have a class of valley with methods to :
- parse input to:
  - define grid, walls, entry and exit points
  - starting positions and directions of blizzards
- create a minute by minute updated map of the valley
  
I was not sure how to best approach finding the best route through the valley- it doesn't look like Djikstra's algorithm will work here in a simple case - we would have to establish possible routes with waits minute by minute.
I decieded on a breadth-first search but I was not sure that we could realistically consider all possible routes as I can see that getting rapidly beyond a manageable scale. We shall need some way of pruning dead routes. Whilst I got some intial code 'working' it was not tracking the blizzards motion correctly, assessed by visual comparison of the grid at each minute with the worked example.

I looked around for other solutions and found [James Crawford's Java based solution on reddit](https://www.reddit.com/r/adventofcode/comments/zu28ij/comment/jjeh95l/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button):

> This was a fun challenge. I figured out that there was no need to simulate the movement of the blizzards since at any point in time t we can work out which blizzards would have occupied any given square by checking the original map for the current row and column for a blizzard that is t squares away and of a type that would mean at time t it occupies the square in question.

I also riffed on his brief description (not the actual code) to implement the solution for part 2