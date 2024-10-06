from setuptools import setup, find_packages

setup(
    name="EmotionEngine",
    version="1.0",
    description="Toy Playground Engine",
    author="Kevin STOETZEL",
    author_email="kevin.stoetzel@gmail.com",
    packages=find_packages(),
    install_requires=["pygame", "PyYAML"],
)
