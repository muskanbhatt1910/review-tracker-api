import mysql.connector

def getReview() :
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bhatt",
    database="Reviews"
    )

    mycursor = mydb.cursor()

    mycursor.execute("Select * from pari_data where Store = 'Acer PS';")
    row = mycursor.fetchall()[0]

    return row
    # mycursor.execute("Select Week(curdate())")
    # week = (mycursor.fetchall())[0][0]
    # # print(week)

    # sql = "INSERT INTO Pari_Data VALUES (%s, " + str(week) + ", %s, %s, %s);"
    # mycursor.executemany(sql, rows)

    # mydb.commit()

    # print(mycursor.rowcount, "was inserted.")
