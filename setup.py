from setuptools import setup, find_packages

setup(
    name='family_tree_matcher',
    version='0.1',
    packages=find_packages(),
    author='Alba Ramos Pedroviejo',
    author_email='alba.ramos.pedroviejo@gmail.com',
    description='Find your lost ancestors with family tree matcher',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/albaramosp/family_tree_matcher',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
