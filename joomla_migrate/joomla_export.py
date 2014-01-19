 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import MySQLdb
import json
import collections
import datetime
from optparse import OptionParser
import os

def get_entries(from_table, hostname, port, user, password, database, query_dict):
    
    db = MySQLdb.connect(
        host=hostname,
        port=port,
        user=user,
        passwd=password,
        db=database,
        use_unicode=True, 
        charset="utf8"
        )

    cursor = db.cursor()    

    queries = query_dict
    table = str(from_table)
    fields = queries[table]['fields']
    query = queries[table]['query']

    cursor.execute(query)
    rows = cursor.fetchall()


    rowarray_list = []
    for row in rows:
        a = collections.OrderedDict()
        # a = {}
        if len(row) == len(fields):
            n = 0
            for i in row:
                a[fields[n]] = i
                n += 1
        rowarray_list.append(a)

    db.close()

    return rowarray_list


def main():
    parser = OptionParser()
    parser.add_option("-H", "--host", dest="hostname",
                      help="database hostname")
    parser.add_option("-P", "--port", dest="port",
                      help="database port")
    parser.add_option("-d", "--database", dest="database",
                      help="database")
    parser.add_option("-u", "--user", dest="user",
                      help="database user")
    parser.add_option("-p", "--password", dest="password",
                      help="database user password")
    parser.add_option("-t", "--table-prefix", dest="table_prefix", default="jos",
                      help="joomla database table prefix, default is 'jos'")
    # parser.add_option("-d", "--directory", dest="directory", default="joomla_export",
    #                   help="files output directory")
    (options, args) = parser.parse_args()

    # if len(args) < 3:
    #     parser.error("wrong number of arguments")

    # print options
    # print args

    table_prefix = options.table_prefix or "jos"

    queries = {
        "users": {
            "fields": ["name", "username", "email", "registerdate", "usertype"], 
            "query": "SELECT name, username, email, registerdate, usertype FROM {}_users;".format(table_prefix),
            },
        "sections": {
            'fields': ['title', 'alias', 'description'],
            'query': "SELECT title, alias, description from {}_sections;".format(table_prefix),
        },
        "content": {
            "fields": ['id', 'title', 'alias', 'introtext', 'created', 'modified', 'created_by', 'state', 'access', "section" ],    # 'created_by' = content.created_by(int) join from table users.name(varchar)
            'query': "SELECT a.id, a.title, a.alias, a.introtext, a.created, a.modified, b.username, a.state, a.access, c.title \
                        FROM {0}_content a \
                            LEFT JOIN {0}_users b ON a.created_by = b.id \
                            LEFT JOIN {0}_sections c ON a.sectionid = c.id \
                                WHERE a.state != -2;".format(table_prefix)
        }
    }



    # Get entries from DB
    users = get_entries(
                        from_table='users', 
                        hostname=options.hostname, 
                        port=int(options.port),
                        database=options.database,
                        user=options.user,
                        password=options.password,
                        query_dict = queries,
                        )

    sections = get_entries(
                        from_table='sections', 
                        hostname=options.hostname, 
                        port=int(options.port),
                        database=options.database,
                        user=options.user,
                        password=options.password,
                        query_dict = queries,
                        )

    posts = get_entries(
                        from_table='content', 
                        hostname=options.hostname, 
                        port=int(options.port),
                        database=options.database,
                        user=options.user,
                        password=options.password,
                        query_dict = queries,
                        )



    # Change format from datetime to iso string
    for user in users:
        for entry in user:
            if type(user[entry]) == datetime.datetime:
                user[entry] = user[entry].isoformat()

    for section in sections:
        for entry in section:
            if type(section[entry]) == datetime.datetime:
                section[entry] = section[entry].isoformat()

    for post in posts:
        for entry in post:
            if type(post[entry]) == datetime.datetime:
                post[entry] = post[entry].isoformat()

    directory = "joomla_export"
    working_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(working_dir, directory)
    if os.path.exists(export_dir):
        pass
    else:
        os.mkdir(export_dir)


    # users_j = json.dumps(users)
    # sections_j = json.dumps(sections)
    # posts_j = json.dumps(posts)

    with open(os.path.join(export_dir, "users.json"), "w") as f:
        json.dump(users, f, indent=4, encoding="utf-8", separators=(',', ': '))
    with open(os.path.join(export_dir, "sections.json"), "w") as f:
        json.dump(sections, f, indent=4, encoding="utf-8", separators=(',', ': '))
    with open(os.path.join(export_dir, "posts.json"), "w") as f:
        json.dump(posts, f, indent=4, encoding="utf-8", separators=(',', ': '))

    print("Export successful")

if  __name__ == "__main__":
    main()


