#!/usr/bin/env python3
"""
Script to regenerate index.html with proper pagination including the 3 new Tag1 articles.
"""

import json
from datetime import datetime

POSTS_PER_BATCH = 10

def parse_date(date_str):
    """Parse date string in format DD.MM.YYYY to datetime object."""
    return datetime.strptime(date_str, "%d.%m.%Y")

def format_date(date_str):
    """Format date for display."""
    dt = parse_date(date_str)
    return dt.strftime("%a, %d.%m.%Y")

def generate_article_html(article):
    """Generate HTML for a single article preview."""
    tags_html = ""
    if article.get('tags'):
        tags_items = "\n          ".join([
            f'<div class="field--item"><span>{tag}</span></div>'
            for tag in article['tags']
        ])
        tags_html = f'''
  <div class="field field--name-field-tags field--type-entity-reference field--label-inline">
    <div class="field--label">Tags</div>
          <div class="field--items">
              {tags_items}
              </div>
      </div>'''
    
    teaser_html = ""
    if article.get('teaser'):
        teaser_html = f'''
            <div class="field field--name-body field--type-text-with-summary field--label-hidden field--item">{article['teaser']}</div>
      '''
    
    return f'''    <div class="views-row"><article role="article" about="/{article['path']}" class="post-preview">

  
      <h2 class="post-title">
      <a href="{article['path']}/" rel="bookmark">
<span>{article['title']}</span>
</a>
    </h2>
    

      <div class="post-meta submitted">
      <article typeof="schema:Person" about="/users/slashrsm">
  </article>

      <div class="post-date">
        
<span>{format_date(article['published_date'])}</span>

        
      </div>
      <!--<div class="comments-counter"><a href="/{article['path']}#disqus_thread" data-disqus-identifier="node/XXX" hreflang="en">Comments</a></div>-->
    </div>
  
  <div class="post-subtitle">
    {teaser_html}{tags_html}<ul class="links inline list-inline"><li class="node-readmore"><a href="{article['path']}/" rel="tag" title="{article['title']}" hreflang="en">Read more<span class="visually-hidden"> about {article['title']}</span></a></li></ul>
  </div>

</article>
</div>'''

def main():
    # Read catalog
    with open('articles_catalog.json', 'r') as f:
        catalog = json.load(f)
    
    # Filter articles for front page
    frontpage_articles = [a for a in catalog if a.get('published_on_frontpage', True)]
    
    # Sort by date (newest first) - should already be sorted but let's make sure
    frontpage_articles.sort(key=lambda x: parse_date(x['published_date']), reverse=True)
    
    # Calculate number of batches
    total_batches = (len(frontpage_articles) + POSTS_PER_BATCH - 1) // POSTS_PER_BATCH
    
    print(f"Total articles: {len(frontpage_articles)}")
    print(f"Posts per batch: {POSTS_PER_BATCH}")
    print(f"Total batches: {total_batches}")
    
    # Generate batches HTML
    batches_html = ""
    for batch_num in range(total_batches):
        start_idx = batch_num * POSTS_PER_BATCH
        end_idx = min(start_idx + POSTS_PER_BATCH, len(frontpage_articles))
        batch_articles = frontpage_articles[start_idx:end_idx]
        
        display_style = '' if batch_num == 0 else ' style="display:none"'
        
        articles_html = "\n".join([generate_article_html(article) for article in batch_articles])
        
        batches_html += f'''          <div class="post-batch" data-batch="{batch_num}"{display_style}>
{articles_html}
          </div>
'''
    
    # Read the current index.html to get the header and footer
    with open('index.html', 'r') as f:
        current_html = f.read()
    
    # Find where batches start and end
    batch_start = current_html.find('<div class="post-batch"')
    batch_end = current_html.rfind('</div>\n          <div class="post-batch"') + 6  # Include the closing </div>
    batch_end = current_html.find('</div>\n      </div>\n\n        <div id="load-more-container"', batch_end) + 6
    
    # Replace the batches section
    new_html = current_html[:batch_start] + batches_html + current_html[batch_end:]
    
    # Update the total batches in the JavaScript
    js_start = new_html.find('var totalBatches = ')
    if js_start != -1:
        js_end = new_html.find(';', js_start)
        new_html = new_html[:js_start] + f'var totalBatches = {total_batches}' + new_html[js_end:]
    
    # Write the new index.html
    with open('index.html', 'w') as f:
        f.write(new_html)
    
    print("\n✓ Successfully regenerated index.html")
    print(f"  - Batch 0 has {len(frontpage_articles[:POSTS_PER_BATCH])} articles")
    print(f"  - Total of {total_batches} batches")
    
    # Show first batch articles
    print("\nFirst batch articles (newest first):")
    for i, article in enumerate(frontpage_articles[:POSTS_PER_BATCH], 1):
        print(f"  {i}. {article['title']} ({article['published_date']})")

if __name__ == '__main__':
    main()
