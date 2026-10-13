"""문자열 관련 유틸.

작성자: 하은 (@haeunyn)
"""


def truncate(text: str, max_length: int = 20, suffix: str = "...") -> str:
    """긴 문자열을 자르고 뒤에 말줄임표를 붙인다.

    목록 화면처럼 한 줄에 다 보여줄 수 없는 곳에서 쓴다.

    Args:
        text: 자를 문자열
        max_length: 결과의 최대 길이(말줄임표 포함). 1 이상이어야 한다
        suffix: 잘렸을 때 뒤에 붙일 문자열

    Returns:
        max_length 이하로 줄어든 문자열. 자를 필요가 없으면 원본 그대로.

    Raises:
        ValueError: max_length 가 1 미만일 때

    Examples:
        >>> truncate("안녕하세요 반갑습니다", 8)
        '안녕하세요...'
        >>> truncate("짧음", 10)
        '짧음'
        >>> truncate("abcdefghij", 5, suffix="…")
        'abcd…'
    """
    if max_length < 1:
        raise ValueError(f"max_length 는 1 이상이어야 합니다: {max_length}")

    if len(text) <= max_length:
        return text

    # suffix 가 max_length 보다 길면 자를 자리가 없다 → suffix 자체를 잘라서 쓴다
    if len(suffix) >= max_length:
        return suffix[:max_length]

    return text[: max_length - len(suffix)] + suffix


if __name__ == "__main__":
    # 간단 확인용. `python src/utils/text.py` 로 실행하면 예시가 돈다.
    import doctest

    result = doctest.testmod()
    print(f"docstring 예시 테스트: {result.attempted}개 중 {result.failed}개 실패")
