from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.0.2',
    author='Yunusov_Grigory',
    author_email='grigoriyzawr@gmail.com',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean=clean_folder.clean:start']}
)