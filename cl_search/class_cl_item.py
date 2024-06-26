from cl_search.utils import download_images
from cl_search.utils import get_city_name
from cl_search.utils import parse_post_id
from cl_search.utils import split_url_size


class CL_item:
    pass


class List(CL_item):
    kind = "list"

    def __init__(self, title, price, timestamp, location, date, post_url, post_id):
        self.title = title
        self.price = price
        self.timestamp = timestamp
        self.location = location
        self.date = date
        self.post_url = post_url
        self.post_id = post_id

    def as_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "timestamp": self.timestamp,
            "location": self.location,
            "date": self.date,
            "post_url": self.post_url,
            "post_id": self.post_id,
        }

    def as_list(self):
        return [
            self.title,
            self.price,
            self.timestamp,
            self.location,
            self.date,
            self.post_url,
            self.post_id,
        ]

    @classmethod
    def organize_listing_data(cls, link: str, posts_data: list, **kwargs):
        city_name = get_city_name(link)
        craigslist_posts = []

        for posts in posts_data:
            title = getattr(posts.select_one("a span.label"), "text", None)
            price_element = posts.find("span", "priceinfo")
            price = (
                price_element.text.strip()
                if price_element is not None
                else "Price not given"
            )
            post_url = (
                posts.find("a", "posting-title").get("href")
                if posts.find("a", "posting-title")
                else ""
            )
            timestamp = getattr(posts.select_one(
                'span[title*="GMT"]'), "text", None)

            meta = posts.find("span", class_="meta")
            if meta:
                meta_info = meta.get_text(strip=True)
                separator = meta.find("span", class_="separator")
                if separator:
                    date = meta_info.split(separator.text)[2]
                    if date.endswith("pichide"):
                        date = date[:-7]

                    location = meta_info.split(separator.text)[1]
                    if location.strip() == "":
                        location = f"{city_name} area"

            post_id = parse_post_id(post_url)

            craigslist_posts.append(
                cls(title, price, timestamp, location, date, post_url, post_id)
            )

        return craigslist_posts


class Narrow_list(CL_item):
    kind = "narrow list"

    def __init__(self, title, price, timestamp, location, date, post_url, post_id):
        self.title = title
        self.price = price
        self.timestamp = timestamp
        self.location = location
        self.date = date
        self.post_url = post_url
        self.post_id = post_id

    def as_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "timestamp": self.timestamp,
            "location": self.location,
            "date": self.date,
            "post_url": self.post_url,
            "post_id": self.post_id,
        }

    @classmethod
    def organize_listing_data(cls, link: str, posts_data: list, **kwargs):
        city_name = get_city_name(link)
        craigslist_posts = []

        for posts in posts_data:
            title = getattr(posts.select_one("a span.label"), "text", None)
            price_element = posts.find("span", "priceinfo")
            price = (
                price_element.text.strip()
                if price_element is not None
                else "Price not given"
            )
            post_url = (
                posts.find("a", "posting-title").get("href")
                if posts.find("a", "posting-title")
                else ""
            )
            timestamp = getattr(posts.select_one(
                'span[title*="GMT"]'), "text", None)

            meta = posts.find("div", class_="supertitle")
            if meta:
                meta_info = meta.get_text(strip=True)
                separator = meta.find("span", class_="separator")
                if separator:
                    split_meta = meta_info.split(separator.text)
                    date = split_meta[0]
                    location = split_meta[1]

                else:
                    location = meta_info
                    date = timestamp

            if location:
                if location.strip() == "":
                    location = f"{city_name} area"

            post_id = parse_post_id(post_url)

            craigslist_posts.append(
                cls(title, price, timestamp, location, date, post_url, post_id)
            )

        return craigslist_posts


class Thumb(CL_item):
    kind = "thumb"

    def __init__(
        self,
        title,
        price,
        timestamp,
        location,
        date,
        image_url,
        post_url,
        post_id,
        image_path,
    ):
        self.title = title
        self.price = price
        self.timestamp = timestamp
        self.location = location
        self.date = date
        self.image_url = image_url
        self.post_url = post_url
        self.post_id = post_id
        self.image_path = image_path

    def as_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "timestamp": self.timestamp,
            "location": self.location,
            "date": self.date,
            "post_url": self.post_url,
            "image_url": self.image_url,
            "post_id": self.post_id,
            "image_path": self.image_path,
        }

    # finish writing this
    @classmethod
    def organize_listing_data(cls, link: str, posts_data: list, **kwargs):
        images_mode = kwargs.get("images_mode")

        city_name = get_city_name(link)
        craigslist_posts = []

        for posts in posts_data:
            title = getattr(posts.select_one("a span.label"), "text", None)
            price_element = posts.find("span", "priceinfo")
            price = (
                price_element.text.strip()
                if price_element is not None
                else "Price not given"
            )
            post_url = (
                posts.find("a", "posting-title").get("href")
                if posts.find("a", "posting-title")
                else ""
            )
            timestamp = getattr(posts.select_one(
                'span[title*="GMT"]'), "text", None)

            meta = posts.find("div", class_="supertitle")
            if meta:
                meta_info = meta.get_text(strip=True)
                separator = meta.find("span", class_="separator")
                if separator:
                    split_meta = meta_info.split(separator.text)
                    date = split_meta[0]
                    location = split_meta[1]

                else:
                    location = meta_info
                    date = timestamp

            if location:
                if location.strip() == "":
                    location = f"{city_name} area"

            image_url_src = posts.find("img").get(
                "src") if posts.find("img") else ""

            if image_url_src.strip() == "":
                image_url = "No image"

            else:
                base_image_src = split_url_size(image_url_src)
                image_url = str(base_image_src + '_600x450.jpg')

            if images_mode is True:
                image_path = download_images(image_url)

            else:
                image_path = "No image path"

            post_id = parse_post_id(post_url)

            craigslist_posts.append(
                cls(
                    title,
                    price,
                    timestamp,
                    location,
                    date,
                    image_url,
                    post_url,
                    post_id,
                    image_path,
                )
            )

        return craigslist_posts


