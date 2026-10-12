from functions.get_files_info import get_files_info


def test() -> None:
    result = get_files_info("calculator", ".")
    print(f"Result for current directory:\n{result}")

    result = get_files_info("calculator", "pkg")
    print(f"Result for current directory:\n{result}")

    result = get_files_info("calculator", "/bin")
    print(f"Result for current directory:\n{result}")

    result = get_files_info("calculator", "../")
    print(f"Result for current directory:\n{result}")


if __name__ == "__main__":
    test()
