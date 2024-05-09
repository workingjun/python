import io
import sys


def method_description(name, obj):
    

    help_strings = []

    for method_name in name:
        method = getattr(obj, method_name)
        
        # 문자열 버퍼 생성
        buffer = io.StringIO()
        
        # 이전의 sys.stdout 저장
        old_stdout = sys.stdout
        
        # help() 함수의 출력을 문자열 버퍼에 캡처
        sys.stdout = buffer
        help(method)
        
        # 이전의 sys.stdout으로 복원
        sys.stdout = old_stdout
        
        # 문자열 버퍼의 내용을 리스트에 추가
        help_strings.append(buffer.getvalue())
        buffer.close()
    return help_strings



