from  .database.connection import get_connection
from  .models.account import UserBankAccount


def create_account(name, phone, pin):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO accounts (name, phone, pin)
            VALUES (?, ?, ?)
        """, (name, phone, pin))

        connection.commit()

        account = UserBankAccount(
            name=name,
            phone=phone,
            pin=pin
        )

        return account

    except Exception as error:
        print("Error creating account:", error)
        return None

    finally:
        connection.close()