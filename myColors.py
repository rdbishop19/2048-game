# Color file supporting 2048

BLACK = (0, 0, 0)
RED = (0, 20, 0)
PINK = (0, 40, 0)
PURPLE = (0, 60, 0)
DEEP_PURPLE = (0, 80, 0)
BLUE = (0, 100, 0)
TEAL = (0, 120, 0)
L_GREEN = (0, 140, 0)
GREEN = (0, 160, 0)
ORANGE = (0, 180, 0)
DEEP_ORANGE = (0, 200, 0)
BROWN = (0, 255, 0)

color_dict = { 0:BLACK, 2:RED, 4:PINK, 8:PURPLE, 16:DEEP_PURPLE, 32:BLUE, 64:TEAL, 128:L_GREEN, 256:GREEN, 512:ORANGE, 1024: DEEP_ORANGE, 2048:BROWN}
color_dict2 = { 2048:BLACK, 1024:BLACK, 512:BLACK, 256:BLACK, 128:BLACK, 64:BROWN, 32:BROWN, 16:BROWN, 8:BROWN, 4:BROWN, 2: BROWN, 0:BROWN}

def getColor(i):
	return color_dict[i]

def getColorNum(i):
    return color_dict2[i]