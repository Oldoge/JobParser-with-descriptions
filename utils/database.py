import sqlite3
import os

class JobDatabase:
    def __init__(self, db_path="results/jobs.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # create jobs table with additional fields for analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                grade TEXT,
                salary TEXT,
                country TEXT,
                posted TEXT,
                link TEXT UNIQUE,
                source TEXT,
                description TEXT,
                match_score INTEGER DEFAULT NULL,
                analysis_report TEXT DEFAULT NULL
            )
        ''')
        self.conn.commit()

    def save_job(self, job):
        """save job to database, ignoring duplicates based on link"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO jobs 
                (title, grade, salary, country, posted, link, source, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job.get("Title"),
                job.get("Grade"),
                job.get("Salary"),
                job.get("Country"),
                job.get("Posted"),
                job.get("Link"),
                job.get("Source"),
                job.get("Description")
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating database: {e}")

    def get_all_jobs(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM jobs')
        return cursor.fetchall()

    def close(self):
        self.conn.close()