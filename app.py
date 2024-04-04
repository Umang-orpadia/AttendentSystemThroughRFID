from bottle import route, run, template, request
from pymongo import MongoClient
import datetime

MONGODB_URI = "mongodb+srv://sysadmin:kraFY1B9omw619ik@attendance-system.cumins2.mongodb.net/?retryWrites=true&w=majority&appName=attendance-system"

client = MongoClient(MONGODB_URI)
db = client["attendance_db"]
attendance_collection = db["attendance"]

def get_attendance_data(date=None): 
  if date:
    attendance_records = attendance_collection.find({"date": date})
  else:
    attendance_records = attendance_collection.find() 

  attendance_data = []
  for record in attendance_records:
    record['_id'] = str(record['_id']) 
    attendance_data.append(record) 
  return attendance_data

@route('/') 
def admin_panel():
  return template('admin.html') 

@route('/attendance') 
def get_attendance():
  attendance_data = get_attendance_data()
  return {'attendance': attendance_data} 

@route('/attendance/<date>') 
def get_attendance_for_date(date):
    attendance_data = get_attendance_data(date) 
    return {'attendance': attendance_data} 

run(host='0.0.0.0', port=8080, debug=True)
