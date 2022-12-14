from flask import *
from flask_cors import CORS
import mysql.connector
import json
import logging
import pandas as pd
from flask import Flask, request

app = Flask(__name__)
CORS(app)


class Store:
      def __init__(self, value, label):
        self.value = value
        self.label = label

# stores_selected = ('HP GHM', 'Asus PS', 'Lenovo PS')

def getReview(stores_selected_str) :
  if(len(stores_selected_str)) == 0 :
    return [0,0,0,0]


  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="bhatt",
  database="Reviews"
  )

  mycursor = mydb.cursor()

  # Sql Query
  # stores_selected = ('HP GHM', 'Asus PS', 'Lenovo PS')
  print("my sql query: ", "Select Store, Rating, Current_Reviews, Avg_Rating_Current_Wk, New_Rev_Current_Wk from Pari WHERE Store in " + stores_selected_str +";")
  mycursor.execute("Select Store, Rating, Current_Reviews, Avg_Rating_Current_Wk, New_Rev_Current_Wk from Pari WHERE Store in " + stores_selected_str +";")
  rows = mycursor.fetchall()

  # Dataframe Calculations
  df = pd.DataFrame(rows, columns=['Store', 'Rating', 'Reviews', 'Avg_Rating_Current_Wk', 'New_Rev_Current_Wk'])

  total_reviews = int(df.Reviews.sum(axis=0))
  avg_rating = float(round(((df.Rating*df.Reviews).sum(axis=0)/total_reviews),2))
  Total_New_reviews_wk = int(df.New_Rev_Current_Wk.sum(axis=0))

  if Total_New_reviews_wk>0:
    Avg_Rating_Wk = int((df.Avg_Rating_Current_Wk*df.New_Rev_Current_Wk).sum(axis=0)/Total_New_reviews_wk)
  else:
    Avg_Rating_Wk = 0

  # Final Values
  values = [avg_rating, total_reviews, Avg_Rating_Wk, Total_New_reviews_wk]

  # Check Val
  # print(values)

  # Close SQL connection
  mydb.close()
  
  return values

@app.route('/', methods=['GET', 'POST'])
def index():
  print("API called")
  stores_selected = ()
  print("json.loads(request.data)", json.loads(request.data))
  if (json.loads(request.data) != {} and json.loads(request.data) != None):
    print("enters if: request.data is not null")
    if 'selectedStores' in json.loads(request.data):
      print("enters if: request.data containsStores")
      if (json.loads(request.data))['selectedStores'] :
        stores_selected = (json.loads(request.data))['selectedStores']
        print("stores_selected within if nested", stores_selected)
  print("final stores_selected value", stores_selected)
  # print(len(stores_selected))
  stores_selected_str = ""
  if len(stores_selected) > 0:
    stores_selected_str = '(\'' + stores_selected[0] + '\')'

  if len(stores_selected)>1:
    stores_selected_str = str(tuple(stores_selected))
    
  print("str tuple value: ", stores_selected_str)
  row = getReview(stores_selected_str)
  value = [
    {
      "title":"Rating",
      "value":row[0],
      "diff":"20",
      "id": "total_rating"
    },
    {
      "title":"Total Reviews",
      "value":row[1],
      "diff":"10",
      "id": "total_reviews"
    },
    {
      "title":"Average rating this week",
      "value":row[2],
      "diff":"2",
      "id": "avg_rating_week"
    },
    {
      "title":"New reviews this week",
      "value":9,
      "diff":"2",
      "id": "total_reviews_week"
    }
  ]
  
  #logging.info("Muskan",json.dumps(value))
  return json.dumps(value)

@app.route('/stores/')
def get_stores():

  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="bhatt",
  database="Reviews"
  )

  mycursor = mydb.cursor()

  mycursor.execute("Select store from pari;")
  col = mycursor.fetchall()
  stores_list = []
  json_list = []
  for i in col:
    stores_list.append(i[0])
    store_json = {
      "value" : i[0], 
      "label" : i[0]
    }
    json_list.append(store_json)

  print(json_list)
  mydb.close()
  
  return json_list
  # print(stores_list)
  # return json.dumps(stores_list)

  # Stores = []
  # for store_name in stores_list:
  #   Stores.append(Store(store_name,store_name))

  # return Stores
  # return "Muskan"
  # return str("Muskan")

  # value = [
  #     {
  #         "title":"Rating",
  #         "value":row[2],
  #         "diff":"20"
  #     },
  #     {
  #         "title":"Total Reviews",
  #         "value":row[4],
  #         "diff":"10"
  #     },
  #     {
  #         "title":"Average rating this week",
  #         "value":row[3],
  #         "diff":"2"
  #     }
  # ]
  
  # #logging.info("Muskan",json.dumps(value))
  # return json.dumps(value)
#adding variables
@app.route('/user/<username>')
def show_user(username):
  #returns the username
  return 'Username: %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
  #returns the post, the post_id should be an int
  return str(post_id)


@app.route('/pari_data', methods=['GET', 'POST'])
def get_pari_data():
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="bhatt",
  database="Reviews"
  )

  mycursor = mydb.cursor()

  mycursor.execute("Select * from pari_data;")
  rows = mycursor.fetchall()
  pari_data = []
  for row in rows:
    row_data = {
      "store_name" : row[0], 
      "week_number" : row[1],
      "total_rating" : row[2],
      "avg_rating_week" : row[3],
      "total_reviews" : row[4]
    }
    pari_data.append(row_data)

  print(pari_data)
  mydb.close()
  
  return pari_data