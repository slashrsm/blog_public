This is my blog post in a static html form. It was hosted by Drupal in the past, but I scraped it and am not maintainging it in this form. 

It has multiple features:
- individual posts in subfolders
- infinitely paginated homepage listing (via Javascript)

You are my assistant that will help me manage it.

If you need to run any scripts please create them on the filesystem and do not remove them afterwards. 

The article catalog is maintained in the `articles-catalog.json` file. When adding/removing/editing articles we should keep it up to date. The file should be ordered by the published date (newest post first). Each record in the file has the following fields:
- title: title of the post
- published_date: date when the post was published in dd.mm.yyyy format
- path: path on the filesystem where the post appears
- tags: tags attached to the post (found in the .field--name-field-tags element in the post HTML file)
- teaser: teaser used to promote the post on the front page (/index.html) - found in the .field--name-body.field--type-text-with-summary element of each article (article.post-preview)
- published_on_frontpage: boolean, whether the post appears on the front page.
