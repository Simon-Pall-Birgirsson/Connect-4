from machine import Pin, SoftI2C
from I2C_LCD import I2cLcd
from neopixel import NeoPixel
from time import sleep_ms

E = (0, 0, 0)
X = (255, 0, 0)
O = (0, 0, 255)
    
    
NUM_LEDS = 7*9
neopixel = NeoPixel(Pin(4, Pin.OUT), NUM_LEDS)
NUM_LEDS_LENGTH = 9
NUM_LEDS_HEIGHT = 7
button_left = Pin(10, Pin.IN, Pin.PULL_UP)
button_right = Pin(9, Pin.IN, Pin.PULL_UP)
button_drop = Pin(18, Pin.IN, Pin.PULL_UP)
i2c = SoftI2C(scl=Pin(42), sda=Pin(41))  
lcd = I2cLcd(i2c, 39, 2, 16)

#Kernels
"""
k4_h = [[1, 1, 1, 1]] #4 long horizontal
k4_v = [[1],[1],[1],[1]] #4 long vertical
k4_dr = [[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]] #4 long top-left to bottom-right
k4_ur = [[0, 0, 0, 1],[0, 0, 1, 0],[0, 1, 0, 0],[1, 0, 0, 0]] #4 long top-right to bottom-left
k5_h = [[1, 1, 1, 1, 1]] #5 long horizontal
k5_v = [[1],[1],[1],[1],[1]] #5 long vertical
k5_dr = [[1, 0, 0, 0, 0],[0, 1, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 1, 0],[0, 0, 0, 0, 1]] #5 long top-left to bottom-right
k5_ur = [[0, 0, 0, 0, 1],[0, 0, 0, 1, 0],[0, 0, 1, 0, 0],[0, 1, 0, 0, 0],[1, 0, 0, 0, 0]] #5 long top-right to bottom-left
k2x2 = [[1, 1],[1, 1]] #2x2 square
kernels = [k4_h, k4_v, k4_dr, k4_ur,k5_h, k5_v, k5_dr, k5_ur, k2x2] #All the kernels in a list
"""
#Why the hell are the comments piss colored

led_states = [
    [E,E,E,E,E,E,E,E,E],
    [E,E,E,E,E,E,E,E,E],
    [E,E,E,E,E,E,E,E,E],
    [E,E,E,E,E,E,E,E,E],
    [E,E,E,E,E,E,E,E,E],
    [E,E,E,E,E,E,E,E,E],
    [E,E,E,E,E,E,E,E,E]
    ]

led_selector_state = [E,E,E,E,E,E,E,E,E]


selector_pos = 0
"""
#Can move down function
def can_move_down(x, y):
    if y == 6:
        return (False, y)
    
    if led_states[y+1][x] != E:
        return (False, y)
    
    if y+1 == 6:
        return (True, y+1)
    
    return can_move_down(x, y+1)

def gravity():
    moved = True
    while moved:
        moved = False
        
        for y in range(NUM_LEDS_HEIGHT - 2, -1, -1):
            for x in range(NUM_LEDS_LENGTH):
                if led_states[y][x] != E:
                    can, new_y = can_move_down(x, y)
                    if can and new_y != y:
                        led_states[new_y][x] = led_states[y][x]
                        led_states[y][x] = E
                        moved = True
"""
def gravity():
    for x in range(NUM_LEDS_LENGTH):
        stack = []


        for y in range(NUM_LEDS_HEIGHT):
            if led_states[y][x] != E:
                stack.append(led_states[y][x])

        y = NUM_LEDS_HEIGHT - 1
        for piece in reversed(stack):
            led_states[y][x] = piece
            y -= 1

        for yy in range(y, -1, -1):
            led_states[yy][x] = E


def victory(state):
    if state == 0:
        for i in range(len(led_states)):
            for u in range(len(led_states[i])):
                if i % 2 == 0:
                    led_states[i][u] = X
                else:
                    led_states[i][u] = O
                sleep_ms(2500)
    elif state == 1:
        for i in range(len(led_states)):
            for u in range(len(led_states[i])):
                led_states[i][u] = X
                sleep_ms(2500)
    elif state == 2:
        for i in range(len(led_states)):
            for u in range(len(led_states[i])):
                led_states[i][u] = O
                sleep_ms(2500)

turn = True # True = X, False = O
buzzer_anger = False #if the buzzer should do a bad tone if the player did something wrong # Unused for now 
player_x_score = 0
player_o_score = 0
flash_on = True

