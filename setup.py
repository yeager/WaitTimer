from setuptools import setup, find_packages

setup(
    name="waittimer",
    version="1.0.0",
    description="Visuell väntetimer för barn",
    author="WaitTimer",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["PyGObject>=3.42"],
        package_data={
        "": ["locale/*/LC_MESSAGES/*.mo"],
    },
    entry_points={
        "console_scripts": [
            "waittimer=waittimer.main:main",
        ],
    },
)
