from numpy import append
import pygame
import sys

from pygame.constants import K_RETURN

pressedKeys = []


def processInstruct(instructString: list):

    # instructionString format ABXY

    # AB denotes type of transformation
    # XY specify numerical values associated with transformation

    # for x in instructString:
    #     print(pygame.key.name(x))

    # Checking for transformation type
    # Length less than 2 causes index range error
    if (len(instructString) > 2 and pygame.key.name(instructString[0]) +
            pygame.key.name(instructString[1]) == 'rn'):
        print("rotate")
        # call roation function with parameters pygame.key.name(instructString[2]) and more


def keyPressed(eventKey):

    pressedKeys.append(eventKey)
    # print(pressedKeys)
    if eventKey == pygame.K_q:
        sys.exit()

    elif eventKey == pygame.K_RETURN:
        processInstruct(pressedKeys)
        pressedKeys.clear()