# unfinished
class Preview(CL_item):
    kind = "preview"

    def __init__(
        self,
        title,
        price,
        timestamp,
        location,
        date,
        post_url,
        image_urls,
        post_id,
        image_paths,
        post_description,
        address_info,
        attribute,
    ):
        self.title = title
        self.price = price
        self.timestamp = timestamp
        self.location = location
        self.date = date
        self.post_url = post_url
        self.image_urls = image_urls
        self.post_id = post_id
        self.image_paths = image_paths
        self.post_description = post_description
        self.address_info = address_info
        self.attribute = attribute

    def as_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "timestamp": self.timestamp,
            "location": self.location,
            "date": self.date,
            "post_url": self.post_url,
            "image_urls": self.image_urls,
            "post_id": self.post_id,
            "image_paths": self.image_paths,
            "post_description": self.post_description,
            "address_info": self.address_info,
            "attribute": self.attribute,
        }

    # finish writing this
    @classmethod
    def organize_listing_data(cls, link: str, posts_data: list, **kwargs):
        images_mode = kwargs.get("images_mode")

        city_name = get_city_name(link)

        craigslist_posts = []
        image_paths = []
        attribute = []

        for posts in posts_data:
            title = getattr(posts.find("div", "posting-title"), "text", None)
            price_element = posts.find("span", "priceinfo")
            price = (
                price_element.text.strip()
                if price_element is not None
                else "Price not given"
            )
            post_url_element = posts.select_one("div.posting-title a")
            post_url = post_url_element.get("href") if post_url_element else ""

            meta = posts.select_one("div.meta div.location")
            if meta:
                meta_info = meta.get_text(strip=True)
                separator = meta.find("span", class_="separator")
                if separator:
                    date = meta_info.split(separator.text)[0]
                    location = meta_info.split(separator.text)[1]
                    if location.strip() == "":
                        location = f"{city_name} area"
                else:
                    location = meta_info.split(separator.text)[0]

            timestamp = getattr(posts.find("span", "time-ago"), "text", None)
            post_description = posts.find("div", "posting-description")
            if post_description:
                pass

            address_info = posts.find("div", "address-info")

            if address_info:
                pass

            attribute = posts.find_all("div", "attrib")

            if attribute:
                pass

            # rewrite for preview
            image_urls = []
            image_url_src = posts.find("img").get(
                "src") if posts.find("img") else ""

            if image_url_src.strip() == "":
                image_url = "No image"

            else:
                base_image_src = split_url_size(image_url_src)
                image_url = str(base_image_src + '_600x450.jpg')

            if images_mode is True:
                image_path = download_images(image_url)

            else:
                image_path = "No image path"

            image_paths.append(image_path)
            post_id = parse_post_id(post_url)

            craigslist_posts.append(
                cls(
                    title,
                    price,
                    timestamp,
                    location,
                    date,
                    post_url,
                    image_urls,
                    post_id,
                    image_paths,
                    post_description,
                    address_info,
                    attribute,
                )
            )

        return craigslist_posts


