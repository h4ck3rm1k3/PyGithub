from github import Github

import netrc
n= netrc.netrc()
(login,account,password) = n.authenticators("github")

g = Github(login, password)

users = g.search_users("", location="OK")
seen ={}

def all_following():
    for person in g.get_user().get_following():
        seen[person.url] =1
        #print person.url
        # print person.bio
        # print person.email
        # print person.location
        # print person.gravatar_id

print "loading existing users"
all_following()

print "scanning new users"
for person in users:
#    print x
    if person.url not in seen :
        print person.url,person.bio, person.email, person.location

        status =g.get_user().add_to_following(person)
        # if not person.has_in_following():
        print "Adding",status, person.bio, person.email, person.location
        

