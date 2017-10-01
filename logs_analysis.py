#!/usr/bin/env python3
#
# Full Stack Nanodegree Program - Udacity
# Project 3 - Logs Analysis
# Author - Dima K

import psycopg2
import sys

DBNAME = "news"


def connect():
    """Connect to database"""
    try:
        conn = psycopg2.connect(database=DBNAME)
        cur = conn.cursor()
        # print("Successfully connected to '" + DBNAME + "' database.")
        return conn, cur
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error connecting to database: \n" + error)
        print("\nExiting...")
        sys.exit()


def disconnect(conn, cur):
    """Disconnect from database"""
    cur.close()
    conn.close()
    # print("\nDisconnected from database.")


def print_top_articles():
    """What are the most popular three articles of all time?"""

    create_view_top_articles = (
        "CREATE VIEW top_articles AS " +
        "SELECT COUNT(path) AS num, path " +
        "FROM log GROUP BY path ORDER BY num DESC;")
    get_popular_articles_names = (
        "SELECT title, num " +
        "FROM top_articles, articles " +
        "WHERE top_articles.path = '/article/' || articles.slug limit 3;")

    print("\nRunning Task: " + print_top_articles.__doc__ + "\n")

    conn, cur = connect()
    cur.execute(create_view_top_articles)
    cur.execute(get_popular_articles_names)
    results = cur.fetchall()

    for title, views in results:
        print('\t{} - {} views'.format(title, views))

    disconnect(conn, cur)


def print_top_authors():
    """Who are the most popular article authors of all time?"""

    create_view_top_articles = (
        "CREATE VIEW top_articles AS " +
        "SELECT COUNT(path) AS num, path " +
        "FROM log GROUP BY path ORDER BY num DESC;")
    create_view_top_authors = (
        "CREATE VIEW top_authors as " +
        "SELECT sum(num) as views, author " +
        "FROM top_articles, articles " +
        "WHERE top_articles.path LIKE '%' || articles.slug GROUP BY author;")
    get_popular_artists = (
        "SELECT name, views " +
        "FROM authors, top_authors " +
        "WHERE top_authors.author = authors.id ORDER BY views DESC;")

    print("\nRunning Task: " + print_top_authors.__doc__ + "\n")

    conn, cur = connect()
    cur.execute(create_view_top_articles)
    cur.execute(create_view_top_authors)
    cur.execute(get_popular_artists)
    results = cur.fetchall()

    for title, views in results:
        print('\t\"{}\" - {} views'.format(title, views))

    disconnect(conn, cur)


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

    print("\nRunning Task: " + print_errors.__doc__ + "\n")

    conn, cur = connect()
    cur.execute(create_view_total_requests)
    cur.execute(create_view_error_requests)
    cur.execute(calculate_error_percentage)
    results = cur.fetchall()

    for result in results:
        print('\t{0:%B %d, %Y} - {1}% errors'.format(result[0], result[1]))

    disconnect(conn, cur)


if __name__ == '__main__':
    print("Starting Logs Analysis...")
    print_top_articles()
    print_top_authors()
    print_errors()
    print("Finished Logs Analysis...")
