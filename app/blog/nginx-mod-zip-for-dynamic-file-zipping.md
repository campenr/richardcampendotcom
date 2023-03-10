# Django and Dynamic ZIP files

## The background

[Add skip link to code]

I hit an issue when building something at work recently. Or to be more accurate, I was doing something almost by reflex when I thought, surely there must be a better way. The thing in question was building some functionality to allow users to download a ZIP archive of files, but the files in question came from a content managed list and therefore, the generation of the ZIP needed to be dynamic. My reflex was thinking "well, i'm already in python/django, and I have the records for the documents the user wants, I can just do this all in python". Part of me though, yeah cool good enough. Most of me though, thought that feels real dirty, and django is not the place to do this. If you've ever run Django in a production system you'll already know not to serve files from Django itself, use a dedicated webserver to do it. For the uninitiated, I reference the official documentation itself reccomends (or at least describes the common use of) a dedicated web server to host static content, which includes media content (with their documentation on serving media content in production linking ultimately to the above documentation).

My standard stack for hosting Django (or indeed any website with a backend really) uses NGINX as a web server / reverse-proxy; forwarding app requests to the python app, and serving static/media files directly. Stock standard approach, no doubt used by millions, nothing exciting here. So my next thought was, "maybe I can generate/cache the ZIP files on disk as requested (or in advance using some kind of background process) so the files are on disk for NGINX to serve". That sounds like a lot of work though, and would likely result in a lot of clutter with files that are never or no longer needed over the apps lifetime.

My final thought was "can I create the ZIP files dynamically, but not in python?". If you search how to do such a thing with Django, the top results all advocate using some kind solution like: do it in python with zipfile, or do it in python with zipfile, or even do it in python with zipfile. All these examples at some point mention that you should use the web server and not Django to serve such content, but then tell you how to do the opposite.

The exception to this in my search was a (as of writing not committed to in 6 or so years) repository for a package called django-zip-stream. This package provides a clean interface for letting django offload the dynamic creation of zip archives from other files to NGINX using an NGINX module called mod_zip. Perfect. The missing piece. A way to do this in NGINX. But of course there are a couple of bumps on the road to success here, namely: mod_zip needs to be compiled (against the same version of nginx you are running, presumably on the same OS), mod_zip needs to be installed against your running NGINX installation (unless you fancy the alternative of compiling NGINX itself from source with the module statically linked), and then you need to generate the correct response from Django to trigger the ZIP creation. For this last piece, the aforementioned django package may be good enough for you.
What follows are working code solutions to: build the mod_zip module, run nginx with mod_zip, and create the needed requests (in this case with a lightweight FastAPI app, because I didn't want to test this with a full django app).

## The code

See the example repo here for all files used.

The examples require a new enough version of docker to use multi-stage builds. If this is not enabled by default for your version you can try using `DOCKER_BUILDKIT=1` to enable it.

### Building mod_zip (for dynamically linking at runtime)

mod_zip's official documentation has build instructions that amount to: re-build NGINX from source using the --add-module=/path/to/mod_zip flag to add this module at compile time. But if you're like me and don't want to recompile NGINX from source, and just want to add the module at runtime, you need to instead turn to NGINX's own documentation on converting static modules to dynamic modules. Even though we don't want to compile NGINX from source, we still need the NGINX source in order to build the module. The below Dockerfile does just that, and creates the module shared object that you can then add to your existing NGINX installation. This docker image served my needs exactly (Ubuntu 22.04, NGINX v1.22.1) but you can edit it for your own needs, or even paramaterise it for a more general solution if so inclined. Also, little to no effort at docker best practices are employed here. It's just a throwaway build machine.

Note the specific flags passed to NGINX's configure script. This was a result of debugging module <name> is not binary compatible errors that lead me to this StackExchange answer, which led to me doing the opposite, which worked :shrug:

```dockerfile
FROM ubuntu:jammy as builder

# Setup build dependencies

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    git \
    zlib1g-dev \
    libpcre3-dev

# get source files for mod_zip and nginx

RUN : \
    && git clone https://github.com/evanmiller/mod_zip.git \
    && git clone https://github.com/nginx/nginx.git && cd ./nginx && git checkout release-1.22.1 \
    && :

# build the mod_zip module

RUN : \
    && cd ./nginx \
    && ./auto/configure --with-compat --add-dynamic-module=../mod_zip/ \
    && make -f ./objs/Makefile modules \
    && :

# file is at ./nginx/objs/ngx_http_zip_module.so
```

The following commands will build the module for you and dump it into the host machine:

```bash
docker build -t mod_zip_builder .
# OR if using the complete Dockerfile from the example repo / end of this blog
docker build --target=builder -t mod_zip_builder .
# Then run it and get the file
docker run -it --rm --name mod_zip_build mod_zip_builder /bin/bash
docker cp mod_zip_build:~/nginx/objs/ngx_http_zip_module.so .
```

For completeness, I wrote a small  FastAPI application that installs the mod_zip module and has an endpoint for performing the dynamic zipping. The core components are the following addition to our Dockerfile, a simple NGINX config, a simple FastAPI app, and some files to serve up (again see the example repo for all the files).

```dockerfile
FROM nginx:1.22 as runner

COPY --from=builder ./nginx/objs/ngx_http_zip_module.so /usr/lib/nginx/modules/

# setup mod_zip plugin

RUN : \
    && chmod 644 /usr/lib/nginx/modules/ngx_http_zip_module.so \
    && sed -i '1 s/^/load_module modules\/ngx_http_zip_module.so;\n/' /etc/nginx/nginx.conf \
    && :

# setup demo FastAPI application

RUN : \
    && rm /etc/nginx/conf.d/default.conf \
    && apt-get update && apt-get install -y --no-install-recommends python3 python3-pip \
    && python3 -m pip install virtualenv \
    && virtualenv venv \
    && . ./venv/bin/activate \
    && python -m pip install fastapi uvicorn \
    && :

COPY main.py  .
COPY fastapi_demo.conf /etc/nginx/conf.d/
COPY test1.txt /usr/share/nginx/html/
COPY test2.txt /usr/share/nginx/html/

```

```nginx
# fastapi_demo.conf

upstream fastapi_demo {
    server 127.0.0.1:8000;
}

server {
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
    }

    location /zip/ {
        proxy_pass http://fastapi_demo;
    }
}

```

```python
# ./main.py

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/zip/")
def zipfiles():
    return PlainTextResponse(
        content=build_content(),
        headers={
            'X-Archive-Files': 'zip',
            'Content-Disposition': 'attachment; filename=mod_zip_demo.zip',
        },
    )

def build_content():
    content = ''
    content += '098f1c6b 7 /test1.txt Test1.txt\r\n'
    content += '440a6aa5 12 /test2.txt Test2.txt\r\n'
    return content

```

After building the new image you need can run it as above. To start the FastAPI application use: `docker exec -it --user root zip_demo venv/bin/python -m uvicorn main:app`. Hitting `localhost:8080` will serve the default NGINX page, and either /`localhost:8080/test1.txt` or `localhost:8080/test2.txt` will serve the individual files through NGINX as normal. Hitting `localhost:8080/zip/` will proxy the request to FastAPI which then sends a response that triggers mod_zip to do it's magic and zip up the files in the mainfest.
