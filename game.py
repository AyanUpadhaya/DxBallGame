# Dx ball game in python @ Ayan Upadhaya
# Press 'r' to play and pause

import turtle
from playsound import playsound
import random
import math

class Tiles:
	def __init__(self,number):
		self.number = number
		self.tiles_list = []
		self.space = 0 
	def CreateTiles(self,side,top):
		for i in range(0,self.number):
			self.tiles_list.append(turtle.Turtle())
		for tile in self.tiles_list:
			tile.shape('square')
			tile.color('white','yellow')
			tile.speed(0)
			tile.shapesize(stretch_wid = 1,stretch_len=2)
			tile.penup()
			tile.setposition(side+self.space,top)
			self.space+=45

	#for checking collision with ball and tiles

	def checkCollision(self,t1,t2):
		distance=math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
		if distance<15:
			return True

		else:
			return False
			
	

class Paddle:
	def __init__(self,master,shape,shapesize,color,speed,position):
		self.master = master
		self.shape = shape
		self.shapesize = shapesize
		self.color = color
		self.speed = speed
		self.position = position
	def draw(self):
		self.master.shape(self.shape)
		self.master.shapesize(stretch_wid = self.shapesize[0],stretch_len = self.shapesize[1])
		self.master.color(self.color)
		self.master.speed(self.speed)
		self.master.penup()
		self.master.goto(self.position[0],self.position[1])

	def paddle_move_left(self):
		x = self.master.xcor()
		x-=20
		self.master.setx(x)

	def paddle_move_right(self):
		x = self.master.xcor()
		x+=20
		self.master.setx(x)


class Ball(Paddle):
	def __init__(self,master,shape,shapesize,color,speed,position,dx,dy):
		super().__init__(master,shape,shapesize,color,speed,position)
		self.dx = dx #sine
		self.dy = dy #cosine

	def moveball(self):
		self.master.setx(self.master.xcor()+self.dx)
		self.master.sety(self.master.ycor()+self.dy)


class TitleWriter:
	def __init__(self,headeTitle,color,position):
		self.headTitle=headeTitle
		self.color = color
		self.position = position
		self.pen = turtle.Turtle()
		self.pen.hideturtle()
		self.pen.color(self.color)

	def writeTitle(self):
		self.pen.clear()
		self.pen.speed(0)
		self.pen.penup()
		self.pen.hideturtle()
		self.pen.goto(self.position[0],self.position[1])
		self.pen.write("{}".format(self.headTitle),align = "center",font=('Courier',18,'bold'))



#Game Class
class Game:
	def __init__(self,title,width,height,background,tracer):
		
		#window attributes

		self.window = turtle.Screen()
		self.title = title
		self.width = width
		self.height = height
		self.background = background
		self.tracer = tracer
		self.isPause = True
		self.limitScore = 0
		self.istileHide = False



		#objects
		self.paddle = Paddle(turtle.Turtle(),'square',[1,10],'white',0,[0,-250])
		self.ball = Ball(turtle.Turtle(),'circle',[1,1],'white',3,[0,0],1,-1)
		
		# tiles
		self.tiles = Tiles(12)
		self.tiles2 = Tiles(12)
		self.totalTiles = self.tiles.number+self.tiles2.number-5

		#Score Writer
		self.headTitle = TitleWriter('DX Ball','white',[0,260])
		self.gameOverTitle = TitleWriter('Game Over','white',[0,260])

		#limit writer
		self.limitWriter = LimitWriter('white',[-260,260])
		self.limitWriter.writeLimit(self.limitScore)


	#for pause and playing game press 'r'
	def pause_play(self):
		if self.isPause:
			self.isPause = False
		else:
			self.isPause = True



	def run(self):
		self.window.title(self.title)
		self.window.setup(width = self.width,height =self.height)
		self.window.bgcolor(self.background)
		self.window.tracer(self.tracer)

		#create objects

		self.paddle.draw()
		self.ball.draw()

		self.tiles.CreateTiles(-230,200)
		self.tiles2.CreateTiles(-230,175)

		#write head title
		self.headTitle.writeTitle()

		#event listener
		self.window.listen()
		self.window.onkeypress(self.paddle.paddle_move_left,"Left")
		self.window.onkeypress(self.paddle.paddle_move_right,"Right")
		self.window.onkeypress(self.pause_play,"r")
		

		run = True
		while run:

			if not self.isPause:
				self.ball.moveball()

				#controll ball
				if self.ball.master.ycor() > 290:
					self.ball.master.sety(290)
					self.ball.dy *= -1

				if self.ball.master.ycor() < -290:
					self.ball.master.sety(-290)
					self.ball.dy *= -1

				if self.ball.master.xcor() > 390:
					self.ball.master.setx(390)
					self.ball.dx *= -1

				if self.ball.master.xcor() < -390:
					self.ball.master.setx(-390)
					self.ball.dx *= -1 

			

				#paddle hitting by checking collision
				if (self.ball.master.ycor() < -235 and self.ball.master.ycor()> -250) and (self.paddle.master.xcor()+60 > self.ball.master.xcor() and self.paddle.master.xcor()-60 < self.ball.master.xcor()):	
					self.ball.dy *=-1
					playsound('sound/bounce.wav')
					self.window.update()

				#ball collision with tiles
				for tile in self.tiles.tiles_list:
					if self.tiles.checkCollision(tile,self.ball.master):
						self.istileHide = True
						tile.hideturtle()

						
			
				for tile2 in self.tiles2.tiles_list:
					if self.tiles.checkCollision(tile2,self.ball.master):
						self.istileHide = True
						tile2.hideturtle()
				


				self.window.update()
			else:
				self.window.update()



dxballGame = Game('Dx Ball',800,600,'black',3)

if __name__=="__main__":
	dxballGame.run()