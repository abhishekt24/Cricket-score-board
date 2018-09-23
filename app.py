#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Comeon1997",
  database="cricket_score"
)

over_data={"run":0,"wickets":0,"extras":0,"player1_score":0,"player2_score":0}
overs=[{}]
mycursor = mydb.cursor()
sql="select ball_num from ball_wise order by over_num,ball_num desc limit 1"
mycursor.execute(sql)
count=int(mycursor.fetchone()[0])
if(count==6):
	count=0
app = Flask(__name__)


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


def update_database(ball):
	global count
	wicket =0
	extras =0
	player1 =0
	player2 =0
	if(count==0):
		if(ball["wicket"]==True):
			wicket=1
		if(ball["extra"]!="none"):
			extras=ball["run"]
		if(ball["player_id"]==1 and ball["extra"]=="none"):
			player1=ball["run"]
		if(ball["player_id"]==2 and ball["extra"]=="none"):
			player2=ball["run"] 
		sql="INSERT INTO overs_data values (%s,%s,%s,%s,%s,%s)"
        	#sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
		num=ball['over_num']+1
		val = (num,ball['run'], wicket,extras,player1,player2)
		count+=1
		mycursor.execute(sql, val)
		mydb.commit()
	else:
		if(ball["extra"]!="none"):
			extras=ball['run']
		if(ball["player_id"]==1 and ball["extra"]=="none"):
			player1=ball["run"]
		if(ball["player_id"]==2 and ball["extra"]=="none"):
			player2=ball["run"] 
		if(ball["wicket"]==True):
			wicket=1
			if(ball["player_id"]==1 and ball["run"]%2==0):
				sql="UPDATE overs_data set wickets=wickets+1,player1_score=0"
				mycursor.execute(sql)
				mydb.commit()
			else:
				sql="UPDATE overs_data set wicket=wicket+1,player2_score=0"
				mycursor.execute(sql)
				mydb.commit()
		sql="UPDATE overs_data set runs=runs+%s,extras=%s,player1_score=player1_score+%s,player2_score=player2_score+%s where 	over_num=%s"
		val=(ball['run'],extras,player1,player2,ball['over_num']+1)
		mycursor.execute(sql,val)
		mydb.commit()
		
	sql="INSERT INTO ball_wise values(%s,%s,%s,%s,%s,%s)"
	val=(ball['ball_num'],ball['over_num']+1,ball['run'],ball['wicket'],ball['extra'],ball['player_id'])
	mycursor.execute(sql,val)
	mydb.commit()

    

	if(ball["extra"]!="NB" and ball["extra"]!="WD"):
		count+=1
	if(count==6):
		count=0
	#over_data={"run":0,"wickets":0,"extras":0,"player1_score":0,"player2_score":0}
	#overs.append(over_data)
	return jsonify({'ball': ball}), 201


@app.route('/scores/api/v1.0/over_data',methods=['GET'])
def send_overs_data():
	 return jsonify({'over': overs})
if __name__ == '__main__':
    app.run(debug=True)
