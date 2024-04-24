from setuptools import setup, find_packages

setup(
    name='demo_1st',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add your project dependencies here
    ],
    extras_require={
        'test': [
            # Add test dependencies here
        ]
    }
)
