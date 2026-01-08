"""
Setup MySQL database for Salon Backend
"""

import pymysql
import os

def setup_database():
    try:
        # Connect to MySQL (without database)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS salon_db")
        print("✅ Database 'salon_db' created or already exists")
        
        # Use the database
        cursor.execute("USE salon_db")
        
        # Show tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"📋 Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("📋 No tables found - run migrations first")
        
        connection.close()
        print("\n🎯 Database setup complete!")
        print("📝 Next steps:")
        print("   1. python manage.py makemigrations")
        print("   2. python manage.py migrate")
        print("   3. python manage.py createsuperuser")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_database()
