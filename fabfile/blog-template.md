Title: {{title}}
Date: 2013-02-18
Tags: <TAG1>, <TAG2>
Slug: {{slug}}
Author: <AUTHOR>
Summary: <YOUR SUMMARY HERE>
Media: static/images/<SOMEPIC>.png

HEAD PARAGRAPH


Some code:

    #!python
    def blog():
        with lcd("blog"):
            local("mkdir -p output")
            local("make html")

        local("rsync -a --delete blog/output/ '%s'" % OUTPUT_BLOG)