class Grid(CL_item):
    kind = "grid"

    def __init__(
        self,
        title,
        price,
        timestamp,
        location,
        post_url,
        image_url,
        post_id,
        image_path,
    ):
        self.title = title
        self.price = price
        self.timestamp = timestamp
        self.location = location
        self.post_url = post_url
        self.image_url = image_url
        self.post_id = post_id
        self.image_path = image_path

    def as_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "timestamp": self.timestamp,
            "location": self.location,
            "post_url": self.post_url,
            "image_url": self.image_url,
            "post_id": self.post_id,
            "image_path": self.image_path,
        }

    @classmethod
    def organize_listing_data(cls, link: str, posts_data: list, **kwargs):
        images_mode = kwargs.get("images_mode")

        city_name = get_city_name(link)
        craigslist_posts = []

        for posts in posts_data:
            title = getattr(posts.select_one("a span.label"), "text", None)
            price_element = posts.find("span", "priceinfo")
            price = (
                price_element.text.strip()
                if price_element is not None
                else "Price not given"
            )
            post_url = (
                posts.find("a", "posting-title").get("href")
                if posts.find("a", "posting-title")
                else ""
            )

            meta = posts.find("div", class_="meta")
            if meta:
                meta_info = meta.get_text(strip=True)
                separator = meta.find("span", class_="separator")
                if separator:
                    timestamp = meta_info.split(separator.text)[0]
                    location = meta_info.split(separator.text)[1]
                    if location.strip() == "":
                        location = f"{city_name} area"

            image_url_src = posts.find("img").get(
                "src") if posts.find("img") else ""

            if image_url_src.strip() == "":
                image_url = "No image"

            else:
                base_image_src = split_url_size(image_url_src)
                image_url = str(base_image_src + '_600x450.jpg')

            if images_mode is True:
                image_path = download_images(image_url)

            else:
                image_path = "No image path"

            post_id = parse_post_id(post_url)

            craigslist_posts.append(
                cls(
                    title,
                    price,
                    timestamp,
                    location,
                    post_url,
                    image_url,
                    post_id,
                    image_path,
                )
            )

        return craigslist_posts


class Gallery(CL_item):
    kind = "gallery"

    def __init__(
        self,
        title,
        price,
        timestamp,
        location,
        post_url,
        image_url,
        post_id,
        image_path,
    ):
        self.title = title
        self.price = price
        self.timestamp = timestamp
        self.location = location
        self.post_url = post_url
        self.image_url = image_url
        self.post_id = post_id
        self.image_path = image_path

    def as_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "timestamp": self.timestamp,
            "location": self.location,
            "post_url": self.post_url,
            "image_url": self.image_url,
            "post_id": self.post_id,
            "image_path": self.image_path,
        }

    @classmethod
    def organize_listing_data(cls, link: str, posts_data: list, **kwargs):
        images_mode = kwargs.get("images_mode")

        city_name = get_city_name(link)
        craigslist_posts = []

        for posts in posts_data:
            title = getattr(posts.find("a", "posting-title"), "text", None)
            price_element = posts.find("span", "priceinfo")
            price = (
                price_element.text.strip()
                if price_element is not None
                else "Price not given"
            )
            post_url = (
                posts.find("a", "posting-title").get("href")
                if posts.find("a", "posting-title")
                else ""
            )

            meta = posts.find("div", class_="meta")
            if meta:
                meta_info = meta.get_text(strip=True)
                separator = meta.find("span", class_="separator")
                if separator:
                    timestamp = meta_info.split(separator.text)[0]
                    location = meta_info.split(separator.text)[1]
                    if location.strip() == "":
                        location = f"{city_name} area"

            image_url_src = posts.find("img").get(
                "src") if posts.find("img") else ""

            if image_url_src.strip() == "":
                image_url = "No image"

            else:
                base_image_src = split_url_size(image_url_src)
                image_url = str(base_image_src + '_600x450.jpg')

            if images_mode is True:
                image_path = download_images(image_url)

            else:
                image_path = "No image path"

            post_id = parse_post_id(post_url)

            craigslist_posts.append(
                cls(
                    title,
                    price,
                    timestamp,
                    location,
                    post_url,
                    image_url,
                    post_id,
                    image_path,
                )
            )

        return craigslist_posts


def identify_cl_item_type(link: str, posts_data: list, **kwargs):
    for posts in posts_data:
        result_node_wide = posts.parent.find("div", class_="result-node-wide")
        result_node_narrow = posts.parent.find(
            "div", class_="result-node-narrow")
        result_node = posts.parent.find("div", class_="result-node")
        gallery_card = posts.parent.find("div", class_="gallery-card")

        if result_node:
            card_content = posts.find("div", class_="card-content")
            cl_gallery = posts.find("div", class_="cl-gallery")

            if card_content:
                cl_item_data = Preview.organize_listing_data(
                    link, posts_data, **kwargs
                )
                return cl_item_data

            elif cl_gallery:
                cl_item_data = Grid.organize_listing_data(
                    link, posts_data, **kwargs
                )
                return cl_item_data

            else:
                cl_item_data = Thumb.organize_listing_data(
                    link, posts_data, **kwargs
                )
                return cl_item_data

        if result_node_wide:
            cl_item_data = List.organize_listing_data(
                link, posts_data, **kwargs
            )
            return cl_item_data

        if result_node_narrow:
            cl_item_data = Narrow_list.organize_listing_data(
                link, posts_data, **kwargs
            )
            return cl_item_data

        if gallery_card:
            cl_item_data = Gallery.organize_listing_data(
                link, posts_data, **kwargs
            )
            return cl_item_data

    return None
