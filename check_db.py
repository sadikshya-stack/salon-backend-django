"""
Check existing database tables and data
"""

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def check_database():
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='salon_db',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("🗄️ Database: salon_db")
        print("=" * 40)
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print("📋 Tables found:")
            for table in tables:
                table_name = table[0]
                print(f"  - {table_name}")
                
                # Count records in each table
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    Records: {count}")
        else:
            print("❌ No tables found")
        
        connection.close()
        print("\n✅ Database check complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database()
