from functions.get_files_content import get_file_content


def run_all_test_cases():
    result1 = get_file_content("calculator", "lorem.txt")
    result2 = get_file_content("calculator", "main.py")
    result3 = get_file_content("calculator", "pkg/calculator.py")
    result4 = get_file_content("calculator", "/bin/cat")
    result5 = get_file_content("calculator", "pkg/does_not_exist.py")

    print(result1)
    print(result2)
    print(result3)
    print(result4)
    print(result5)


run_all_test_cases()
