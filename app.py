#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request
import mysql.connector

#mysql connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Comeon1997",
  database="cricket_score"
)


#over_data={"run":0,"wickets":0,"extras":0,"player1_score":0,"player2_score":0}

mycursor = mydb.cursor()
#fetch latest ball from the database
#sql="select ball_num from ball_wise order by over_num,ball_num desc limit 1"
#mycursor.execute(sql)
#res=mycursor.fetchone()
count=0
#if res is not None:
#	count=res[0]
#if(count==6):
#	count=0

app = Flask(__name__)
p1=1
p2=2
player1=0
player2=0
# to fetch the latest scores when the program starts
mycursor.execute("select runs from players where player_no="+str(p1))
player1=mycursor.fetchone()[0]
mycursor.execute("select runs from players where player_no="+str(p2))
player1=mycursor.fetchone()[0]

# add ball data
@app.route('/scores/api/v1.0/add_ball', methods=['POST'])
def create_task():
	global count
	if not request.json:
		abort(400)
	ball = {
	'over_num':request.json['over_num'],
	'ball_num':request.json['ball_num'],
	'run':request.json['run'],
	'wicket':request.json['wicket'],
        'extra':request.json['extra'],
	'player_id':request.json['player_id']
	}
	return update_database(ball)

#function to update score in the database
def update_database(ball):
	#at any given point player1,player2 stores scores of player1,player2 resp
	global count,p1,p2,player1,player2
	wicket =0
	extras =0
	flag=0
	

	#if the ball is the first ball of the over add data to oversdata because of foreign key constraint in the database
	if(ball['ball_num']==1):
		if(ball["extra"]!="none"):
			extras=ball["run"]
		if(ball["player_id"]==1 and ball["extra"]=="none"):
			player1=player1+ball["run"]
		if(ball["player_id"]==2 and ball["extra"]=="none"):
			player2=player2+ball["run"] 
		#if the player gets out
		if(ball["wicket"]==True):
			wicket=1
			flag=1
			#change the status of the player to out and change current player
			if(ball["player_id"]==1):
				mycursor.execute("update players set status='out' where player_no="+str(p1))
				mydb.commit()
				p1=max(p1,p2)+1
				player1=0
			else:
				mycursor.execute("update players set status=\"out\" where player_no="+str(p2))
				mydb.commit()
				p2=max(p1,p2)+1
				player2=0	
					
		#insert values into overs table data
		sql="INSERT INTO overs_data values (%s,%s,%s,%s,%s,%s)"
		num=ball['over_num']+1
		val = (num,ball['run'], wicket,extras,player1,player2)
		count+=1
		mycursor.execute(sql, val)
		mydb.commit()
		
	#when the ball is not the first ball of the over
	else:
		if(ball["extra"]!="none"):
			extras=ball['run']
		if(ball["player_id"]==1 and ball["extra"]=="none"):
			player1=player1+ball["run"]
		if(ball["player_id"]==2 and ball["extra"]=="none"):
			player2=player2+ball["run"] 
		#if the wicket falls change the player1 and player2 and make runs of that player as 0
		if(ball["wicket"]==True):
			wicket=1
			if(ball["player_id"]==1 and ball["run"]%2==0):
				sql="UPDATE overs_data set wickets=wickets+1,player1_score=0 where over_num="+str(ball['over_num']+1)
				mycursor.execute(sql)
				mydb.commit()
				mycursor.execute("update players set status=\"out\" where player_no="+str(p1))
				mydb.commit()
				p1=max(p1,p2)+1
				player1=0
			else:
				sql="UPDATE overs_data set wickets=wickets+1,player2_score=0 where over_num="+str(ball['over_num']+1)
				mycursor.execute(sql)
				mydb.commit()
				
				mycursor.execute("update players set status=\"out\" where player_no="+str(p2))
				mydb.commit()
				p2=max(p1,p2)+1
				player2=0
		
		# update overs data		
		sql="UPDATE overs_data set runs=runs+%s,extras=extras+%s,player1_score=%s,player2_score=%s where over_num=%s"
		val=(ball['run'],extras,player1,player2,ball['over_num']+1)
		mycursor.execute(sql,val)
		mydb.commit()

	# update players score and status to not out
	mycursor.execute("update players set runs=%s,status='not out' where player_no=%s",(player1,p1))
	mydb.commit()
	mycursor.execute("update players set runs=%s,status='not out' where player_no=%s",(player2,p2))
	mydb.commit()
	
	
	#insert data into balls table where data of every ball is stored
	sql="INSERT INTO ball_wise values(%s,%s,%s,%s,%s,%s)"
	val=(ball['ball_num'],ball['over_num']+1,ball['run'],ball['wicket'],ball['extra'],ball['player_id'])
	mycursor.execute(sql,val)
	mydb.commit()

        #return the current ball
	return jsonify({'ball': ball}), 201


@app.route('/scores/api/v1.0/over_data/<int:over>',methods=['GET'])
def send_overs_data(over):

	if(over<=0): 			#if the invalid over is entered
		return "invalid over"	
	sql="select * from overs_data where over_num="+str(over)
	mycursor.execute(sql)
	data=mycursor.fetchone()
	field_names=['over_num','runs','wickets','extras','player1','player2']
	over_data=dict(zip(field_names, data))
	if(data is not None):
		return jsonify({'over': over_data})
		

@app.route('/scores/api/v1.0/all_data',methods=['GET'])
def all_data():
	mycursor.execute("select * from overs_data")
	result=mycursor.fetchall()
	total_runs=0
	total_wickets=0
	total_extras=0
	players=[]
	for row in result:
		total_runs+=row[1]
		total_wickets+=row[2]
		total_extras+=row[3]
	all_data={"runs":total_runs,"wickets":total_wickets,"extras":total_extras}
	
	#add all players scores till now
	mycursor.execute("select * from players where status='out' or status='not out'")
	result=mycursor.fetchall()
	for row in result:
		player="player"+str(row[0])
		all_data[player]=row[1]
	
	return jsonify({'all_data':all_data})
	

if __name__ == '__main__':
    app.run(debug=True)
