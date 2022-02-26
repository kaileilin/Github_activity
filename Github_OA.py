import requests
import csv 
import sys
from tqdm import tqdm
import pandas as pd
from pandas.io.json import json_normalize
import time
import pandas as pd
from time import sleep

# Initiliaze github api
github_api = "https://api.github.com"

# security token 
with requests.sessions.Session() as session:

    session.auth = ("kaileili", "")

pull_requests_url = github_api + '/repos/tensorflow/tensorflow/pulls'

issue_url = github_api + '/repos/tensorflow/tensorflow/issues'

commits_url = github_api +'/repos/tensorflow/tensorflow/commits'

contributors_url = github_api +'/repos/tensorflow/tensorflow/contributors'


# Contributor DataTable 

class contributors:
    def __init__(self,login,contributor_id,contributions):
        # Constants
        self.login = login
        self.contributor_id = contributor_id
        self.contributions = contributions

# Transever to dictionary 
    def as_dict(self):
        return {'login': self.login, 'id': self.contributor_id, 'contributions': self.contributions}


def get_contributors(repo,owner):

    # collect contributors from each repo
    sum_contributors = []
    
    
    contributors_url = github_api +'/repos/{}/{}/contributors'.format(owner,repo)
    
     
    # collect contributors names,id and their contributions count 
    # Make use of pagination parameter in Github API to return results up to the limit
    
    t = 0
    
    while t <300:
        
        response = session.get(contributors_url).json()

        t += 1
       
        for contributor in response:
            login = contributor['login']
            contributions = contributor['contributions']
            contributor_id = contributor['id']

            sum_contributors.append(contributors(login,contributor_id,contributions))


    return sum_contributors

    ## PR DataTable 

class Pull_Requsts:
    
    def __init__(self,title,pr_id,number,login,author_id,state,created_at,closed_at,updated_at,merged_at,language,Rr_id):
           # Constants
        self.title = title 
        self.pr_id = pr_id
        self.number = number
        self.login = login
        self.author_id = author_id
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.updated_at = updated_at
        self.merged_at = merged_at
        self.language = language 
        self.Rr_id = Rr_id

    
       
        
    def as_dict(self):
         # Transever to dictionary 
        return {'title': self.title, 'pull_id': self.pr_id, 
               'number': self.number,
                'state':self.state,
        'login' : self.login,
        'author_id': self.author_id, 
        'created_at' : self.created_at,
        'closed_at': self.closed_at,
        'updated_at': self.updated_at,
               'merged_at':self.merged_at,
               'language':self.language,
               'requested_reviewer_id':self.pr_id}

def get_pull_requests(repo,owner):
    
    pull_requests = []

    t = 0 

    # collect pull requests names,id and their requests count 
    # Make use of pagination parameter in Github API to return results up to the limit
    pull_requests_url = github_api +'/repos/{}/{}/pulls'.format(owner,repo)
    
    while t < 300 :
        
        response = session.get(pull_requests_url,params={'start': len(pull_requests_url), 'limit': 50
                                     }).json()

        t += 1 
        
        for pulls in response:

            title = pulls['title']
            pr_id = pulls['id']
            number =  pulls['number']
            state = pulls['state']
            login = pulls['user']['login']
            author_id = pulls['user']['id']
            created_at = pulls['created_at']
            closed_at = pulls['closed_at']
            updated_at = pulls['updated_at']
            merged_at = pulls['merged_at']
            language = pulls['head']['repo']['language']
            
            if len(pulls['requested_reviewers']) == 0:
                continue 
            else:
                Rr_id = pulls['requested_reviewers']
                
           


            pull_requests.append(Pull_Requsts(title,pr_id,number,login,author_id,state,created_at,closed_at,updated_at,merged_at,language,Rr_id))



    return(pull_requests) 

    ## Issues 

