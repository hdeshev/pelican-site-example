# Pelican and Custom Pages Example Site

Wanna share HTML templates across a statically-generated site and a Pelican blog? That's pretty easy since you can use Jinja to render your pages much in the same way Pelican does.

Read more in [this blog post](http://stackful.io/blog/static-site-jinja-pelican-shared-templates.html).

# Getting it Running

You need a Python interpreter with virtualenv set up.

* Install the prerequisites: `pip install -r requirements.txt`
* Build the entire site with Fabric: `fab build`
* Enjoy the result in the `output` folder.
