The Kevin Crane Blog
====================

[http://thekevincrane.com](http://thekevincrane.com "Go to the damn site")

Personal blog to write dumb things and show off projects.

##Notes For Kevin

- Steps to deploy:
    - Code locally, push to origin
    - ``` fab deploy ``` (should be totally it)
    - ``` fab backup_db ``` (periodically, very important; should probably automate someday)
    - Possibly need to migrate the DB with ``` ./manage.py db upgrade [AND/OR] migrate ```, though hopefully not past the first time
- Provision a new Ubuntu machine:
    - ``` fab install ```
    - Afterwards, make sure DB set up, migrations set up
- Checklist for adding new Flask app to site (e.g. personal playground project):
    - New python package (w/ views, models)
    - New folder in /templates
    - Register a blueprint in \_\_init\_\_.py
    - Add to navbar (or a new dropdown)
    - ``` ./manage.py db migrate ``` (once after new models added)

TODO:
- Search indexing
- SSL token
- Change bootstrap CSS file (don't use Flatly theme, make smaller, customize pieces that are included)
- Custom FontAwesome set (only choose icons I need, make smaller)
- Occasional automated security screening (e.g. https://www.scanmyserver.com/)
