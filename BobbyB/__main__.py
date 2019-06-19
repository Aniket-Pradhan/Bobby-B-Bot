import os
import aiohttp
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

router = routing.Router()


@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
	"""
	Whenever an issue is opened, greet the author and say thanks.
	"""
	url = event.data["issue"]["comments_url"]
	body = event.data["issue"]["body"]
	author = event.data["issue"]["user"]["login"]

	if "bobby b" in body.lower():
		message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
		await gh.post(url, data={"body": message})


async def main(request):
	body = await request.read()

	secret = os.environ.get("GH_SECRET")
	oauth_token = os.environ.get("GH_AUTH")

	event = sansio.Event.from_http(request.headers, body, secret=secret)
	async with aiohttp.ClientSession() as session:
		gh = gh_aiohttp.GitHubAPI(session, "mariatta",
								  oauth_token=oauth_token)
		await router.dispatch(event, gh)
	return web.Response(status=200)


if __name__ == "__main__":
	app = web.Application()
	app.router.add_post("/", main)
	port = os.environ.get("PORT")
	if port is not None:
		port = int(port)

	web.run_app(app, port=port)
