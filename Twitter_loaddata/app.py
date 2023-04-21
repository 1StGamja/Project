from flask import Flask, render_template, request
import psycopg2
import os
from sqlalchemy import distinct
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    today = datetime.today().strftime("%Y%m%d")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="dlQmsdl00"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS public.twt_jogeon_{today} (LIKE public.twt_jogeon_20230421)")
    cursor.close()
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="dlQmsdl00",
        options=f"-c search_path=public,twt_jogeon_{today}"
    )

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    keyword_filter = request.args.get('keyword_filter', '', type=str)
    author_filter = request.args.get('author_filter', '', type=str)
    limit = 30
    offset = (page - 1) * limit

    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = f"SELECT COUNT(*) FROM public.twt_jogeon_{datetime.today().strftime('%Y%m%d')}"
    query_params = []

    if keyword_filter or author_filter:
        query += " WHERE"
        if keyword_filter:
            query += " keyword = %s"
            query_params.append(keyword_filter)
            if author_filter:
                query += " AND"
        if author_filter:
            query += " author_screen_name = %s"
            query_params.append(author_filter)

    cursor.execute(query, query_params)
    total_rows = cursor.fetchone()[0]
    total_pages = -(-total_rows // limit)

    query = (
        f"SELECT id, created_at, author_name, author_screen_name, keyword, full_text "
        f"FROM public.twt_jogeon_{datetime.today().strftime('%Y%m%d')}"
    )
    
    if keyword_filter or author_filter:
        query += " WHERE"
        if keyword_filter:
            query += " keyword = %s"
            if author_filter:
                query += " AND"
        if author_filter:
            query += " author_screen_name = %s"
    
    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    query_params.extend([limit, offset])
    cursor.execute(query, query_params)

    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        'index.html',
        results=results,
        page=page,
        total_pages=total_pages,
        keyword_filter=keyword_filter,
        author_filter=author_filter
    )

if __name__ == '__main__':
    app.run(host='192.168.1.235', port=5000, debug=True)
