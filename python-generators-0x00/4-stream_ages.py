import seed

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield float(age)
    cursor.close()
    connection.close()

def average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    print(f"Average age of users: {total / count if count > 0 else 0:.2f}")

if __name__ == "__main__":
    average_age()
