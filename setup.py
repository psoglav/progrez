from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='progrez',
      version='0.1',
      description='The dynamic, async and beautiful progress bar',
      long_description=readme(),
      url='https://github.com/psoglav/progrez',
      author='psoglav',
      author_email="psoglav.ih8u@gmail.com",
      license='MIT',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Printing',
      ],
      keywords="progress bar loader async typewriter",
      packages=['progrez'],
      install_requires=[
          'requests',
          'py-term',
          'colored',
      ],
      zip_safe=False)