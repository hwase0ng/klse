from setuptools import setup

setup(name='klse',
      version='0.1',
      description='klse csv download and conversion to mt4',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Text Processing :: Linguistic',
      ],
      url='http://github.com/royste0918/klse',
      author='roysten',
      author_email='roysten.tan@gmail.com',
      license='MIT',
      packages=['klse'],
      install_requires=[
          'csv',
      ],
      include_package_data=True,
      zip_safe=False)
