from slack_bolt.async_app import AsyncRespond, AsyncAck


async def hello_world_command(ack: AsyncAck, respond: AsyncRespond, body: dict):
    await ack()
    user_id = body["user_id"]
    await respond(f"Hi <@{user_id}>!")
