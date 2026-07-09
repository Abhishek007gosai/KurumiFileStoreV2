from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import pytz
from datetime import datetime

from config import *


name = """
BY CODEFLIX BOTS
"""


def get_indian_time():
    """Returns the current time in IST."""
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )

        self.LOGGER = LOGGER
        self.web_app = None
        self.web_runner = None

    async def start(self):
        await super().start()

        bot_info = await self.get_me()
        self.uptime = get_indian_time()
        self.username = bot_info.username

        # Check database channel
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel

            test_msg = await self.send_message(
                chat_id=db_channel.id,
                text="Bot Started Successfully"
            )

            await test_msg.delete()

        except Exception as e:
            self.LOGGER(__name__).warning(str(e))
            self.LOGGER(__name__).warning(
                f"Make sure bot is admin in DB Channel.\n"
                f"Check CHANNEL_ID value: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Bot stopped. Join https://t.me/CodeflixSupport for support"
            )
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)

        self.LOGGER(__name__).info(
            f"""
Bot Running Successfully!

Username: @{self.username}

Created By:
@Codeflix_Bots
"""
        )

        # Start Web Server
        try:
            self.web_app = await web_server()

            self.web_runner = web.AppRunner(self.web_app)
            await self.web_runner.setup()

            site = web.TCPSite(
                self.web_runner,
                "0.0.0.0",
                PORT
            )

            await site.start()

            self.LOGGER(__name__).info(
                f"Web Server Started On Port {PORT}"
            )

        except Exception as e:
            self.LOGGER(__name__).error(
                f"Web Server Error: {e}"
            )

        # Notify owner
        try:
            await self.send_message(
                OWNER_ID,
                text="<b><blockquote>Bot Restarted Successfully</blockquote></b>"
            )
        except Exception:
            pass


    async def stop(self, *args):
        try:
            if self.web_runner:
                await self.web_runner.cleanup()
        except Exception:
            pass

        await super().stop()

        self.LOGGER(__name__).info(
            "Bot stopped."
        )


    def run(self):
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(self.start())

            self.LOGGER(__name__).info(
                "Bot is now running."
            )

            loop.run_forever()

        except KeyboardInterrupt:
            self.LOGGER(__name__).info(
                "Shutting down..."
            )

        except Exception as e:
            self.LOGGER(__name__).error(
                f"Runtime Error: {e}"
            )

        finally:
            loop.run_until_complete(self.stop())


if __name__ == "__main__":
    Bot().run()
