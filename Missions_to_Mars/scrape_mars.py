#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import os
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape ():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # ## NASA Mars News
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find first list item in class 'slide'
    articles = soup.find_all('li', class_='slide')[0]
    print(articles.prettify())

    # Within class 'slide,' find the headline in class 'content_title'
    headline = articles.find(class_='content_title').text
    
    # Within class 'slide,' find the paragraph in class 'article_teaser_body'
    paragraph = articles.find(class_='article_teaser_body').text
    
    # ## JPL Mars Space Images - Featured Image
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html

    soup = bs(html, 'html.parser')

    # Look into the header where the image is coded
    image = soup.find_all('div', class_='header')[0]
    print(image.prettify())

    # Find image source under class 'headerimage fade-in'
    featured_image = image.find('img', class_='headerimage fade-in')
    featured_image = featured_image.attrs.get('src', None)

    # Create variable with only root URL (minus file name)
    url = os.path.dirname(url)

    # String together root URL and file name for image in new variable
    featured_image_url = f'{url}/{featured_image}'
    # ## Mars Facts

    url = "https://space-facts.com/mars/"

    # Read website's tables in Pandas
    tables = pd.read_html(url)

    # Create variable for first table
    mars_df = tables[0]

    # Generate HTML table
    mars_html = mars_df.to_html()
    mars_html = mars_html.replace('\n', '')
    
    # ## Mars Hemispheres

    # Store 4 different page addresses as variables
    url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/"
    cerberus_html = requests.get(f'{url}cerberus_enhanced')
    schiaparelli_html = requests.get(f'{url}schiaparelli_enhanced')
    syrtis_major_html = requests.get(f'{url}syrtis_major_enhanced')
    valles_marineris_html = requests.get(f'{url}valles_marineris_enhanced')

    # Create and parse BeautifulSoup objects for four pages
    soup_c = bs(cerberus_html.text, 'html.parser')
    soup_s = bs(schiaparelli_html.text, 'html.parser')
    soup_sm = bs(syrtis_major_html.text, 'html.parser')
    soup_v = bs(valles_marineris_html.text, 'html.parser')

    # Create list to hold dictionaries
    hemisphere_image_urls = []

    # Find results within class 'container' that contain the information we need
    results_c = soup_c.find_all('div', class_='container')
    results_s = soup_s.find_all('div', class_='container')
    results_sm = soup_sm.find_all('div', class_='container')
    results_v = soup_v.find_all('div', class_='container')
    # Create list to loop through all four pages' results
    results = [results_c, results_s, results_sm, results_v]

    # Loop through results on all four pages
    for result in results:

        # Loop through the information within one page
        for r in result:

            # Find title and image url, append to the list we made
            title = r.find('h2', class_='title').text
            img_url = r.find('img', class_='wide-image')
            img_url = img_url.attrs.get('src', None)
            results_dict = {"title": title, "img_url": img_url}
            hemisphere_image_urls.append(results_dict)

    browser.quit()

    return {
        "headline": headline,
        "paragraph": paragraph,
        "featured_image_url": featured_image_url,
        "mars_html": mars_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }
