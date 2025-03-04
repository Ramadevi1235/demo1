import datetime

# Function to read attendance data from a text file
def read_attendance(file_name):
    attendance = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                date_str = line.strip()
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                attendance.append(date)
    except FileNotFoundError:
        pass
    return attendance

# Function to mark attendance
def mark_attendance(file_name):
    date_today = datetime.datetime.now().date()
    attendance = read_attendance(file_name)
    if date_today not in attendance:
        with open(file_name, 'a') as file:
            file.write(f"{date_today}\n")
        print("Attendance marked for today.")
    else:
        print("Attendance already marked for today.")

# Function to calculate required attendance
def calculate_days_needed(total_classes, attended_days, required_percentage):
    required_days = total_classes * (required_percentage / 100)
    days_needed = required_days - attended_days
    if days_needed < 0:
        days_needed = 0
    return days_needed

# Function to calculate attendance percentage
def calculate_attendance_percentage(attended_days, total_classes):
    percentage = (attended_days / total_classes) * 100
    return percentage

# Function to load user data
def load_user_data(file_name):
    user_data = {}
    try:
        with open(file_name, 'r') as file:
            for line in file:
                user_id, total_classes, required_percentage = line.strip().split(',')
                user_data[user_id] = {
                    "total_classes": int(total_classes),
                    "required_percentage": int(required_percentage)
                }
    except FileNotFoundError:
        pass
    return user_data


def save_user_data(file_name, user_data):
    with open(file_name, 'w') as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['total_classes']},{data['required_percentage']}\n")

def handle_choice(choice, user_id, user_data_file, attendance_file, user_data):
    switch_case = {
        '1': lambda: mark_attendance(attendance_file),
        '2': lambda: display_attendance_status(user_id, attendance_file, user_data[user_id]['total_classes'], user_data[user_id]['required_percentage']),
        '3': lambda: save_user_data(user_data_file, user_data),
        '4': lambda: print("Exiting the program.")
    }
    func = switch_case.get(choice, lambda: print("Invalid choice"))
    func()

# Function to display attendance status
def display_attendance_status(user_id, attendance_file, total_classes, required_percentage):
    attendance = read_attendance(attendance_file)
    attended_days = len(attendance)
    days_needed = calculate_days_needed(total_classes, attended_days, required_percentage)
    attendance_percentage = calculate_attendance_percentage(attended_days, total_classes)

    print(f"User ID: {user_id}")
    print(f"Total days attended: {attended_days}")
    print(f"Attendance percentage: {attendance_percentage:.2f}%")
    print(f"Total days yet to attend classes to reach {required_percentage}%: {days_needed}")

# Main code
user_data_file = 'user_data.txt'
user_data = load_user_data(user_data_file)

user_id = input("Please enter your USN number: \n")

if user_id not in user_data:
    # Hardcoded values for total classes and required percentage
    total_classes = 40
    required_percentage = 85
    user_data[user_id] = {
        "total_classes": total_classes,
        "required_percentage": required_percentage
    }

attendance_file = f"{user_id}_attendance.txt"

while True:
    print("\nChoose an option:")
    print("1. Mark attendance for today")
    print("2. Display attendance status")
    print("3. Save user data")
    print("4. Quit")

    choice = input("Enter your choice: ")
    if choice == '4':
        print("Exiting the program.")
        save_user_data(user_data_file, user_data)
        break
    handle_choice(choice, user_id, user_data_file, attendance_file, user_data)

