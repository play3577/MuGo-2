# MuGo AI
Forked form [MuGo](https://github.com/brilee/MuGo)

# Usage
class: ``AI``  
* Constructor parameters:   
  - [Required]``game_id``: a string to mark a game  
  - [Optional]``mode``:Ignore it, I have not complete the function  
  - [Optional]``moudle_file``:The MuGo AI moudle file, default value = ``./AI_FILE/savedmodel``<b>WARNING: AI file directory now is changed!</b>  
  - [Optional]``debug``:Whether to output debugging information, default value=``False``  
* Main function: ``play()`` parameters:
  - [Required]``chess_message``:A string to describe the position of the piece <b>IN SGF FORMAT</b>,
      example: ``W[aa]``
  - [Optional]``first``:Is it the first move, default value=``False``




# Example
> AI vs AI

```python
from AI import AI
import random

def main():
    game_id = str(random.randint(1, 100000))
    ai_1 = AI(game_id+'-1')
    ai_2 = AI(game_id+'-2')
    result = ai_1.play('', first=True)
    print(result)
    while True:
        result = ai_2.play(result)
        print(result)
        result = ai_1.play(result)
        print(result)

if __name__ == '__main__':
    main()

```
