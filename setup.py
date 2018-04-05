import setuptools

setuptools.setup(
    name="vboxmanage-plus",
    version="0.1.0",
    author="Stéphane Klein",
    author_email="contact@stephane-klein.info",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points="""
    [console_scripts]
    vboxmanage_plus = vboxmanage_plus:cli
    """
)
