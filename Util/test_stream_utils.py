"""
수정된 stream_utils 함수들을 테스트하는 파일
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from stream_utils import print_stream_content, get_stream_content, stream_with_callback
from langchain_aws import ChatBedrockConverse
import os


def test_string_chunks():
    """문자열 chunk를 테스트합니다."""
    print("=== 문자열 chunk 테스트 ===")

    # 문자열 chunk들로 구성된 스트림
    string_stream = iter(
        ["안녕하세요", " ", "반갑습니다", "!", " ", "테스트", "입니다", "."]
    )

    print("1. print_stream_content 테스트:")
    print_stream_content(string_stream)
    print()

    # 새로운 스트림 생성 (이전 스트림은 소진됨)
    string_stream2 = iter(["파이썬", " ", "프로그래밍", " ", "테스트", "입니다", "."])

    print("2. get_stream_content 테스트:")
    result = get_stream_content(string_stream2)
    print(f"추출된 텍스트: '{result}'")
    print()

    # 콜백 테스트
    string_stream3 = iter(["콜백", " ", "함수", " ", "테스트", "입니다", "."])

    def test_callback(text):
        print(f"[콜백] '{text}'", end="")

    print("3. stream_with_callback 테스트:")
    result = stream_with_callback(string_stream3, test_callback)
    print(f"\n반환된 전체 텍스트: '{result}'")
    print()


def test_mixed_chunks():
    """혼합된 타입의 chunk를 테스트합니다."""
    print("=== 혼합 타입 chunk 테스트 ===")

    # 문자열과 객체가 섞인 스트림 시뮬레이션
    class MockChunk:
        def __init__(self, content):
            self.content = content

    mixed_stream = iter(
        ["시작: ", MockChunk("객체"), " ", MockChunk("내용"), " ", "끝"]
    )

    print("혼합 타입 스트림 테스트:")
    print_stream_content(mixed_stream)
    print()


def test_empty_stream():
    """빈 스트림을 테스트합니다."""
    print("=== 빈 스트림 테스트 ===")

    empty_stream = iter([])

    print("빈 스트림 테스트:")
    print_stream_content(empty_stream)
    print()

def test_stream_with_llm():
    llm = ChatBedrockConverse(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        model="apac.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="ap-northeast-2",
    )

    examples = [
            {
                "question": "스티브 잡스와 아인슈타인 중 누가 더 오래 살았나요?",
                "answer": """이 질문에 추가 질문이 필요한가요: 예.
        추가 질문: 스티브 잡스는 몇 살에 사망했나요?
        중간 답변: 스티브 잡스는 56세에 사망했습니다.
        추가 질문: 아인슈타인은 몇 살에 사망했나요?
        중간 답변: 아인슈타인은 76세에 사망했습니다.
        최종 답변은: 아인슈타인
        """,
            },
            {
                "question": "네이버의 창립자는 언제 태어났나요?",
                "answer": """이 질문에 추가 질문이 필요한가요: 예.
        추가 질문: 네이버의 창립자는 누구인가요?
        중간 답변: 네이버는 이해진에 의해 창립되었습니다.
        추가 질문: 이해진은 언제 태어났나요?
        중간 답변: 이해진은 1967년 6월 22일에 태어났습니다.
        최종 답변은: 1967년 6월 22일
        """,
            },
            {
                "question": "율곡 이이의 어머니가 태어난 해의 통치하던 왕은 누구인가요?",
                "answer": """이 질문에 추가 질문이 필요한가요: 예.
        추가 질문: 율곡 이이의 어머니는 누구인가요?
        중간 답변: 율곡 이이의 어머니는 신사임당입니다.
        추가 질문: 신사임당은 언제 태어났나요?
        중간 답변: 신사임당은 1504년에 태어났습니다.
        추가 질문: 1504년에 조선을 통치한 왕은 누구인가요?
        중간 답변: 1504년에 조선을 통치한 왕은 연산군입니다.
        최종 답변은: 연산군
        """,
            },
            {
                "question": "올드보이와 기생충의 감독이 같은 나라 출신인가요?",
                "answer": """이 질문에 추가 질문이 필요한가요: 예.
        추가 질문: 올드보이의 감독은 누구인가요?
        중간 답변: 올드보이의 감독은 박찬욱입니다.
        추가 질문: 박찬욱은 어느 나라 출신인가요?
        중간 답변: 박찬욱은 대한민국 출신입니다.
        추가 질문: 기생충의 감독은 누구인가요?
        중간 답변: 기생충의 감독은 봉준호입니다.
        추가 질문: 봉준호는 어느 나라 출신인가요?
        중간 답변: 봉준호는 대한민국 출신입니다.
        최종 답변은: 예
        """,
            },
    ]

    example_prompt = PromptTemplate.from_template(
    "Question:\n{question}\nAnswer:\n{answer}"
    )

    prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question:\n{question}\nAnswer:",
    input_variables=["question"],
)

    question = "Google이 창립된 연도에 Bill Gates의 나이는 몇 살인가요?"

    chain = prompt | llm | StrOutputParser()

    answer = chain.stream({"question": question})

    print_stream_content(answer)

if __name__ == "__main__":
    test_string_chunks()
    test_mixed_chunks()
    test_empty_stream()
    test_stream_with_llm()

    print("✅ 모든 테스트가 완료되었습니다!")
