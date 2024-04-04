import pymongo
import datetime
import time 
import serial

# MongoDB connection code
MONGODB_URI = "mongodb+srv://sysadmin:kraFY1B9omw619ik@attendance-system.cumins2.mongodb.net/?retryWrites=true&w=majority&appName=attendance-system"

# Connecting to the database
client = pymongo.MongoClient(MONGODB_URI)
db = client["attendance_db"] 
attendance_collection = db["attendance"]
students_collection = db["students"]


#Code to just check if connection is succesful
try:
    client = pymongo.MongoClient(MONGODB_URI)
    result = client.admin.command('ismaster') 
    print("Connected to MongoDB!")
except Exception as e:
    print(f"An error occurred: {e}")


# Creating the student collection
def create_students_collection():
    try:
        db.create_collection("students")  
        print("Students collection created successfully.")
    except Exception as e:
        print(f"Message: {e}")

# Attendance Function (marks the attendance by checking the correct lecture)
def mark_attendance(student_name):
    now = datetime.datetime.now()

    if 19 <= now.hour < 21:  
        lecture_number = 1
    elif 21 <= now.hour < 23:  
        lecture_number = 2
    else:
        lecture_number = 0  

    today = now.date()

    # Check if the student exists in the 'students' collection
    student_exists = students_collection.find_one({"student_name": student_name})

    if student_exists is None:
        print(f"Student '{student_name}' not found. Please add them to the student list.")
    else:
        # Checks if there is an existing record already
        existing_record = attendance_collection.find_one({
            "student_name": student_name,
            "lecture_number": lecture_number,
            "date": today.isoformat()
        })

        if existing_record is None:
            attendance_document = {
                "student_name": student_name,
                "lecture_number": lecture_number,
                "date": today.isoformat(),
                "time": now.time().isoformat() 
          }
            attendance_collection.insert_one(attendance_document)
            print(f"Attendance marked for {student_name}, lecture {lecture_number}")
        else:
            print("Student already marked present for this lecture today")



# Serial Port Configuration
ser = serial.Serial('/dev/ttyACM0', 9600)  

def read_rfid_from_arduino():
    while True:
        rfid_data = ser.readline().decode().strip()
        if rfid_data:  # Only return if there's actual data, igores empty data strings
            return rfid_data
        else:
            time.sleep(0.5)  # Small delay to avoid overloading the serial port, scans every 0.5 sec

# Main Logic
if __name__ == "__main__":
    create_students_collection() # Optional: Call to create 'students' collection

    while True:
        RFID_tag = read_rfid_from_arduino()
        if RFID_tag: 
            if RFID_tag == "Student1": 
                mark_attendance('student1')
            elif RFID_tag == "Student2":
                mark_attendance('student2')
            elif RFID_tag == "unknown":
                print("Unknown card/tag detected")

