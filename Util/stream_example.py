"""
LangChain 스트리밍 유틸리티 함수 사용 예시
"""

from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from stream_utils import print_stream_content, get_stream_content, stream_with_callback


def example_basic_streaming():
    """기본 스트리밍 출력 예시"""
    print("=== 기본 스트리밍 출력 예시 ===")

    # LLM 객체 생성
    llm = ChatBedrockConverse(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        model="apac.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="ap-northeast-2",
    )

    # 질의
    question = "대한민국의 수도는 뭐야?"
    answer = llm.stream(question)

    # 깔끔한 스트리밍 출력
    print_stream_content(answer)
    print()


def example_get_content_only():
    """텍스트만 추출하는 예시 (출력하지 않음)"""
    print("=== 텍스트만 추출하는 예시 ===")

    llm = ChatBedrockConverse(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        model="apac.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="ap-northeast-2",
    )

    question = "파이썬의 장점을 3가지 설명해줘"
    answer = llm.stream(question)

    # 텍스트만 추출 (출력하지 않음)
    full_response = get_stream_content(answer)
    print(f"전체 응답 길이: {len(full_response)} 문자")
    print(f"응답 내용: {full_response[:100]}...")
    print()


def example_with_callback():
    """콜백 함수를 사용한 예시"""
    print("=== 콜백 함수를 사용한 예시 ===")

    def custom_callback(text):
        """각 텍스트 청크에 대해 호출되는 콜백 함수"""
        print(f"[청크] {text}", end="", flush=True)

    llm = ChatBedrockConverse(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        model="apac.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="ap-northeast-2",
    )

    question = "인공지능의 미래에 대해 간단히 설명해줘"
    answer = llm.stream(question)

    # 콜백 함수와 함께 스트리밍
    full_response = stream_with_callback(answer, custom_callback)
    print(f"\n\n전체 응답 길이: {len(full_response)} 문자")
    print()


def example_with_chain():
    """Chain과 함께 사용하는 예시"""
    print("=== Chain과 함께 사용하는 예시 ===")

    llm = ChatBedrockConverse(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        model="apac.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="ap-northeast-2",
    )

    # 프롬프트 템플릿 생성
    prompt = PromptTemplate.from_template(
        "다음 주제에 대해 간단히 설명해주세요: {topic}"
    )

    # Chain 생성
    chain = prompt | llm | StrOutputParser()

    # 스트리밍 실행
    answer = chain.stream({"topic": "머신러닝"})

    # 깔끔한 출력
    print_stream_content(answer)
    print()


if __name__ == "__main__":
    # 환경 변수 확인
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        print("AWS 인증 정보가 설정되지 않았습니다.")
        print("AWS_ACCESS_KEY_ID와 AWS_SECRET_ACCESS_KEY 환경 변수를 설정해주세요.")
    else:
        # 예시 실행
        example_basic_streaming()
        example_get_content_only()
        example_with_callback()
        example_with_chain()
