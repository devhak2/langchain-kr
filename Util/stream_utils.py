"""
LangChain 스트리밍 응답을 위한 유틸리티 함수들
"""

from typing import Iterator, Union, Any
from langchain_core.messages import AIMessageChunk, BaseMessageChunk


def print_stream_content(
    stream: Iterator[Union[AIMessageChunk, BaseMessageChunk, str]],
    end: str = "\n",
    flush: bool = True,
) -> None:
    """
    LangChain 스트리밍 응답에서 텍스트 내용만 깔끔하게 출력합니다.

    Args:
        stream: LangChain 스트리밍 응답 이터레이터 (chunk가 문자열일 수도 있음)
        end: 출력 끝에 추가할 문자열 (기본값: "\n")
        flush: 즉시 출력할지 여부 (기본값: True)
    """
    for chunk in stream:
        # chunk가 문자열인 경우
        if isinstance(chunk, str):
            print(chunk, end="", flush=flush)
        # chunk가 객체이고 content 속성이 있는 경우
        elif hasattr(chunk, "content"):
            # content가 리스트인 경우 (예: [{'type': 'text', 'text': '...'}])
            if isinstance(chunk.content, list):
                for item in chunk.content:
                    if isinstance(item, dict) and "text" in item:
                        text = item["text"]
                        print(text, end="", flush=flush)
            # content가 문자열인 경우
            elif isinstance(chunk.content, str):
                print(chunk.content, end="", flush=flush)

    print(end, end="", flush=flush)


def get_stream_content(
    stream: Iterator[Union[AIMessageChunk, BaseMessageChunk, str]]
) -> str:
    """
    LangChain 스트리밍 응답에서 텍스트 내용만 추출하여 반환합니다 (출력하지 않음).

    Args:
        stream: LangChain 스트리밍 응답 이터레이터 (chunk가 문자열일 수도 있음)

    Returns:
        str: 전체 응답 텍스트
    """
    full_response = ""

    for chunk in stream:
        # chunk가 문자열인 경우
        if isinstance(chunk, str):
            full_response += chunk
        # chunk가 객체이고 content 속성이 있는 경우
        elif hasattr(chunk, "content"):
            # content가 리스트인 경우 (예: [{'type': 'text', 'text': '...'}])
            if isinstance(chunk.content, list):
                for item in chunk.content:
                    if isinstance(item, dict) and "text" in item:
                        full_response += item["text"]
            # content가 문자열인 경우
            elif isinstance(chunk.content, str):
                full_response += chunk.content

    return full_response


def stream_with_callback(
    stream: Iterator[Union[AIMessageChunk, BaseMessageChunk, str]], callback=None
) -> str:
    """
    LangChain 스트리밍 응답을 처리하면서 콜백 함수를 호출합니다.

    Args:
        stream: LangChain 스트리밍 응답 이터레이터 (chunk가 문자열일 수도 있음)
        callback: 각 텍스트 청크에 대해 호출할 콜백 함수 (text: str) -> None

    Returns:
        str: 전체 응답 텍스트
    """
    full_response = ""

    for chunk in stream:
        # chunk가 문자열인 경우
        if isinstance(chunk, str):
            full_response += chunk
            if callback:
                callback(chunk)
        # chunk가 객체이고 content 속성이 있는 경우
        elif hasattr(chunk, "content"):
            # content가 리스트인 경우
            if isinstance(chunk.content, list):
                for item in chunk.content:
                    if isinstance(item, dict) and "text" in item:
                        text = item["text"]
                        full_response += text
                        if callback:
                            callback(text)
            # content가 문자열인 경우
            elif isinstance(chunk.content, str):
                full_response += chunk.content
                if callback:
                    callback(chunk.content)

    return full_response
