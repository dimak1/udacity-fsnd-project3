#!/usr/bin/env python3
#
# Full Stack Nanodegree Program - Udacity
# Project 3 - Logs Analysis
# Author - Dima K

import psycopg2
import sys

print("Starting Logs Analysis...")

DBNAME = "news"


def connect():
    """Connect to database"""
    global conn, cur
    try:
        conn = psycopg2.connect(database=DBNAME)
        cur = conn.cursor()
        print("Successfully connected to '" + DBNAME + "' database.")
    except:
        print("Error connecting to database. Exiting...")
        sys.exit()


def disconnect():
    """Disconnect from database"""
    cur.close()
    conn.close()
    print("\nDisconnected from database. Exiting...")


def print_top_articles():
    """What are the most popular three articles of all time?"""

    create_view_top_articles = (
        "CREATE VIEW top_articles AS " +
        "SELECT COUNT(path) AS num, path " +
        "FROM log GROUP BY path ORDER BY num DESC;")
    get_popular_articles_names = (
        "SELECT title, num " +
        "FROM top_articles, articles " +
        "WHERE top_articles.path LIKE '%' || articles.slug limit 3;")

    cur.execute(create_view_top_articles)
    cur.execute(get_popular_articles_names)
    results = cur.fetchall()
    for result in results:
        print("\t", result[0], "-", result[1], "views")


def print_top_authors():
    """Who are the most popular article authors of all time?"""

    create_view_top_authors = (
        "CREATE VIEW top_authors as " +
        "SELECT sum(num) as views, author " +
        "FROM top_articles, articles " +
        "WHERE top_articles.path LIKE '%' || articles.slug GROUP BY author;")
    get_popular_artists = (
        "SELECT name, views " +
        "FROM authors, top_authors " +
        "WHERE top_authors.author = authors.id ORDER BY views DESC;")

    cur.execute(create_view_top_authors)
    cur.execute(get_popular_artists)
    results = cur.fetchall()
    for result in results:
        print("\t", result[0], "-", result[1], "views")


def print_errors():
    """On which days did more than 1% of requests lead to errors?"""

    create_view_total_requests = (
        "CREATE VIEW total_requests AS " +
        "SELECT date(time), count(status) as count " +
        "FROM log GROUP BY date;")
    create_view_error_requests = (
        "CREATE VIEW error_requests AS " +
        "SELECT date(time), count(status) as count " +
        "FROM log WHERE status LIKE '404%' GROUP BY date;")
    calculate_error_percentage = (
        "SELECT total_requests.date, ROUND(" +
        "(CAST(error_requests.count as decimal)/" +
        "total_requests.count*100.00),2) as percent " +
        "FROM total_requests, error_requests " +
        "WHERE total_requests.date=error_requests.date AND " +
        "(CAST(error_requests.count as decimal)/" +
        "total_requests.count*100.00)>1 ORDER BY percent DESC;")

    cur.execute(create_view_total_requests)
    cur.execute(create_view_error_requests)
    cur.execute(calculate_error_percentage)

    results = cur.fetchall()
    for result in results:
        print('\t{0:%B %d, %Y} - {1}% errors'.format(result[0], result[1]))
        # print("\t", result[0], "-", result[1], "% errors")


if __name__ == '__main__':
    connect()
    print("\nRunning Task 1: " + print_top_articles.__doc__ + "\n")
    print_top_articles()
    print("\nRunning Task 2: " + print_top_authors.__doc__ + "\n")
    print_top_authors()
    print("\nRunning Task 3: " + print_errors.__doc__ + "\n")
    print_errors()
    disconnect()
