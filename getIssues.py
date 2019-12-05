import pygsheets
from github import Github
import json

with open('git_secret.json') as json_file:
    git_creds = json.load(json_file)

git = Github(git_creds['login_username'], git_creds['password'])
repo = git.get_repo(git_creds['repo'])

issues = repo.get_issues(state='open')

issuesClosed = repo.get_issues(state='closed')

# The headers of your spreadsheet
matrix_issues = [['number', 'title', 'state', 'opened on', 'closed on', 'feature','min','max']]


def get_labels(label):
    label = label.name
    result = ''
    containsFeat = label.find('Feat')
    containsEst = label.find('Est')
    if containsEst != -1:
        estimate = label.replace('Est:', '').replace('days', '').split('-')
        result = estimate[0]
        result = estimate[1]
    elif containsFeat != -1:
        result = label.replace('Feat:', '')
    return


# Add as many get as you'd like

def get_feat(labels):
    return [x.name.replace('Feat:', '') for x in labels if 'Feat:' in x.name]


def get_est(labels):
    return get_min_max([x.name.replace('Est:', '').replace('days', '') for x in labels if 'Est:' in x.name])


def get_min_max(est):
    try:
        min_max = est[0].split('-')
    except:
        min_max = ['', '']
    finally:
        return min_max


def convert_to_list(issue):
    closedAt = 0
    if issue.closed_at:
        closedAt = issue.closed_at.strftime('%Y/%m/%d')
    createdAt = issue.created_at.strftime('%Y/%m/%d')
    feat = get_feat(issue.labels)
    min_max = get_est(issue.labels)
    separator = ','
    return [issue.number, issue.title, issue.state, createdAt, closedAt,separator.join(feat)] + min_max


listIssues = list(map(convert_to_list, issues))
print(listIssues[0])
listClosedIssues = list(map(convert_to_list, issuesClosed))
matrix_issues += listIssues + listClosedIssues

gc = pygsheets.authorize()

# The name of your google spreadsheet
print('begining writing')
sh = gc.open('git_hub_issues')
wks = sh[0]
wks.update_values('A1:M999', matrix_issues)
