import sys

def main():

    print('Hello world')

# main 함수
if __name__=='__main__':
    main()

# python3 명령에 의해 실행되지 않고 다른 파이썬 코드에 import 되어 사용될 때, 실행
# import spotify_api
else:
    print('this script is being imported')
