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

WHich gave a correct result for Part 1