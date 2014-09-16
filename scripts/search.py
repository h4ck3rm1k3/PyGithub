from github import Github
import time
import netrc

followed = 0 
n= netrc.netrc()
(login,account,password) = n.authenticators("github")

g = Github(login, password)


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

for state in ( "MI", "MN", "WI", "ND", "IL", "MN", "KS", "OK", "NE", "CO", "TX", "WY", "SD", "IA", "AR", "KS", "MO"):
    print "searching for state %s" % state
    users = g.search_users("", location=state)
    for person in users:
        if person.url not in seen :
            print person.url,person.bio, person.email, person.location
            status =g.get_user().add_to_following(person)
            # if not person.has_in_following():
            print "Adding",status, person.bio, person.email, person.location
            followed = followed +1
            if followed > 4999:
                print "going to sleep for one hour to avoid overusing the api"
                #sleep for one hour, you have 5000 api calls per hour https://developer.github.com/v3/#rate-limiting
                time.sleep(3601)
                followed = 0 # reset the count
