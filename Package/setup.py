from setuptools import setup,find_packages

setup(
        ### 包与作者信息
        name = 'meoteofence',
        version = '0.1',
        author = 'shihua',
        author_email = "hua.shi@meritech-data.com",
        python_requires = ">=3.9.12",
        license = "MIT",

        ### 源码与依赖
        packages = find_packages(),
        include_package_data = True,
        description = 'Meoteofence is a preprocessing program for numerical weather forecasting, which is mainly used to segment the original meteorological data according to the five dimensions of starting time, prediction time, spatial hierarchy, meteorological physical quantities and station coordinate grid. The main technology uses HDF5 to organize the matrix data after analysis, uses hook technology to organize the code, and adds parallel processing at the prediction time level.',
        # install_requires = ['pluggy','tables','pandas','numpy'],

        ### 包接入点，命令行索引
        # entry_points = {
        #     'console_scripts': [
        #         'fichectl = fiche.cli:fiche'
        #     ]
        # }      
)