#!/usr/bin/env python

import os
import re
import datetime
from glob import glob
from fabric.api import env, local, lcd, puts, roles, execute, sudo
from fabric.contrib.project import rsync_project
from fabric.network import normalize
from jinja2 import Environment, FileSystemLoader
from itertools import chain
from fnmatch import fnmatch

env.use_ssh_config = True
env.roledefs = {
    'web': ['web'],
}

DEPLOY_DIR = "/var/www/pelican-sample-site.com"
OUTPUT = "output"
OUTPUT_BLOG = os.path.join(OUTPUT, "blog")
THEME_PATH = "blog/bootstrap2"
TEMPLATE_CONTEXT = {
    "BLOGURL": "http://pelican-sample-site.com/blog",
    "FEED_ALL_ATOM": "atom.all.xml",
    "FEED_ALL_RSS": "rss.all.xml",
}

EXCLUDE_PATTERNS = [line.strip() for line in open("site_excludes", "r").readlines()]


def root_site():
    local("rsync -a --delete --exclude-from=site_excludes  * %(output)s" %
            dict(output=OUTPUT))
    render_site_html()


def render_site_html():
    subdirs = [child for child in os.listdir(".")
            if os.path.isdir(child) and not(child.startswith(".")) and not excluded(child)]
    dirs = chain(["."], subdirs)
    for d in dirs:
        for template in glob("%s/**.html" % d):
            if "root.html" not in template.lower():
                template_destination = os.path.join(OUTPUT, template)
                render(template, template_destination)


def excluded(path):
    for exclude_pattern in EXCLUDE_PATTERNS:
        if fnmatch(path, exclude_pattern):
            return True
    return False


def blog():
    with lcd("blog"):
        local("mkdir -p output")
        local("make html")

    local("rsync -a --delete blog/output/ '%s'" % OUTPUT_BLOG)


def clean():
    local("rm -rf output")


def build():
    local("mkdir -p '%s'" % OUTPUT_BLOG)
    root_site()
    blog()


def new_blog(title, slug=None, overwrite="no"):
    if slug is None:
        slug = slugify(title)

    now = datetime.datetime.now()
    month_part = now.strftime("%Y-%m")
    post_date = now.strftime("%Y-%m-%d")

    params = dict(
        date=post_date,
        title=title,
        slug=slug,
    )

    out_file = "blog/content/{}/{}.md".format(month_part, slug)
    local("mkdir -p '{}' || true".format(os.path.dirname(out_file)))
    if not os.path.exists(out_file) or overwrite.lower() == "yes":
        render("fabfile/blog-template.md", out_file, **params)
    else:
        print("{} already exists. Pass 'overwrite=yes' to destroy it.".
                format(out_file))


def slugify(text):
    normalized = "".join([c.lower() if c.isalnum() else "-"
            for c in text])
    no_repetitions = re.sub(r"--+", "-", normalized)
    clean_start = re.sub(r"^-+", "", no_repetitions)
    clean_end = re.sub(r"-+$", "", clean_start)
    return clean_end


def render(template, destination, **kwargs):
    jenv = Environment(loader=FileSystemLoader(['.', os.path.join(THEME_PATH, "templates")]))
    params = dict(TEMPLATE_CONTEXT, **kwargs)
    params["PAGE"] = template
    params["SITEURL"] = os.path.relpath(os.path.abspath("."), os.path.dirname(os.path.abspath(template)))
    text = jenv.get_template(template).render(params)
    with open(destination, "w") as output:
        puts("Rendering: {} to {}".format(template, destination))
        output.write(text.encode("utf-8"))


@roles("web")
def deploy():
    execute(clean)
    execute(build)

    sudo("mkdir -p '%s' || true" % DEPLOY_DIR)
    user, host, port = normalize(env.host_string)
    sudo("chown -R %s '%s'" % (user, DEPLOY_DIR))

    rsync_project(local_dir="output/", remote_dir=DEPLOY_DIR, extra_opts="-c --delete")
    sudo("chown -R www-data.www-data '%s'" % DEPLOY_DIR)
