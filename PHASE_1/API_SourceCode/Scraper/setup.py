from setuptools import setup, find_packages

setup(
    name='Scraper',
    version='1.0',
    packages=find_packages(),
    package_data={
        'Scraper': ['resources/*']
    },
    entry_points={
        'scrapy': ['settings = Scraper.settings']
    },
    zip_safe=False,
)
