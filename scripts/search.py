from github import Github
import time
import netrc
import shelve

from github.GithubException import GithubException

def check_quota(g):
    rateLimit = g.get_rate_limit()
    requests_left = rateLimit.rate.remaining
    resettime  = rateLimit.rate.reset
    print "reset",resettime, "left",requests_left

    if requests_left <  2:
        now = datetime.datetime.now() 
        tosleep = (resettime-now).seconds
        print "going to sleep" , tosleep
        time.sleep(tosleep)

        print "going to sleep for one hour to avoid overusing the api"
        #sleep for one hour, you have 5000 api calls per hour https://developer.github.com/v3/#rate-limiting
        time.sleep(3601)        
    else:
        # give em a brake
        time.sleep(1)

def all_following(g):
    for person in g.get_user().get_following():
        seen[person.url.encode()] =1

def main(g):
    seen = shelve.open("shelvefile")

    if len(seen.keys())< 10 :  # if we are starting out,read in the existing users
        all_following(g)

    check_quota(g)
    print "scanning new users"

    my_user = g.get_user()
    #https://api.github.com/rate_limit
    for state in ( "MI", "MN", "WI", "ND", "IL", "MN", "KS", "OK", "NE", "CO", "TX", "WY", "SD", "IA", "AR", "KS", "MO"):
        print "searching for state %s" % state
        users = g.search_users("", location=state)
        for person in users:
            u = person.url.encode()
            if u not in seen :
                seen[u] =1
                #if not  my_user.has_in_following(person):
                print person.url,person.bio, person.email, person.location
                status = my_user.add_to_following(person)
                # if not person.has_in_following():
                print "Adding",status, person.bio, person.email, person.location
                check_quota(g)


while(True):

    n= netrc.netrc()
    (login,account,password) = n.authenticators("github")
    g = Github(login, password)

    try:
        main(g)
    except Exception as e:
        print e
        time.sleep(3600)
        check_quota(g)
