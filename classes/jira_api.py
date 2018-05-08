__author__ = "Peter Maddison"
__copyright__ = "Copyright 2018, Peter Maddison"
__version__ = "1.0"
__maintainer__ = "Peter Maddison"
__email__ = "peter.maddison@bmo.com"
__status__ = "Development"

import requests
import json
import logging
import base64 as b64
from requests.auth import HTTPBasicAuth
logger = logging.getLogger(__name__)


class JIRAApi(object):
    """
    JIRA API for automation tests
    """
    def __init__(self, username, password):
        """
        Initialize a session with authorization
        @param username: Username of user
        @param password: Password of user
        """
        self._BASE_URL = 'http://192.168.33.30:8080/rest/api/2'
        self.s = requests.Session()
        self.s.auth = (username, password)
        self.s.verify = False
        
    def get_issue(self, issue_key_id, fields='all'):
        """
        Get issue information.
        
        STATUS 200 Application/json.Returns a full representation of an issue in JSON format.
        STATUS 404 Returned if the requested issue was not found, or the user does not have permission to view it.
        
        
        @param issue_key_id: Issue key or id
        @param fields: Multi-value parameter defining the fields returned for the issue. 
            By default, all fields are returned. Allowed values:
            *all - return all fields.
            *navigable - return navigable fields only.
            summary,comment - return the summary and comments fields only.
            -comment - return all fields except comments.
            *all,-comment - same as above
        @return: response
        """
        logger.info("getting issue detail")
        url = "{}/issue/{}".format(self._BASE_URL, issue_key_id)
        payload = {'fields': fields}
        return self.s.get(url, params=payload)

    def get_issue_changelog(self, issue_key_id):
        logger.info("getting issue changelog detail")
        url = "{}/issue/{}?expand=changelog&fields=changelog".format(self._BASE_URL, issue_key_id)
        return self.s.get(url)

    def get_issue_summary(self, issue_key_id):
        logger.info("getting issue changelog detail")
        url = "{}/issue/{}?expand=summary&fields=summary".format(self._BASE_URL, issue_key_id)
        return self.s.get(url)    
    
    def delete_issue(self, issue_key_id):
        """
        Delete issue
        
        STATUS 400 Returned if an error occurs.
        STATUS 401 Returned if the calling user is not authenticated.
        STATUS 204 Returned if the issue was successfully removed.
        STATUS 403 Returned if the calling user does not have permission to delete the issue.
        STATUS 404 Returned if the issue does not exist.
        
        @param issue_key_id: Issue key or id
        @return: response
        """
        logger.info("Deleting issue")
        url = "{}/issue/{}".format(self._BASE_URL, issue_key_id)
        return self.s.delete(url)
        
    def remove_attachment(self, attachment_id):
        """
        Remove an attachment from an issue
        
        STATUS 204 Removal was successful
        STATUS 403 The calling user is not permitted to remove the requested attachment.
        STATUS 404 Any of: there is no attachment with the requested id or attachments feature is disabled
        
        @param attachment_id: Attachment id
        @return: response
        """
        logger.info("removing attachment")
        url = "{}/attachment/{}".format(self._BASE_URL, attachment_id)
        return self.s.delete(url)
    
    def delete_comment(self, issue_key_id, comment_id):  
        """
        Delete an Issue comment.
        
        STATUS 400 Returned if the input is invalid (e.g. missing required fields, invalid values, and so forth).
        STATUS 204 Returned if delete was successful
        
        @param issue_key_id: Issue key or id
        @param comment_id: Comment id
        @return response
        """
        logger.info("Deleting comment")
        url = "{}/issue/{}/comment/{}".format(self._BASE_URL, issue_key_id, comment_id)
        return self.s.delete(url)
    
    def edit_issue(self, issue_key_id, payload):  
        """
        edits an issue.
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-editIssue
        
        STATUS 400 Returned if the issue update has failed.
        STATUS 204 Returned if the issue was updated successfully.
        STATUS 403 Returned if the user attempts disabling email notification or override screen security but doesn't have permission to do that.
        
        @param issue_key_id: Issue key or id
        @param payload: (Dict) Payload
        @return response
        """
        logger.info("Editing Issue")
        url = "{}/issue/{}".format(self._BASE_URL, issue_key_id)
        return self.s.put(url, json=payload)
    
    def get_issue_watchers(self, issue_key_id):
        """
        Returns the list of watchers for the issue with the given key.
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-getIssueWatchers
        
        STATUS 200 Application/json.Returns the list of watchers for the issue.
        STATUS 404 Returned if the requested issue was not found, or the user does not have permission to view it.
        
        @param issue_key_id: Issue key or id
        @return response
        """
        logger.info("Getting Issue Watchers")
        url = "{}/issue/{}/watchers".format(self._BASE_URL, issue_key_id)
        return self.s.get(url)
    
    def remove_watcher(self, issue_key_id, username):
        """
        Removes the user from the issue's watcher list.
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-getIssueWatchers
        
        STATUS 400 Returned if the query parameter was not supplied.username
        STATUS 401 Returned if the user does not have permission to remove the issue's watcher.
        STATUS 204 Returned if the watcher was removed successfully.
        STATUS 404 Returned if the issue does not exist.
        
        @param issue_key_id: Issue key or id
        @return response
        """
        logger.info("Removing Issue Watcher")
        payload = {"username": username}
        url = "{}/issue/{}/watchers".format(self._BASE_URL, issue_key_id)
        return self.s.delete(url, params=payload)
    
    
    def get_votes(self, issue_key_id):
        """
        Returns voting data for an issue - whether the issue was voted for, 
        total number of votes and users who voted for the issue.
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-getVotes
        
        STATUS 200 - application/json.Voting data for the current issue.
        STATUS 404 Returned if the user does not have permission to view the issue or voting is disabled.
        
        @param issue_key_id: Issue key or id
        @return response
        """
        logger.info("Getting Issue Vote")
        url = "{}/issue/{}/votes".format(self._BASE_URL, issue_key_id)
        return self.s.get(url)
    
    def remove_vote(self, issue_key_id):
        """
        Removes a current user's vote from an issue (aka "unvote").
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-removeVote
        
        STATUS 204 Empty response body is returned on success.
        STATUS 404 Returned if the user cannot remove a vote for some reason. 
            Possible reasons: the user did not vote on the issue, the user is the reporter, 
            voting is disabled, the issue does not exist, etc.
        
        @param issue_key_id: Issue key or id
        @return response
        """
        logger.info("Removing Issue Vote")
        url = "{}/issue/{}/votes".format(self._BASE_URL, issue_key_id)
        return self.s.delete(url)
        
    def create_issue(self, payload):
        """
        Creates an issue or a sub-task from a JSON representation.
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-createIssues
        
        STATUS 201 - application/json.Returns a link to the created issue.
        STATUS 400 Returned if the input is invalid, e.g. missing required fields, invalid field values, etc.
        
        @param payload: (JSON/Dict) Payload
        @return response
        """
        logger.info("Creating issue")
        url = "{}/issue".format(self._BASE_URL)
        return self.s.post(url, json=payload)
    
    def assign(self, issue_key_id, payload):
        """
        Assigns the issue to the user
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue-assign
        
        STATUS 400Returned in case of problems with the provided user representation.
        STATUS 401Returned if the user does not have permission to assign the issue.
        STATUS 204Returned if the issue was successfully assigned.
        STATUS 404Returned if the issue or user does not exist.
        
        @param issue_key_id: Issue key or id
        @param payload: (JSON/Dict) Payload
        @return response
        """
        logger.info("Assigning issue")
        url = "{}/issue/{}/assignee".format(self._BASE_URL, issue_key_id)
        return self.s.put(url, json=payload)
        
    def get_worklog(self, issue_key_id, work_log_id=''):
        """
        Returns a work log or list of worklogs
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue/{issueIdOrKey}/worklog-getWorklog
        
        STATUS 200 - application/jsonReturned if the work log with the given id exists and the 
            currently authenticated user has permission to view it. The returned response contains a full 
            representation of the work log in JSON format.
        STATUS 404 Returned if the work log with the given id does not exist or if 
            the currently authenticated user does not have permission to view it.
        
        @param issue_key_id: Issue key or id
        @param work_log_id: Work log id
        @return response
        """
        logger.info("Getting Issue Work log")
        url = "{}/issue/{}/worklog/{}".format(self._BASE_URL, issue_key_id, work_log_id)
        return self.s.get(url)
        
    def delete_worklog(self, issue_key_id, work_log_id):
        """
        Deletes a worklog based on id
        https://docs.atlassian.com/jira/REST/cloud/#api/2/issue/{issueIdOrKey}/worklog-deleteWorklog
        
        STATUS 400    Returned if the input is invalid (e.g. missing required fields, invalid values, and so forth).
        STATUS 204    Returned if delete was successful
        STATUS 403    Returned if the calling user does not have permission to delete the worklog
        
        @param issue_key_id: Issue key or id
        @param work_log_id: Work log id
        @return response
        """
        logger.info("Getting Issue Work log")
        url = "{}/issue/{}/worklog/{}".format(self._BASE_URL, issue_key_id, work_log_id)
        return self.s.delete(url)

    def get_releases(self, project_key):
        """
        Gets a release id based on a release name

        @param release_name: Name of release
        """
        logger.info("Getting all versions from a project")
        url = "{}/project/{}/versions".format(self._BASE_URL, project_key)
        return self.s.get(url)

    def get_issues_in_release(self, fixversion, fields='all'):
        """
        Return all issues in a given release
        """
        logger.info("Getting all issues in a release")
        url = "{}/search?jql=fixVersion=\"{}\"&fields={}".format(self._BASE_URL, fixversion, fields)
        return self.s.get(url)

    def get_issues_in_project(self, project, fields='all'):
        """
        Return all issues in a given project
        """
        logger.info("Getting all issues in a release")
        url = "{}/search?jql=project=\"{}\"&fields={}".format(self._BASE_URL, project, fields)
        return self.s.get(url)