while True:
    
    current_piece = X if turn else O
    
    if player_x_score >= 250 and player_x_score == player_o_score:
        victory(0)
    
    if player_x_score >= 250:
        victory(1)
        
    if player_o_score >= 250:
        victory(2)
    num = 0
    
    for i in led_states:
        for u in i:
            neopixel[num] = u
            
            num += 1
    neopixel.write()
    
    num = 0
    
    if button_left.value() == 0:
        selector_pos = (selector_pos - 1) % NUM_LEDS_LENGTH

    if button_right.value() == 0:
        selector_pos = (selector_pos + 1) % NUM_LEDS_LENGTH
                
    if button_drop.value() == 0:
        if led_states[selector_pos][0] == E:
            if turn:
                led_states[selector_pos][0] == X
            else:
                led_states[selector_pos][o] == O
        sleep_ms(150) 

                

    gravity()                
        
    flash_col = None
    for x in range(NUM_LEDS_LENGTH):
        if led_states[0][x] == E:
            flash_col = x
            break

    for y in range(NUM_LEDS_HEIGHT):
        for x in range(NUM_LEDS_LENGTH):
            color = led_states[y][x]
            if y == 0 and x == flash_col:
                color = current_piece if flash_on else E
            neopixel[y * NUM_LEDS_LENGTH + x] = color

    neopixel.write()
    flash_on = not flash_on
    sleep_ms(100)


 
            
    gravity()
    
    X_long4_count = 0
    X_long5_count = 0
    X_square_count = 0
    
    O_long4_count = 0
    O_long5_count = 0
    O_square_count = 0
    
    for i in range(len(led_states)):
        for u in range(len(led_states[i])):
            #5 longs
            if u <= 4 and led_states[i][u] == X and led_states[i][u+1] == X and led_states[i][u+2] == X and led_states[i][u+3] == X and led_states[i][u+4] == X:
                X_long5_count += 1
                led_states[i][u] = E
                led_states[i][u+1] = E
                led_states[i][u+2] = E
                led_states[i][u+3] = E
                led_states[i][u+4] = E
            
            if u <= 4 and i <= 4 and led_states[i][u] == X and led_states[i+1][u+1] == X and led_states[i+2][u+2] == X and led_states[i+3][u+3] == X and led_states[i+4][u+4] == X:
                X_long4_count += 1
                led_states[i][u] = E
                led_states[i+1][u+1] = E
                led_states[i+2][u+2] = E
                led_states[i+3][u+3] = E
                led_states[i+4][u+4] = E
                
            if i <= 2 and led_states[i][u] == X and led_states[i+1][u] == X and led_states[i+2][u] == X and led_states[i+3][u] == X and led_states[i+4][u] == X:
                X_long4_count += 1
                led_states[i][u] = E
                led_states[i+1][u] = E
                led_states[i+2][u] = E
                led_states[i+3][u] = E
                led_states[i+4][u] = E
                
            if u >= 4 and i <= 4 and led_states[i][u] == X and led_states[i-1][u-1] == X and led_states[i-2][u-2] == X and led_states[i-3][u-3] == X and led_states[i-4][u-4] == X:
                X_long4_count += 1
                led_states[i][u] = E
                led_states[i-1][u-1] = E
                led_states[i-2][u-2] = E
                led_states[i-3][u-3] = E
                led_states[i-4][u-4] = E
             
            # 4 longs 
            if u <= 5 and led_states[i][u] == X and led_states[i][u+1] == X and led_states[i][u+2] == X and led_states[i][u+3] == X:
                X_long4_count += 1
                led_states[i][u] = E
                led_states[i][u+1] = E
                led_states[i][u+2] = E
                led_states[i][u+3] = E
                
            if u <= 5 and i <= 3 and led_states[i][u] == X and led_states[i+1][u+1] == X and led_states[i+2][u+2] == X and led_states[i+3][u+3] == X:
                X_long4_count += 1
                led_states[i][u] = E
                led_states[i+1][u+1] = E
                led_states[i+2][u+2] = E
                led_states[i+3][u+3] = E
                
            if i <= 3 and led_states[i][u] == X and led_states[i+1][u] == X and led_states[i+2][u] == X and led_states[i+3][u] == X and led_states[i+4][u] == X:
                X_long4_count += 1
                led_states[i][u] = E
                led_states[i+1][u] = E
                led_states[i+2][u] = E
                led_states[i+3][u] = E
                
            if u >= 4 and i <= 3 and led_states[i][u] == X and led_states[i-1][u-1] == X and led_states[i-2][u-2] == X and led_states[i-3][u-3] == X:
                X_long4_count += 1
                led_states[i][u] = E
                led_states[i-1][u-1] = E
                led_states[i-2][u-2] = E
                led_states[i-3][u-3] = E
        
            #2x2 square
            if u <= 7 and i <= 5 and led_states[i][u] == X and led_states[i+1][u] == X and led_states[i][u+1] == X and led_states[i+1][u+1] == X:
                X_square_count += 1
                led_states[i][u] = E
                led_states[i+1][u] = E
                led_states[i][u+1] = E
                led_states[i+1][u+1] = E
                
            # 5-longs 
            if u <= 4 and led_states[i][u] == O and led_states[i][u+1] == O and led_states[i][u+2] == O and led_states[i][u+3] == O and led_states[i][u+4] == O:
                O_long5_count += 1
                led_states[i][u] = E
                led_states[i][u+1] = E
                led_states[i][u+2] = E
                led_states[i][u+3] = E
                led_states[i][u+4] = E

            
            if u <= 4 and i <= 4 and led_states[i][u] == O and led_states[i+1][u+1] == O and led_states[i+2][u+2] == O and led_states[i+3][u+3] == O and led_states[i+4][u+4] == O:
                O_long5_count += 1
                led_states[i][u] = E
                led_states[i+1][u+1] = E
                led_states[i+2][u+2] = E
                led_states[i+3][u+3] = E
                led_states[i+4][u+4] = E

            
            if i <= 2 and led_states[i][u] == O and led_states[i+1][u] == O and led_states[i+2][u] == O and led_states[i+3][u] == O and led_states[i+4][u] == O:
                O_long5_count += 1
                led_states[i][u] = E
                led_states[i+1][u] = E
                led_states[i+2][u] = E
                led_states[i+3][u] = E
                led_states[i+4][u] = E

            
            if u >= 4 and i <= 3 and led_states[i][u] == O and led_states[i-1][u-1] == O and led_states[i-2][u-2] == O and led_states[i-3][u-3] == O and led_states[i-4][u-4] == O:
                O_long5_count += 1
                led_states[i][u] = E
                led_states[i-1][u-1] = E
                led_states[i-2][u-2] = E
                led_states[i-3][u-3] = E
                led_states[i-4][u-4] = E

            # 4-longs
            if u <= 5 and led_states[i][u] == O and led_states[i][u+1] == O and led_states[i][u+2] == O and led_states[i][u+3] == O:
                O_long4_count += 1
                led_states[i][u] = E
                led_states[i][u+1] = E
                led_states[i][u+2] = E
                led_states[i][u+3] = E

            
            if u <= 5 and i <= 3 and led_states[i][u] == O and led_states[i+1][u+1] == O and led_states[i+2][u+2] == O and led_states[i+3][u+3] == O:
                O_long4_count += 1
                led_states[i][u] = E
                led_states[i+1][u+1] = E
                led_states[i+2][u+2] = E
                led_states[i+3][u+3] = E

            
            if i <= 3 and led_states[i][u] == O and led_states[i+1][u] == O and led_states[i+2][u] == O and led_states[i+3][u] == O:
                O_long4_count += 1
                led_states[i][u] = E
                led_states[i+1][u] = E
                led_states[i+2][u] = E
                led_states[i+3][u] = E

            
            if u >= 5 and i <= 4 and led_states[i][u] == O and led_states[i-1][u-1] == O and led_states[i-2][u-2] == O and led_states[i-3][u-3] == O:
                O_long4_count += 1
                led_states[i][u] = E
                led_states[i-1][u-1] = E
                led_states[i-2][u-2] = E
                led_states[i-3][u-3] = E

            # 2×2 square
            if u <= 7 and i <= 5 and led_states[i][u] == O and led_states[i+1][u] == O and led_states[i][u+1] == O and led_states[i+1][u+1] == O:
                O_square_count += 1
                led_states[i][u] = E
                led_states[i+1][u] = E
                led_states[i][u+1] = E
                led_states[i+1][u+1] = E

    gravity()
            
    player_x_score = (X_long4_count * 10) + (X_square_count * 15) + (X_long5_count * 25)
    player_o_score = (O_long4_count * 10) + (O_square_count * 15) + (O_long5_count * 25)
    



    lcd.clear()

    o_score_str = str(player_o_score)
    lcd.putstr(" " * (16 - len(o_score_str)) + o_score_str)

    lcd.move_to(0, 1)
    lcd.putstr(str(player_x_score))