class issues:

    def __init__(self,title,isue_id,num,author,author_id,state,created_at,closed_at,updated_at,comments_cnt):
        # constants 
        self.title = title 
        self.isue_id = isue_id
        self.num = num
        self.author = author
        self.author_id = author_id
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.updated_at = updated_at
        self.comments_cnt = comments_cnt 
       
    
       
        
    def to_dict(self):
         # Transever to dictionary 
        return {'title':self.title,
        'isue_id':self.isue_id ,
        'num':self.num ,
        'author':self.author ,
        'author_id':self.author_id,
        'state':self.state ,
        'created_at':self.created_at,
        'closed_at':self.closed_at,
        'updated_at':self.updated_at,
        'comments_cnt':self.comments_cnt }

def get_issues(repo,owner):
    
    
    issues_list = []
  
    issue_url = github_api +'/repos/{}/{}/issues'.format(owner,repo)
    
    t = 0 
    while t <300:
        
        response = session.get(issue_url,params={'start': len(issue_url), 'limit': 50}).json()
        
        t += 1 

        for issue in response:

            title = issue['title']
            isue_id = issue['id']
            num =  issue['number']
            state = issue['state']
            author = issue['user']['login']
            author_id = issue['user']['id']
            created_at = issue['created_at']
            closed_at = issue['closed_at']
            updated_at = issue['updated_at']
            comments_cnt = issue['comments']



            issues_list.append(issues(title,isue_id,num,author,author_id,state,created_at,closed_at,updated_at,comments_cnt))


    return(issues_list) 

## Commits 

class commits:



    def __init__(self,message,sha,authored_date,author,author_id,committer_id,committed_date,comments_cnt):
        # Constants 
        self.message = message
        self.sha = sha
        self.authored_date = authored_date
        self.author = author
        self.author_id = author_id
        self.committer_id = committer_id
        self.committed_date = committed_date
        self.comments_cnt = comments_cnt
       
    
        
    def to_diction(self):
        # Transverse to Dictonary 
        return { 'message':self.message,
        'sha':self.sha,
        'authored_date':self.authored_date,
        'author':self.author,
       'author_id': self.author_id, 'committer_id': self.committer_id, 'committed_date' : self.committed_date,
               'comments_cnt': self.comments_cnt}

def get_commits(repo,owner):
    
    commits_list = []
    
    
    commits_url = github_api +'/repos/{}/{}/commits'.format(owner,repo)
    
    
    t = 0
    
    while t < 300:
        response = session.get(commits_url,params={'start': len(commits_url), 'limit': 50}).json()
        #time.sleep(60)  # wait 60 seconds
        t += 1
        for commit in response:
            message = commit['commit']['message']
            sha = commit['sha']
            authored_date = commit['commit']['author']['date']
            author = commit['author']['login']
            author_id = commit['author']['id']
            committer_id = commit['committer']['id']
            committed_date = commit['commit']['committer']['date']
            comments_cnt = commit['commit']['comment_count']

            commits_list.append(commits(message,sha,authored_date,author,author_id,committer_id,committed_date,comments_cnt))


    return(commits_list) 
   


if __name__ == "__main__":

    
    repo = sys.argv[1]

    owner = sys.argv[2]
    
    print("preparing for downloading contributors")
    #get_contributors(repo,owner)
    contributor_fun = get_contributors(repo,owner)
    df_contri = pd.DataFrame([x.as_dict() for x in contributor_fun])
    print(df_contri.head(10))
    print('let us rest ')
    time.sleep(90)
    print("preparing for downloading pull requests")
    #get_pull_requests(repo,owner)
    prs_API = get_pull_requests(repo,owner)
    df_prs = pd.DataFrame([x.as_dict() for x in prs_API ])
    print(df_prs.head(10))
    print('let us rest ')
    time.sleep(90)
    print("preparing for downloading issues")
    issue_API = get_issues(repo,owner)
    df_issue = pd.DataFrame([x.to_dict() for x in issue_API])
    print(df_issue.head(10))
    print('let us rest ')
    time.sleep(90)
    print("preparing for downloading commits")
    commit_API = get_commits(repo,owner)
    df_commit = pd.DataFrame([x.to_diction() for x in commit_API])
    print(df_commit.head(10))




