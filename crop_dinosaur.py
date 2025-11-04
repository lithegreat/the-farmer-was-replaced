# ===== 恐龙养殖模块 =====
# 类似贪吃蛇的智能算法，使用 measure() 追踪苹果位置
# 装备恐龙帽，吃苹果增长尾巴，收获 n² 根骨头
# 策略：持续吃苹果直到完全无法移动
# 使用 list 记录尾巴路径来避免碰撞

import utils

# 全局变量：记录恐龙尾巴的路径
tail_path = []

def abs_value(n):
	if n < 0:
		return -n
	return n

def is_position_in_tail(x, y):
	# 检查位置是否在尾巴路径中
	for pos in tail_path:
		if pos[0] == x and pos[1] == y:
			return True
	return False

def add_position_to_tail(x, y):
	# 添加位置到尾巴路径
	tail_path.append([x, y])

def farm_dinosaur(target_size=None):
	global tail_path
	
	# 如果指定了目标大小，调整农场
	if target_size != None:
		current_size = get_world_size()
		if current_size != target_size:
			set_world_size(target_size)
	
	# 获取农场大小
	size = get_world_size()
	
	# 检查仙人掌资源
	cactus_count = num_items(Items.Cactus)
	required_cactus = size * size
	
	if cactus_count < required_cactus:
		return False
	
	# 装备恐龙帽
	change_hat(Hats.Dinosaur_Hat)
	
	# 初始化尾巴路径，记录起始位置
	tail_path = []
	start_x = get_pos_x()
	start_y = get_pos_y()
	add_position_to_tail(start_x, start_y)
	
	# 无限循环，直到四个方向都无法移动
	stuck_count = 0
	max_attempts = size * size * 10
	attempts = 0
	
	while attempts < max_attempts:
		# 获取下一个苹果的位置
		apple_pos = measure()
		apple_x = apple_pos[0]
		apple_y = apple_pos[1]
		
		# 尝试导航到苹果
		success = navigate_to_apple(apple_x, apple_y, size)
		
		if not success:
			if try_any_move_avoid_tail():
				stuck_count = 0
			else:
				stuck_count = stuck_count + 1
				if stuck_count >= 3:
					break
		else:
			stuck_count = 0
		
		attempts = attempts + 1
	
	# 卸下恐龙帽
	change_hat(Hats.Straw_Hat)
	
	return True


def can_move_to(x, y, world_size):
	# 检查位置是否在地图范围内且不在尾巴路径中
	if x < 0 or x >= world_size or y < 0 or y >= world_size:
		return False
	return not is_position_in_tail(x, y)

def safe_move(direction, world_size):
	# 安全移动：检查目标位置是否安全，然后移动并记录
	current_x = get_pos_x()
	current_y = get_pos_y()
	
	# 计算目标位置
	target_x = current_x
	target_y = current_y
	
	if direction == North:
		target_y = current_y + 1
	else:
		if direction == South:
			target_y = current_y - 1
		else:
			if direction == East:
				target_x = current_x + 1
			else:
				if direction == West:
					target_x = current_x - 1
	
	# 检查目标位置是否安全
	if can_move_to(target_x, target_y, world_size):
		if move(direction):
			# 移动成功，记录新位置到尾巴
			add_position_to_tail(target_x, target_y)
			return True
	
	return False

