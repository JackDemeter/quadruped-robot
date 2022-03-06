import time

if __name__ == '__main__':
    from quadruped import Quadruped

def stair(r):
    
    # Function for walking up stairs
    pause = 0.25

    # Initialize:
    r.leg_position('FL', -1, -15)
    r.leg_position('FR', 2, -16)
    r.leg_position('BL', -3, -15)
    r.leg_position('BR', 0, -15)
    time.sleep(3)

    #Ready to Pounce:
    r.leg_position('BL', 0, -9)
    r.leg_position('BR', 2, -8)

    #Front Paws up:
    r.leg_position('FL', -1, -15, z = -2)
    time.sleep(pause)
    r.leg_position('FR', 2, -6)
    time.sleep(pause)
    
    #Front steps:
    r.leg_position('FR', 10, -8)
    time.sleep(pause)
    r.leg_position('FR', 11, -13)
    time.sleep(pause)
    r.leg_position('BL', -1, -10)
    time.sleep(pause)
    r.leg_position('FL', -1, -15)
    time.sleep(pause)
    r.leg_position('FL', 3, -6)
    time.sleep(pause)
    r.leg_position('FL', 9, -12)
    time.sleep(pause)

    #Lean Forward & Lift Back Paws:
    r.leg_position('BL', -8, -15)
    r.leg_position('BR', -5, -15)
    time.sleep(1)

    r.leg_position('FL', 9, -15)
    r.leg_position('FR', 11, -16)
    time.sleep(pause)
    
    r.leg_position('FL', 5, -15)
    r.leg_position('FR', 7, -16)
    r.leg_position('BL', -12, -15)
    r.leg_position('BR', -9, -17)
    time.sleep(pause)
    # Bring back right forward:
    r.leg_position('BR', -9, -14)
    time.sleep(pause)
    r.leg_position('BR', -2, -14)
    time.sleep(pause)
    r.leg_position('BR', -2, -17)
    time.sleep(pause)

    # Shift weight
    r.leg_position('BL', -12, -16)
    r.leg_position('FR', 7, -13, z = 2)
    r.leg_position('FL', 5, -16, z = 2)
    time.sleep(pause)

    #Bring back left leg forward:
    r.leg_position('BL', -8, -12)
    time.sleep(pause)
    r.leg_position('BL', -2, -15)
    time.sleep(pause)
    r.leg_position('BL', -2, -17)
    time.sleep(pause)

    #Shift back to normal
    r.leg_position('FL', 5, -16)
    r.leg_position('FR', 8, -15)
    time.sleep(pause)

    # FR Step 2 up:
    [r.leg_position('FL', 5, -16), r.leg_position('FR', 8, -15), r.leg_position('BL', -2, -17), r.leg_position('BR', -2, -18)]
    time.sleep(pause)
    [r.leg_position('FL', 5, -16), r.leg_position('FR', 8, -9), r.leg_position('BL', -2, -17), r.leg_position('BR', -2, -18)]
    time.sleep(pause)
    [r.leg_position('FL', 5, -16), r.leg_position('FR', 14, -9), r.leg_position('BL', -2, -17), r.leg_position('BR', -2, -18)]
    time.sleep(pause)
    [r.leg_position('FL', 5, -16), r.leg_position('FR', 14, -12), r.leg_position('BL', -2, -17), r.leg_position('BR', -2, -18)]
    time.sleep(pause)

    # Slide forward:
    [r.leg_position('FL', 2, -16), r.leg_position('FR', 14, -12), r.leg_position('BL', -5, -17), r.leg_position('BR', -5, -18)]
    time.sleep(pause)
    [r.leg_position('BL', -5, -18), r.leg_position('BR', -5, -17)]

    # # 2nd Step up Front:
    
    r.leg_position('FL', 2, -7)
    time.sleep(pause)
    r.leg_position('FL', 11, -7)
    time.sleep(pause)
    r.leg_position('FL', 13, -14)
    time.sleep(pause)
    
    [r.leg_position('FL', 8, -14), r.leg_position('FR', 9, -12), r.leg_position('BL', -10, -15), r.leg_position('BR', -10, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 8, -14, z =1), r.leg_position('FR', 9, -10, z =1), r.leg_position('BL', -10, -15), r.leg_position('BR', -10, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 8, -14, z =1), r.leg_position('FR', 9, -10, z =1), r.leg_position('BL', -10, -14), r.leg_position('BR', -10, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 8, -14, z =1), r.leg_position('FR', 9, -10, z =1), r.leg_position('BL', -6, -15), r.leg_position('BR', -10, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 8, -14, z =1), r.leg_position('FR', 9, -10, z =1), r.leg_position('BL', -6, -18), r.leg_position('BR', -10, -16)]
    time.sleep(pause)


    [r.leg_position('FL', 8, -10, z =1), r.leg_position('FR', 9, -12, z =2), r.leg_position('BL', -6, -18), r.leg_position('BR', -10, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 8, -10, z =1), r.leg_position('FR', 9, -12, z =2), r.leg_position('BL', -6, -18), r.leg_position('BR', -10, -14)]
    time.sleep(pause)
    [r.leg_position('FL', 8, -10, z =1), r.leg_position('FR', 9, -12, z =2), r.leg_position('BL', -6, -16), r.leg_position('BR', -3, -14)]
    time.sleep(pause)
    [r.leg_position('FL', 8, -10, z =1), r.leg_position('FR', 9, -12, z =2), r.leg_position('BL', -6, -14), r.leg_position('BR', -3, -17)]
    time.sleep(pause)

    r.leg_position('FR', 9, -3, z =2)
    time.sleep(pause)
    r.leg_position('FR', 16, -3, z = 2)
    time.sleep(pause)
    r.leg_position('FR', 16, -8, z = 1)
    time.sleep(pause)


    [r.leg_position('FL', 1, -16, z =2), r.leg_position('FR', 13, -11), r.leg_position('BL', -9, -16), r.leg_position('BR', -6, -17)]

    [r.leg_position('FL', 1, -16, z =2), r.leg_position('FR', 13, -10), r.leg_position('BL', -9, -16), r.leg_position('BR', -6, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 1, -6, z =2), r.leg_position('FR', 13, -10), r.leg_position('BL', -9, -16), r.leg_position('BR', -6, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 13, -6, z =2), r.leg_position('FR', 13, -11), r.leg_position('BL', -9, -16), r.leg_position('BR', -6, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 13, -6), r.leg_position('FR', 13, -13, z = 2), r.leg_position('BL', -9, -16), r.leg_position('BR', -6, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 13, -11), r.leg_position('FR', 13, -13, z = 2), r.leg_position('BL', -9, -16), r.leg_position('BR', -6, -17)]
    time.sleep(pause)
    [r.leg_position('FL', 13, -11), r.leg_position('FR', 13, -13, z = 2), r.leg_position('BL', -13, -14), r.leg_position('BR', -10, -17)]
    time.sleep(pause)
    [r.leg_position('FL', 13, -11), r.leg_position('FR', 13, -13, z = 2), r.leg_position('BL', -13, -14), r.leg_position('BR', -10, -17)]
    time.sleep(pause)
    r.leg_position('BR', -10, -12)
    time.sleep(pause)
    r.leg_position('BR', -5, -12)
    time.sleep(pause)
    r.leg_position('BR', -5, -17)
    time.sleep(pause)
    [r.leg_position('FL', 7, -14), r.leg_position('FR', 7, -8),r.leg_position('BL', -13, -14), r.leg_position('BR', -5, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 7, -14), r.leg_position('FR', 7, -8),r.leg_position('BL', -5, -14), r.leg_position('BR', -5, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 7, -14), r.leg_position('FR', 7, -8),r.leg_position('BL', -5, -16), r.leg_position('BR', -5, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 7, -11), r.leg_position('FR', 7, -11),r.leg_position('BL', -5, -16), r.leg_position('BR', -5, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 7, -8), r.leg_position('FR', 7, -8),r.leg_position('BL', -5, -16), r.leg_position('BR', -5, -16)]
    time.sleep(pause)
    [r.leg_position('FL', 4, -8), r.leg_position('FR', 4, -8),r.leg_position('BL', -12, -16), r.leg_position('BR', -12, -16)]
    time.sleep(pause)
    [r.leg_position('FL', -1, -8), r.leg_position('FR', -1, -8),r.leg_position('BL', -12, -16), r.leg_position('BR', -12, -16)]
    time.sleep(pause)
    [r.leg_position('FL', -1, -8), r.leg_position('FR', -1, -10, z=2),r.leg_position('BL', -12, -16), r.leg_position('BR', -10, -13)]
    time.sleep(pause)
    [r.leg_position('FL', -1, -8), r.leg_position('FR', -1, -10, z=2),r.leg_position('BL', -12, -16), r.leg_position('BR', -3, -11)]
    time.sleep(pause)
    [r.leg_position('FL', -1, -8), r.leg_position('FR', -1, -10, z=2),r.leg_position('BL', -12, -16), r.leg_position('BR', -2, -14)]
    time.sleep(pause)
    [r.leg_position('FL', -1, -8), r.leg_position('FR', -1, -8, z=2),r.leg_position('BL', -13, -13), r.leg_position('BR', -2, -14)]
    time.sleep(pause)
    [r.leg_position('FL', -1, -8), r.leg_position('FR', -1, -8, z=2),r.leg_position('BL', -3, -9), r.leg_position('BR', -2, -14)]
    time.sleep(pause)
    [r.leg_position('FL', -1, -8), r.leg_position('FR', -1, -8, z=2),r.leg_position('BL', 0, -14), r.leg_position('BR', -2, -14)]
    time.sleep(pause)
    [r.leg_position('FL', -3, -10), r.leg_position('FR', -3, -10, z=2),r.leg_position('BL', -2, -16), r.leg_position('BR', -2, -14)]
    time.sleep(pause)
    [r.leg_position('FL', -5, -12, z=-2), r.leg_position('FR', -5, -13, z=2),r.leg_position('BL', -5, -16), r.leg_position('BR', -5, -16)]
    time.sleep(pause)
    [r.leg_position('FL', -5, -12), r.leg_position('FR', -5, -13),r.leg_position('BL', -5, -16), r.leg_position('BR', -5, -16)]
    time.sleep(pause)

    # FR to 4th
    [r.leg_position('FL', -5, -12), r.leg_position('FR', -3, -9),r.leg_position('BL', -5, -16), r.leg_position('BR', -5, -16)]
    time.sleep(pause)
    [r.leg_position('FL', -5, -12), r.leg_position('FR', 9, -6),r.leg_position('BL', -5, -16), r.leg_position('BR', -5, -16)]


    
    
    
    
    
    
    
    
    # Step 3
    #Lifting up FL
    # [r.leg_position('FL', 8, -10, z =1), r.leg_position('FR', 9, -6, z =2), r.leg_position('BL', -6, -10), r.leg_position('BR', -3, -10)]
    # time.sleep(pause)
    # Move body forward
    # [r.leg_position('FL', 1, -17, z =1), r.leg_position('FR', 9, -6, z = 2), r.leg_position('BL', -13, -13), r.leg_position('BR', -13, -13)]
    # time.sleep(pause)
    # r.leg_position('FR', 13, -5, z = 1)
    # time.sleep(pause)
    # r.leg_position('FR', 13, -14)
    # time.sleep(pause)
    # # Shift to right side
    # [r.leg_position('FL', 4, -14, z =1), r.leg_position('FR', 15, -10), r.leg_position('BL', -11, -17), r.leg_position('BR', -8, -15)]
    # time.sleep(pause)
    # #Lift up FL paw
    # [r.leg_position('FL', 4, -6), r.leg_position('FR', 15, -10), r.leg_position('BL', -11, -17), r.leg_position('BR', -8, -15)]
    # time.sleep(pause)
    # [r.leg_position('FL', 12, -6), r.leg_position('FR', 15, -10), r.leg_position('BL', -11, -17), r.leg_position('BR', -8, -15)]
    # time.sleep(pause)
    # [r.leg_position('FL', 13, -10), r.leg_position('FR', 15, -10), r.leg_position('BL', -11, -16), r.leg_position('BR', -8, -17)]
    # time.sleep(pause)
    # # Shift forward

    # [r.leg_position('FL', 8, -10), r.leg_position('FR', 11, -10, z = 1), r.leg_position('BL', -13, -13), r.leg_position('BR', -10, -11)]
    # time.sleep(pause)
    # # BR Lift
    # [r.leg_position('FL', 8, -10), r.leg_position('FR', 11, -10, z = 1), r.leg_position('BL', -13, -13), r.leg_position('BR', -3, -11)]
    # time.sleep(pause)
    # [r.leg_position('FL', 8, -10), r.leg_position('FR', 11, -10, z = 1), r.leg_position('BL', -13, -13), r.leg_position('BR', -3, -18)]
    # time.sleep(pause)
    
    
    #---------------------------------------------------------------
    #Old-----------------------------------------------------------

    # r.leg_position('FR', 8, -15, z = 2)
    
    # r.leg_position('FL', 4, -6)
    # time.sleep(pause)
    # r.leg_position('FL', 9, -10)
    # time.sleep(pause)

    # r.leg_position('FL', 9, -10, z = 2)

    # r.leg_position('FR', 7, -6)
    # time.sleep(pause)
    # r.leg_position('FR', 12, -11)
    

    
    # r.leg_position('FR', 9, -10, z = -3)
    # r.leg_position('BL', 2, -6)
    # time.sleep(0.1)
    # r.leg_position('BL', -1, -17)
    # time.sleep(0.1)
    # r.leg_position('FR', 9, -10)
    # time.sleep(pause)
    # r.leg_position('FL', 7, -11, z = -3)
    # r.leg_position('BR', 2, -6)
    # time.sleep(0.1)
    # r.leg_position('BR', 2, -17)
    # time.sleep(0.1)
    # r.leg_position('FL', 7, -11)
    # time.sleep(pause)

    # #Front Paws up - Step 2:
    # r.leg_position('FL', 7, -6)
    # time.sleep(pause)
    # r.leg_position('FL', 9, -12)
    # time.sleep(pause)

    # r.leg_position('FR', 9, -6)
    # time.sleep(pause)
    # r.leg_position('FR', 10, -8)
    # time.sleep(pause)
    # r.leg_position('FR', 11, -13)
    # time.sleep(pause)

    
if __name__ == '__main__':
    r = Quadruped()
    stair(r)



