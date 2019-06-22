import os
import json
import aiohttp
from random import randint
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

router = routing.Router()

def user_default_quotes():
	quotes = [
		"You want to know the horrible truth? I can't even remember what she looked like. I only know she was the one thing I ever wanted... someone took her away from me, and seven kingdoms couldn't fill the hole she left behind.",
		"You heard the Hand, the king's too fat for his armor! Go find the breastplate stretcher! NOW!",
		"I swear to you, I was never so alive as when I was winning this throne, or so dead as now that I've won it.",
		"A DOTHRAKI HOOORDE, NED, ON AN OPEN FIELD!",
		"You want to know the horrible truth? I can't even remember what she looked like. I only know she was the one thing I ever wanted... someone took her away from me, and seven kingdoms couldn't fill the hole she left behind.",
		"I'm not trying to honor you, I'm trying to get you to run my kingdom while I eat, drink, and whore my way to an early grave.",
		"Wear it in silence or I'll honor you again",
		"They never tell you how they all shit themselves. They don't put that part in the songs... stupid boy. Now the Tarlys bend the knee like everyone else. He could have lingered on the edge of the battle with the smart boys, and today his wife would be making him miserable, his sons would be ingrates, and he'd be waking three times in the night to piss into a bowl.",
		"It's a neat little trick you do: you move your lips, and your father's voice comes out.",
		"I want the funeral feast to be the biggest the kingdom ever saw, and I want everyone to taste the boar that got me.",
		"SURROUNDED BY LANNISTERS! EVERY TIME I CLOSE MY EYES I SEE THEIR BLONDE HAIR AND THEIR SMUG, SATISFIED FACES!",
		"YOUR MOTHER WAS A DUMB WHORE WITH A FAT ASS.",
		"GODS WHAT A STUPID NAME!",
		"BOW BEFORE YOUR KING! BOW YA SHITS!",
		"IS THAT WHAT EMPTY MEANS!? SO GET MOOOORE!",
		"Bessie; Thank the gods for Bessi... and her tits"
	]
	return quotes

def get_random_quote():
	try:
		with open("quotes.json", "r") as read_file:
			quotes = json.load(read_file)
	except:
		print("ERROR")
		quotes = use_default_quotes()
	ind = randint(0, len(quotes))
	return quotes[ind]

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
	url = event.data["issue"]["comments_url"]
	body = event.data["issue"]["body"]

	if "bobby b" in body.lower():
		message = get_random_quote()
		await gh.post(url, data={"body": message})


@router.register("issue_comment", action="created")
async def issue_comment_event(event, gh, *args, **kwargs):
	url = event.data["issue"]["comments_url"]
	body = event.data["comment"]["body"]

	if "bobby b" in body.lower():
		message = get_random_quote()
		await gh.post(url, data={"body": message})

@router.register("pull_request", action="opened")
async def issue_comment_event(event, gh, *args, **kwargs):
	url = event.data["pull_request"]["comments_url"]
	body = event.data["pull_request"]["body"]

	if "bobby b" in body.lower():
		message = get_random_quote()
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