def navigate_to_apple(target_x, target_y, world_size):
	max_steps = world_size * 2
	steps = 0
	last_distance = -1
	stuck_count = 0
	
	while steps < max_steps:
		# 获取当前位置
		current_x = get_pos_x()
		current_y = get_pos_y()
		
		# 计算曼哈顿距离
		distance = abs_value(target_x - current_x) + abs_value(target_y - current_y)
		
		if distance == 0:
			return True
		
		# 检查是否卡住
		if last_distance != -1 and distance >= last_distance:
			stuck_count = stuck_count + 1
			if stuck_count >= 4:
				# 尝试所有可能的方向
				if try_alternative_path_avoid_tail(target_x, target_y, world_size):
					stuck_count = 0
				else:
					return False
		else:
			stuck_count = 0
		
		last_distance = distance
		
		# 计算x和y方向的距离
		dx = target_x - current_x
		dy = target_y - current_y
		
		# 优先向距离更大的方向移动
		moved = False
		
		if abs_value(dx) >= abs_value(dy):
			# x方向距离更大
			if dx > 0:
				if safe_move(East, world_size):
					moved = True
			else:
				if safe_move(West, world_size):
					moved = True
			
			# 如果x方向失败，尝试y方向
			if not moved:
				if dy > 0:
					if safe_move(North, world_size):
						moved = True
				else:
					if safe_move(South, world_size):
						moved = True
		else:
			# y方向距离更大
			if dy > 0:
				if safe_move(North, world_size):
					moved = True
			else:
				if safe_move(South, world_size):
					moved = True
			
			# 如果y方向失败，尝试x方向
			if not moved:
				if dx > 0:
					if safe_move(East, world_size):
						moved = True
				else:
					if safe_move(West, world_size):
						moved = True
		
		if not moved:
			# 尝试其他可用的方向（绕路）
			if try_any_move_avoid_tail_internal(world_size):
				moved = True
			else:
				return False
		
		steps = steps + 1
	
	return False


def try_any_move_avoid_tail_internal(world_size):
	# 尝试任意方向移动，避开尾巴
	directions = [North, East, South, West]
	
	for direction in directions:
		if safe_move(direction, world_size):
			return True
	
	return False


def try_any_move_avoid_tail():
	# 不带world_size参数的版本，用于主循环
	world_size = get_world_size()
	return try_any_move_avoid_tail_internal(world_size)


def try_alternative_path_avoid_tail(target_x, target_y, world_size):
	# 当卡住时，尝试垂直方向移动以绕过障碍（尾巴）
	current_x = get_pos_x()
	current_y = get_pos_y()
	
	# 计算当前方向的垂直方向
	dx = target_x - current_x
	dy = target_y - current_y
	
	# 尝试垂直于目标方向的移动
	if abs_value(dx) > abs_value(dy):
		# 主要是横向移动，尝试纵向
		if safe_move(North, world_size):
			return True
		if safe_move(South, world_size):
			return True
	else:
		# 主要是纵向移动，尝试横向
		if safe_move(East, world_size):
			return True
		if safe_move(West, world_size):
			return True
	
	# 如果垂直方向也失败，尝试所有方向
	return try_any_move_avoid_tail_internal(world_size)


def farm_dinosaur_efficient(apple_count=50):
	global tail_path
	
	size = get_world_size()
	
	# 检查资源
	cactus_count = num_items(Items.Cactus)
	if cactus_count < apple_count:
		return False
	
	# 装备恐龙帽
	change_hat(Hats.Dinosaur_Hat)
	
	# 初始化尾巴路径
	tail_path = []
	start_x = get_pos_x()
	start_y = get_pos_y()
	add_position_to_tail(start_x, start_y)
	
	# 吃指定数量的苹果
	apples_eaten = 0
	max_attempts = apple_count * 5
	attempts = 0
	
	while apples_eaten < apple_count and attempts < max_attempts:
		apple_pos = measure()
		apple_x = apple_pos[0]
		apple_y = apple_pos[1]
		
		if navigate_to_apple(apple_x, apple_y, size):
			apples_eaten = apples_eaten + 1
		else:
			if not try_any_move_avoid_tail():
				break
		
		attempts = attempts + 1
	
	# 卸下恐龙帽
	change_hat(Hats.Straw_Hat)
	
	return True


def farm_dinosaur_optimal():
	cactus_count = num_items(Items.Cactus)
	
	# 根据资源选择农场大小
	if cactus_count >= 400:
		target_size = 6
	else:
		if cactus_count >= 200:
			target_size = 5
		else:
			if cactus_count >= 100:
				target_size = 4
			else:
				return False
	
	return farm_dinosaur(target_size)
