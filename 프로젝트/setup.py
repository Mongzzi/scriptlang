from distutils.core import setup, Extension

module_spam = Extension('spam', sources = ['spammodule.c'])

setup(
    name='weather',
    version='1.0',

    # 파일명이 아니라 모듈명을 입력 (.py라는 확장자는 제외)
    py_modules=['weather', 'noti', 'common_functions', 'teller'],

    packages=['image', 'adr'],
    package_data = {'image': ['*.png'],'image': ['*.PNG'], 'adr' : ['adress'] },

    ext_modules=[module_spam]
)


# 이 파일의 경로 위치에서 python setup.py sdist --formats=zip 실행
# 파일 받은 사람이 압축을 풀고
# 압축을 풀은 디렉토리에서 python setup.py install 실행
# 그 후 해당 파이선 파일을 실행시킹면 잘 작동하는지 확인
# 설치를 하면 C:\Python39\Lib\site-packages 경로에 파일들이 생김.