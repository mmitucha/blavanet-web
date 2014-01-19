 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from django.core.management import setup_environ
from blavanetproject import settings
setup_environ(settings)
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
import datetime
from django.contrib.auth.models import User
from blog.models import Post, Category



def main():
    parser = OptionParser()
    parser.add_option("-f", "--import-file", dest="import_file",
                      help="file to import from")
    parser.add_option("-m", "--model", dest="model", 
                      choices=["User", "Category", "Post"],
                      help="model to import [User, Category, Post]",)
    (options, args) = parser.parse_args()

    if options.model == "User":

        try:
            with open(options.import_file, "r") as f:
                users = json.load(f)
        except IOError:
            print("File does not exists.")
            sys.exit()

        n = 0
        for user in users:
            if (len(user['name'].split(" ")) > 1):
                first_name, last_name = user["name"].split(" ")
            else:
                first_name, last_name = user["name"], "" # Ugly hack
            if user['usertype'] == "Super Administrator":
                is_super_user = True
            else:
                is_super_user = False

            date_joined = datetime.datetime.strptime(
                                              user["registerdate"], 
                                              "%Y-%m-%dT%H:%M:%S"
                                              )

            try: 
                u = User(
                         email=user["email"], 
                         username=user["username"],
                         first_name=first_name,
                         last_name=last_name, 
                         # is_staff=True,
                         is_active=True,
                         is_superuser=is_super_user,
                         date_joined=date_joined,
                         )
                u.save()
            except IntegrityError:
                print("User '{0}' already exists, skipping.".format(user["username"]))

            n += 1
        print("Successfully uploaded {0} users.".format(n))


    elif options.model == "Category":

        try:
            with open(options.import_file, "r") as f:
                categories = json.load(f)
        except IOError:
            print("File does not exists.")
            sys.exit()

        n = 0
        for category in categories:
            try:
                c = Category(
                             title=category["title"],
                             description=category["description"]
                             )
                c.save()
            except IntegrityError:
                print("Category '{}' already exists, skipping".format(category["title"]))

            n += 1

        print("Successfully uploaded {0} categories.".format(n))

    elif options.model == "Post":

        try:
            with open(options.import_file, "r") as f:
                posts = json.load(f)
        except IOError:
            print("File does not exists.")
            sys.exit()


        n = 0
        for post in posts:

            created_at = datetime.datetime.strptime(
                                  post["created"], 
                                  "%Y-%m-%dT%H:%M:%S"
                                  )
            if post["modified"]:
                updated_at = datetime.datetime.strptime(
                                      post["modified"], 
                                      "%Y-%m-%dT%H:%M:%S"
                                      )
            else:
                updated_at = created_at
            # Joomla post states:
            #   0 - unpublished
            #   1 - published
            #   -1 - archived
            #   -2 - marked to deletion
            # We care just about Published or Unpublished
            if post["state"] == 1:
                published = True
            else:
                published = False

            try:
                author = User.objects.get(username=post["created"])
            # if user does not exists, try "admin" user
            except ObjectDoesNotExist:
                author = User.objects.get(username="admin")

            try:
                section = Category.objects.get(title=post["section"])
            except ObjectDoesNotExist:
                section = Category(title="Uncategorized").save()
            try:
                p = Post(
                         title=post["title"],
                         content=post["introtext"],
                         created_at=created_at,
                         updated_at=updated_at,
                         published=published,
                         author=author,
                         category=section,
                         )
                p.save()
            except IntegrityError:
                print("Post '{}' already exists, skipping".format(post["title"]))
            n += 1
        print("Successfully uploaded {0} posts.".format(n))


    else:
        print("You did not set up proper model to import.")

if  __name__ == "__main__":
    main()
