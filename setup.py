import setuptools
from distutils.core import setup


setup(
  name='scraping_scheduler',
  packages=setuptools.find_packages(),
  version='0.0.7',
  license='CC-BY-4.0',
  description='A bundle that includes task scheduler and scraping broker clients',
  author='Jian Jian',
  author_email='jjian03@syr.edu',
  url='https://github.com/iBranch-DataScience/scraping_scheduler',
  download_url='https://github.com/iBranch-DataScience/scraping_scheduler/releases',
  package_data={
      '': ['LICENSE'],
      'scraping_scheduler': ['ibranch/resource/*',],
  },
  include_package_data=True,
  keywords=[
      'scraping',
      'scheduler',
      'scraping-scheduler',
      'iBranch',
      'ibranch',
      'IBRANCH',
      'iSchool',
      'ischool',
      'ISCHOOL',
      'Syracuse University',
      'syracuse university',
      'su',
      'Su',
      'SU',
  ],
  install_requires=[
      'APScheduler',
      'config-with-yaml',
      'numpy',
      'pandas',
      'requests',
      'selenium',
      'singleton-decorator',
      'urllib3',
  ],
  classifiers=[
    'Development Status :: 1 - Planning',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'LICENSE :: CC-BY-4.0',
    'Programming Language :: Python :: 3',
  ],
)
