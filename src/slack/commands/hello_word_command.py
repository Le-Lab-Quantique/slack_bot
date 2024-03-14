from slack_bolt import Ack, Respond


def hello_world_command(ack: Ack, respond: Respond, body: dict):
    ack()
    user_id = body["user_id"]
    respond(f"Hi <@{user_id}>!")
