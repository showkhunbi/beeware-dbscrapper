import requests
from bs4 import BeautifulSoup
from dbscrapper.pageContent import page, homepage
import pandas as pd


def get_url(select, page_number=1):
    if select == "Latest Posts":
        url = "https://delaniblog.com.ng/"
    elif select == "Home":
        url = "https://delaniblog.com.ng/"
    elif select == "Music":
        url = "https://delaniblog.com.ng/category/download-mp3/"
    elif select == "Entertainment":
        url = "https://delaniblog.com.ng/category/entertainment/"
    elif select == "Videos":
        url = "https://delaniblog.com.ng/category/world/videos/"
    elif select == "Album & EP":
        url = "https://delaniblog.com.ng/category/album-download/"
    elif select == "Lyrics":
        url = "https://delaniblog.com.ng/category/download-mp3/lyrics/"
    elif select == "Mixtape":
        url = "https://delaniblog.com.ng/category/mixtape/"
    elif select == "Trending":
        url = "https://delaniblog.com.ng/category/download-mp3/trending/"

    if page_number != 1:
        url = url + "page/" + str(page_number)
        return url
    else:
        return url


def get_data(select, page_number):
    url = get_url(select, page_number)
    site = requests.get(url)
    # site = homepage

    soup = BeautifulSoup(site.content, "html.parser")

    if select == "Latest Posts":
        latest_posts = soup.find(
            class_="mvp-flex-story-wrap left relative").find_all("a")
        latest_posts_heads = [item.find(
            class_="mvp-flex-story-text left relative").find("h2").text for item in latest_posts]
        latest_posts_links = [item.get("href") for item in latest_posts]

        headings = latest_posts_heads
        links = latest_posts_links

    else:
        body = soup.find(class_="mvp-main-blog-body left relative")

        story = body.find_all(
            class_="mvp-blog-story-wrap left relative infinite-post")
        # story_link = story[0].find("a").get("href")
        # story_head = story[0].find("a").find(class_="mvp-blog-story-text left relative").find("h2").text
        story_heads = [item.find("a").find(
            class_="mvp-blog-story-text left relative").find("h2").text for item in story]
        story_links = [item.find("a").get("href") for item in story]

        if ("/page/" in url) or (url == "https://delaniblog.com.ng/"):
            recent_story_heads = []
            recent_story_links = []
        else:
            recent_story = body.find(id="mvp-cat-feat-wrap").find_all("a")
            # recent_story_link = recent_story[0].get("href")
            # recent_story_head = recent_story[0].find("h2").text
            recent_story_heads = [
                item.find("h2").text for item in recent_story]
            recent_story_links = [item.get("href") for item in recent_story]

        headings = recent_story_heads + story_heads
        links = recent_story_links + story_links

    blog_page = pd.DataFrame({
        "headings": headings,
        "links": links
    })
    return blog_page


def get_max_page_number(select):
    # get max Page number
    url = get_url(select)
    site = requests.get(url)
    website = BeautifulSoup(site.content, "html.parser")
    try:
        last_page = website.find(class_="pagination").find_all("span")[
            0].text.split(" ")[-1]
    except:
        last_page = 1
    return last_page
