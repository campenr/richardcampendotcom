## Source for my personal website at https://campen.co

The website is built using the flask microframework, and utilises the jinja2 templating engine that comes with it. Some
of the pages on my website are actually separate flask apps. A shared jinja2 template base 
([campen.co_templateBase.html](https://github.com/campenr/campen.co_templateBase))
is used to maintain a consistent appearance across these separate and my main website. This shared template
base is utilised as a git submodule by all apps running under the campen.co domain. Similarly, all shared static content
is hosted at static.campen.co to prevent code/file duplication between apps running under the campen.co domain.
