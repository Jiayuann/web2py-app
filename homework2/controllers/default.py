# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    posts = db(db.post).select(db.post.ALL,orderby =~db.post.created_on, limitby = (0,10))
    count_post =len(posts)
    print('hello')
    return dict(posts = posts,
                count_post = count_post,
                )


@auth.requires_login()
def edit():
    if request.args(0):
        post = db.post[request.args(0, cast=int)]
        form = SQLFORM(db.post,
                       post,
                       labels={'post_title':'Title','post_content':'Content','post_image':'Image'},
                       submit_button='Update your comment',
                       showid=False,
                       deletable=True,
                       )
    else:
        form = SQLFORM(db.post,
                       labels={'post_title': 'Title', 'post_content':'Content','post_image':'Image'},
                       submit_button='Create your comment',
                       )

    if form.process().accepted:
        response.flash = 'Comment Accepted'
    elif form.errors:
        response.flash = 'Please complete your form'
    else:
        response.flash = 'Please post your comment'
    return dict(form = form)



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


