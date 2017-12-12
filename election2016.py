from __future__ import print_function

from lxml import html
import requests
import librato
import os

# Electoral Vote and Popular Vote
def handler(event, context):
    page = requests.get("http://www.nytimes.com/elections/results/president")
    tree = html.fromstring(page.content)
    democrat_electoral = tree.xpath("//div[@class='eln-group eln-democrat ']/div[@class='eln-count']/text()")[0]
    republican_electoral = tree.xpath("//div[@class='eln-group eln-republican eln-winner']/div[@class='eln-count']/text()")[0]
    
    print(democrat_electoral)
    print(republican_electoral)

    democrat_popular = tree.xpath("//div[@class='eln-group eln-democrat']/div[@class='eln-value']/span[@class='eln-popular-vote-count']/text()")[0].split(" votes")[0].replace(",","")
    republican_popular = tree.xpath("//div[@class='eln-group eln-republican']/div[@class='eln-value']/span[@class='eln-popular-vote-count']/text()")[0].split(" votes")[0].replace(",","")
    
    print(democrat_popular)
    print(republican_popular)

    # Send em to Librato
    username = os.environ['LIBRATO_USER']
    token = os.environ['LIBRATO_TOKEN']
    api = librato.connect(username, token)
    api.submit("election.electoral_votes.democrats", democrat_electoral, description="Democrats")
    api.submit("election.electoral_votes.gop", republican_electoral, description="GOP")

    api.submit("election.popular_vote.democrats", int(democrat_popular), description="Democrats")
    api.submit("election.popular_vote.gop", int(republican_popular), description="GOP")


handler("", "")
