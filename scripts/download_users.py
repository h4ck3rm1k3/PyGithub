from github import Github
import time
import netrc
import shelve
import pprint
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

def all_following(seen, g):
    for person in g.get_user().get_following():
       
        data = [
            pprint.pprint(person),
            person.url,
            person.avatar_url,
            person.blog,
            person.bio,
            person.company,
            person.collaborators,
            person.contributions,
            person.created_at,
            person.disk_usage,
            person.followers,
            person.following,
            person.gravatar_id,
            person.hireable,
            person.html_url,
            person.id,
            person.type,
            person.updated_at,
            person.url,
            person.email,
            person.location
        ]

        #if not  my_user.has_in_following(person):
        #print "\t".join([str(x).encode('utf8') for x in ])
        print             person.url
        
        seen[person.url.encode()] =data
        check_quota(g)

def main(g):
    seen = shelve.open("shelvefile2")

    all_following(seen,g)



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
