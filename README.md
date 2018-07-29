Chat demo web app created with aiohttp and next.js
==================================================

Architecture
------------

### Production


    Build phase:
                    Next.js app                          Static files (prerendered)
                    ~~~~~~~~~~~~~~~~     next export     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    pages/*.js         -------------->   out/_next/…/page/*.js
                    components/*.js                      out/_next/static/commons/main-….js
                    util/*.js                            out/index.html
                                                         out/chat/index.html                 <-+
                                                         out/login/index.html                  | serve
                                                                                               | HTML & JS
                                                                                               | as static
                                                                                               | files
    Deployed:                                                                                  |
                                                                                               | /*
                    User           HTTPS, WSS    nginx or other    HTTP, WS    aiohttp         |
                    Web browser  ------------->  load balancer   ----------->  web app  -------+
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
