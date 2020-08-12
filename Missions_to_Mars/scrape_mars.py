# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# %%
def scrape():
    # %%
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # %%
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)


    # %%
    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    ###### NASA Mars News
    # ---------------------------------


    # %%
    for result in soup:
        # Identify and return title of listing
        title = soup.find_all("div", class_ = "content_title")[1].text
        # Identify and return price of listing
        paragraph = soup.find_all("div", class_= "rollover_description_inner")[0].text
        # Print results only if title, price, and link are available
        if (title and paragraph):
            print('-------------')
            print(title)
            print(paragraph)


    # %%
    ###### JPL Mars Space Images - Featured Image
    # ---------------------------------------------


    # %%
    Space_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(Space_images)


    # %%
    browser.click_link_by_partial_text('FULL IMAGE')


    # %%
    browser.click_link_by_partial_text('more info')


    # %%
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find_all('figure', class_='lede')
    results = image[0].a['href']
    print_image_url = 'https://www.jpl.nasa.gov/' + results
    print(print_image_url)


    # %%
    ###### Mars Weather
    # ------------------------------


    # %%
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter)
    time.sleep(4)


    # %%
    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    # time.sleep(10)
    mars_weather =  soup.find_all('article', class_="css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-o7ynqc r-6416eg")[0].text.strip().replace('Mars Weather@MarsWxReport·19hInSight ','')
    mars_weather


    # %%
    ###### Mars Facts
    # ------------------------------


    # %%
    mars_facts = pd.read_html('https://space-facts.com/mars/')
    mars_df = mars_facts[0]
    mars_df.columns = ['Descriptions', 'Value']
    mars_df


    # %%
    ###### Mars Hemispheres
    # ------------------------------


    # %%
    Hemi_Url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(Hemi_Url)
    html = browser.html
    soup = bs(html, 'html.parser')

    image_names = []
    results = soup.find_all('div', class_="collapsible results")
    titles = results[0].find_all('h3')
    for name in titles:
        image_names.append(name.text)

    image_names


    # %%
    thumbnail_results = results[0].find_all('a')
    links = []

    for thumbnail in thumbnail_results:
        if (thumbnail.img):
            thumbnail_url = 'https://astrogeology.usgs.gov' + thumbnail['href']
            links.append(thumbnail_url)

    links


    # %%
    full_imgs = []

    for url in links:
        
        # Click through each thumbanil link
        browser.visit(url)
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # Scrape each page for the relative image path
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
        
        # Combine the reltaive image path to get the full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
        
        # Add full image links to a list
        full_imgs.append(img_link)

    full_imgs


    # %%
    mars_hemi = list(zip(image_names, full_imgs))

    mars_df_dict = []

    for title, img in mars_hemi:
        mars_dict = {}
        mars_dict['title'] = title
        mars_dict['img_url'] = img
        mars_df_dict.append(mars_dict)

    mars_df_dict


    # %%
    Mars_scrape_dict = {
        "title": title,
        "paragraph": paragraph,
        "print_image_url": print_image_url,
        "mars_weather": mars_weather,
        "mars_df": mars_df.to_html(),
        "mars_hemi": mars_df_dict,
    }

    Mars_scrape_dict

    browser.quit()

    return Mars_scrape_dict


# %%



