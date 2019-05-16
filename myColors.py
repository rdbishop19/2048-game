# Color file supporting 2048

BLACK = (0, 0, 0)
GREEN_1 = (0, 20, 0)
GREEN_2 = (0, 40, 0)
GREEN_3 = (0, 60, 0)
GREEN_4 = (0, 80, 0)
GREEN_5 = (0, 100, 0)
GREEN_6 = (0, 120, 0)
GREEN_7 = (0, 140, 0)
GREEN_8 = (0, 160, 0)
GREEN_9 = (0, 180, 0)
GREEN_10 = (0, 200, 0)
GREEN = (0, 255, 0)

color_dict = { 0:BLACK, 2:GREEN_1, 4:GREEN_2, 8:GREEN_3, 16:GREEN_4, 32:GREEN_5, 64:GREEN_6, 128:GREEN_7, 256:GREEN_8, 512:GREEN_9, 1024: GREEN_10, 2048:GREEN}
color_dict2 = { 2048:BLACK, 1024:BLACK, 512:BLACK, 256:BLACK, 128:BLACK, 64:GREEN, 32:GREEN, 16:GREEN, 8:GREEN, 4:GREEN, 2: GREEN, 0:GREEN}

def get_color_tile(i):
	return color_dict[i]

def get_color_num(i):
    return color_dict2[i]