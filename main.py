import turtle, math, random
TAU = 6.283185
PHI = 1.618033

screen = turtle.Screen()
screen.bgcolor('White')
screen.tracer(1500)

bill = turtle.Turtle()
bill.hideturtle()
bill.color('Red')
bill.speed(0)




def tri(left_corner, side_length):
  bill.penup()
  bill.goto(*left_corner)
  bill.pendown()
  for _ in range(3):
    bill.forward(side_length)
    bill.left(120)


def sierp_tri(left_corner, side_length, depth = 6):
  if depth == 0:
    tri(left_corner, side_length)
    return
  
  mdpt_left = (left_corner[0] + side_length / 4, 
               left_corner[1] + side_length * math.sqrt(3) / 4)
  mdpt_bottom = (left_corner[0] + side_length / 2, 
                 left_corner[1])
  
  sierp_tri(left_corner, side_length/2, depth-1)
  sierp_tri(mdpt_left, side_length/2, depth-1)
  sierp_tri(mdpt_bottom, side_length/2, depth-1)


def square(bottom_left, side_length):
  bill.penup()
  bill.goto(*bottom_left)
  bill.pendown()
  for _ in range(4):
    bill.forward(side_length)
    bill.left(90)


#try to make faster
def sierp_carpet(bottom_left, side_length, depth = 6):
  if depth == 0:
    return
  
  new_side_length = side_length / 3
  x, y = bottom_left
  
  square((x, y), side_length)
  square((x + new_side_length, y + new_side_length), new_side_length)

  colors = ['Blue', 'Green', 'BlueViolet', 'Red', ]
  bill.color(colors[random.randint(0, 3)])
  
  sierp_carpet((x, y), new_side_length, depth - 1)

  x += new_side_length
  sierp_carpet((x, y), new_side_length, depth - 1)

  x += new_side_length
  sierp_carpet((x, y), new_side_length, depth - 1)

  y += new_side_length
  sierp_carpet((x, y), new_side_length, depth - 1)

  y += new_side_length
  sierp_carpet((x, y), new_side_length, depth - 1)

  x -= new_side_length
  sierp_carpet((x, y), new_side_length, depth - 1)

  x -= new_side_length
  sierp_carpet((x, y), new_side_length, depth - 1)

  y -= new_side_length
  sierp_carpet((x, y), new_side_length, depth - 1)


def pent(center, r):
  bill.penup()
  bill.goto(center[0], center[1] + r)
  bill.pendown()
  
  bill.goto(center[0] - r*0.951056, 
            center[1] + r*0.309017)
  bill.goto(center[0] - r*0.587785,
            center[1] - r*0.809016)
  bill.goto(center[0] + r*0.587784,
            center[1] - r*0.809017)
  bill.goto(center[0] + r*0.951056,
            center[1] + r*0.309016)
  bill.goto(center[0], center[1] + r)


def invis_pent(center, r):
  return [(center[0], center[1] + r),
          (center[0] - r*0.951056, center[1] + r*0.309017),
          (center[0] - r*0.587785, center[1] - r*0.809016),
          (center[0] + r*0.587784, center[1] - r*0.809017),
          (center[0] + r*0.951056, center[1] + r*0.309016),
          (center[0], center[1] + r)]


def sierp_pent(center, r, depth = 6):
  if depth == 0:
    pent(center, r)
    return
  
  new_r = r/(1 + PHI)
  
  lst_new_centers = invis_pent(center, r - new_r)
  
  colors = ['Blue', 'Green', 'BlueViolet', 'Red', ]
  for new_center in lst_new_centers:
    bill.color(colors[random.randint(0, 3)])
    sierp_pent(new_center, new_r, depth - 1)


def sum(start, end, func):
  sum = 0
  for k in range(start, end + 1):
    sum += func(k)
  return sum


def reg_poly(sides, center, r):
  one_angle = TAU/sides
  angle = 0

  lst_verticies = []
  x = center[0] + r*math.cos(angle)
  y = center[1] + r*math.sin(angle)
  lst_verticies.append((x, y))
  
  bill.penup()
  bill.goto(x, y)
  bill.pendown()
  
  for _ in range(sides):
    angle += one_angle
    x = center[0] + r*math.cos(angle)
    y = center[1] + r*math.sin(angle)
    lst_verticies.append((x, y))
    bill.goto(x, y)
  
  return lst_verticies


def invis_reg_poly(sides, center, r):
  one_angle = TAU/sides
  angle = 0

  lst_verticies = []
  x = center[0] + r*math.cos(angle)
  y = center[1] + r*math.sin(angle)
  lst_verticies.append((x, y))
  
  for _ in range(sides):
    angle += one_angle
    x = center[0] + r*math.cos(angle)
    y = center[1] + r*math.sin(angle)
    lst_verticies.append((x, y))

  return lst_verticies


def n_flake_recurs(n, center, r, scale_fact, depth = 6):
  if depth == 0:
    reg_poly(n, center, r)
    return

  new_r = r * scale_fact
  new_centers = invis_reg_poly(n, center, r - new_r)

  colors = ['Blue', 'Green', 'BlueViolet', 'Red', ]
  for new_center in new_centers:
    bill.color(colors[random.randint(0, 3)])
    n_flake_recurs(n, new_center, new_r, scale_fact, depth - 1)


def n_flake(n, center, r, depth = 6):
  scale_fact = 1/(2*(1 + sum(1, int(n/4), lambda k: math.cos(TAU*k/n))))
  n_flake_recurs(n, center, r, scale_fact, depth)


def chaos(center, r, reps):
  reg_poly(3, center, r)
  verticies = invis_reg_poly(3, center, r)
  bill.penup()
  bill.goto(verticies[0])
  bill.pendown()

  x, y = center
  for _ in range(reps):
    vertex = verticies[random.randint(0, 2)]
    x += (vertex[0] - x)/2
    y += (vertex[1] - y)/2
    
    bill.penup()
    bill.goto(x, y)
    bill.pendown()
    bill.dot()




#sierp_carpet((-200, -200), 500)
#sierp_pent((0, 0), 300)
n_flake(6, (0, 0), 300)
#chaos((0, 0), 300, 100000)
screen.update()
turtle.done()