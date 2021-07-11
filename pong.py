# https://youtu.be/XGf2GcyHPhc
import turtle
from playsound import playsound


# Window
swidth = 800    # screen width in pixels
sheight = 600   # screen height in pixels
hwidth = swidth/2  # half width
hheight = sheight/2  # half height
win = turtle.Screen()
win.title("Pong by The Monsters from @TokyoEdTech")
win.bgcolor("black")
win.setup(width=swidth, height=sheight)
win.tracer(0)

# Score
p_a_score = 0
p_b_score = 0

# Paddle A
p_a = turtle.Turtle()
p_a.speed(0)   # maximum movement speed
p_a.shape("square")  # default 20 px by 20 px
p_a.color("#ff6ecc")
p_a.shapesize(stretch_wid=5, stretch_len=1)    # 100 px tall, 20 px wide
p_a.penup()    # removes default line trail
p_a.goto(-((swidth/2)-40), 0)

# Paddle B
p_b = turtle.Turtle()
p_b.speed(0)   # maximum movement speed
p_b.shape("square")  # default 20 px by 20 px
p_b.color("#cd78ff")
p_b.shapesize(stretch_wid=5, stretch_len=1)    # 100 px tall, 20 px wide
p_b.penup()    # removes default line trail
p_b.goto(((swidth/2)-45), 0)

# Ball
speed = 0.15  # movement speed relative to cpu clock
ball = turtle.Turtle()
ball.speed(0)   # maximum movement speed
ball.shape("square")    # default 20 px by 20 px
ball.color("yellow")
ball.penup()    # removes default line trail
ball.goto(0, 0)  # 0,0 in center of turtle.Screen()
ball.dx = speed     # dx movement speed
ball.dy = speed   # dy movement speed

# Pen Scoreboard
pen = turtle.Turtle()
pen.speed(0)
pen.color("red")
pen.penup()
pen.hideturtle()
pen.goto(0, (hheight-40))
pen.write("Player A: " + str(p_a_score) + "  Player G: " +
          str(p_b_score), align="center", font=("Courier", 24, "normal"))

# Functions


def paddle_a_up():
    y = p_a.ycor()
    y += 20
    p_a.sety(y)


def paddle_a_dn():
    y = p_a.ycor()
    y -= 20
    p_a.sety(y)


def paddle_b_up():
    y = p_b.ycor()
    y += 20
    p_b.sety(y)


def paddle_b_dn():
    y = p_b.ycor()
    y -= 20
    p_b.sety(y)


def Sound_Pong():
    playsound(
        'C:\\Users\\dczel\\Desktop\\Examples\\PY-CSV-Graph\\PYGames\\Sounds\\Pong.wav')

def Sound_Score():
    playsound(
        'C:\\Users\\dczel\\Desktop\\Examples\\PY-CSV-Graph\\PYGames\\Sounds\\FartArmy.wav')


# Keyboard binding
win.listen()
win.onkeypress(paddle_a_up, "w")        # not upper case
win.onkeypress(paddle_a_dn, "s")        # not upper case
win.onkeypress(paddle_b_up, "Up")       # Up arrow
win.onkeypress(paddle_b_dn, "Down")     # Down arrow


# Main game loop
while True:
    win.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)    # + dx sets direction of first movement
    ball.sety(ball.ycor() + ball.dy)    # + dy sets direction of first movement

    # Border checking
    if ball.ycor() > (hheight-10):      # check upper screen edge
        ball.sety(hheight-10)
        ball.dy *= -1
        Sound_Pong()

    elif ball.ycor() < -(hheight-15):   # check lower screen edge
        ball.sety(-(hheight-15))
        ball.dy *= -1
        Sound_Pong()

    elif ball.xcor() > (hwidth-5):     # check right screen edge
        p_a_score += 1    # increase paddle_a score
        pen.clear()
        pen.write("Player A: " + str(p_a_score) + "  Player G: " +
                  str(p_b_score), align="center", font=("Courier", 24, "normal"))
        Sound_Score()
        ball.goto(0, 0)
        ball.dx *= -1

    elif ball.xcor() < -(hwidth):    # check left screen edge
        p_b_score += 1    # increase paddle_b score
        pen.clear()
        pen.write("Player A: " + str(p_a_score) + "  Player Gw: " +
                  str(p_b_score), align="center", font=("Courier", 24, "normal"))
        Sound_Score()
        ball.goto(0, 0)
        ball.dx *= -1

    # Paddle and ball collisions
    if (ball.xcor() > (hwidth-63) and ball.xcor() < (hwidth-50)) and (p_b.ycor() + 40 >= ball.ycor() >= p_b.ycor() - 40):
        ball.setx(hwidth-63)
        ball.dx *= -1
        Sound_Pong()

    if (ball.xcor() < -(hwidth-58) and ball.xcor() > -(hwidth-50)) and (p_a.ycor() + 40 >= ball.ycor() >= p_a.ycor() - 40):
        ball.setx(-(hwidth-58))
        ball.dx *= -1
        Sound_Pong()
