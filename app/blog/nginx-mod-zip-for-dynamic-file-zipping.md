# Nginx mod_zip for dynamic file zipping

## The background

I hit an issue when building something at work recently. Or to be more accurate, I was doing something almost by reflex when I thought, surely there must be a better way. The thing in question was building some functionality to allow users to download a zip archive of files, but the files in question came from a content managed list and therefore, the generation of the zip needed to be dynamic. The reflex when in the zone for a given language is just to do _ALL THE THINGS_ in that language. Part of me thought, yeah cool do it in python, good enough. But it felt wrong, and so down the rabbit hole we go. 

If you've ever run Django in a production system you'll already know not to serve files from Django itself, use a dedicated webserver to do it. For the uninitiated, I reference the [official documentation](https://docs.djangoproject.com/en/4.1/howto/static-files/deployment/#serving-static-files-from-a-dedicated-server) which itself recommends (or at least describes the common use of) a dedicated web server to host static content. My specific use case here was Django, but this will hold true across many web frameworks, unless you're going more bare metal with something like golang and forgoing a standalone webserver.

My standard stack for hosting Django (or indeed any website with a backend really) uses [nginx](https://nginx.org/) as a web server / reverse-proxy; forwarding app requests to the backend app, and serving static/media files directly. Stock standard approach, no doubt used by millions around the world, nothing exciting here. The key is that nginx (and web servers in general) are really fast at serving your static content, much more so than your backend application. So my next thought was, _"maybe I can generate/cache the zip files on disk as requested (or in advance using some kind of background process) so the files are on disk for nginx to serve"_. That sounds like a lot of work though, and would likely result in a lot of clutter with files that are never or no longer needed over the apps lifetime.

So my next (and final) thought then was _"can I create the zip files dynamically, but not in python?"_. If you search how to do such a thing with Django, the top results all advocate using some kind solution like: [do it in python with zipfile](https://stackoverflow.com/questions/67454/serving-dynamically-generated-zip-archives-in-django), or [do it in python with zipfile](https://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html), or even [do it in python with zipfile](https://djangosnippets.org/snippets/365/). All these examples at some point mention that you should use the web server and not Django to serve such content, but then tell you how to do the opposite.

The exception to this in my search was a package called [django-zip-stream](https://github.com/travcunn/django-zip-stream). This package provides a clean interface for letting Django offload the dynamic creation of zip archives from other files to nginx using an nginx module called [mod_zip](https://www.nginx.com/resources/wiki/modules/zip/). Perfect. The missing piece. A way to do this in nginx. But of course there are a couple of bumps on the road to success here, namely:

- mod_zip needs to be compiled (against the same version of nginx you are running, presumably on the same OS)
- mod_zip needs to be installed against your running nginx installation (unless you fancy the alternative of compiling nginx itself from source with the module statically linked. See note below)
- your application needs to generate the correct response to trigger the zip creation by mod_zip

For the last item, the aforementioned Django package may be good enough for you, or at least point you in the right direction. 

**Note: ** The official [mod_zip documentation](https://www.nginx.com/resources/wiki/modules/zip/) only discusses the static module addition i.e. recompiling nginx itself, but if you dig into the [source code](https://github.com/evanmiller/mod_zip), specifically, [the configure script](https://github.com/evanmiller/mod_zip/blob/5b2604b3914f87db2077f2239b8a98b66cf622af/config#L3), you can see that it handles configuration as a dynamic module i.e. add to an existing nginx installation.

What follows are working code solutions to the first two, less straightforward items: building the mod_zip module and running nginx with mod_zip enabled. To tie it all together I have written a demo application that generates the needed requests (in this case with a lightweight [FastAPI](https://fastapi.tiangolo.com/) app, because I didn't want to test this with a full Django app).

## The code

See the [example files here](https://github.com/campenr/examples/tree/main/nginx_mod_zip_for_dynamic_file_zipping).

[mod_zip's official documentation](https://www.nginx.com/resources/wiki/modules/zip/) has build instructions that amount to: re-build nginx from source using the `--add-module=/path/to/mod_zip` flag to add this module at compile time. As noted above the module is already able to be configured for dynamic adding at runtime, so if you're like me and don't want to recompile nginx from source you need to instead turn to nginx's own documentation on [converting static modules to dynamic modules](https://www.nginx.com/resources/wiki/extending/converting/).

Even though we don't want to compile nginx from source, we still need the nginx source in order to build the module. The below Dockerfile does just that, and creates the module shared object that you can then add to your existing nginx installation. This docker image served my needs exactly (Ubuntu 22.04, nginx v1.22.1) but you can edit it for your own needs, or even paramaterise it for a more general solution if so inclined.

**Note: ** The later example Dockerfile requires a new enough version of docker to use multi-stage builds. If this is not enabled by default for your version you can try using `DOCKER_BUILDKIT=1` to enable it. Alternatively, if you only care about the builder and not the full demo you can ignore this and just run the builder without multi-stage.

**Note: ** The specific flags passed to nginx's configure script were trial and error and your milage may vary. This was a result of debugging `module <name> is not binary compatible` errors that lead me to [this StackExchange answer](https://serverfault.com/a/988273), which led to me doing the opposite, which worked 🤷

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
    && git clone https://github.com/nginx/nginx.git \
    && cd ./nginx && git checkout release-1.22.1 \
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

The demo application is a lightweight stack consisting of a single file backend application, and nginx webserver / proxy. I choose FastAPI for the demo as I could write the proof of concept in a single python file with it and have it still be easily readable. The principals will translate to any backend app. The core components of the demo are: the following addition to our Dockerfile, a simple nginx config, a simple FastAPI app, and some files to serve up (again see the example repo for all the files).

**Note: ** The demo code expects some understanding of how to configure nginx to proxy requests to a backend python application like Django or FastAPI, as well as how to run them with an application runner like [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/), or in the case of this demo [uvicorn](https://www.uvicorn.org/) as per the [FastAPI getting started docs](https://fastapi.tiangolo.com/#run-it). For more information on the topic I point you to these useful tutorials: [one](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html), [two](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04).

**Note: ** Because I'm using hardcoded test files I have also hardcoded the [crc](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) (cyclic redundancy check) values in the response. You can [search for a real algorithm here](https://duckduckgo.com/?q=python+crc32&t=h_&ia=web). I've also hardcoded the file sizes and urls for simplicity in the demo.

```dockerfile
FROM nginx:1.22 as runner

# setup mod_zip plugin

COPY --from=builder ./nginx/objs/ngx_http_zip_module.so /usr/lib/nginx/modules/
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
    # sadly mod_zip doesn't like the wildcard _ server name.
    # there's probably a work around but it's not a big issue for my use case.
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
# main.py

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/zip/")
def zipfiles():
    return PlainTextResponse(
        content=build_content(),
        headers={
            # header to trigger mod_zip behaviour.
            # If you want to debug the response you can just comment this line out.
            'X-Archive-Files': 'zip',
            # header to manually set file name
            'Content-Disposition': 'attachment; filename=mod_zip_demo.zip',
            # can also add a Last-Modified header for performance.
        },
    )

def build_content():
    # a space delimited list of:
    #   crc32, file size, url that resolves to source file, name of file.
    # Note the use of \r\n as per the mod_zip docs.
    content = ''
    content += '098f1c6b 7 /test1.txt Test1.txt\r\n'
    content += '440a6aa5 12 /test2.txt Test2.txt\r\n'
    return content

```

The following commands will build and then run the demo:

```bash
docker build -t mod_zip_demo .
docker run -it --rm --name zip_demo mod_zip_demo /bin/bash
docker exec -it --user root zip_demo venv/bin/python -m uvicorn main:app
```

Hitting `localhost:8080` will serve the default nginx page, and either `localhost:8080/test1.txt` or `localhost:8080/test2.txt` will serve the individual files through nginx as normal. Hitting `localhost:8080/zip/` will proxy the request to FastAPI which then sends a response that triggers mod_zip to do it's magic and zip up the files as per our manifest content 🎉

A couple of final notes: In a real world application you may have more complex needs around serving the files i.e. the file urls supplied to mod_zip may need to route through your application so that you can enforce permission checks. This is less performant than using nginx servable urls directly, but still a better choice than doing it all in python as the heavy work involved shouldn't be processing the requests but rather the zip compression. Also, if your hosting setup is more complex where say, the files are served from S3, this may not be the most performant approach as you are forcing a trip to the server when normally you would just put a CDN in from of S3 and serve that content directly. In such a case the earlier option of caching the zip files (eagerly or lazily) could be a better option. Like all things the specifics depend on your exact use case. Also, if you follow the approach taken here note than major/minor upgrades to nginx will require manually upgrading the module as well.
