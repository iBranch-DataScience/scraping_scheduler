from distutils.core import setup


setup(
  name='scraping-scheduler',
  packages=['scraping_scheduler'],
  version='0.0.2',
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='A bundle that includes task scheduler and scraping broker clients',
  author='Jian Jian',
  author_email='jjian03@syr.edu',
  url='https://github.com/iBranch-DataScience/scraping_scheduler',
  download_url='https://github.com/iBranch-DataScience/scraping_scheduler/archive/0.0.2.tar.gz',
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
