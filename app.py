#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify
from bot import Bot
from waitress import serve

import os

app = Flask(__name__)


class GitlabBot(Bot):
    def __init__(self, auth_message, token):
        super(GitlabBot, self).__init__(token)
        self.auth_message = auth_message
        self.chats = {}
        self.send_to_all("Hi !")

    def text_recv(self, txt, chat_id):
        """registering chats"""
        txt = txt.strip()

        if txt.startswith("/"):
            txt = txt[1:]

        if txt == self.auth_message:
            if str(chat_id) in self.chats:
                self.reply(chat_id, "\U0001F60E  boy, you already got the power.")
            else:
                self.reply(chat_id, "\U0001F60E  Ok boy, you got the power !")
                self.chats[chat_id] = True
        elif txt == "shutupbot":
            del self.chats[chat_id]
            self.reply(chat_id, "\U0001F63F Ok, take it easy\nbye.")
        else:
            self.reply(chat_id, "\U0001F612 I won't talk to you.")

    def send_to_all(self, msg):
        for c in self.chats:
            self.reply(c, msg)


auth_message = os.environ.get("AUTHMSG")
token = os.environ.get("TOKEN")
bot_instance = GitlabBot(auth_message, token)


@app.route("/", methods=["GET"])
def index():
    return jsonify(["Hello", "World"])


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("Accepted event:", data)
        # json contains an attribute that differenciates between the types, see
        # https://docs.gitlab.com/ce/user/project/integrations/webhooks.html
        # for more infos
        kind = data["object_kind"]
        if kind == "push":
            msg = generatePushMsg(data)
        elif kind == "tag_push":
            msg = generatePushMsg(data)  # TODO:Make own function for this
        elif kind == "issue":
            msg = generateIssueMsg(data)
        elif kind == "note":
            msg = generateCommentMsg(data)
        elif kind == "merge_request":
            msg = generateMergeRequestMsg(data)
        elif kind == "wiki_page":
            msg = generateWikiMsg(data)
        elif kind == "pipeline":
            msg = generatePipelineMsg(data)
        elif kind == "build":
            msg = generateBuildMsg(data)
        bot_instance.send_to_all(msg)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


def generatePushMsg(data):
    msg = "*{0} ({1}) - {2} new commits*\n".format(
        data["project"]["name"],
        data["project"]["default_branch"],
        data["total_commits_count"],
    )
    for commit in data["commits"]:
        msg = msg + "----------------------------------------------------------------\n"
        msg = msg + commit["message"].rstrip()
        msg = msg + "\n" + commit["url"].replace("_", "\_") + "\n"
    msg = msg + "----------------------------------------------------------------\n"
    return msg


def generateIssueMsg(data):
    action = data["object_attributes"]["action"]
    if action == "open":
        assignees = ""
        for assignee in data.get("assignees", []):
            assignees += assignee["name"] + " "
        msg = "*{0}* new issue for *{1}*:\n".format(data["project"]["name"], assignees)
    elif action == "reopen":
        assignees = ""
        for assignee in data.get("assignees", []):
            assignees += assignee["name"] + " "
        msg = "*{0}* issue re-opened for *{1}*:\n".format(
            data["project"]["name"], assignees
        )
    elif action == "close":
        msg = "*{0}* issue closed by *{1}*:\n".format(
            data["project"]["name"], data["user"]["name"]
        )
    elif action == "update":
        assignees = ""
        for assignee in data.get("assignees", []):
            assignees += assignee["name"] + " "
        msg = "*{0}* issue assigned to *{1}*:\n".format(
            data["project"]["name"], assignees
        )

    msg = msg + "[{0}]({1})".format(
        data["object_attributes"]["title"], data["object_attributes"]["url"]
    )
    return msg


def generateCommentMsg(data):
    ntype = data["object_attributes"]["noteable_type"]
    if ntype == "Commit":
        msg = "note to commit"
    elif ntype == "MergeRequest":
        msg = "note to MergeRequest"
    elif ntype == "Issue":
        msg = "note to Issue"
    elif ntype == "Snippet":
        msg = "note on code snippet"
    return msg


def generateMergeRequestMsg(data):
    return "new MergeRequest"


def generateWikiMsg(data):
    return "new wiki stuff"


def generatePipelineMsg(data):
    return "new pipeline stuff"


def generateBuildMsg(data):
    return "new build stuff"


if __name__ == "__main__":
    print("App started")
    bot_instance.run_threaded()
    serve(app, host="0.0.0.0", port=10111)
