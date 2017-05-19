# authortwitter
Python tool that grabs the Twitter username of a blog post's author with a URL.
Different blogs have different ways of displaying author Twitter usernames. Increasingly, blogs are starting to use the `<meta name="twitter:creator" content="@username">` tag, but a lot still don't. Usernames could be in a Twitter button at the bottom of the post, or buried in the author's own user archive page. Each blog that's supported as detailed below has the current XPath routes for the username.

Compatible with Python 3.x

Requires:
`lxml`, `requests`, `urllib`, `re`

## Examples
`https://www.engadget.com/2017/05/19/watch-an-ai-teach-itself-to-drive-in-gta-v/` will output `OutOnALumb`
`https://contently.com/strategist/2017/05/18/new-demand-waterfall/` will output `JoeLazauskas`
`http://contentmarketinginstitute.com/2017/05/create-high-converting-content/` will output `shane_barker`

## Blogs supported
<pre>
* bufferapp.com
* citylab.com
* coindesk.com
* consumerist.com
* contently.com
* contentmarketinginstitute.com
* conversionxl.com
* convinceandconvert.com
* engadget.com
* entrepreneur.com
* kinja.com
* lifehacker.com
* marketingland.com
* martech.zone
* mashable.com
* nakedsecurity.sophos.com
* shopify.com
* socialmediaexplorer.com
* socialmediatoday.com
* techcrunch.com
* theregister.co.uk
* theverge.com
* venturebeat.com
</pre>
