from functions.get_files_info import get_files_info


def run_all_test_cases():
    result1 = get_files_info("calculator", ".")
    result2 = get_files_info("calculator", "pkg")
    result3 = get_files_info("calculator", "/bin")
    result4 = get_files_info("calculator", "../")
    print(result1)
    print(result2)
    print(result3)
    print(result4)


run_all_test_cases()

