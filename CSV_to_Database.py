import  psycopg2
import pandas

conn = psycopg2.connect("dbname=Investment user=postgres password=123") 
cur = conn.cursor()
