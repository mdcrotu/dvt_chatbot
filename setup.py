from setuptools import setup

setup(
    name="dvt_chatbot",
    version="0.1",
    packages=["dvt_chatbot"],  # <-- add this line if not already present
    include_package_data=True,
    install_requires=[
        "flask",
        "sentence-transformers",
        "rapidfuzz",
        "beautifulsoup4",
        "requests",
    ],
)
