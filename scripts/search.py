from github import Github
import time
import netrc

n= netrc.netrc()
(login,account,password) = n.authenticators("github")

g = Github(login, password)
(requests_left, limit)=g.rate_limiting
print "left",requests_left, "limit", limit
#seen ={}
import shelve

seen = shelve.open("shelvefile")

def all_following():
    for person in g.get_user().get_following():
        seen[person.url.encode()] =1

if len(seen.keys())< 10 :  # if we are starting out,read in the existing users
    all_following()


print "scanning new users"
my_user = g.get_user()
#https://api.github.com/rate_limit
for state in ( "MI", "MN", "WI", "ND", "IL", "MN", "KS", "OK", "NE", "CO", "TX", "WY", "SD", "IA", "AR", "KS", "MO"):
    print "searching for state %s" % state
    users = g.search_users("", location=state)
    for person in users:
        (requests_left, limit)=g.rate_limiting
        print "left",requests_left, "limit", limit
        u = person.url.encode()
        if u not in seen :
            seen[u] =1
            #if not  my_user.has_in_following(person):
            print person.url,person.bio, person.email, person.location
            status = my_user.add_to_following(person)
            # if not person.has_in_following():
            print "Adding",status, person.bio, person.email, person.location


        else:
            print "Already Follows,", person.url

        if requests_left <  2:
            print "going to sleep for one hour to avoid overusing the api"
            #sleep for one hour, you have 5000 api calls per hour https://developer.github.com/v3/#rate-limiting
            time.sleep(3601)        
        else:
            # give em a brake
            time.sleep(1)
