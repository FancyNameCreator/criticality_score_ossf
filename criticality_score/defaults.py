# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Defaults used in OSS criticality score calculation."""
import re

# Weights for various parameters.
CREATED_SINCE_WEIGHT = 1            # selected
UPDATED_SINCE_WEIGHT = -1
CONTRIBUTOR_COUNT_WEIGHT = -3       # selected
ORG_COUNT_WEIGHT = 1
COMMIT_FREQUENCY_WEIGHT = 1
RECENT_RELEASES_WEIGHT = 0.5
OPEN_ISSUES_WEIGHT = 1              # selected
UPDATED_ISSUES_WEIGHT = 0.5
COMMENT_FREQUENCY_WEIGHT = 1
DEPENDENTS_COUNT_WEIGHT = 2         # selected

# Max thresholds for various parameters.
CREATED_SINCE_THRESHOLD = 120
UPDATED_SINCE_THRESHOLD = 120
CONTRIBUTOR_COUNT_THRESHOLD = 5000
ORG_COUNT_THRESHOLD = 10
COMMIT_FREQUENCY_THRESHOLD = 1000
RECENT_RELEASES_THRESHOLD = 26
OPEN_ISSUES_THRESHOLD = 5000
UPDATED_ISSUES_THRESHOLD = 5000
COMMENT_FREQUENCY_THRESHOLD = 15
DEPENDENTS_COUNT_THRESHOLD = 500000
DEPENDENTS_PAGERANK_THRESHOLD = 3

# Others.
TOP_CONTRIBUTOR_COUNT = 15
ISSUE_LOOKBACK_DAYS = 180
RELEASE_LOOKBACK_DAYS = 365
FAIL_RETRIES = 7

# Regex to match dependents count.
DEPENDENTS_REGEX = re.compile(b'.*[^0-9,]([0-9,]+).*commit result', re.DOTALL)


# Available signals
SIGNALS = [
    'created_since',
    'updated_since',
    'contributor_count',
    'org_count',
    'commit_frequency',
    'recent_releases_count',
    'updated_issues_count',
    'open_issues_count',
    'comment_frequency',
    'dependents_count'
]
