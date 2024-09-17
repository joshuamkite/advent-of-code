Here I 'manually' set up 

- initial data parsing
- grid mapping
- vector functions

but there were various problems with the code, e.g. wrapping behaviour. LLM advised:

- Added a find_start_position method to correctly identify the starting position.
- Updated the move method to handle wrapping according to the problem description.
- Simplified the read_route method to use the new move method.
- Removed separate methods for moving in different directions, as they're now handled by the single move method.
- Updated the main function to use the new structure.

Which gave a correct result for Part 1

For Part 2 I struggled with the concepts for mapping the mesh to a cube and was not able to  advance to a meaningful solution. I am clearly [not alone in finding this challenge tricky](https://www.reddit.com/r/adventofcode/comments/zsct8w/2022_day_22_solutions/) I wound up taking the solution presented here wholesale from https://coeleveld.com/2022-advent-of-code-python/ **It is not my own work!**
