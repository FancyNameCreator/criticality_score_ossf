import datetime

from run import get_repository

repo_url = "https://github.com/DefinitelyTyped/DefinitelyTyped"

repo = get_repository(repo_url)

issues_since_time = datetime.datetime.utcnow() - datetime.timedelta(days=180)
print(repo._repo.get_issues(state='open', since=issues_since_time).totalCount)