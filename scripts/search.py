from github import Github

import netrc
n= netrc.netrc()
(login,account,password) = n.authenticators("github")

g = Github(login, password)

users = g.search_users("", location="Kansas")

for person in users:
#    print x
    status =g.get_user().add_to_following(person)
    # if not person.has_in_following():
    print "Adding",status, person.bio, person.email, person.location
        


def all_following():
    for person in g.get_user().get_following():
        print person.bio
        print person.email
        print person.location
        print person.gravatar_id
