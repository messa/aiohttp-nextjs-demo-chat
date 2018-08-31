Chat demo web app created with aiohttp and next.js
==================================================

Requirements:

- Python 3.6
- aiohttp, requests_oauthlib etc. – Python dependencies managed by `setup.py`
- node.js, npm

See `Dockerfile` or `Makefile` how to run this example.

See also my [`aiohttp.web` tips](https://github.com/messa/tips/blob/master/Python%20-%20aiohttp%20server.md) :)


Architecture
------------

### Production


    Build phase:
                    Next.js app                          Static files (prerendered)
                    ~~~~~~~~~~~~~~~~     next export     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    pages/*.js         -------------->   out/_next/…/page/*.js
                    components/*.js                      out/_next/static/commons/main-….js
                    util/*.js                            out/index.html
                                                         out/chat/index.html                    <-+
                                                         out/login/index.html                     | serve
                                                                                                  | HTML & JS
                                                                                                  | as static
                                                                                                  | files
    Deployed:                                                                             request |
                                                                                          path    | /*
                    User           HTTPS, WSS    nginx or other    HTTP, WS    aiohttp    routing |
                    Web browser  ------------->  load balancer   ----------->  web app  ----------+
                                                                                                  | /api/*
                                                                                                  | /auth/*
                                                                                                  v
                                                                                            JSON API with
                                                                                              live data

### Development

Using `npm run dev` that runs `next` with HMR etc.

                                                               /api/*
                                                               /auth/*
                                                             +---------> aiohttp web app
    Developer     HTTP, WS   nginx with           proxy_pass |
    Web browser -----------> dev configuration  -------------+
                             (see nginx.conf)                |
                                                             | /*
                                                             +--------> Next.js development server


Links
-----

Similar projects etc., not directly related to this repo

https://steelkiwi.com/blog/an-example-of-a-simple-chat-written-in-aiohttp/
