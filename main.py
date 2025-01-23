def goto(tx, ty):
    current_x = get_pos_x()
    current_y = get_pos_y()
    while current_x != tx:
        if current_x < tx:
            move(East)
            current_x += 1
        else:
            move(West)
            current_x -= 1
    while current_y != ty:
        if current_y < ty:
            move(North)
            current_y += 1
        else:
            move(South)
            current_y -= 1

def make_spiral_map(size):
    x, y = 0, 0
    dx, dy = 1, 0
    spiral_map = []

    for _ in range(size * size):
        spiral_map.append([x, y])

        nx = x + dx
        ny = y + dy

        if nx >= size:
            nx = 0
        elif nx < 0:
            nx = size - 1
        if ny >= size:
            ny = 0
        elif ny < 0:
            ny = size - 1

        if [nx, ny] in spiral_map:  # Check if next position already in path
            if dx == 1 and dy == 0:
                dx = 0
                dy = 1
            elif dx == 0 and dy == 1:
                dx = -1
                dy = 0
            elif dx == -1 and dy == 0:
                dx = 0
                dy = -1
            elif dx == 0 and dy == -1:
                dx = 1
                dy = 0

            nx = x + dx
            ny = y + dy
            if nx >= size:
                nx = 0
            elif nx < 0:
                nx = size - 1
            if ny >= size:
                ny = 0
            elif ny < 0:
                ny = size - 1

        x = nx
        y = ny

    return spiral_map

def water():
	if get_ground_type() == Grounds.Soil: # Could skip this if always soil
		while get_water() < 0.5:
			use_item(Items.Water)

def work(te):
	if can_harvest():
		return harvest()
	if te != Entities.Grass and get_entity_type() != te:
		return plant(te)
	if te == Entities.Grass and get_ground_type() == Grounds.Soil:
		till()
	return False

def work_basic(path, te, tg):
	for cell in path:
		goto(cell[0], cell[1])
		if get_ground_type() != tg:
			till()
		if get_entity_type() == None:
			plant(te)
	for cell in path:
		goto(cell[0], cell[1])
		work(te)
		
def work_pumpkin(path):
	for cell in path:
		goto(cell[0], cell[1])
		if get_entity_type() != Entities.Pumpkin:
			plant(Entities.Pumpkin)
			use_item(Items.Water)
	for cell in path:
		goto(cell[0], cell[1])
		while not can_harvest():
			if get_entity_type() != Entities.Pumpkin:
				plant(Entities.Pumpkin)
			if get_water() < 0.75: # Maybe do some math with w/s
				use_item(Items.Water)

size = None # int
groundType = None # Grounds
itemType = None # Entities
itemCap = 10000 # int
path = [] # list

while True:
	size = get_world_size()
	path = make_spiral_map(size)
	
	groundType = Grounds.Soil
	if num_items(Items.Hay) < itemCap:
		itemType = Entities.Grass
		groundType = Grounds.Grassland
	elif num_items(Items.Wood) < itemCap:
		itemType = Entities.Tree
	elif num_items(Items.Carrot) < itemCap:
		itemType = Entities.Carrot
	else:
		itemType = Entities.Pumpkin
	if itemType == Entities.Pumpkin:
		for cell in path:
			goto(cell[0], cell[1])
			if Grounds.Grassland == get_ground_type():
				till()
			if Entities.Pumpkin != get_entity_type():
				harvest() # Make sure its cleared
		work_pumpkin(path)
		goto(0, 0) # All pumpkins grown
		harvest()
	else:
		work_basic(path, itemType, groundType)
	